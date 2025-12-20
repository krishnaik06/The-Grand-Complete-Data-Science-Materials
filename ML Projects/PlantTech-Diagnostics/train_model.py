import numpy as np
import os
import pickle
from PIL import Image
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import warnings

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


class SimplePlantClassifier:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=50, random_state=42)
        self.label_encoder = LabelEncoder()

    def load_dataset(self, dataset_path):
        """Load and process dataset"""
        print(f"Loading dataset from: {dataset_path}")

        features = []
        labels = []
        extractor = SimpleFeatureExtractor()

        for class_name in os.listdir(dataset_path):
            class_path = os.path.join(dataset_path, class_name)

            if not os.path.isdir(class_path):
                continue

            print(f"Processing: {class_name}")
            count = 0

            for img_name in os.listdir(class_path):
                if img_name.lower().endswith(('.jpg', '.jpeg', '.png')):
                    img_path = os.path.join(class_path, img_name)

                    try:
                        feature_vector = extractor.extract_basic_features(img_path)
                        if feature_vector is not None:
                            features.append(feature_vector)
                            labels.append(class_name)
                            count += 1

                        if count >= 100:  # Limit for demo
                            break
                    except:
                        continue

            print(f"  Loaded {count} images")

        return np.array(features), np.array(labels)

    def train(self, features, labels):
        """Train the classifier"""
        print(f"\nTraining with {len(features)} samples...")

        # Encode labels
        encoded_labels = self.label_encoder.fit_transform(labels)

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            features, encoded_labels, test_size=0.2, random_state=42
        )

        # Train
        self.model.fit(X_train, y_train)

        # Test
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        print(f"Accuracy: {accuracy:.3f} ({accuracy * 100:.1f}%)")
        return accuracy

    def save_model(self, filename="plant_disease_model.pkl"):
        """Save trained model to file"""
        model_data = {
            'model': self.model,
            'label_encoder': self.label_encoder
        }

        with open(filename, 'wb') as f:
            pickle.dump(model_data, f)

        print(f" Model saved as: {filename}")


# MAIN TRAINING SCRIPT
if __name__ == "__main__":
    print("=== TRAINING PLANT DISEASE MODEL ===")

    # Initialize classifier
    classifier = SimplePlantClassifier()

    # Load dataset
    dataset_path = "TomatoDataset"

    if not os.path.exists(dataset_path):
        print(f" Dataset folder '{dataset_path}' not found!")
        print("Please download dataset and organize as shown in instructions.")
    else:
        # Train model
        features, labels = classifier.load_dataset(dataset_path)

        if len(features) > 0:
            accuracy = classifier.train(features, labels)

            # Save trained model
            classifier.save_model("plant_disease_model.pkl")

            print(f"\n TRAINING COMPLETED!")
            print(f"   Accuracy: {accuracy * 100:.1f}%")

        else:
            print(" No images found! ")
