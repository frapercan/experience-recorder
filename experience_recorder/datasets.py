import json

import webdataset as wds
import os


import tarfile

# Ruta del directorio que se quiere comprimir
source_dir = "./datasets/2048"

# Nombre del archivo tar que se va a crear
tar_filename = "2048.tar"

# Crear el archivo tar y añadir el directorio completo a él
with tarfile.open(tar_filename, "w") as tar:
    tar.add(source_dir, arcname="")


dataset = wds.WebDataset(tar_filename)

for i,sample in enumerate(dataset):
    print(json.loads(sample['info.json'].decode('utf8')))
