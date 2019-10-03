from urllib import urlopen
import tarfile
from io import BytesIO
import os
import requests

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

def make_file(model_tar, tar_file, dir):
    with open(f.get_info()['name'], 'w') as fh:
        fh.write(tarobj.extractfile(tar_file).read())

print('Donwloading pretrained model...')
if not os.path.exists('./models/mask_rcnn_inception_v2_coco_2018_01_28/'):
    if not os.path.exists('./models'):
        os.mkdir('./models')
    url = 'http://download.tensorflow.org/models/object_detection/mask_rcnn_inception_v2_coco_2018_01_28.tar.gz'
    response = urlopen(url)
    print('Unzipping model...')
    model_bytes_zipped = response.read()
    with open('models/model_download.tar.gz', 'wb') as fh:
        fh.write(model_bytes_zipped)
    with tarfile.open('models/model_download.tar.gz') as tar:
        tar.extractall(path='models')
else:
    print('SKIPPING: Pretrained model already downloaded')

print('Generating config')
if not os.path.exists('configs/mask_rcnn_inception_v2.config'):
    if not os.path.exists('./configs'):
        os.mkdir('./configs')
    with open('mask_rcnn_inception_v2_base.config', 'r') as fh:
        config_text = fh.read()
    config_text = config_text.replace('$HOME', os.environ['HOME'])
    with open('configs/mask_rcnn_inception_v2.config', 'w') as fh:
        fh.write(config_text)
else:
    print('SKIPPING: config already generated')

print('Downloading dataset...')
if not os.path.exists('data'):
    os.mkdir('data')
    shareable_link = 'https://drive.google.com/open?id=18mc6BbSUXdLgoM_JllYd871o-Ng5vpSz'
    id = '18mc6BbSUXdLgoM_JllYd871o-Ng5vpSz'
    download_file_from_google_drive(id, 'data')
    pass
else:
    print('SKIPPING: data folder already exists, delete it and run this script again to download the dataset')