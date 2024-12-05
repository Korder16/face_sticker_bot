import cv2
import urllib
import insightface
import numpy as np
from tqdm import tqdm
from pathlib import Path
from insightface.app import FaceAnalysis
from insightface.app.common import Face
from os import listdir
from os.path import isfile, join
import json
import sys
import os
import io


def download_model():
    url = "https://huggingface.co/CountFloyd/deepfake/resolve/main/inswapper_128.onnx"
    download_file_path = "./models/inswapper_128.onnx"

    Path('./models/').mkdir(exist_ok=True)

    if not Path(download_file_path).is_file():
        request = urllib.request.urlopen(url)
        total = int(request.headers.get("Content-Length", 0))
        with tqdm(
            total=total,
            desc="Downloading",
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
        ) as progress:
            urllib.request.urlretrieve(
                url,
                download_file_path,
                reporthook=lambda count, block_size, total_size: progress.update(
                    block_size
                ),
            )


def swap_faces(source: io.BytesIO, template_dir: str, user_id: int):
    download_model()

    faces_file_path = "./configs/faces_dict.json"
    with open(faces_file_path) as json_file:
        loaded_r = json.load(json_file)

    template_files = [
        file for file in listdir(template_dir) if isfile(join(template_dir, file))
    ]

    for file in template_files:
        for face in loaded_r[file]:
            for key in face.keys():
                if key in [
                    "bbox",
                    "kps",
                    "landmark_3d_68",
                    "pose",
                    "landmark_2d_106",
                    "embedding",
                ]:
                    face[key] = np.array(face[key])
                elif key in ["det_score"]:
                    face[key] = float(face[key])
                elif key in ["gender"]:
                    face[key] = int(face[key])
        loaded_r[file][0] = Face(loaded_r[file][0])

    model_filepath = "./models/inswapper_128.onnx"

    sys.stdout = open(os.devnull, "w")
    app = FaceAnalysis(name="buffalo_l")
    app.prepare(ctx_id=0, det_size=(640, 640))
    swapper = insightface.model_zoo.get_model(model_filepath)
    sys.stdout = sys.__stdout__

    nparr = np.frombuffer(source.getvalue(), np.uint8)
    source_img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)

    source_face = app.get(source_img)[0]

    output_bytes_oi = []

    for file in template_files:
        res = cv2.imread(template_dir + file)
        faces = loaded_r[file]

        for face in faces:
            res = swapper.get(res, face, source_face, paste_back=True)

        _, buffer = cv2.imencode(".jpg", res)
        output_bytes_oi.append(buffer)

    return output_bytes_oi