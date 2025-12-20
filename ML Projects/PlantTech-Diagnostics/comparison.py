import numpy as np
from PIL import Image
import os
import warnings
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, f1_score
from sklearn.tree import plot_tree
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import seaborn as sns

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


class MultiWindowVisualizer:
    def __init__(self):
        self.algorithms = {
            'SVM': SVC(kernel='rbf', probability=True, random_state=42),
            'Random Forest': RandomForestClassifier(n_estimators=50, max_depth=4, random_state=42),
            'KNN': KNeighborsClassifier(n_neighbors=5)
        }

        self.label_encoder = LabelEncoder()
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=2)
        self.extractor = SimpleFeatureExtractor()
        self.colors = None
        self.accuracies = {}

        # Set matplotlib to interactive mode
        plt.ion()

    def generate_colors(self, n_colors):
        """Generate enough colors for all classes"""
        if n_colors <= 10:
            base_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7',
                           '#DDA0DD', '#F0B27A', '#85C1E9', '#F8C471', '#82E0AA']
            return base_colors[:n_colors]
        else:
            cmap = plt.cm.get_cmap('tab20')
            if n_colors > 20:
                cmap = plt.cm.get_cmap('hsv')
            return [cmap(i / n_colors) for i in range(n_colors)]

    def load_dataset(self, dataset_path):
        """Load and process dataset"""
        print("Loading dataset...")

        features = []
        labels = []

        for class_name in os.listdir(dataset_path):
            class_path = os.path.join(dataset_path, class_name)

            if not os.path.isdir(class_path):
                continue

            print(f"   Processing: {class_name}")
            count = 0

            for img_name in os.listdir(class_path):
                if img_name.lower().endswith(('.jpg', '.jpeg', '.png')):
                    img_path = os.path.join(class_path, img_name)

                    try:
                        feature_vector = self.extractor.extract_basic_features(img_path)
                        if feature_vector is not None:
                            features.append(feature_vector)
                            labels.append(class_name)
                            count += 1

                        if count >= 100:
                            break
                    except:
                        continue

            print(f"    {count} images")

        return np.array(features), np.array(labels)

    def prepare_data(self, features, labels):
        """Prepare data for visualization"""
        print("\n Preparing data for visualization...")

        # Encode labels
        encoded_labels = self.label_encoder.fit_transform(labels)

        # Generate colors
        n_classes = len(np.unique(encoded_labels))
        self.colors = self.generate_colors(n_classes)
        print(f"    Dataset has {n_classes} classes")

        # Scale features
        scaled_features = self.scaler.fit_transform(features)

        # Apply PCA for 2D visualization
        pca_features = self.pca.fit_transform(scaled_features)

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            pca_features, encoded_labels, test_size=0.3, random_state=42, stratify=encoded_labels
        )

        X_train_full, X_test_full, _, _ = train_test_split(
            scaled_features, encoded_labels, test_size=0.3, random_state=42, stratify=encoded_labels
        )

        return X_train, X_test, y_train, y_test, X_train_full, X_test_full

    def create_svm_window(self, X_train, y_train):
        """Create SVM visualization in separate window"""
        print("Creating SVM window...")

        # Create new figure for SVM
        fig_svm = plt.figure(figsize=(14, 10))
        fig_svm.canvas.manager.set_window_title('SVM Classification - Plant Disease Detection')
        fig_svm.suptitle('Support Vector Machine (SVM) with RBF Kernel\nPlant Disease Detection',
                         fontsize=18, fontweight='bold')

        # Train SVM on 2D data
        svm_2d = SVC(kernel='rbf', C=1.0, gamma='scale', random_state=42)
        svm_2d.fit(X_train, y_train)

        # Create mesh for decision boundary
        h = 0.02
        x_min, x_max = X_train[:, 0].min() - 1, X_train[:, 0].max() + 1
        y_min, y_max = X_train[:, 1].min() - 1, X_train[:, 1].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

        # Predict on mesh
        Z = svm_2d.predict(np.column_stack([xx.ravel(), yy.ravel()]))
        Z = Z.reshape(xx.shape)

        # Main plot
        ax = fig_svm.add_subplot(111)

        # Plot decision boundary
        unique_labels = np.unique(y_train)
        contourf = ax.contourf(xx, yy, Z, alpha=0.4, cmap=ListedColormap(self.colors[:len(unique_labels)]))
        ax.contour(xx, yy, Z, colors='black', linewidths=1, alpha=0.8)

        # Plot data points
        for i, label in enumerate(unique_labels):
            mask = y_train == label
            class_name = self.label_encoder.classes_[label]
            # Truncate long class names
            display_name = class_name.replace('Tomato___', '').replace('_', ' ')

            ax.scatter(X_train[mask, 0], X_train[mask, 1],
                       c=[self.colors[i]], alpha=0.9, s=100, edgecolors='black', linewidths=0.5,
                       label=display_name)

        # Highlight support vectors
        support_vectors = svm_2d.support_vectors_
        ax.scatter(support_vectors[:, 0], support_vectors[:, 1],
                   s=400, facecolors='none', edgecolors='red', linewidths=4,
                   label='Support Vectors', alpha=0.9)

        ax.set_xlabel('Principal Component 1', fontsize=16)
        ax.set_ylabel('Principal Component 2', fontsize=16)
        ax.grid(True, alpha=0.3)
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=10)

        # Add accuracy text
        accuracy = svm_2d.score(X_train, y_train)
        self.accuracies['SVM'] = accuracy

        ax.text(0.02, 0.98, f'Training Accuracy: {accuracy:.3f} ({accuracy * 100:.1f}%)',
                transform=ax.transAxes,
                bbox=dict(boxstyle="round,pad=0.5", facecolor="yellow", alpha=0.8),
                verticalalignment='top', fontweight='bold', fontsize=14)

        # Add explanation text
        explanation = "• Red circles: Support Vectors (key data points)\n• Colored regions: Decision boundaries\n• Black lines: Class separation borders"
        ax.text(0.02, 0.02, explanation, transform=ax.transAxes,
                bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.8),
                verticalalignment='bottom', fontsize=12)

        plt.tight_layout()
        plt.savefig('svm_visualization.png', dpi=300, bbox_inches='tight')
        print("   SVM window created and saved")

        # Position window
        try:
            mngr = fig_svm.canvas.manager
            mngr.window.wm_geometry("+50+50")
        except:
            pass  # Skip positioning if it fails

        plt.draw()
        plt.pause(0.1)  # Small pause to ensure rendering

        return accuracy

    def create_random_forest_window(self, X_train_full, y_train):
        """Create Random Forest visualization in separate window"""
        print("Creating Random Forest window...")

        # Create new figure for Random Forest
        fig_rf = plt.figure(figsize=(18, 12))
        fig_rf.canvas.manager.set_window_title('Random Forest Tree - Plant Disease Detection')
        fig_rf.suptitle('Random Forest Decision Tree Structure\nPlant Disease Detection',
                        fontsize=18, fontweight='bold')

        # Train a simple tree for visualization
        rf = RandomForestClassifier(n_estimators=1, max_depth=4, random_state=42)
        rf.fit(X_train_full, y_train)

        # Feature names
        feature_names = ['Red_Avg', 'Green_Avg', 'Blue_Avg', 'Red_Std',
                         'Green_Std', 'Blue_Std', 'Texture_H', 'Texture_V']

        # Convert to Python list and clean class names
        class_names = [name.replace('Tomato___', '').replace('_', ' ')
                       for name in self.label_encoder.classes_]

        # Plot the tree
        ax = fig_rf.add_subplot(111)
        plot_tree(rf.estimators_[0],
                  feature_names=feature_names,
                  class_names=class_names,
                  filled=True,
                  rounded=True,
                  ax=ax,
                  fontsize=9,
                  max_depth=4)

        # Calculate accuracy
        accuracy = rf.score(X_train_full, y_train)
        self.accuracies['Random Forest'] = accuracy

        # Add accuracy text
        ax.text(0.02, 0.98, f'Training Accuracy: {accuracy:.3f} ({accuracy * 100:.1f}%)',
                transform=ax.transAxes,
                bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgreen", alpha=0.8),
                verticalalignment='top', fontweight='bold', fontsize=14)

        # Add explanation
        explanation = """Tree Reading Guide:
• Each box = Decision node or prediction
• Top line = Feature condition (e.g., Red_Avg <= 45.2)
• Samples = Number of training samples at this node  
• Value = Class distribution • Color = Dominant class"""

        ax.text(0.02, 0.02, explanation, transform=ax.transAxes,
                bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow", alpha=0.8),
                verticalalignment='bottom', fontsize=11)

        plt.tight_layout()
        plt.savefig('random_forest_visualization.png', dpi=300, bbox_inches='tight')
        print("   Random Forest window created and saved")

        # Position window
        try:
            mngr = fig_rf.canvas.manager
            mngr.window.wm_geometry("+550+50")
        except:
            pass

        plt.draw()
        plt.pause(0.1)

        return accuracy

    def create_knn_window(self, X_train, y_train):
        """Create KNN visualization in separate window"""
        print(" Creating KNN window...")

        # Create new figure for KNN
        fig_knn = plt.figure(figsize=(14, 10))
        fig_knn.canvas.manager.set_window_title('KNN Algorithm - Plant Disease Detection')
        fig_knn.suptitle('K-Nearest Neighbors (KNN) Algorithm\nPlant Disease Detection (k=5)',
                         fontsize=18, fontweight='bold')

        # Train KNN
        knn_2d = KNeighborsClassifier(n_neighbors=5)
        knn_2d.fit(X_train, y_train)

        # Create mesh for decision boundary
        h = 0.02
        x_min, x_max = X_train[:, 0].min() - 1, X_train[:, 0].max() + 1
        y_min, y_max = X_train[:, 1].min() - 1, X_train[:, 1].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

        # Predict on mesh
        Z = knn_2d.predict(np.column_stack([xx.ravel(), yy.ravel()]))
        Z = Z.reshape(xx.shape)

        ax = fig_knn.add_subplot(111)

        # Plot decision regions
        unique_labels = np.unique(y_train)
        ax.contourf(xx, yy, Z, alpha=0.4, cmap=ListedColormap(self.colors[:len(unique_labels)]))

        # Plot data points
        for i, label in enumerate(unique_labels):
            mask = y_train == label
            class_name = self.label_encoder.classes_[label]
            display_name = class_name.replace('Tomato___', '').replace('_', ' ')

            ax.scatter(X_train[mask, 0], X_train[mask, 1],
                       c=[self.colors[i]], alpha=0.9, s=100, edgecolors='black', linewidths=0.5,
                       label=display_name)

        # Demonstrate KNN with a sample point
        if len(X_train) > 15:
            sample_point = X_train[15]  # Pick a sample point
            distances, indices = knn_2d.kneighbors([sample_point])

            # Highlight the query point
            ax.scatter(sample_point[0], sample_point[1],
                       c='red', s=400, marker='*', edgecolors='black', linewidths=4,
                       label='Query Point', zorder=5)

            # Highlight nearest neighbors
            neighbors = X_train[indices[0]]
            ax.scatter(neighbors[:, 0], neighbors[:, 1],
                       s=200, facecolors='none', edgecolors='red', linewidths=4,
                       label='5 Nearest Neighbors', zorder=4)

            # Draw lines to neighbors
            for neighbor in neighbors:
                ax.plot([sample_point[0], neighbor[0]], [sample_point[1], neighbor[1]],
                        'r--', alpha=0.8, linewidth=3)

        ax.set_xlabel('Principal Component 1', fontsize=16)
        ax.set_ylabel('Principal Component 2', fontsize=16)
        ax.grid(True, alpha=0.3)
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=10)

        # Calculate accuracy
        accuracy = knn_2d.score(X_train, y_train)
        self.accuracies['KNN'] = accuracy

        # Add accuracy text
        ax.text(0.02, 0.98, f'Training Accuracy: {accuracy:.3f} ({accuracy * 100:.1f}%)',
                transform=ax.transAxes,
                bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.8),
                verticalalignment='top', fontweight='bold', fontsize=14)

        # Add explanation
        explanation = """KNN Process:
• Red star = New data point to classify
• Red circles = 5 closest neighbors found
• Dashed lines = Distance measurements
• Final class = Majority vote of 5 neighbors"""

        ax.text(0.02, 0.02, explanation, transform=ax.transAxes,
                bbox=dict(boxstyle="round,pad=0.5", facecolor="lightcyan", alpha=0.8),
                verticalalignment='bottom', fontsize=11)

        plt.tight_layout()
        plt.savefig('knn_visualization.png', dpi=300, bbox_inches='tight')
        print("    KNN window created and saved")

        # Position window
        try:
            mngr = fig_knn.canvas.manager
            mngr.window.wm_geometry("+1050+50")
        except:
            pass

        plt.draw()
        plt.pause(0.1)

        return accuracy

    def create_all_windows(self, X_train, X_test, y_train, y_test, X_train_full, X_test_full):
        """Create all three windows sequentially but keep them all open"""
        print("\n Creating all visualization windows...")
        print("   Each window will open and remain visible.")

        # Create windows one by one
        self.create_svm_window(X_train, y_train)
        self.create_random_forest_window(X_train_full, y_train)
        self.create_knn_window(X_train, y_train)

        print("   All three windows are now open!")

    def display_summary(self):
        """Display final comparison summary"""
        print("\n" + "=" * 60)
        print(" ALGORITHM COMPARISON SUMMARY")
        print("=" * 60)

        if self.accuracies:
            # Sort by accuracy
            sorted_results = sorted(self.accuracies.items(), key=lambda x: x[1], reverse=True)

            print("\n ACCURACY RANKING:")
            for i, (name, accuracy) in enumerate(sorted_results):
                print(f"{i + 1}. {name:<15} {accuracy:.3f} ({accuracy * 100:.1f}%) {f1_score(name)}")

            print(f"\n WINNER: {sorted_results[0][0]}")
            print(f"   Best Accuracy: {sorted_results[0][1]:.1%}")

        print("\n All visualization windows should now be visible!")
        print("   You can interact with each window independently.")


# MAIN EXECUTION
if __name__ == "__main__":
    print("=" * 70)
    print("🌱 PLANT DISEASE DETECTION - MULTIPLE WINDOW VISUALIZATIONS")
    print("=" * 70)

    visualizer = MultiWindowVisualizer()

    # Load dataset
    dataset_path = "TomatoDataset"  # Change to your dataset path

    if os.path.exists(dataset_path):
        features, labels = visualizer.load_dataset(dataset_path)

        if len(features) > 0:
            # Prepare data
            X_train, X_test, y_train, y_test, X_train_full, X_test_full = visualizer.prepare_data(features, labels)

            # Create all windows
            visualizer.create_all_windows(X_train, X_test, y_train, y_test, X_train_full, X_test_full)

            # Display summary
            visualizer.display_summary()

            print(" ALL VISUALIZATIONS COMPLETE!")
            print("    Files saved:")
            print("     • svm_visualization.png")
            print("     • random_forest_visualization.png")
            print("     • knn_visualization.png")

            # Keep all windows open
            input("\nPress Enter to close all windows and exit...")
            plt.close('all')

        else:
            print(" No images found!")
    else:
        print(f" Dataset folder '{dataset_path}' not found!")
