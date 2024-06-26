# Making ASCII art of country outlines to use in quiz
# Using the Image module from the PIL library
from PIL import Image
import os

png_list = os.listdir(
    "/workspaces/125834830/Final Project/ASCII art generation/country.png files"
)

# Loop through all country.png files and save resulting ascii.txt files in corresponding folder
for country in png_list:
    img = Image.open(
        f"/workspaces/125834830/Final Project/ASCII art generation/country.png files/{country}"
    )

    # Rescaling the Image to be appropriate size for command-line
    width, height = img.size
    aspect_ratio = height / width
    new_height = 70
    new_width = new_height / aspect_ratio
    new_height *= (
        0.45  # Manually rescale height as increased height of characters distorts image
    )
    img = img.resize((int(new_width), int(new_height)))

    # Convert image to greyscale
    img = img.convert("L")

    # Characters representing different levels of grey
    scale_chars = ["&", "@", "%", "€", ":", " "]

    # Replacing pixels with ascii greyscale counterparts
    pixels = img.getdata()
    new_pixels = [scale_chars[pixel // 50] for pixel in pixels]
    new_pixels = "".join(new_pixels)

    # Split full string of pixels into strings of length equal to new width
    pixels_count = len(new_pixels)
    ascii_image = [
        new_pixels[index : index + int(new_width)]
        for index in range(0, pixels_count, int(new_width))
    ]
    ascii_image = "\n".join(ascii_image)

    # Save ascii art as text file
    country = country.removesuffix(".png")
    with open(
        f"/workspaces/125834830/Final Project/ASCII art generation/ascii.txt files/{country}_ascii.txt",
        "w",
    ) as file:
        file.write(ascii_image)
