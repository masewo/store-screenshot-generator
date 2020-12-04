import os
import cairosvg
from PIL import Image
from pathlib import Path
from io import BytesIO


def main():
    Path("input").mkdir(parents=True, exist_ok=True)
    Path("output").mkdir(parents=True, exist_ok=True)
    for folder in os.scandir('input\\screenshots'):
        Path("output\\" + folder.name).mkdir(parents=True, exist_ok=True)
        i = 1
        for file in os.scandir(folder.path):
            merge_with_background(i, folder.name, file.path, file.name)
            i += 1


def merge_with_background(i, folder, path, name):
    screenshot = Image.open(path)
    screenshot_size = screenshot.size
    print(screenshot_size)

    if screenshot_size[0] > screenshot_size[1]:
        landscape = True
    else:
        landscape = False

    # TODO calculate correct image size here
    image_size = (2160, 3840)

    if landscape:
        image_size = image_size[::-1]

    background_path = 'input\\backgrounds\\' + str(i) + '_' + ('land' if landscape else 'port') + '.svg'
    background = convert_to_png(background_path, image_size)

    new_image = Image.new('RGBA', (image_size[0], image_size[1]), (255, 0, 0, 0))

    offset = (int(image_size[0] / 2 - screenshot_size[0] / 2), image_size[1] - screenshot_size[1])

    new_image.paste(background, (0, 0))
    new_image.paste(screenshot, offset, screenshot)

    new_image.save("output\\" + folder + "\\" + name, "PNG")


def convert_to_png(path, size):
    out = BytesIO()
    cairosvg.svg2png(url=path, write_to=out, output_width=size[0], output_height=size[1])
    return Image.open(out)


if __name__ == '__main__':
    main()
