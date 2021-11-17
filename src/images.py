import random
from PIL import Image
import numpy as np

def make_some_image(n):
    try:
        os.system("rm random_image/*.png")
    except:
        pass

    all_color_used = {}
    for k in range(n):
        random_number1, random_number2, random_number3 = random.randint(0, 255), random.randint(0, 255), random.randint(
            0, 255)
        w, h = 8, 8
        data = np.zeros((h, w, 3), dtype=np.uint8)

        data[0:, 0:] = [random_number1, random_number2, random_number3]  # red patch in upper left
        img = Image.fromarray(data, 'RGB')
        img.save('random_image/{}.png'.format(k))
        all_color_used['random_image/{}.png'.format(k)] = [random_number1, random_number2, random_number3]

    return all_color_used
