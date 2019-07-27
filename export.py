import glob
import numpy as np
import pydicom
from utils import get_rle_from_image_id,get_classe_from_image_id,get_image_attr_from_dicom
import pandas as pd

####  EXPORT DATA INTO A NUMPY ARRAY AND CSV FILE ####
EXPORT_NPY = './big_images.npy'
METADATA_CSV= './meta.csv'
TRAIN_DICOM_STORE_ID = 'dicom-images-train'
TEST_DICOM_STORE_ID = 'dicom-images-test'
IMAGE_SHAPE = [1024,1024]
def exporter(dicom_store_id):
    content = glob.glob(dicom_store_id+'/**/*.dcm',recursive=True)
    big_images = np.memmap(EXPORT_NPY,mode='w+', shape=(len(content),*IMAGE_SHAPE))
    metadata = pd.DataFrame(columns=['idx','image_id','classe','rle','orientation','spacing','sex','age'])
    for i,dcm_path in enumerate(content):
        dcm_img = pydicom.read_file(dcm_path)
        tmp_meta = {}
        tmp_meta['idx'] = i
        tmp_meta['image_id'] = get_image_attr_from_dicom(dcm_img,'SOPInstanceUID')
        tmp_meta['classe'] = get_classe_from_image_id(tmp_meta['image_id'])
        tmp_meta['rle'] = '#'.join(get_rle_from_image_id(tmp_meta['image_id']))
        tmp_meta['orientation'] = get_image_attr_from_dicom(dcm_img,'ViewPosition')
        tmp_meta['spacing'] = list(map(int,get_image_attr_from_dicom(dcm_img,'PixelSpacing')))
        tmp_meta['sex'] = get_image_attr_from_dicom(dcm_img,'PatientSex')
        tmp_meta['age'] = int(get_image_attr_from_dicom(dcm_img,'PatientAge'))
        big_images[i,:,:] = dcm_img.pixel_array
        metadata = metadata.append(tmp_meta,ignore_index=True)
        if not i % 100 or i == len(content):
            print('Processed instance %d out of %d' %
                  (i, len(content)))
    metadata.to_csv(METADATA_CSV)



exporter(TRAIN_DICOM_STORE_ID)