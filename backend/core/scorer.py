import numpy as np
import cv2
import torch
import gc

class FrameScorer:
    """
    Memory-optimized version for Render Free Tier (512MB RAM limit).
    
    Optimizations:
    - Lazy loading: Models loaded only when first needed
    - No YOLO: Removed to save ~200MB RAM
    - Smaller CLIP: Using ViT-B/32 (smallest available)
    - Memory cleanup: Explicit garbage collection after processing
    """
    
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")
        print("Memory-optimized mode: Models will load on first use")
        
        # Don't load models at startup - lazy load them
        self.clip_model = None
        self.clip_preprocess = None
        self._clip_loaded = False

    def _load_clip_if_needed(self):
        """Lazy load CLIP model only when vibe scoring is requested."""
        if self._clip_loaded:
            return
            
        try:
            print("Loading CLIP model (first time only)...")
            import clip
            # Use smallest CLIP model to save memory
            self.clip_model, self.clip_preprocess = clip.load("ViT-B/32", device=self.device)
            self._clip_loaded = True
            print("CLIP loaded successfully")
        except Exception as e:
            print(f"Warning: CLIP not loaded. Vibe score will be 0. Error: {e}")
            self.clip_model = None
            self.clip_preprocess = None
            self._clip_loaded = True  # Don't try again

    def calculate_technical_score(self, frame: np.ndarray) -> float:
        """
        Score based on:
        1. Sharpness (Laplacian variance)
        2. Exposure (Histogram analysis)
        3. Color Vibrancy (Saturation)
        
        No ML models needed - pure OpenCV (lightweight)
        """
        if frame is None:
            return 0.0
            
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 1. SHARPNESS
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        # Normalize: >500 is very sharp, <100 is blurry
        sharpness_score = np.clip(laplacian_var / 500.0, 0.0, 1.0)
        
        # 2. EXPOSURE
        # Check histogram for clipping
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        total_pixels = gray.shape[0] * gray.shape[1]
        
        # Penalize if too many pixels are clipped (pure black or white)
        clipped_dark = hist[0:10].sum() / total_pixels
        clipped_bright = hist[246:256].sum() / total_pixels
        clipping_penalty = (clipped_dark + clipped_bright) * 2
        
        mean_brightness = np.mean(gray)
        exposure_score = max(0, 1.0 - (abs(mean_brightness - 128) / 128) - clipping_penalty)
        
        # 3. COLOR VIBRANCY
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        saturation = hsv[:, :, 1]
        mean_saturation = np.mean(saturation)
        # Higher saturation = more vibrant colors (0-255 range)
        vibrancy_score = np.clip(mean_saturation / 150.0, 0.0, 1.0)
        
        # Weighted average (prioritize sharpness and exposure)
        return 0.5 * sharpness_score + 0.3 * exposure_score + 0.2 * vibrancy_score

    def calculate_composition_score(self, frame: np.ndarray) -> float:
        """
        Simplified composition score without YOLO (to save memory).
        
        Uses edge detection and center-weighting instead of object detection.
        """
        if frame is None:
            return 0.5
            
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Edge detection to find areas of interest
            edges = cv2.Canny(gray, 50, 150)
            
            # Divide frame into 9 regions (rule of thirds)
            h, w = edges.shape
            third_h, third_w = h // 3, w // 3
            
            # Calculate edge density in each region
            regions = []
            for i in range(3):
                for j in range(3):
                    region = edges[i*third_h:(i+1)*third_h, j*third_w:(j+1)*third_w]
                    density = np.sum(region) / (third_h * third_w * 255)
                    regions.append(density)
            
            # Rule of thirds: prefer content in outer regions (not center)
            # Regions: 0 1 2
            #          3 4 5
            #          6 7 8
            # Center is region 4, prefer 0,2,6,8 (corners) and 1,3,5,7 (edges)
            
            center_density = regions[4]
            edge_density = (regions[1] + regions[3] + regions[5] + regions[7]) / 4
            corner_density = (regions[0] + regions[2] + regions[6] + regions[8]) / 4
            
            # Good composition has more content on edges/corners than center
            if center_density > 0:
                composition_score = (edge_density + corner_density) / (2 * center_density + 0.01)
            else:
                composition_score = edge_density + corner_density
                
            return np.clip(composition_score, 0.0, 1.0)
            
        except Exception as e:
            print(f"Composition score error: {e}")
            return 0.5

    def calculate_vibe_score(self, frame: np.ndarray, text_prompt: str) -> float:
        """
        Score based on semantic similarity to text_prompt using CLIP.
        Model is lazy-loaded on first call to save memory.
        """
        if not text_prompt:
            return 0.0
            
        # Lazy load CLIP only when needed
        self._load_clip_if_needed()
        
        if not self.clip_model:
            return 0.0
        
        try:
            from PIL import Image
            import clip
            
            # Preprocess image
            image = self.clip_preprocess(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))).unsqueeze(0).to(self.device)
            
            # Tokenize text
            text = clip.tokenize([text_prompt]).to(self.device)
            
            with torch.no_grad():
                image_features = self.clip_model.encode_image(image)
                text_features = self.clip_model.encode_text(text)
                
                # Normalize
                image_features /= image_features.norm(dim=-1, keepdim=True)
                text_features /= text_features.norm(dim=-1, keepdim=True)
                
                # Cosine similarity
                similarity = (image_features @ text_features.T).item()
                
            # Clean up tensors
            del image, text, image_features, text_features
            
            return max(0, similarity)
        except Exception as e:
            print(f"CLIP Error: {e}")
            return 0.0

    def get_total_score(self, frame: np.ndarray, text_prompt: str = "") -> dict:
        """Calculate total score with weighted components."""
        tech = self.calculate_technical_score(frame)
        comp = self.calculate_composition_score(frame)
        vibe = self.calculate_vibe_score(frame, text_prompt) if text_prompt else 0.0
        
        # If vibe prompt is provided, prioritize it heavily (50% weight)
        # Otherwise, focus on technical and composition
        if text_prompt:
            # Vibe-focused scoring: 50% vibe, 30% technical, 20% composition
            total = 0.5 * vibe + 0.3 * tech + 0.2 * comp
            
            # Minimum vibe threshold: reject frames that don't match user intent
            if vibe < 0.15:
                total *= 0.5  # Heavily penalize poor vibe matches
        else:
            # No vibe prompt: equal weight to technical and composition
            total = 0.6 * tech + 0.4 * comp
        
        return {
            "total": total,
            "technical": tech,
            "composition": comp,
            "vibe": vibe
        }
    
    def cleanup(self):
        """
        Explicitly clean up models and free memory.
        Call this after processing a video to reduce memory usage.
        """
        if self.clip_model is not None:
            del self.clip_model
            del self.clip_preprocess
            self.clip_model = None
            self.clip_preprocess = None
            self._clip_loaded = False
            
        # Force garbage collection
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        print("Memory cleaned up")
