import os
import cv2
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import random
import shutil

# Define background value and two colors for the binary mask
BACKGROUND_VALUE = 10  # Change this if your background value is different
bg_color = '#BBBD22'
fg_color = '#16417C'
cmap = mcolors.ListedColormap([bg_color, fg_color])

# Path to the folder containing images and masks
data_folder = "E:/Santosh_master_thesis/Understanding_citizenscience_species_segmentation/iNaturalist"

# Get list of class folders
class_folders = os.listdir(data_folder)

# Filter out class folders with "_mask" in their names for masks
mask_classes = [c for c in class_folders if "_mask" in c]

# Define the number of examples to plot for each class
num_examples = 4

# Define the maximum number of subplots
max_subplots = 160

# Plot images and masks
plt.figure(figsize=(20, 20))
plt.subplots_adjust(left=0.02, bottom=0.02, right=0.98,
                    top=0.98, wspace=0.1, hspace=0.1)

# Determine the number of rows and columns for subplots
num_rows = min(len(mask_classes), max_subplots // 2)
num_cols = min(2 * num_examples, max_subplots)

# Adjust the number of columns to include the class name as the first column
# Adding 1 for the class name column
num_cols_adjusted = min(2 * num_examples + 1, max_subplots + num_rows)

plt.figure(figsize=(20, 20))
plt.subplots_adjust(left=0.02, bottom=0.02, right=0.98,
                    top=0.98, wspace=0.1, hspace=0.1)

for i, mask_class in enumerate(sorted(mask_classes)):
    mask_folder = os.path.join(data_folder, mask_class)

    masks = os.listdir(mask_folder)
    # Randomly select masks
    masks = random.sample(masks, min(num_examples, len(masks)))

    # Add class name in the first column of each row
    plt.figtext(0.01, 1 - (i + 0.5) / num_rows,
                f'{mask_class[:-5]}', ha='left', va='center', fontsize=12, fontweight='bold')

    for j, mask_name in enumerate(masks):
        if (i * num_examples + j) >= (max_subplots // 2):
            break

        mask_path = os.path.join(mask_folder, mask_name)

        image_name = mask_name[5:-4] + ".jpg"
        class_folder = mask_class[:-5]
        image_path = os.path.join(data_folder, class_folder, image_name)

        if not os.path.exists(image_path):
            print(f"Image file {image_path} not found.")
            continue

        image = cv2.imread(image_path)
        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

        if image is None or mask is None:
            print(f"Error loading image or mask: {image_path} / {mask_path}")
            continue

        # Convert mask to binary: 0 for background, 1 for foreground
        mask_binary = np.where(mask == BACKGROUND_VALUE, 0, 1)

        # Adjust the subplot indices to account for the first column being used for class names
        image_subplot_index = i * num_cols_adjusted + 2 * j + \
            2  # Shift to the right to accommodate the class name
        mask_subplot_index = i * num_cols_adjusted + 2 * j + 3

        # Plot image
        plt.subplot(num_rows, num_cols_adjusted, image_subplot_index)
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        plt.axis('off')

        # Plot binary mask using the two-color colormap
        plt.subplot(num_rows, num_cols_adjusted, mask_subplot_index)
        plt.imshow(mask_binary, cmap=cmap, vmin=0, vmax=1)
        plt.axis('off')

# Path to save the plot
save_path = os.path.join(data_folder, "plot_image_masks.png")

# Ensure the directory exists
os.makedirs(os.path.dirname(save_path), exist_ok=True)

# Save the plot as an image file
plt.savefig(save_path)
plt.show()
