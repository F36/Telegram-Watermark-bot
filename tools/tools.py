from PIL import Image, ImageFont, ImageDraw, ImageEnhance
import hashlib
import piexif
import config


def getting_ready(path):
    fname = md5(path) + '.jpg'
    image = Image.open(path).convert('RGB')
    try:
        exif_dict = piexif.load(image.info['exif'])
        orientation = exif_dict['0th'][274]
    except KeyError:
        orientation = None
    rotate_values = {3: 180, 6: 270, 8: 90}
    if orientation in rotate_values:
        image = image.rotate(rotate_values[orientation], expand=True)
    for color in ['black', 'white']:
        watermark(image, fname, color)
    return fname


def watermark(img, new_fname, color):
    text = config.WATERMARK
    wm = Image.new('RGBA', img.size, (0, 0, 0, 0))
    fontsize = img.size[1] // 100 * config.FONT_SIZE
    font = ImageFont.truetype(f'tools/fonts/{config.FONT_NAME}', fontsize)
    indent = fontsize // 6
    w, h = font.getsize(text)
    text_position = (img.size[0] - w - indent, img.size[1] - h - indent)
    draw = ImageDraw.Draw(wm, 'RGBA')
    draw.text(text_position, text, font=font, fill=color)
    alpha = wm.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(config.TRANSPARENCY)
    wm.putalpha(alpha)
    out_path = 'images/out/{}/{}'.format(color, new_fname)
    Image.composite(wm, img, wm).save(out_path, 'JPEG', optimize=False, quality=config.QUALITY)


def md5(path):
    with open(path, 'rb') as f:
        md5hash = hashlib.md5()
        for chunk in iter(lambda: f.read(4096), b''):
            md5hash.update(chunk)
    return md5hash.hexdigest()