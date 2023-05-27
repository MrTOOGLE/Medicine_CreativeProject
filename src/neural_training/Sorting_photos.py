import os
import numpy as np

from keras.models import load_model
from keras.utils import load_img
from keras.utils import img_to_array

model = load_model('D:/_Python/Programs/Medicine/src/neural_training/bacterias-25-0.994.hdf5')
path = 'D:/_Python/Programs/Medicine/resources/images'

for subdir, dirs, files in os.walk(path):
    for file in files:
        try:
            image_path = os.path.join(subdir, file)
            # print(image_path)
            book_count, image_name = image_path.split('\\')[1:3]
            image_name = f'{book_count}/{image_name}'

            image = load_img(image_path, target_size=(180, 180))
            image = img_to_array(image)
            image = np.expand_dims(image, axis=0)

            result = model.predict(image)
            if result[0][0] <= 0.5:
                os.rename(image_path, f'D:/_Python/Programs/Medicine/resources/images/Bacterias/{image_name}')
        except OSError:
            pass
