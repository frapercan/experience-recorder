import os
from functools import reduce

import webdataset as wds
import json
from PIL import Image

sink = wds.TarWriter("dataset.tar", encoder=False)
import os
from functools import reduce

datasets_folder = '/home/xaxi/PycharmProjects/experience-recorder/datasets-copy/2048/'
samples_basenames = []
for dataset_folder in os.listdir(datasets_folder):
    filenames = os.listdir(os.path.join(datasets_folder,dataset_folder))
    basenames = [os.path.join(datasets_folder,dataset_folder,basename.split('.')[0]) for basename in filenames ]
    samples_basenames.append(basenames)
samples_basenames = list(set(reduce(lambda x, y: x+y, samples_basenames)))



def create_sample(json_path, image_path):
    # Load the JSON data
    with open(json_path, 'r') as json_file:
        json_data = json.load(json_file)

    # Load the image and convert it to a PIL Image object
    image = Image.open(image_path)

    # Create the sample dictionary
    json_basename = os.path.basename(json_path)  # Get the base name without the directory path
    sample = {
        "__key__": json_basename[:-5],  # Use the JSON file name (without extension) as the sample key
        "json": json_data,
        "image": image
    }

    return sample



with wds.TarWriter('dataset.tar') as sink:
    for i,basename in enumerate(samples_basenames):
        print(i)
        json_path = f'{basename}.json'
        image_path = f'{basename}.png'

        sample = create_sample(json_path, image_path)
        sink.write(sample)
