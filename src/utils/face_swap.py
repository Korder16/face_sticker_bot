import cv2
import urllib
import insightface
from tqdm import tqdm
from pathlib import Path
from insightface.app import FaceAnalysis


def download_model():
    url = "https://huggingface.co/CountFloyd/deepfake/resolve/main/inswapper_128.onnx"
    download_file_path = "./models/inswapper_128.onnx"

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


def swap_faces(source_path: str, target_path: str, output_path: str):

    download_model()

    model_filepath = "./models/inswapper_128.onnx"

    app = FaceAnalysis(name="buffalo_l")
    app.prepare(ctx_id=0, det_size=(640, 640))
    swapper = insightface.model_zoo.get_model(model_filepath)

    source_img = cv2.imread(source_path)
    source_face = app.get(source_img)[0]

    res = cv2.imread(target_path)
    faces = app.get(res)

    swapped_res = res.copy()
    for face in faces:
        swapped_res = swapper.get(swapped_res, face, source_face, paste_back=True)

    cv2.imwrite(output_path, swapped_res)
