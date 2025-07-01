# Import Packages
from PIL import Image
from PIL.ExifTags import TAGS

# Get EXIF data 
def get_exif_data(image_stream):
    readable_exif = {}
    try:
        image = Image.open(image_stream)
        # Use PIL method to get EXIF
        exifdata = image.getexif()
        
        if exifdata:
            for tag_id, value in exifdata.items():
                tag = TAGS.get(tag_id, tag_id)
                readable_exif[tag] = value
    
        readable_exif["width"] = image.width
        readable_exif["height"] = image.height
    
    # Put exception in the same dict
    except Exception as e:
        readable_exif['Error'] = str(e)
    
    return readable_exif
