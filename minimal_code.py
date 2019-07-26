import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from mask import rle2mask,mask2rle
from skimage.transform import rotate
image = np.memmap('./big_images.npy',mode='r',shape=(10675,1024,1024))
meta = pd.read_csv('./meta.csv')

def show_one_image_random(idx=None,annotation=True,force_pneumo=False):
    if not isinstance(idx,int):
        idx = np.random.randint(0, 10675)
        if force_pneumo:
            while meta['classe'][meta['idx'] == idx].values[0]!=1:
                idx = np.random.randint(0, 10675)

    age = meta['age'][meta['idx'] == idx].values[0]
    sex = meta['sex'][meta['idx'] == idx].values[0]
    plt.imshow(image[idx, :, :])
    title = f'sex={sex}, age={age}'
    if annotation:
        rle = meta['rle'][meta['idx'] == idx].values[0]
        if rle!=' -1':
            rle = rle.split('#')
            mymask = np.zeros_like(image[idx,:,:])
            for item in rle:
                mymask = mymask+rle2mask(item,*mymask.shape)


            plt.imshow(rotate(mymask,-90)[:,::-1],alpha=0.5)
            title=title+' pneumo'
    plt.title(title)
    plt.figure()
    plt.imshow(image[idx, :, :])
    plt.show()


if __name__ == '__main__':
    for k in range(100):
        show_one_image_random(force_pneumo=True)

