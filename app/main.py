# Import Packages
from PIL import Image
from PIL.ExifTags import TAGS
from pathlib import Path

# Configuration variables
samples_dir = Path("app/samples")
image_filename = "Coffee.jpg"
image_path = samples_dir / image_filename
image = Image.open(image_path)

# Get EXIF data 
exifdata = image.getexif()
readable_exif = {}
for tag_id, value in exifdata.items():
    tag = TAGS.get(tag_id, tag_id)
    readable_exif[tag] = value

# Print some metadata
print(readable_exif)
