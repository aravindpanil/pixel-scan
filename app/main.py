# Import Packages
from PIL import Image
from PIL.ExifTags import TAGS
from pathlib import Path

# Configuration variables
samples_dir = Path("app/samples")
image_filename = "Glass.jpg"

# Get EXIF data 
def get_exif_data(image):
    exifdata = image.getexif()
    readable_exif = {}
    for tag_id, value in exifdata.items():
        tag = TAGS.get(tag_id, tag_id)
        readable_exif[tag] = value
    
    readable_exif["width"] = image.width
    readable_exif["height"] = image.height
    
    return readable_exif

# Open file with Error handling
try:
    image_path = Path(samples_dir/image_filename)
    image = Image.open(image_path)
    
    readable_exif = get_exif_data(image)
        # Print EXIF data
    if readable_exif:
        print("\nEXIF Data:\n")
        for tag, value in readable_exif.items():
                print(f"{tag}: {value}")
    else:
        print("No EXIF data found")

except FileNotFoundError as e:
    print(f"File not found: {e}. Please check the image name")
except Exception as e:
    print(f"Error opening image: {e}")
