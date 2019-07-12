
#by刘一婧
import colorsys
import cv2
import PIL.Image as Image

def get_dominant_color(image):
    max_score = 0.0001
    dominant_color = None
    for count, (r, g, b) in image.getcolors(image.size[0]*image.size[1]):
        #cvt hsv
        saturation = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)[1]
        y = min(abs(r*2104+g*4130+b*802+4096+131072) >> 13, 235)
        y = (y - 16)/(235 - 16)
        #ignore
        if y > 0.9:
            continue
        score = (saturation+0.1)*count

        if score > max_score:
            max_score = score
            dominant_color = (r, g, b)
    return dominant_color

def hsv_color(h, s, v):
    if 0 <= h <= 180 and 0 <= s <= 255 and 0 <= v <= 46:
        print("black\n")
    if 0 <= h <= 180 and 0 <= s <= 43 and 46 <= v <= 220:
        print("gray\n")
    if 0 <= h <= 180 and 0 <= s <= 30 and 221 <= v <=255:
        print("white\n")
    if 0 <= h <= 10 and 43 <= s <= 255 and 46 <= v <= 255:
        print("red\n")
    if 156 <= h <= 180 and 43 <= s <= 255 and 46 <= v <= 255:
        print("red\n")
    if 11 <= h <= 25 and 43 <= s <= 255 and 46 <= v <= 255:
        print("orange\n")
    if 26 <= h <= 34 and 43 <= s <= 255 and 46 <= v <= 255:
        print("yellow\n")
    if 35 <= h <= 77 and 43 <= s <= 255 and 46 <= v <= 255:
        print("green\n")
    if 78 <= h <= 99 and 43 <= s <= 255 and 46 <= v <= 255:
        print("cyan\n")
    if 100 <= h <= 124 and 43 <= s <= 255 and 46 <= v <= 255:
        print("blue\n")
    if 125 <= h <= 155 and 43 <= s <= 255 and 46 <= v <= 255:
        print("purple\n")

if __name__ == '__main__':
    image = Image.open("D:\\picture\\test\\carcar.jpg")
    image = image.convert('RGB')
    rgb = get_dominant_color(image)
    print(rgb)
    max = max(rgb[0], rgb[1], rgb[2])
    min = min(rgb[0], rgb[1], rgb[2])
    t = max - min
    if t == 0:
        h = 0
        s = 0
        v = max
    else:
        if rgb[0] == max:
            h = 60 * ((rgb[1] - rgb[2])/t + 0)/2
            s = t * 255 / max
            v = max
        if rgb[1] == max:
            h = 60 * ((rgb[2] - rgb[0])/t + 2)/2
            s = t * 255 / max
            v = max
        if rgb[2] == max:
            h = 60 * ((rgb[0] - rgb[1])/t + 4)/2
            s = t * 255 / max
            v = max
    print(h, s, v)
    hsv_color(h, s, v)


