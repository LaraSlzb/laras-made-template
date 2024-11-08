import pandas as pd
import sqlite3 as sql
from zipfile import ZipFile

import requests
from io import BytesIO


def downloadPhysicalActivity():
    df = pd.read_csv('https://data.cdc.gov/api/views/hn4x-zwk7/rows.csv?accessType=DOWNLOAD', sep=',')
    df = df[['YearStart', 'LocationDesc', 'Question', 'Data_Value', 'StratificationCategory1']]
    df.rename(columns={'LocationDesc': 'State'}, inplace=True)
    df = df.loc[(df['YearStart'] == 2020) & (df['StratificationCategory1'] == 'Total') & (
                df['Question'] == 'Percent of adults who engage in no leisure-time physical activity')]
    return df

def downloadMentalHeahlt():
    r = requests.get('https://www.samhsa.gov/data/sites/default/files/reports/rpt44484/2022-nsduh-sae-tables-percent-CSVs/2022-nsduh-sae-tables-percent-CSVs.zip')
    zip_ref = ZipFile(BytesIO(r.content))
    df = pd.read_csv(zip_ref.open('NSDUHsaeExcelTab31-2022.csv'))
    df.columns = df.iloc[4]
    df = df.drop(labels=[0, 1, 2, 3, 4], axis=0)
    return df

if __name__ == '__main__':
    mental = downloadMentalHeahlt()
    physical = downloadPhysicalActivity()
    con = sql.connect('./../data/ProjectTable.sqlite')
    physical.to_sql('physicalActivity', con, if_exists='replace', index=False)
    mental.to_sql('mentalHealth', con, if_exists='replace', index=False)
    join = pd.merge(mental, physical, on='State', how='inner')
    join.to_sql('joinedTable', con, if_exists='replace', index=False)