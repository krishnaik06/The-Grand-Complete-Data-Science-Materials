import numpy as np
import pickle
from PIL import Image
import os
import warnings

warnings.filterwarnings('ignore')


class SimpleFeatureExtractor:
    def extract_basic_features(self, image_path):
        """Extract simple color and texture features"""
        img = Image.open(image_path)
        img = img.resize((64, 64))
        img_array = np.array(img)

        if len(img_array.shape) != 3:
            return None

        features = []

        # Color averages (RGB)
        features.extend([
            np.mean(img_array[:, :, 0]),  # Red
            np.mean(img_array[:, :, 1]),  # Green
            np.mean(img_array[:, :, 2])  # Blue
        ])

        # Color variations
        features.extend([
            np.std(img_array[:, :, 0]),
            np.std(img_array[:, :, 1]),
            np.std(img_array[:, :, 2])
        ])

        # Basic texture
        gray = np.mean(img_array, axis=2)
        h_diff = np.mean(np.abs(np.diff(gray, axis=1)))
        v_diff = np.mean(np.abs(np.diff(gray, axis=0)))
        features.extend([h_diff, v_diff])

        return np.array(features)


class LeafTester:
    def __init__(self, model_file="plant_disease_model.pkl"):
        """Load trained model"""
        if not os.path.exists(model_file):
            print(f" Model file '{model_file}' not found!")
            print("Please run train_model.py first to create the model.")
            return

        # Load saved model
        with open(model_file, 'rb') as f:
            model_data = pickle.load(f)

        self.model = model_data['model']
        self.label_encoder = model_data['label_encoder']
        self.extractor = SimpleFeatureExtractor()

        print(f" Model loaded from: {model_file}")
        print(f" Can detect: {list(self.label_encoder.classes_)}")

    def predict_leaf(self, image_path):
        """Predict disease for single leaf photo"""

        if not os.path.exists(image_path):
            print(f" Photo not found: {image_path}")
            return None, 0

        print(f"\n Analyzing photo: {image_path}")

        try:
            # Extract features
            features = self.extractor.extract_basic_features(image_path)

            if features is None:
                print(" Could not process image (invalid format?)")
                return None, 0

            # Predict
            prediction = self.model.predict([features])[0]
            probabilities = self.model.predict_proba([features])[0]
            confidence = np.max(probabilities)

            # Decode result
            disease_name = self.label_encoder.inverse_transform([prediction])[0]

            # Display results
            print(f" DIAGNOSIS: {disease_name}")
            print(f" CONFIDENCE: {confidence:.3f} ({confidence * 100:.1f}%)")

            # Interpretation
            if confidence > 0.8:
                print(" HIGH CONFIDENCE - Trust this result")
            elif confidence > 0.6:
                print("  MEDIUM CONFIDENCE - Probably correct")


            return disease_name, confidence

        except Exception as e:
            print(f" Error processing image: {str(e)}")
            return None, 0


# MAIN TESTING SCRIPT
if __name__ == "__main__":


    # Load trained model
    tester = LeafTester("plant_disease_model.pkl")

    if hasattr(tester, 'model'):
        print(f" READY TO TEST LEAF PHOTOS!")


        # TEST YOUR PHOTOS HERE
        test_photos = [
            "healthy_leaf.jpg",
            "Suspicious_leaf.JPG"
        ]

        for photo_path in test_photos:
            if os.path.exists(photo_path):
                disease, confidence = tester.predict_leaf(photo_path)

            else:
                print(f"  Skipping: {photo_path} (file not found)")