# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 12:15:27 2018

@author: Junya Zhao
"""
import time
import pandas as pd
import numpy as np
import os
import glob
import pycountry

obs =os.path.dirname(os.getcwd()) 
Datpath= obs + "\\Data\\"
Output = obs + "\\output\\"
#def read_file():
#    #DataName = [(Dataset[i].split(sep="\\")[-1].split(sep=".")[0]) for i in range(0,len(Dataset))]
#    #Dic ={item : Dataset[index] for index, item in enumerate(list(range(len(DataName))))} 
#    for i in range(0,len(Dataset)):
#        vars()[Dataset[i].split(sep="\\")[-1].split(sep=".")[0]] = pd.read_csv(Dataset[i])
def BestMoive(file,perc,imdb,top):
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

#def User_cleaning(file):
#    file= file[file["user_days_spent_watching"]!=0]
#    file= file[file["location"].notnull()]
#    file= file[file["stats_mean_score"]!=0]
#    file= file[file["stats_episodes"]!=0]
#    file= file[file["gender"].notnull()]
#    file= file[file["gender"]!='Non-Binary']
#    return file

def Countrylist():
    AllCountry= list(pycountry.countries)
    CountryName= []
    for i in range(len(AllCountry)):
        CountryName.append(str(AllCountry[i]).split(sep='name=')[1].split(sep=",")[0].replace("'", ""))
    return CountryName

def filterLocation(file):
    CountryName = Countrylist()
    file= file[file['location'].notnull()]
    ValidLocation= file[file['location'].str.contains('|'.join(CountryName))]
    return ValidLocation

def SelectUser(file,column1, column2):
    ValidLocation = filterLocation(file)
    file = ValidLocation[ValidLocation[column1]!=0]
    file= file[file[column1].notnull()]
    file = file[ValidLocation[column2]> 30]
    file=file.drop(['access_rank'],axis=1)
    file.sort_values("user_completed", inplace=True,ascending=False)
    return file

def UserAnimefilter(anime, User, AnimeUser):
    animelist= list(anime["anime_id"].values)
    userlist =list(User["username"].values)
    filtered =pd.DataFrame()
    for df in pd.read_csv(AnimeUser,chunksize=1000000):
        df=df.drop(['my_start_date', 'my_finish_date','my_status','my_rewatching_ep','my_rewatching'],axis=1)
        df = df[df["anime_id"].isin(animelist)]
        df = df[df["username"].isin(userlist)]
        df.to_csv(Output +  "UserAnimefilter.csv",mode='a',index= False)
        print("chunkdone")
        #filtered=pd.concat([filtered,df],ignore_index=True)
        filtered.append(df)
    return filtered

if __name__ == '__main__':     
    start = time.time()
    Dataset = list(glob.glob(Datpath + "*.csv" ))
    #AnimeList = pd.read_csv(Dataset[0])
    anime_cleaned = pd.read_csv(Dataset[1])
#    anime_filtered = pd.read_csv(Dataset[2])
#    UserList = pd.read_csv(Dataset[4])
    users_cleaned = pd.read_csv(Dataset[5])
#    users_filtered = pd.read_csv(Dataset[6])
    TopMoive = BestMoive(anime_cleaned,0.8,0,len(anime_cleaned)) 
    GoodUser = SelectUser(users_cleaned,"stats_mean_score","user_days_spent_watching")
#    TopMoive.to_csv(Output+ "TopMoive.csv",index=False)
#    GoodUser.to_csv(Output+ "GoodUser.csv",index=False)
#   UserAnime =UserAnimefilter(TopMoive, GoodUser, Dataset[3])
    end = time.time()
    print("running time:" ,end-start)