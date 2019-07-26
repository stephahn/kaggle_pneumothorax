import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


if __name__ == '__main__':
    image = np.memmap('./big_images.npy',mode='r',shape=(10675,1024,1024))
    meta = pd.read_csv('./meta.csv')
    idx = np.random.randint(0,10675)
    age = meta['age'][meta['idx']==idx].values[0]
    sex = meta['sex'][meta['idx']==idx].values[0]
    plt.imshow(image[idx,:,:])
    plt.title(f'sex={sex}, age={age}')
    plt.show()