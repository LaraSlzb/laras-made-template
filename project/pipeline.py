from functools import reduce
import pandas as pd
import sqlite3 as sql
from zipfile import ZipFile

import requests
import logging
from io import BytesIO
from retry import retry

'''
This method downloads the CSV file physical Activity and extract it into a dataframe.
'''
@retry(tries=3, delay=10, logger=logging.getLogger())
def downloadPhysicalActivityAndExtract():
    df = pd.read_csv('https://data.cdc.gov/api/views/hn4x-zwk7/rows.csv?accessType=DOWNLOAD', sep=',')
    logging.info('CSV physical activity is successfully downloaded and extracted to a dataframe')
    return df


'''
This method downloads the Zip file and extract the table 27 about mental health into a dataframe
'''
@retry(tries=3, delay=10, logger=logging.getLogger())
def downloadMentalHeahltAndExtract():
    r = requests.get(
        'https://www.samhsa.gov/data/sites/default/files/reports/rpt32805/2019NSDUHsaeExcelPercents/2019NSDUHsaeExcelPercents/2019NSDUHsaeExcelCSVs.zip')
    zip_ref = ZipFile(BytesIO(r.content))
    df = pd.read_csv(zip_ref.open('NSDUHsaeExcelTab27-2019.csv'), encoding='Windows-1252')
    logging.info('Zip file mental health is successfully downloaded and extracted to a dataframe')
    return df


'''
This method filters the dataframe physical activities to the needed rows and columns
'''
def filterColumnsAndRowsPhysicalActivities(df):
    # filter columns
    df = df[['YearStart', 'LocationDesc', 'Question', 'Data_Value', 'StratificationCategory1']]
    # rename for merging
    df = df.rename(columns={'LocationDesc': 'State'})
    # filter lines
    df = df.loc[(df['YearStart'] == 2019) & (df['StratificationCategory1'] == 'Total')]
    logging.info('Dataframe physical activity is successfully filtered')
    return df


'''
This method reformats the dataframe physical health. It combines the different questions with the same state into one line.
'''
def reformatDfPhysicalHealth(df):
    noSport = "Percent of adults who engage in no leisure-time physical activity"
    sport150 = "Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic physical activity and engage in muscle-strengthening activities on 2 or more days a week"
    sport300 = "Percent of adults who achieve at least 300 minutes a week of moderate-intensity aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)"
    muscleSport = "Percent of adults who engage in muscle-strengthening activities on 2 or more days a week"
    noSportdf = extractSingleQuestion(df, noSport)
    sport150df = extractSingleQuestion(df, sport150)
    sport300df = extractSingleQuestion(df, sport300)
    muscleSportdf = extractSingleQuestion(df, muscleSport)

    mergeddf = [noSportdf, sport150df, sport300df, muscleSportdf]
    mergeddf = reduce(lambda left, right: pd.merge(left, right, on=['State'], how='outer'), mergeddf)
    logging.info('Dataframe physical activity is successfully reformated')
    return mergeddf


'''
This method extract a single question and renames its value to the question.
'''
def extractSingleQuestion(df, question):
    questiondf = df.loc[df['Question'] == question]
    questiondf = questiondf[['State', 'Data_Value']]
    return questiondf.rename(columns={'Data_Value': question})


'''
This method filters the dataframe mental health to the needed rows and columns
'''
def filterColumnsAndRowsMentalHealth(df):
    # name columns
    df.columns = df.iloc[4]
    # delete unnecessary lines
    df.drop(labels=[0, 1, 2, 3, 4], axis=0, inplace=True)
    # filter columns
    df = df[['State', '18 or Older Estimate', '18 or Older 95% CI (Lower)', '18 or Older 95% CI (Upper)']]
    logging.info('Dataframe mental health is successfully filtered')
    return df

'''
This method checks if there are enough rows
'''
def checkDataframe(df):
    if len(df) < 50:
        raise ValueError('There are missing rows in the dataframe')


'''
This method loads the dataframe into a sqlite
'''
def loadDfToSqlite(df, name, con):
    df.to_sql(name, con, if_exists='replace', index=False)
    logging.info(f'The dataframe was successfully loaded into the sqlite {name}')


if __name__ == '__main__':
    # Download data and extract to dataframe
    mentalDf = downloadMentalHeahltAndExtract()
    physicalDf = downloadPhysicalActivityAndExtract()

    # filter columns and rows
    mentalDf = filterColumnsAndRowsMentalHealth(mentalDf)
    physicalDf = filterColumnsAndRowsPhysicalActivities(physicalDf)

    # reformat dataframe physical health
    physicalDf = reformatDfPhysicalHealth(physicalDf)

    #check dataframes
    checkDataframe(physicalDf)
    checkDataframe(mentalDf)

    # Join tables on State and check number of rows
    joinedDf = pd.merge(mentalDf, physicalDf, on='State', how='inner')
    checkDataframe(joinedDf)

    # Load dataframes to a sqlite database
    con = sql.connect('./../data/ProjectTable.sqlite')
    loadDfToSqlite(physicalDf, 'physicalActivity', con)
    loadDfToSqlite(mentalDf, 'mentalHealth', con)
    loadDfToSqlite(joinedDf, 'joinedTable', con)
