# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 17:24:00 2016

@author: Animesh Kumar Jha
"""

import os
import json
import pandas as pd

"""Change the current working directory"""
path=""

if(path==""):
    path=os.getcwd()

os.chdir(path)
"""End the Working Directory change snippet"""

def new_my_json(newFile):
    myFile=open(newFile, 'r')
    myObject=myFile.read()
    myFile.close()
    myData=json.loads(myObject)
    
    #print(myData)
    myFrame=pd.DataFrame(myData)
    myFrame.to_csv("raw-data.csv", index=False)

    """Read the raw CSV file in a pandas data frame
    Print its summary
    Find the columns with null values
    Find the total number of columns"""
    df_file=pd.read_csv("raw-data.csv")
    print("Raw Data summary")
    print(df_file.describe())
    df_null_val=df_file.isnull().sum()  
    df_file_columns=list(df_file.columns.values)
    df_null_columns=df_null_val[df_null_val!=0]
    df_null_columns.index[0]

    """Find the columns that have null values"""
    mean_null_columns=[] 
    for obj in df_file_columns:
        for i in range(len(df_null_columns.index)):
            if (obj==df_null_columns.index[i]):
                mean_null_columns.append(int(df_file[obj].mean()))

    """print the columns that have null values and their mean values"""
    for i in range(len(mean_null_columns)):
        print("%s \t has mean value \t %s" %(df_null_columns.index[i], mean_null_columns[i]))

    """Fill the null values in the columns with their respective mean values"""
    for j in range(len(df_null_columns.index)):
        df_file[df_null_columns.index[j]]=df_file[df_null_columns.index[j]].fillna(mean_null_columns[j])

#    df_file_grp=df_file.groupby("continent")
    print("Summary for the cleaned data after filling up the missing values with mean \n")
    print(df_file.describe())
    
    """Write the contents of the updated file to a new CSV file 
    in the current Directory"""
    df_file.to_csv("clean-data.csv", index=False)