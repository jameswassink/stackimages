import os
from PIL import Image

# Set the directory containing the images
image_dir = "./input"
output_dir = "./output"

def stack_images(image1, image2):

    # Get the dimensions of the first image
    width1, height1 = image1.size

    # Check if the images are in portrait orientation
    if height1 < width1:
        image1 = image1.rotate(90, expand=True)  # Rotate the first image 90 degrees
        width1, height1 = image1.size

    if image2:
        # Get the dimensions of the second image
        width2, height2 = image2.size

        if height2 < width2:
            image2 = image2.rotate(90, expand=True)  # Rotate the second image 90 degrees
            width2, height2 = image2.size

        # Check if the images have different widths
        if height1 != height2:
            # Calculate the scale factor to make the widths equal
            scale_factor = height2 / height1 if height1 < height2 else height1 / height2

            # Scale down the smaller image to match the width of the larger one
            if height1 < height2:
                height1 = height2
                width1 = int(width1 * scale_factor)
                # Resize the first image to the new dimensions
                image1 = image1.resize((width1, height1))
            else:
                height2 = height1
                width2 = int(width2 * scale_factor)
            # Resize the first image to the new dimensions
                image2 = image2.resize((width2, height2))

            # Resize the first image to the new dimensions
            image1 = image1.resize((width1, height1))

        # Calculate the dimensions of the stacked image
        stacked_width = width1 + width2
        stacked_height = max(height1, height2)
    else: 
        stacked_width = width1 *2
        stacked_height = height1
    

    # Create a new blank image with the calculated dimensions
    stacked_image = Image.new("RGB", (stacked_width, stacked_height), 'white')

    # Paste the first image at the top
    stacked_image.paste(image1, (0, 0))

    if image2:
        # Paste the second image beside the first
        stacked_image.paste(image2, (width1, 0))

    return stacked_image



# List all files in the directory
image_files = sorted([f for f in os.listdir(image_dir) if (f.endswith(".jpg") or f.endswith(".JPG"))])

num_files = len(image_files)
# Process images two at a time
for i in range(0, num_files, 2):
    # Get the paths of the two images to stack
    image_path1 = os.path.join(image_dir, image_files[i])
    image_path2 = os.path.join(image_dir, image_files[i + 1]) if  i+1 < num_files else  None

    # Open the two images
    image1 = Image.open(image_path1)
    image2 = Image.open(image_path2) if image_path2 else None

    # Rest of the code to resize and stack the images goes here...
    stacked_image = stack_images(image1, image2)

    # Save the stacked image with a suitable filename, e.g., "stacked_1.jpg"
    stacked_image_path = os.path.join(output_dir, f"stacked_{i // 2 + 1}.jpg")
    stacked_image.save(stacked_image_path)

    # Close the images
    image1.close()
    if image2:
        image2.close()

