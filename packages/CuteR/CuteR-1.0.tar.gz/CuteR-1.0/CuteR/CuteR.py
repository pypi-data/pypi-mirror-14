#!/usr/bin/env python2
# encoding: utf-8

from PIL import Image
from PIL import ImageEnhance
import qrcode


def color_replace(image,color):
    """Replace black with other color

    :color: custom color (r,g,b)
    :image: image to replace color
    :returns: TODO

    """
    pixels = image.load()
    size = image.size[0]
    for width in range(size):
        for height in range(size):
            r,g,b = pixels[width,height]
            if (r,g,b) == (0,0,0):
                pixels[width,height] = color


def produce(txt,img,ver=5,err_crt = qrcode.constants.ERROR_CORRECT_H,bri = 1.0, cont = 1.0,\
        colourful = False, rgb = (0,0,0)):
    """

    :txt: QR text
    :img: Image
    :ver: QR version
    :err_crt: QR error correct
    :bri: Brightness enhance
    :cont: Contrast enhance
    :colourful: If colourful mode
    :rgb: color to replace black
    :returns: Produced image

    """
    qr = qrcode.QRCode(version = ver,error_correction = err_crt,box_size=3)
    qr.add_data(txt)
    qr.make(fit=True)
    img_qr = qr.make_image().convert('RGB')
    if colourful and ( rgb != (0,0,0) ):
        color_replace(img_qr,rgb)
    img_img = Image.open(img).convert('RGBA')
    img_size = None

    if img_img.size[0] < img_img.size[1]:
        img_img = img_img.resize((img_qr.size[0]-24,int((img_qr.size[1]-24)*(1.0*img_img.size[1]/img_img.size[0]))))
        img_size = img_img.size[0]
    else:
        img_img = img_img.resize( (int((img_qr.size[0]-24)*(1.0*img_img.size[0]/img_img.size[1])),(img_qr.size[1]-24)) )
        img_size = img_img.size[1]

    enh = ImageEnhance.Contrast(img_img)
    img_enh = enh.enhance(cont)
    enh = ImageEnhance.Brightness(img_enh)
    img_enh = enh.enhance(bri)
    if not colourful:
        img_enh = img_enh.convert('1')
        img_qr = img_qr.convert('1')
    img_res = img_qr
    for x in range(0,img_size):
        for y in range(0,img_size):
            if (x%3 ==1 and  y%3 == 1):
                continue
            if x < 24 and (y < 24 or y > img_size-25):
                continue
            if x > img_size-25 and (y < 24 ):
                continue
            if img_img.getpixel((x,y))[2] == 0:
                continue
            img_res.putpixel((x+12,y+12),img_enh.getpixel((x,y)))
    pos = qrcode.util.pattern_position(qr.version)
    img_qr2 = qr.make_image().convert("RGB")
    if colourful and ( rgb != (0,0,0) ):
        color_replace(img_qr2,rgb)
    for i in pos:
        for j in pos:
            if (i == 6 and j == pos[-1]) or (j == 6 and i == pos[-1])\
                or (i == 6 and j == 6):
                continue
            else:
                rect = (3*(i-2)+12,3*(j-2)+12,3*(i+3)+12,3*(j+3)+12)
                img_tmp = img_qr2.crop(rect)
                img_res.paste(img_tmp,rect)

    return img_res.resize((img_res.size[0]*10,img_res.size[1]*10))


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Combine your QR code with custom picture")
    parser.add_argument("image")
    parser.add_argument("text", help="QRcode Text.")
    parser.add_argument("-o", "--output", help="Name of output file.")
    parser.add_argument("-v", "--version", type=int, help="QR version.In range of [1-40]")
    parser.add_argument("-e", "--errorcorrect", choices={"L","M","Q","H"}, help="Error correct")
    parser.add_argument("-b", "--brightness", type=float, help="Brightness enhance")
    parser.add_argument("-c", "--contrast", type=float, help="Contrast enhance")
    parser.add_argument("-C", "--colourful", action="store_true",help="colourful mode")
    parser.add_argument("-r", "--rgb", nargs=3, metavar=('R','G','B'),type = int, help="color to replace black")
    args = parser.parse_args()

    img = args.image
    txt = args.text
    output = args.output if args.output else 'qr.png'
    ec = qrcode.constants.ERROR_CORRECT_H
    if args.errorcorrect:
        ec_raw = args.errorcorrect
        if ec_raw == 'L':
            ec = qrcode.constants.ERROR_CORRECT_L
        if ec_raw == 'M':
            ec = qrcode.constants.ERROR_CORRECT_M
        if ec_raw == 'Q':
            ec = qrcode.constants.ERROR_CORRECT_Q
    ver = 5
    if args.version:
        if args.version >= 1 and args.version <= 40:
            ver = args.version
    cont = args.contrast if args.contrast else 1.0
    bri = args.brightness if args.brightness else 1.0
    colr = True if args.colourful else False
    if colr :
        if args.rgb:
          rgb = tuple(args.rgb)
        else:
            rgb = (0,0,0)
    else:
        rgb = (0,0,0)
    produce(txt,img,ver,ec,bri, cont ,colourful = colr,rgb=rgb).save(output)

if __name__ == "__main__":
    main()
