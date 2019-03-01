# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 23:34:11 2018

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
TopMoive= pd.read_csv(Output +"TopMoive.csv")
GoodUser= pd.read_csv(Output +"GoodUser.csv")
#UserAnimefilter= UserAnimefilter[UserAnimefilter['my_score'].notnull()]
TopMoive =TopMoive.replace({"rating":{"G - All Ages": "G","PG - Children":"PG","PG-13 - Teens 13 or older":"PG13","R - 17+ (violence & profanity)":"R17",
                 "R+ - Mild Nudity":"Rplus","Rx - Hentai":"Rx"}})

#basic analysis for anime only
animetype=pd.DataFrame(TopMoive.groupby('type')['anime_id'].count())

animetype.reset_index(level=0, inplace=True)
#ax1= sns.barplot(x="type", y="anime_id", data=animetype).set_ylabel("number of anime")

animesource=pd.DataFrame(TopMoive.groupby('source')['anime_id'].count())
animesource.reset_index(level=0, inplace=True)
#ax2 = sns.barplot(y="source", x="anime_id", data=animesource,palette="deep").set_xlabel("number of anime")

animelevel=pd.DataFrame(TopMoive.groupby('rating')['anime_id'].count())
animelevel.reset_index(level=0, inplace=True)
#ax3 = sns.barplot(x="rating", y="anime_id", data=animelevel,palette="deep").set_xlabel("number of anime")



episodes=pd.DataFrame(TopMoive.groupby('episodes')['anime_id'].count())
duration=pd.DataFrame(TopMoive.groupby('duration')['anime_id'].count())
aired_from_year=pd.DataFrame(TopMoive.groupby('aired_from_year')['anime_id'].count())
aired_from_year.reset_index(level=0, inplace=True)
genreDistribution = TopMoive[['anime_id']].join(TopMoive["genre"].str.get_dummies(', ').replace(0, ''))
producerDistribution = TopMoive[['anime_id']].join(TopMoive["producer"].str.get_dummies(', ').replace(0, ''))
licensorDistribution = TopMoive[['anime_id']].join(TopMoive["licensor"].str.get_dummies(', ').replace(0, ''))
studioDistribution = TopMoive[['anime_id']].join(TopMoive["studio"].str.get_dummies(', ').replace(0, ''))



#basic analysis for user only
#location = GoodUser[['username']].join(GoodUser["location"].str.get_dummies(', ').replace(0, '')) not efficient
GoodUser["location"].str.split(',', expand=True)
location = pd.DataFrame(GoodUser.groupby('location')['user_id'].count())
location.reset_index(level=0, inplace=True)

gender = pd.DataFrame(GoodUser.groupby('gender')['user_id'].count())
gender.reset_index(level=0, inplace=True)


Gainax = TopMoive[TopMoive["studio"].str.contains("Gainax")]["IMDB"].mean()
Toei = TopMoive[TopMoive["studio"].str.contains("Toei")]["IMDB"].mean()