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
		"""
		this functions gets user image
		return: user image
		"""
		image = imread(image)
		# Ensure image has 3 channels (RGB). If grayscale, convert to RGB
		if len(image.shape) == 2:
			image = np.stack((image,)*3, axis=-1)
		return image

	def GrayImgae(self,image):
		"""
		This funciton converts the user image to Gray Scale
		return: Gray scale Image
		"""
		image_gray = color.rgb2gray(image)
		image_gray = resize(image_gray, (1572, 2213), anti_aliasing=True)
		return image_gray

	def DividingLeads(self,image):
		"""
		This Funciton Divides the Ecg image into 13 Leads including long lead. Bipolar limb leads(Leads1,2,3). Augmented unipolar limb leads(aVR,aVF,aVL). Unipolar (+) chest leads(V1,V2,V3,V4,V5,V6)
  		return : List containing all 13 leads divided
		"""
		# Validate image shape
		if image.shape[0] < 1480 or image.shape[1] < 2125:
			raise ValueError("Input image must be at least 1480x2125 pixels. Current shape: {}".format(image.shape))

		Lead_1 = image[300:600, 150:643] # Lead 1
		Lead_2 = image[300:600, 646:1135] # Lead aVR
		Lead_3 = image[300:600, 1140:1625] # Lead V1
		Lead_4 = image[300:600, 1630:2125] # Lead V4
		Lead_5 = image[600:900, 150:643] #Lead 2
		Lead_6 = image[600:900, 646:1135] # Lead aVL
		Lead_7 = image[600:900, 1140:1625] # Lead V2
		Lead_8 = image[600:900, 1630:2125] #Lead V5
		Lead_9 = image[900:1200, 150:643] # Lead 3
		Lead_10 = image[900:1200, 646:1135] # Lead aVF
		Lead_11 = image[900:1200, 1140:1625] # Lead V3
		Lead_12 = image[900:1200, 1630:2125] # Lead V6
		Lead_13 = image[1250:1480, 150:2125] # Long Lead

		Leads = [Lead_1, Lead_2, Lead_3, Lead_4, Lead_5, Lead_6, Lead_7, Lead_8, Lead_9, Lead_10, Lead_11, Lead_12, Lead_13]

		fig, ax = plt.subplots(4, 3)
		fig.set_size_inches(10, 10)
		x_counter = 0
		y_counter = 0

		for x, y in enumerate(Leads[:len(Leads) - 1]):
			try:
				if (x + 1) % 3 == 0:
					ax[x_counter][y_counter].imshow(y)
					ax[x_counter][y_counter].axis('off')
					ax[x_counter][y_counter].set_title("Leads {}".format(x + 1))
					x_counter += 1
					y_counter = 0
				else:
					ax[x_counter][y_counter].imshow(y)
					ax[x_counter][y_counter].axis('off')
					ax[x_counter][y_counter].set_title("Leads {}".format(x + 1))
					y_counter += 1
			except Exception as e:
				print(f"Error displaying lead {x + 1}: {e}")
				continue

		fig.tight_layout()
		fig.savefig('Leads_1-12_figure.png')

		fig1, ax1 = plt.subplots()
		fig1.set_size_inches(10, 10)
		ax1.imshow(Lead_13)
		ax1.set_title("Leads 13")
		ax1.axis('off')
		fig1.savefig('Long_Lead_13_figure.png')

		return Leads

	# other methods remain unchanged
