from PIL import Image

def image_to_jsoncomponent(image: Image.Image, size: tuple = (25, 25), char: str = "█") -> str:
    image.thumbnail(size, Image.LANCZOS)
    width, height = image.size
    pixel_data = []

    for y in range(height):
        for x in range(width):
            r, g, b = image.getpixel((x, y))[:3]
            hex_code = "{" + f'"text":"{char}","color":"#{r:02x}{g:02x}{b:02x}"' + "}"
            pixel_data.append(hex_code)

    colored_characters = ""
    for i in range(0, len(pixel_data), width):
        row = pixel_data[i:min(i + width, len(pixel_data))]
        row_text = ",".join(row)
        colored_characters += row_text + ",\"\\n\","
    return "[" + colored_characters[:-6] + "]"
    
# EXAMPLE
image = Image.open("path/to/file.png")
output = image_to_jsoncomponent(image)
print(output)
