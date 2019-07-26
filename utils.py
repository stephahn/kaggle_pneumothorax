
import pandas as pd
import pydicom

ANNOTATIONS = './train-rle.csv'

def get_classe_from_image_id(image_id):
    rle=get_rle_from_image_id(image_id)
    if len(rle)==1:
        if rle[0]==' -1':
            return 0
        else:
            return 1
    else:
        return 1
def get_rle_from_image_id(image_id):
    df = pd.read_csv(ANNOTATIONS, sep=',')
    rle = df[' EncodedPixels'].values[df['ImageId'].values == image_id]
    return rle
def get_image_attr_from_dicom(dcm_file,attr):
    if isinstance(dcm_file,str):
        dcm_file = pydicom.read_file(dcm_file)
    return getattr(dcm_file,attr)

