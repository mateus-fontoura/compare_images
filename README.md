# Image Comparison Script :camera:
This Python script fetches an image from a URL(Usually Azion post process from IMS) and compares it to a reference image(Origin original image). It repeats this process multiple times and creates a mosaic image of all the fetched images side by side to be compared manually or not, It will add an "X" in the middle of the image if its different in the Mosaic.


#Note - The lib uses a "color-mode" information(RGB as an example) and that can change the colors of the mosaic, but not the colors of the requested images, so its possible that manual check would be a good thing too.

#Note2 - The downloaded images and the mosaic will be sent to the same folder as the script, remember to put it inside of a subfolder to make things easier.
