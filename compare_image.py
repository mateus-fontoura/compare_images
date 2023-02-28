# used to analise the ticket 12499.
# C

import requests
from io import BytesIO
from PIL import Image, ImageDraw
import time


def main():
    # Set the URL of the Azion edge image(after the IMS processing)
    url = "https://zgyjfdd59y.map.azionedge.net/img/2022/12/produto/4045/pijama-feminino-just-smile-pink-jc186-37-2.jpg?ims=fit-in/400x650"

    # Set the URL of the reference image from the Origin to fetch
    reference_image_url = "https://caeju.s3.amazonaws.com/img/2022/12/produto/4045/pijama-feminino-just-smile-pink-jc186-37-2.jpg"
    
    # Set the number of comparisons to make(If changed here, remember to change the rows and cols)
    num_comparisons = 100

    # Set the number of rows and columns in the mosaic image(Inverse of the above)
    num_rows = 10
    num_cols = 10

    # Set a flag to indicate whether the fetched image is the same as the reference image
    is_same = True

    # Set a counter to keep track of the number of requests made
    counter = 0

    # Set a variable to store the previous reference image content
    previous_reference_image_content = None

    # Create a list to store the fetched images
    fetched_images = []

    for i in range(num_comparisons):
        # Make the request without using cache
        response = requests.get(url, headers={"Cache-Control": "no-cache"})

        # Load the fetched image as a Pillow image object
        fetched_image = Image.open(BytesIO(response.content))

        # Fetch the reference image if it is not the same as the previous reference image
        response = requests.get(reference_image_url, headers={"Cache-Control": "no-cache"})
        
        reference_image_content = response.content
        if reference_image_content != previous_reference_image_content:
            with open("reference_image.png", "wb") as f:
                f.write(reference_image_content)
            previous_reference_image_content = reference_image_content
            reference_image = Image.open(BytesIO(reference_image_content))
            print(reference_image.mode)
        else:
            reference_image = Image.open("reference_image.png")

        # Resize the fetched image to the size of the reference image
        fetched_image = fetched_image.resize(reference_image.size)

        # Compare the colors of the fetched image and the reference image pixel by pixel
        fetched_pixels = fetched_image.load()
        reference_pixels = reference_image.load()
        width, height = fetched_image.size
        for x in range(width):
            for y in range(height):
                fetched_color = fetched_pixels[x, y]
                reference_color = reference_pixels[x, y]
                if fetched_color != reference_color:
                    # If the colors don't match, save the fetched image and stop the loop
                    fetched_image.save(f"new_image_{i}.png")
                    is_same = False
                    break
            if not is_same:
                break

        if is_same:
            # If the images are the same, wait for 1 second before making the next request
            counter += 1
            time.sleep(1)
        else:
            # If the images are different, save the fetched image, and add it to the list of fetched images
            fetched_images.append(fetched_image)

            # If we have fetched enough images, exit the loop
            if len(fetched_images) == num_comparisons:
                break
    fetched_image = fetched_image.convert("RGB")

   # Create a new image to store the mosaic
    mosaic_width = num_cols * reference_image.width
    mosaic_height = num_rows * reference_image.height
    mosaic = Image.new("RGB", (mosaic_width, mosaic_height), color=(255, 255, 255))

    # Create a draw object for the mosaic image
    draw = ImageDraw.Draw(mosaic)

    # Set the X size
    x_size = int(0.3 * reference_image.width)

    # Paste the fetched images onto the mosaic image
    for i in range(num_comparisons):
        col_idx = i % num_cols
        row_idx = i // num_cols
        x = col_idx * reference_image.width
        y = row_idx * reference_image.height

        if i < len(fetched_images):
            fetched_image = fetched_images[i]

            # Draw a white X on the mosaic image if the fetched image is different from the reference image
            if not is_same:
                x_center = x + reference_image.width // 2
                y_center = y + reference_image.height // 2
                draw.line((x_center - x_size, y_center - x_size, x_center + x_size, y_center + x_size), fill=(255, 255, 255), width=3)
                draw.line((x_center - x_size, y_center + x_size, x_center + x_size, y_center - x_size), fill=(255, 255, 255), width=3)

            mosaic.paste(fetched_image, (x, y))

    # Save the mosaic image
    mosaic.save("mosaic_400x650.png")
    print("Mosaic image saved as mosaic.png")


if __name__ == "__main__":
    main()

