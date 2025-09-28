import pyexiv2

# onefolder splits up tags using pipes, storing them hierarchically in
# Xmp.lr.hierarchicalSubject

def get_tags(image_path):
    img = pyexiv2.Image(image_path)
    xmp = img.read_xmp()

    tags = xmp['Xmp.lr.hierarchicalSubject']

    split_tags = []
    for tag in tags:
        split_tags += tag.split('|')

    return split_tags

def get_alt_text(image_path):
    img = pyexiv2.Image(image_path)
    exif = img.read_exif()

    alt_text = ""
    try:
        alt_text = exif['Exif.Image.ImageDescription']
    except:
        alt_text = ""

    return alt_text
