import os
import sqlite3

import pytest
import pandas as pd
from pipeline import *


def test_downloadPhysicalAcitivityAndExtract():
    result = downloadPhysicalActivityAndExtract()

    assert isinstance(result, pd.DataFrame)
    assert len(result) > 0


def test_downloadMentalHeahltAndExtract():
    result = downloadMentalHeahltAndExtract()

    assert isinstance(result, pd.DataFrame)
    assert len(result) > 0


def test_extractSingleQuestion():
    question_filtered = 'How are you?'
    question_unimportant = 'Not important'
    data = {'Question': [question_filtered, question_unimportant, question_filtered],
            'State': ['California', 'Texas', 'Alasca'],
            'Data_Value': [34, 35, 36],
            'Unimportant_column': [1, 2, 3]}
    df = pd.DataFrame(data)

    result = extractSingleQuestion(df, question_filtered)

    assert len(result) == 2
    assert len(result.columns) == 2
    assert result.iloc[0]['State'] == 'California'
    assert result.iloc[1]['State'] == 'Alasca'
    assert result.iloc[0][question_filtered] == 34
    assert result.iloc[1][question_filtered] == 36


def test_mapMentalHealthValuesToDecimal_correctValues():
    df = pd.DataFrame(index=[1, 2, 3])
    df['Mental Health'] = '0%'
    df['Mental Health CI Lower'] = '20%'
    df['Mental Health CI Upper'] = '35.356%'

    result = mapMentalHealthValuesToDecimal(df)

    assert result['Mental Health'].iloc[0] == 0
    assert result['Mental Health CI Lower'].iloc[0] == 20
    assert result['Mental Health CI Upper'].iloc[0] == 35.356


def test_mapMentalHealthValuesToDecimal_incorrectValues():
    df = pd.DataFrame(index=[1, 2, 3])
    df['Mental Health'] = '0%'
    df['Mental Health CI Lower'] = 'Hallo'
    df['Mental Health CI Upper'] = '35.356%'

    with pytest.raises(ValueError):
        mapMentalHealthValuesToDecimal(df)


def test_pipeline():
    path = './data/ProjectTable.sqlite'
    if os.path.exists(path):
        os.remove(path)

    main()

    assert os.path.exists(path)
    helper_test_db()


def helper_test_db():
    con = sqlite3.connect('./data/ProjectTable.sqlite')
    curs = con.cursor()

    curs.execute("select * from CorrelationPaAndMh")
    result = curs.fetchall()
    curs.close()

    assert len(result) > 49
