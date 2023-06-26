from PIL import Image
from io import BytesIO
import sys

if len(sys.argv) < 2:
    path = input("Please enter a path: ")
else:
    path = sys.argv[1]


mcify_lowpixel_image = Image.open(path)
mcify_lowpixel_image.thumbnail((25, 25), Image.LANCZOS)
width, height = mcify_lowpixel_image.size
pixel_data = []

for y in range(height):
    for x in range(width):
        r, g, b = mcify_lowpixel_image.getpixel((x, y))[:3]
        hex_code =  "{" + f'"text":"█","color":"#{r:02x}{g:02x}{b:02x}"' + "}"
        pixel_data.append(hex_code)

jsoncomponent = ""
for i in range(0, len(pixel_data), width):
    row = pixel_data[i:min(i + width, len(pixel_data))]
    row_text = ",".join(row)
    jsoncomponent += row_text + ",\"\\n\","
print("["+jsoncomponent[:-6]+"]")