# Add Watermark on images
from PIL import Image, ImageDraw, ImageFont
import sys

def watermark(img_path,word,scal,size):
    img1 = Image.open(img_path)
    img1 =img1.resize((int(img1.size[0]*scal),int(img1.size[1]*scal)))
    img1 = img1.convert('RGBA')
    text_overlay = Image.new('RGBA', img1.size, (255, 255, 255, 0))
    image_draw = ImageDraw.Draw(text_overlay)
    font = ImageFont.truetype(r'arial.ttf', size)  # 字体大小
    image_draw.text((0, int(img1.size[1]*0.5)), word, font=font, fill=(0, 0, 0, 40),align='center')
    if img1.size[1]>img1.size[0]:
        text_overlay=text_overlay.rotate(60)
    else:
        text_overlay=text_overlay.rotate(30)
    img1 = Image.alpha_composite(img1, text_overlay)
    img1 = img1.convert('RGB')
    return img1
 
if __name__ == "__main__":
    img = watermark(sys.argv[1],
                    'Only For Personal Homepage Display \n https://hilmr.github.io/',
                    float(sys.argv[2]),int(sys.argv[3]))
    img.save(sys.argv[4], quality=80)