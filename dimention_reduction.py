import numpy as np
import pandas as pd
import time

# import plot
import plotly.io as plt_io
import plotly.graph_objects as go
import matplotlib

from sklearn.preprocessing import StandardScaler

# import tool - PCA
from sklearn.decomposition import PCA

# import tool - TSNE
from sklearn.manifold import TSNE
# import tool - UMAP
import umap
# import tool - LDA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA

# load data
train = pd.read_csv('~/Desktop/kaggle_dimention_reduction/sign_mnist_test/sign_mnist_test.csv')
train.head()

#picking only the first 10 labels
train = train[train['label'] < 10]
# Setting the label and the feature columns
y = train.loc[:,'label'].values
x = train.loc[:,'pixel1':].values


def plot_2d(component1, component2):
    
    fig = go.Figure(data=go.Scatter(
        x = component1,
        y = component2,
        mode='markers',
        marker=dict(
            size=20,
            color=y, #set color equal to a variable
            colorscale='Rainbow', # one of plotly colorscales
            showscale=True,
            line_width=1
        )
    ))
    fig.update_layout(margin=dict( l=100,r=100,b=100,t=100),width=2000,height=1200)                 
    fig.layout.template = 'plotly_dark'
    
    fig.show()

def plot_3d(component1,component2,component3):
	fig = go.Figure(data=[go.Scatter3d(
		x=component1,
      	y=component2,
        z=component3,
        mode='markers',
        marker=dict(
            size=10,
            color=y,                # set color to an array/list of desired values
            colorscale='Rainbow',   # choose a colorscale
            opacity=1,
            line_width=1)
    	)])
	fig.update_layout(margin=dict(l=100,r=100,b=100,t=100),width=2000,height=1200)
	fig.layout.template = 'plotly_dark'
	fig.show()


## Standardizing the data
x = StandardScaler().fit_transform(x)

# PCA
start = time.time()
pca = PCA(n_components=3)
principalComponents = pca.fit_transform(x)
print('Duration: {} seconds'.format(time.time() - start))
principal = pd.DataFrame(data = principalComponents
             , columns = ['principal component 1', 'principal component 2','principal component 3'])


plot_2d(principalComponents[:, 0],principalComponents[:, 1])
plot_3d(principalComponents[:, 0],principalComponents[:, 1],principalComponents[:, 2])


# tSNE
start = time.time()
pca_50 = PCA(n_components=50)
pca_result_50 = pca_50.fit_transform(x)
tsne = TSNE(random_state = 42, n_components=3,verbose=0, perplexity=40, n_iter=400).fit_transform(pca_result_50)
print('Duration: {} seconds'.format(time.time() - start))

plot_2d(tsne[:, 0],tsne[:, 1])
plot_3d(tsne[:, 0],tsne[:, 1],tsne[:,2])


# UMAP
start = time.time()
reducer = umap.UMAP(random_state=42,n_components=3)
embedding = reducer.fit_transform(x)
print('Duration: {} seconds'.format(time.time() - start))

plot_2d(reducer.embedding_[:, 0],reducer.embedding_[:, 1])
plot_3d(reducer.embedding_[:, 0],reducer.embedding_[:, 1],reducer.embedding_[:, 2])


# LDA
start = time.time()
X_LDA = LDA(n_components=3).fit_transform(x,y)
print('Duration: {} seconds'.format(time.time() - start))

plot_2d(X_LDA[:, 0],X_LDA[:, 1])
plot_3d(X_LDA[:, 0],X_LDA[:, 1],X_LDA[:, 2])


