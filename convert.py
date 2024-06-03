import rembg
import numpy as np
from PIL import Image

import os
rootdir = 'storage/app/public/product/'

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        print(os.path.join(subdir, file))
        # Load the input image
        input_image = Image.open(os.path.join(subdir, file))

        # Convert the input image to a numpy array
        input_array = np.array(input_image)

        # Apply background removal using rembg
        output_array = rembg.remove(input_array,bgcolor=[255,255,255,255])

        # Create a PIL Image from the output array
        output_image = Image.fromarray(output_array)

        # Save the output image
        rb = output_image.convert('RGB')
        print(os.path.join(subdir, file))
        rb.save(os.path.join(subdir, file))