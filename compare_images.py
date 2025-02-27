import sys
import os
from PIL import Image, ImageDraw
import numpy as np


def compare_images(image1_path, image2_path):
    # Open the images
    img1 = Image.open(image1_path).convert("RGBA")
    img2 = Image.open(image2_path).convert("RGBA")

    # Ensure the dimensions match
    if img1.size != img2.size:
        raise ValueError("The dimensions of the images do not match!")

    # Convert images to numpy arrays
    arr1 = np.array(img1)
    arr2 = np.array(img2)

    # Create a blank result image
    result_img = img1.copy()
    result_pixels = np.array(result_img)

    # Find differences
    diff_mask = np.any(arr1 != arr2, axis=-1)  # Mask of differing pixels

    # Apply transparency to the result
    result_pixels[..., 3] = 128  # Set alpha channel (semi-transparency)

    # Highlight differences in red (without transparency)
    result_pixels[diff_mask] = [255, 0, 0, 255]  # Red color

    # Update the result image
    result_img = Image.fromarray(result_pixels)

    # Draw yellow circles around small clusters of differing pixels
    draw = ImageDraw.Draw(result_img)
    #for y in range(diff_mask.shape[0]):
        #for x in range(diff_mask.shape[1]):
            #if diff_mask[y, x]:
                # Check if this is an isolated or small cluster of pixels
                #cluster_size = np.sum(diff_mask[max(0, y-1):y+2, max(0, x-1):x+2])
                #if cluster_size <= 3:  # Small cluster (e.g., <= 3 pixels)
                    #draw.ellipse(
                       # (x-5, y-5, x+5, y+5), outline="yellow", width=3
                    #)

    return result_img


def save_result_image(result_img, image1_path, image2_path):
    # Get the parent folder and file names without extensions
    parent_folder = os.path.dirname(image1_path)
    image1_name = os.path.splitext(os.path.basename(image1_path))[0]
    image2_name = os.path.splitext(os.path.basename(image2_path))[0]

    # Create the result file name
    result_file_name = f"{image1_name}_vs_{image2_name}_comparison.png"
    result_path = os.path.join(parent_folder, result_file_name)

    # Save the result
    result_img.save(result_path)
    print(f"Result saved to: {result_path}")


def main():
    if len(sys.argv) != 3:
        print("Usage: python compare_images.py <image1_path> <image2_path>")
        sys.exit(1)

    image1_path = sys.argv[1]
    image2_path = sys.argv[2]

    try:
        # Compare the images and create the result
        result_img = compare_images(image1_path, image2_path)

        # Save the result
        save_result_image(result_img, image1_path, image2_path)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
