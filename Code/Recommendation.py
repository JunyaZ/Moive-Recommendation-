# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 15:06:21 2018

@author: Junya Zhao
"""

import pandas as pd
import numpy as np
import os
import seaborn as sns 
from sklearn.metrics import jaccard_similarity_score
from scipy.spatial.distance import pdist, squareform
from sklearn.metrics.pairwise import euclidean_distances
obs =os.path.dirname(os.getcwd()) 
Datpath= obs + "\\Data\\"
Output = obs + "\\output\\"

def Bestanime(file,perc,imdb,top):
    m = file['scored_by'].quantile(perc)
    C = file[file['score'].notnull()]['score'].mean()
    v= file['scored_by']
    R = file['score']
    result= pd.DataFrame((v/(v+m) * R) + (m/(m+v) * C)).rename(columns = {0:'IMDB'})
    result = pd.concat([file,result],axis=1)
    #result =result.drop(["title_english","title_japanese","title_synonyms","image_url","status","airing","aired_string","background","premiered","broadcast","related","opening_theme","ending_theme"],axis=1)
    result =result.drop(["airing","aired_string","background","premiered","broadcast","related","opening_theme","ending_theme"],axis=1)
    result= result[result["IMDB"]>imdb]
    result.sort_values("IMDB", inplace=True,ascending=False)
    return result[:top]

def Animegenre(file,animeId,threshold):
    genreDistribution = file[['anime_id']].join(file["genre"].str.get_dummies(', '))
    Selected =pd.DataFrame()
    for i in range(0,len(file)):
        score= jaccard_similarity_score(genreDistribution[genreDistribution["anime_id"]==animeId].iloc[:,1:],genreDistribution.iloc[i:i+1,1:])
        if score > threshold:
            Selected=pd.concat([Selected,genreDistribution.iloc[i:i+1,0:]],sort=False)
    animelist= list(Selected["anime_id"].values)
#    recommendationAnime = file[file["anime_id"].isin(animelist)]
#    recommendationAnime["type"].unique()
    return animelist
    
def UserMatrix(UserAnimefilter,GoodUser):
    GoodUser['age'] = GoodUser['birth_date'].apply(lambda row: (2018-int(row.split(sep= "-")[0])))
    GoodUser["gender"] = GoodUser["gender"].replace({"Female":0,"Male":1})
    GoodUser[GoodUser["age"] <= 13] =0
    GoodUser[GoodUser["age"] > 13] =1
    AGE_GENDER =GoodUser[["username","age","gender"]]
    UserAnimefilter.my_score = pd.to_numeric(UserAnimefilter.my_score, errors='coerce')
    my_score=pd.DataFrame(UserAnimefilter.groupby('username')['my_score'].apply(list))
    my_score =my_score["my_score"].apply(pd.Series)
    my_score = (my_score - my_score.mean()) / (my_score.max() - my_score.min())
    my_score.reset_index(level=0, inplace=True)
    anime_id=pd.DataFrame(UserAnimefilter.groupby('username')['anime_id'].apply(list))
    anime_id =anime_id["anime_id"].apply(pd.Series)
    anime_id.reset_index(level=0, inplace=True)
    UserMatrix =pd.concat([my_score,AGE_GENDER],axis =1)
    UserMatrix =UserMatrix.T.groupby(level=0).first().T
    UserMatrix = UserMatrix.fillna(0)
    return UserMatrix

def SelectedUser(UserAnimefilter,GoodUser,Username,user_index):
    UserMatrixbulider= UserMatrix(UserAnimefilter,GoodUser)
    targetUser =  UserMatrixbulider[UserMatrixbulider["username"]==Username]
    distance= dict()
    for i in range(0,len(UserMatrixbulider)):
        dist = euclidean_distances(targetUser.iloc[:,:-1], UserMatrixbulider.iloc[i:i+1,:-1])
        distance.update({UserMatrixbulider.at[i,"username"]:dist[0][0] })
        SelectedUser =min(distance, key=distance.get)
    return SelectedUser
        
def recommendation(animeId,user_index):
    GoodUser= pd.read_csv(Output +"GoodUser.csv")
    UserAnimefilter = pd.read_csv(Output + "UserAnimefilter.csv")
    file= pd.read_csv(Datpath +"anime_cleaned.csv" )
    

#   if there is no user and anime information, the system will recommendate the top 100 anime
    if animeId==None and user_index== None:
        Topanime = Bestanime(file,0.8,7,100) 
        return Topanime
#   if there the input only contains anime information, the system will recommendate anime that most samliar to input anime
    elif user_index==None:
        recommendatedAnime = Animegenre(file,animeId,0.8)
        return recommendatedAnime
#   if there the input only contains anime information, the system will recommendate anime that most samliar to input anime
    elif animeId==None:            
        SelectedUsername = SelectedUser(UserAnimefilter,GoodUser,GoodUser["username"][user_index],user_index)
        print("The user who are most samliar to input user:", SelectedUsername)
        selectedAnime = UserAnimefilter[UserAnimefilter["username"]==SelectedUsername]
        Animelist = selectedAnime[selectedAnime["my_score"]>8.5]["anime_id"].values.tolist()
        LikedAnime = list(map(int, Animelist))
        return LikedAnime
    else:
        recommendatedAnime = Animegenre(file,animeId,0.8)
        SelectedUsername = SelectedUser(UserAnimefilter,GoodUser,GoodUser["username"][user_index],user_index)
        selectedAnime = UserAnimefilter[UserAnimefilter["username"]==SelectedUsername]
        Animelist = selectedAnime[selectedAnime["my_score"]>8.5]["anime_id"].values.tolist()
        LikedAnime = list(map(int, Animelist))
        return set(recommendatedAnime).intersection(LikedAnime)
    
if __name__ == '__main__':
#    GoodUser= pd.read_csv(Output +"GoodUser.csv")
#    UserAnimefilter = pd.read_csv(Output + "UserAnimefilter.csv")
#    file= pd.read_csv(Datpath +"anime_cleaned.csv" )
    recommendaed_AnimeList1 =recommendation(None,None)
    recommendaed_AnimeList2 =recommendation(None,466)
    recommendaed_AnimeList3 =recommendation(12189,None)
    recommendaed_AnimeList4 =recommendation(12189,466)
#    UserMatrix_output = UserMatrix(UserAnimefilter,GoodUser)
#    SelectedUsername = SelectedUser(UserAnimefilter,GoodUser,GoodUser["username"][0])
#    selectedAnime = UserAnimefilter[UserAnimefilter["username"]==SelectedUsername]["anime_id"]
    print(recommendaed_AnimeList1) 
    print(recommendaed_AnimeList2)  
    print(recommendaed_AnimeList3)  
    print(recommendaed_AnimeList4)   
#    print(selectedAnime)
    