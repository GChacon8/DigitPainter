import os
from PIL import Image
import numpy as np
import argparse
import joblib

def count_images_per_label(labels):
    label_counts = np.zeros(10, dtype=int)
    for label in labels:
        label_counts[label] += 1
    return label_counts

def load_images(root_dir):
    image_data = []  # To store flattened image data
    labels = []      # To store corresponding labels

    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith(".png"):
                image_path = os.path.join(dirpath, filename)
                try:
                    # Convert to grayscale
                    image = Image.open(image_path).convert("L")  
                    if image.size == (28, 28):
                        # Check if first character of filename is a digit
                        if filename[0].isdigit():
                            # Flatten the image
                            flattened_image = np.array(image).flatten()
                            image_data.append(flattened_image)
                            # Extract label from filename (first character)
                            label = int(filename[0])
                            labels.append(label)
                except Exception as e:
                    print(f"Error processing {image_path}: {e}")

    return np.array(image_data), np.array(labels)

def save_data(image_data, labels, output_filename):
    data_dict = {"image_data": image_data, "labels": labels}
    joblib.dump(data_dict, output_filename)
    print(f"Data saved to {output_filename}")

def main():
    parser = argparse.ArgumentParser(description="Image data collection and preprocessing")
    parser.add_argument("--root", default="./Imagenes", help="Root directory containing images")
    parser.add_argument("--out",default="testdata.job", help="Output filename for saved data")
    args = parser.parse_args()

    image_data, labels = load_images(args.root)
    save_data(image_data, labels, args.out)

    # Compute statistics
    label_counts = count_images_per_label(labels)
    total_images = len(labels)
    
    print("Number of Images for Each Label:")
    for label, count in enumerate(label_counts):
        print(f"Label {label}: {count} images")

    print(f"Total Number of Images: {total_images}")
    
    # How to load the data back:
    # loaded_data = joblib.load(args.out)
    # loaded_image_data = loaded_data["image_data"]
    # loaded_labels = loaded_data["labels"]  


if __name__ == "__main__":
    main()
