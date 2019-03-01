# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 00:50:08 2018

@author: Junya Zhao
"""

import pandas as pd
import numpy as np
import os
import seaborn as sns 

obs =os.path.dirname(os.getcwd()) 
Datpath= obs + "\\Data\\"
Output = obs + "\\output\\"
# read the preprocessed datasets
#UserAnimefilter= pd.read_csv(Output +"UserAnimefilter.csv")
allMoive= pd.read_csv(Output +"Topmoiveall.csv")
TopMoive= pd.read_csv(Output +"TopMoive.csv")
GoodUser= pd.read_csv(Output +"GoodUser.csv")
a1=sns.jointplot(x='IMDB', y='popularity', data=TopMoive,color="rosybrown")
a2=sns.jointplot(x='IMDB', y='rank', data=TopMoive,color="rosybrown")
a3=sns.jointplot(x='score', y='popularity', data=TopMoive,color="rosybrown")
a4=sns.jointplot(x='score', y='rank', data=TopMoive,color="rosybrown")
# comparison
b1=sns.jointplot(x='IMDB', y='popularity', data=allMoive)
b2=sns.jointplot(x='IMDB', y='rank', data=allMoive)
b3=sns.jointplot(x='score', y='popularity', data=allMoive)
b4=sns.jointplot(x='score', y='rank', data=allMoive)
