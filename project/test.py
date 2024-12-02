import os
import sqlite3

from pipeline import *


def test_downloadPhysicalAcitivityAndExtract():
    result = downloadPhysicalActivityAndExtract()

    assert isinstance(result, pd.DataFrame)
    assert len(result) > 0

def test_downloadMentalHeahltAndExtract():
    result = downloadMentalHeahltAndExtract()

    assert isinstance(result, pd.DataFrame)
    assert len(result) > 0

def test_pipeline():
    path = './../data/ProjectTable.sqlite'

    main()

    assert os.path.exists(path)
    helper_test_db()

def helper_test_db():
    con = sqlite3.connect('./../data/ProjectTable.sqlite')
    curs = con.cursor()

    curs.execute("select * from CorrelationPaAndMh")
    result = curs.fetchall()
    curs.close()

    assert len(result) > 49
