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

    if screenshot_size[0] > screenshot_size[1]:
        landscape = True
    else:
        landscape = False

    image_size = (2160, 3840)  # android
    # image_size = (2048, 2732)  # ipad
    # image_size = (1284, 2778)  # iphone 6,5
    # image_size = (1242, 2208)  # iphone 5,5

    if landscape:
        image_size = image_size[::-1]

    percent_of_height_visible = 0.80  # change me
    percent_of_height_padding = 0.01  # change me

    percent_of_height_for_screenshot = percent_of_height_visible - 2 * percent_of_height_padding

    maximum_screenshot_height = min(screenshot_size[1], image_size[1] * percent_of_height_for_screenshot)
    scaled_screenshot_size = (
        screenshot_size[0] * (maximum_screenshot_height / screenshot_size[1]), maximum_screenshot_height)

    screenshot.thumbnail(scaled_screenshot_size, Image.LANCZOS)

    background_path = 'input\\backgrounds\\' + str(i) + '_' + ('land' if landscape else 'port') + '.svg'
    background = convert_to_png(background_path, image_size)

    new_image = Image.new('RGBA', (image_size[0], image_size[1]), (1, 161, 145, 255))

    offset = (
        int(image_size[0] / 2 - scaled_screenshot_size[0] / 2),
        int(image_size[1] - scaled_screenshot_size[1] - image_size[1] * percent_of_height_padding))

    new_image.paste(background, (0, 0))
    new_image.paste(screenshot, offset, screenshot)

    new_image.save("output\\" + folder + "\\" + name, "PNG")


def convert_to_png(path, size):
    out = BytesIO()
    cairosvg.svg2png(url=path, write_to=out,
                     output_width=size[0],
                     # output_height=size[1],  # change me
                     # parent_width=size[0],
                     # parent_height=size[1],
                     background_color="rgba(1, 161, 145, 255)"
                     )
    return Image.open(out)


if __name__ == '__main__':
    main()
