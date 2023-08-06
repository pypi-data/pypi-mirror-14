import pytest
import pickle
from yahoo_ff import yahoo_ff


# TODO add many more tests
#       check if 3 arguments in time in annually, if not, fill with NaN

def test_package_sec_annually():
    aapl = yahoo_ff('aapl')
    aapltest = pickle.load(open('test.p', "rb"))

    for field in aapl.incomestatement_fields:
        assert aapltest.incomestatement_annual[field] == \
               aapl.incomestatement_annual[field]

    for field in aapl.balancesheet_fields:
        assert aapltest.balancesheet_annual[field] == \
               aapl.balancesheet_annual[field]


    for field in aapl.cashflow_fields:
        assert aapltest.cashflow_annual[field] == \
               aapl.cashflow_annual[field]

