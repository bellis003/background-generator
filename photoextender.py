from PIL import Image, UnidentifiedImageError
import os

def extend_image_horizontally(img, new_width, column_width):
    original_width, original_height = img.size
    
    if new_width <= original_width:
        print("The new width should be greater than the original width.")
        return None
    
    left_column = img.crop((0, 0, column_width, original_height))
    right_column = img.crop((original_width-column_width, 0, original_width, original_height))
    
    extension_width = (new_width - original_width) // 2
    
    new_img = Image.new('RGB', (new_width, original_height))
    
    for x in range(0, extension_width, column_width):
        new_img.paste(left_column, (x, 0))

    for x in range(new_width-extension_width, new_width, column_width):
        new_img.paste(right_column, (x, 0))
    
    new_img.paste(img, (extension_width, 0))
    
    return new_img

# The main portion
folder_path = '/Users/ellisbr/Desktop/BETEST/ImageProcessing/TGluck_Extended'
destination_path = os.path.join(folder_path, 'Extended')

origin_paths = {
    "original_gray": 1,  # column_width = 1 for gray images
    "original_green": 1900  # column_width = 1500 for green images
}

# Ensure destination path exists, if not, create it
if not os.path.exists(destination_path):
    os.mkdir(destination_path)

failed_images = []

for origin, column_width in origin_paths.items():
    origin_path = os.path.join(folder_path, origin)
    
    if os.path.exists(origin_path) and os.path.isdir(origin_path):
        print(f"Processing Folder: '{origin}'")
    else:
        print(f"Folder '{origin}' does not exist!")
        continue
    
    contents = os.listdir(origin_path)

    for item in contents:
        if not item.endswith('.DS_Store'):
            item_path = os.path.join(origin_path, item)
            if os.path.isfile(item_path):
                filename, extension = os.path.splitext(item)
                if extension.lower() in ['.jpg', '.png']:
                    try:
                        with Image.open(item_path) as img:
                            new_width = 20000  # Desired width

                            new_img = extend_image_horizontally(img, new_width, column_width)
                            
                            if new_img:
                                new_filename = filename + '_extended' + extension
                                new_path = os.path.join(destination_path, new_filename)
                                new_img.save(new_path)
                                print(f'New image saved at {new_path}')
                    except (UnidentifiedImageError, IOError) as e:
                        print(f"An error occurred while processing {item}: {e}")
                        failed_images.append(item)

if failed_images:
    print("Failed to process the following images:")
    for image in failed_images:
        print(image)



