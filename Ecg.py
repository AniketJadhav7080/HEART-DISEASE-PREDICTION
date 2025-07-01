# ecg_module.py

from skimage.io import imread
from skimage import color
import matplotlib.pyplot as plt
from skimage.filters import threshold_otsu,gaussian
from skimage.transform import resize
from numpy import asarray
from skimage.metrics import structural_similarity
from skimage import measure
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier
import joblib
import pickle
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
import os
from natsort import natsorted
from sklearn import linear_model, tree, ensemble
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression

class ECG:
    def  getImage(self,image):
        # ... no changes
        image=imread(image)
        return image

    def GrayImgae(self,image):
        # ... no changes
        image_gray = color.rgb2gray(image)
        image_gray=resize(image_gray,(1572,2213))
        return image_gray

    def DividingLeads(self,image):
        # ... no changes
        # entire method unchanged
        # returns 13 leads
        return Leads

    def PreprocessingLeads(self,Leads):
        # ... no changes
        fig2 , ax2 = plt.subplots(4,3)
        fig2.set_size_inches(10, 10)
        x_counter=0
        y_counter=0
        for x,y in enumerate(Leads[:len(Leads)-1]):
            grayscale = color.rgb2gray(y)
            blurred_image = gaussian(grayscale, sigma=1)
            global_thresh = threshold_otsu(blurred_image)
            binary_global = blurred_image < global_thresh
            binary_global = resize(binary_global, (300, 450))
            if (x+1)%3==0:
                ax2[x_counter][y_counter].imshow(binary_global,cmap="gray")
                ax2[x_counter][y_counter].axis('off')
                ax2[x_counter][y_counter].set_title("pre-processed Leads {} image".format(x+1))
                x_counter+=1
                y_counter=0
            else:
                ax2[x_counter][y_counter].imshow(binary_global,cmap="gray")
                ax2[x_counter][y_counter].axis('off')
                ax2[x_counter][y_counter].set_title("pre-processed Leads {} image".format(x+1))
                y_counter+=1
        fig2.savefig('Preprossed_Leads_1-12_figure.png')

        fig3 , ax3 = plt.subplots()
        fig3.set_size_inches(10, 10)
        grayscale = color.rgb2gray(Leads[-1])
        blurred_image = gaussian(grayscale, sigma=1)
        global_thresh = threshold_otsu(blurred_image)
        print(global_thresh)
        binary_global = blurred_image < global_thresh
        ax3.imshow(binary_global,cmap='gray')
        ax3.set_title("Leads 13")
        ax3.axis('off')
        fig3.savefig('Preprossed_Leads_13_figure.png')

    def SignalExtraction_Scaling(self,Leads):
        # ... no changes
        return

    def CombineConvert1Dsignal(self):
        # ... no changes
        return test_final

    def DimensionalReduciton(self,test_final):
        # ... no changes
        return final_df

    def ModelLoad_predict(self,final_df):
        # ... no changes
        return result
