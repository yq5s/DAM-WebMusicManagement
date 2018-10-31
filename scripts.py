from PIL import Image
import os
def jpg2png_batch(where):
    for path, _, files in os.walk(where):
        for file in files:
            f,e = os.path.splitext(file)
            if e in ('.jpg', '.JPG'):
                fpath = os.path.join(path, file)
                Image.open(fpath).save(os.path.join(path, f + '.png'))
                os.remove(fpath)
