import pywt
import cv2
import logging
import numpy as np
import time
from utils import constants

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# embedding.py
class WatermarkEmbedding:
    def __init__(self):
        # Initialize any variables
        self.ALPHA = 0.1
        self.FWT_LEVELS = 1
        self.FWT_WAVELET = 'db3'

    def load_image(self, image_path):
        """Load an image from the specified path."""
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)
        if image is None:
            logging.error(f"Error loading image at {image_path}")
            exit()
        return image

    def save_image(self, image, image_path):
        """Save an image to the specified path."""
        result = cv2.imwrite(image_path, image)
        if result:
            print("Media Saved at " + image_path)
        else:
            print("Error while saving media at " + image_path)
            exit()
    
    def fwt2(self, image):
        """Perform Fast Wavelet Transform."""
        wavelet = self.FWT_WAVELET
        level = self.FWT_LEVELS
        coeffs = pywt.wavedec2(image, wavelet, level=level)
        return coeffs

    def ifwt2(self, coeffs):
        """Perform Inverse Fast Wavelet Transform."""
        wavelet = self.FWT_WAVELET
        return pywt.waverec2(coeffs, wavelet)

    def qim_embed(self, coeff, watermark):
        """Embed watermark using Quantization Index Modulation."""
        alpha = self.ALPHA
        h, w = coeff.shape
        
        # Check if watermark is larger than the coefficient and resize if needed
        if watermark.shape[0] > h or watermark.shape[1] > w:
            watermark = cv2.resize(watermark, (w, h))

        # Replicate the watermark to match the size of the coefficient
        watermark_replicated = np.tile(watermark, (h // watermark.shape[0] + 1, w // watermark.shape[1] + 1))
        
        # Crop to the required size
        watermark_replicated = watermark_replicated[:h, :w]
        
        # If h or w are smaller than the watermark size, replicate to fill the remaining area
        if watermark_replicated.shape[0] < h or watermark_replicated.shape[1] < w:
            watermark_replicated = np.pad(watermark_replicated, 
                                        ((0, max(0, h - watermark_replicated.shape[0])),
                                         (0, max(0, w - watermark_replicated.shape[1]))),
                                        mode='constant', constant_values=0)
        
        # Ensure the replicated watermark matches the coefficient size
        watermark_replicated = watermark_replicated[:h, :w]
        LL_watermarked = np.copy(coeff)
        for i in range(h):
            for j in range(w):
                bit = watermark_replicated[i, j]
                if bit == 0:
                    LL_watermarked[i, j] = alpha * np.round(coeff[i, j] / alpha)
                else:
                    LL_watermarked[i, j] = alpha * np.round(coeff[i, j] / alpha) + alpha / 2

        return LL_watermarked
        #return coeff + alpha * watermark_replicated

    def embedding(self, host_media_file, watermark_file):
        """Embed watermark into each channel of the original image."""

        # Performance metrics
        start_time = time.time()

        # Load images
        print("Loading the host media file " + host_media_file + " and watermark " + watermark_file)
        load_start = time.time()
        host_media = self.load_image(constants.HOST_MEDIA_DIR + host_media_file)
        watermark = self.load_image(constants.WATERMARK_DIR + watermark_file)
        load_end = time.time()

        # Split media into RGB channels
        print("Splitting the files into RGB channels")
        split_start = time.time()
        original_channels = cv2.split(host_media)
        watermark_channels = cv2.split(watermark)
        split_end = time.time()

        # Embed watermark into each channel
        watermarked_channels = []
        embed_start = time.time()
        for i in range(3):  # Assuming RGB channels
            print("Processing Channels")
            coeffs = self.fwt2(original_channels[i])
            LL, _ = coeffs[0], coeffs[1]
            LL_wm = self.qim_embed(LL, watermark_channels[i])
            coeffs[0] = LL_wm
            watermarked_channel = self.ifwt2(coeffs)
            watermarked_channels.append(np.clip(watermarked_channel, 0, 255).astype(np.uint8))
        embed_end = time.time()

        # Merge channels and save the watermarked image
        merge_start = time.time()
        file = 'watermarked_media_' + host_media_file
        watermarked_media = cv2.merge(watermarked_channels)
        self.save_image(watermarked_media, constants.WATERMARKED_MEDIA_DIR + file)
        merge_end = time.time()

        # Log performance metrics
        total_time = time.time() - start_time
        print("Performance Metrics:")
        print(f"  Loading Time: {load_end - load_start:.4f} seconds")
        print(f"  Splitting Time: {split_end - split_start:.4f} seconds")
        print(f"  Embedding Time: {embed_end - embed_start:.4f} seconds")
        print(f"  Merging and Saving Time: {merge_end - merge_start:.4f} seconds")
        print(f"  Total Embedding Time: {total_time:.4f} seconds")

        return file