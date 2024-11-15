import pandas as pd
import sqlite3 as sql
from zipfile import ZipFile

import requests
import logging
from io import BytesIO
from retry import retry


@retry(tries=3, delay=10, logger=logging.getLogger())
def downloadPhysicalActivityAndExtract():
    # download csv file
    df = pd.read_csv('https://data.cdc.gov/api/views/hn4x-zwk7/rows.csv?accessType=DOWNLOAD', sep=',')
    logging.info('CSV physical activity is successfully downloaded and extracted to a dataframe')
    return df


@retry(tries=3, delay=10, logger=logging.getLogger())
def downloadMentalHeahltAndExtract():
    # download zip file
    r = requests.get(
        'https://www.samhsa.gov/data/sites/default/files/reports/rpt44484/2022-nsduh-sae-tables-percent-CSVs/2022-nsduh-sae-tables-percent-CSVs.zip')
    zip_ref = ZipFile(BytesIO(r.content))
    # load csv file
    df = pd.read_csv(zip_ref.open('NSDUHsaeExcelTab31-2022.csv'))
    logging.info('Zip file mental health is successfully downloaded and extracted to a dataframe')
    return df


def filterColumnsAndRowsPhysicalActivities(df):
    # filter columns
    df = df[['YearStart', 'LocationDesc', 'Question', 'Data_Value', 'StratificationCategory1']]
    # rename for merging
    df = df.rename(columns={'LocationDesc': 'State'})
    # filter lines
    df = df.loc[(df['YearStart'] == 2020) & (df['StratificationCategory1'] == 'Total') & (
            df['Question'] == 'Percent of adults who engage in no leisure-time physical activity')]
    logging.info('Dataframe physical activity is successfully filtered')
    return df


def filterColumnsAndRowsMentalHealth(df):
    # name columns
    df.columns = df.iloc[4]
    # delete unnecessary lines
    df.drop(labels=[0, 1, 2, 3, 4], axis=0, inplace=True)
    # filter columns
    df = df[['State', '18+ Estimate', '18+ 95% CI (Lower)', '18+ 95% CI (Upper)']]
    return df


def loadDfToSqlite(df, name, con):
    df.to_sql(name, con, if_exists='replace', index=False)
    logging.info(f'The dataframe was successfully loaded into the sqlite {name}')


if __name__ == '__main__':
    #Download data and extract to dataframe
    mentalDf = downloadMentalHeahltAndExtract()
    physicalDf = downloadPhysicalActivityAndExtract()

    #filter columns and rows
    mentalDf = filterColumnsAndRowsMentalHealth(mentalDf)
    physicalDf = filterColumnsAndRowsPhysicalActivities(physicalDf)

    #Join tables on State
    joinedDf = pd.merge(mentalDf, physicalDf, on='State', how='inner')

    #Load dataframes to a sqlite database
    con = sql.connect('./../data/ProjectTable.sqlite')
    loadDfToSqlite(physicalDf, 'physicalActivity', con)
    loadDfToSqlite(mentalDf, 'mentalHealth', con)
    loadDfToSqlite(joinedDf, 'joinedTable', con)
