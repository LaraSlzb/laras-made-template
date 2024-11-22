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
    pysicalActivityDf = pd.read_csv('https://data.cdc.gov/api/views/hn4x-zwk7/rows.csv?accessType=DOWNLOAD', sep=',')
    logging.info('CSV physical activity is successfully downloaded and extracted to a dataframe')
    return pysicalActivityDf


'''
This method downloads the Zip file and extract the table 27 about mental health into a dataframe
'''
@retry(tries=3, delay=10, logger=logging.getLogger())
def downloadMentalHeahltAndExtract():
    request = requests.get(
        'https://www.samhsa.gov/data/sites/default/files/reports/rpt32805/2019NSDUHsaeExcelPercents/2019NSDUHsaeExcelPercents/2019NSDUHsaeExcelCSVs.zip')
    zip_ref = ZipFile(BytesIO(request.content))
    mentalHealthDf = pd.read_csv(zip_ref.open('NSDUHsaeExcelTab27-2019.csv'), encoding='Windows-1252')
    logging.info('Zip file mental health is successfully downloaded and extracted to a dataframe')
    return mentalHealthDf


'''
This method filters the dataframe physical activities to the needed rows and columns
'''
def renameAndFilterColumnsAndRowsPhysicalActivities(df):
    df = df[['YearStart', 'LocationDesc', 'Question', 'Data_Value', 'StratificationCategory1']]
    df = df.rename(columns={'LocationDesc': 'State'})
    df = df.loc[(df['YearStart'] == 2019) & (df['StratificationCategory1'] == 'Total') & (df['State'] != 'New Jersey')]
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

    mergedDf = []
    for question in [noSport, sport150, sport300, muscleSport]:
        mergedDf.append(df, question)

    mergedDf = reduce(lambda left, right: pd.merge(left, right, on=['State'], how='outer'), mergedDf)
    logging.info('Dataframe physical activity is successfully reformated')
    return mergedDf


'''
This method extract a single question and renames its value to the question.
'''
def extractSingleQuestion(df, question):
    questionDf = df.loc[df['Question'] == question]
    questionDf = questionDf[['State', 'Data_Value']]
    return questionDf.rename(columns={'Data_Value': question})


'''
This method filters the dataframe mental health to the needed rows and columns
'''
def renameAndFilterColumnsAndRowsMentalHealth(df):
    df.columns = df.iloc[4]
    df.drop(labels=[0, 1, 2, 3, 4], axis=0, inplace=True)  # drop unstructured data
    df = df[['State', '18 or Older Estimate', '18 or Older 95% CI (Lower)', '18 or Older 95% CI (Upper)']]
    df = df.rename(
        columns={'18 or Older Estimate': 'Mental Health', '18 or Older 95% CI (Lower)': 'Mental Health CI Lower',
                 '18 or Older 95% CI (Upper)': 'Mental Health CI Upper'})
    logging.info('Dataframe mental health is successfully filtered')
    return df


'''
This methods maps the percentages in the dataframe mental health to floats
'''
def mapMentalHealthValuesToDecimal(df):
    percentageColumns = ['Mental Health', 'Mental Health CI Lower', 'Mental Health CI Upper']
    for columnName in percentageColumns:
        df[columnName] = df[columnName].map(lambda value: float(value.strip('%')))
    logging.info('The values in the dataframe Mental Health were successfully transformed to floats')
    return df


'''
This method checks if there are enough rows
'''
def checkDataframeLen(df):
    if len(df) < 50 - 1:  # New Jersey is dropped as the data was not available
        raise ValueError('There are missing rows in the dataframe')


'''
This method checks if the percentage values are in the correct range
'''
def checkDataframeValues(df):
    for columnName in df.columns:
        if columnName != 'State':
            if ~pd.Series(df[columnName]).between(0, 100).all():
                raise ValueError('There are incorrect values in the dataframe')


'''
This method loads the dataframe into a sqlite
'''
def loadDfToSqlite(df, name, con):
    df.to_sql(name, con, if_exists='replace', index=False)
    logging.info(f'The dataframe was successfully loaded into the sqlite {name}')


if __name__ == '__main__':
    mentalDf = downloadMentalHeahltAndExtract()
    physicalDf = downloadPhysicalActivityAndExtract()

    mentalDf = renameAndFilterColumnsAndRowsMentalHealth(mentalDf)
    physicalDf = renameAndFilterColumnsAndRowsPhysicalActivities(physicalDf)

    physicalDf = reformatDfPhysicalHealth(physicalDf)

    mentalDf = mapMentalHealthValuesToDecimal(mentalDf)

    checkDataframeLen(physicalDf)
    checkDataframeLen(mentalDf)
    checkDataframeValues(physicalDf)
    checkDataframeValues(mentalDf)

    joinedDf = pd.merge(mentalDf, physicalDf, on='State', how='inner')
    checkDataframeLen(joinedDf)

    con = sql.connect('./../data/ProjectTable.sqlite')
    loadDfToSqlite(joinedDf, 'CorrelationPaAndMh', con)
