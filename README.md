# Image Comparison Script :camera:
This Python script fetches an image from a URL(Usually Azion post process from IMS) and compares it to a reference image(Origin original image). It repeats this process multiple times and creates a mosaic image of all the fetched images side by side to be compared manually or not, It will add an "X" in the middle of the image if its different in the Mosaic.

The script works as follows:

It sets the URL of the image to fetch and the URL of the reference image to compare it to.

It sets the number of comparisons to make and the number of rows and columns in the mosaic image.

It makes a request to fetch the image from the URL and loads it as a Pillow image object.

It compares the colors of the fetched image and the reference image pixel by pixel. If the colors don't match, it saves the fetched image and marks it with a big white X in the middle of the mosaic image. If the colors match, it waits for one second before making the next request.

After making the desired number of comparisons, it creates a mosaic image of all the fetched images side by side. If any of the fetched images were different from the reference image, the mosaic image will have a big white X in the middle of it to indicate this.
