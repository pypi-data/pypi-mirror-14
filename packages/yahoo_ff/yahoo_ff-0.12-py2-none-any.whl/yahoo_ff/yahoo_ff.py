import time
import json

from dateutil import parser
import Quandl
import pandas as pd
import constants

from .tools import *


class yahoo_ff:
    '''class contains incomestatement, balancesheet, cashflow and price history for a ticker'''
    incomestatement_fields = constants.incomestatement_fields
    balancesheet_fields = constants.balancesheet_fields
    cashflow_fields = constants.cashflow_fields
    sleep = 1 # sec

    def __init__(self, ticker):
            self.flag = 0
            self.ticker = ticker
            self.__wait()
            self.__construct_incomestatement_annual()
            self.__wait()
            self.__construct_incomestatement_quarterly()
            self.__wait()
            self.__construct_balancesheet_annual()
            self.__wait()
            self.__construct_balancesheet_quarterly()
            self.__wait()
            self.__construct_cashflow_annual()
            self.__wait()
            self.__construct_cashflow_quarterly()
            self.__wait()
            self.__construct_stockinfo()
            self.__wait()
            self.__get_pricehistory()
            print 'flag is ' + str(self.flag)

    def __construct_incomestatement_annual(self):
        '''populate self.incomestatement_annual'''
        try:
            html = get_source_code(
                get_annual_incomestatement_url(
                    self.ticker)).split('Get Income Statement for:')[1]

            self.incomestatement_annual = self.__get_endofperiod(html)
            for field in self.incomestatement_fields:
                self.incomestatement_annual[field] = request(html, field)
            print 'Annual income statement for ' + str(self.ticker) + ' successfuly obtained'
        except Exception,e:
            self.flag = 1
            print 'failed construct_incomestatement_annual for ' + self.ticker + '; ' + str(e)

    def __construct_incomestatement_quarterly(self):
        '''populate self.incomestatement_quarterly'''
        try:
            html = get_source_code(
                get_quarterly_incomestatement_url(
                    self.ticker)).split('Get Income Statement for:')[1]

            self.incomestatement_quarterly = self.__get_endofperiod(html)
            for field in self.incomestatement_fields:
                self.incomestatement_quarterly[field] = request(html, field)
            print 'Quarterly income statement for ' + str(self.ticker) + ' successfuly obtained'
        except Exception, e:
            self.flag = 1
            print 'failed construct_incomestatement_quarterly for ' + self.ticker + '; ' + str(e)

    def __construct_balancesheet_annual(self):
        '''populate self.balancesheet_annual'''
        try:
            html = get_source_code(
                get_annual_balancesheet_url(
                    self.ticker)).split('Get Balance Sheet for:')[1]
            self.balancesheet_annual = self.__get_endofperiod(html)
            for field in self.balancesheet_fields:
                self.balancesheet_annual[field] = request(html, field)
            print 'Annual balance sheet for ' + str(self.ticker) + ' successfuly obtained'
        except Exception, e:
            self.flag = 1
            print 'failed construct_balancesheet_annual for ' + self.ticker + '; ' + str(e)

    def __construct_balancesheet_quarterly(self):
        '''populate self.balancesheet_quarterly'''
        try:
            html = get_source_code(
            get_quarterly_balancesheet_url(
                self.ticker)).split('Get Balance Sheet for:')[1]
            self.balancesheet_quarterly = self.__get_endofperiod(html)
            for field in self.balancesheet_fields:
                self.balancesheet_quarterly[field] = request(html, field)
            print 'Quarterly balance sheet for ' + str(self.ticker) + ' successfuly obtained'
        except Exception, e:
            self.flag = 1
            print 'failed construct_balancesheet_quarterly for ' + self.ticker + '; ' + str(e)

    def __construct_cashflow_annual(self):
        '''populate self.cashflow_annual'''
        try:
            html = get_source_code(
                get_annual_cashflow_url(
                    self.ticker)).split('Get Cash Flow for:')[1]
            self.cashflow_annual = self.__get_endofperiod(html)
            for field in self.cashflow_fields:
                self.cashflow_annual[field] = request(html, field)
            print 'Annual Cash Flows for ' + str(self.ticker) + ' successfuly obtained'
        except Exception, e:
            self.flag = 1
            print 'failed construct_cashflow_annual for ' + self.ticker + '; ' + str(e)

    def __construct_cashflow_quarterly(self):
        '''populate self.cashflow_quarterly'''
        try:
            html = get_source_code(
                get_quarterly_cashflow_url(
                    self.ticker)).split('Get Cash Flow for:')[1]
            self.cashflow_quarterly = self.__get_endofperiod(html)
            for field in self.cashflow_fields:
                self.cashflow_quarterly[field] = request(html, field)
            print 'Quarterly Cash Flows for ' + str(self.ticker) + ' successfuly obtained'
        except Exception, e:
            self.flag = 1
            print 'failed construct_cashflow_quarterly for ' + self.ticker + '; ' + str(e)

    def __construct_stockinfo(self):
        '''get basic information on the stock (sector, industry, nb of employees'''
        try:
            html = get_source_code(get_stockinfo_url(self.ticker))
            self.infos = get_infos(html)
            html = get_source_code(get_keystats_url(self.ticker))
            self.keystats = get_keystats(html)

        except Exception, e:
            self.flag = 1
            print 'failed construct_stockinfo for ' + self.ticker + '; ' + str(e)

    def __get_endofperiod(self, html):
        '''scrape the html source code for the ending periods of each column'''
        source_code = html
        end_periods = source_code.split('Period Ending')[1]
        end_periods = end_periods.split('</TR>')[0]
        # take out unwanted html formatting
        end_periods = end_periods.replace(
            '<TD class="yfnc_modtitle1" align="right"><b>', '')
        end_periods = end_periods.replace('<th scope="col" style="border-top:2px solid '
                                          '#000;text-align:right; font-weight:bold">', '')
        end_periods = end_periods.replace('</span></small></td>', '')
        end_periods = end_periods.replace('</span></small></TD>', '')
        end_periods = end_periods.replace('</b>', '')
        #s split
        end_periods = end_periods.split('</th>')
        # if '</th>' is not used to split periods
        if len(end_periods) == 1:
            end_periods = end_periods[0].split('</TD>')

        return {'endofperiod': [parser.parse(x[-constants.date_string_length:]) for x in
                                end_periods if x is not '']}

    def __get_pricehistory(self):
        '''get stock price history and volume traded using quandl api'''
        with open('yahoo_ff/credentials.json', 'r') as creds:
            credentials = json.load(creds)
            try:
                self.pricehistory = Quandl.get(
                    'WIKI/' + self.ticker, authtoken=credentials['Quandl']['key'])
            except Exception, e:
                self.flag = 1
                print 'failed get_pricehistory for ' + self.ticker + '; ' + str(e)

    def __wait(self):
        time.sleep(yahoo_ff.sleep)

        def package_sec_annually(self):
            '''package all annual info from incomestatement, blanacesheet and cashflow into a pandas
            dataframe'''
            isa = pd.DataFrame(self.incomestatement_annual)
            bsa = pd.DataFrame(self.balancesheet_annual)
            csa = pd.DataFrame(self.cashflow_annual)
            df = pd.merge(isa, bsa, on='endofperiod')
            df1 = pd.merge(df, csa, on='endofperiod')
            df1.set_index('endofperiod', inplace=True)
            df1 = df1.transpose()
            return df1

        def package_sec_quarterly(self):
            '''package all quarterly info from incomestatement, blanacesheet and cashflow into a pandas
            dataframe'''
            isa = pd.DataFrame(self.incomestatement_quarterly)
            bsa = pd.DataFrame(self.balancesheet_quarterly)
            csa = pd.DataFrame(self.cashflow_quarterly)
            df = pd.merge(isa, bsa, on='endofperiod')
            df1 = pd.merge(df, csa, on='endofperiod')
            df1.set_index('endofperiod', inplace=True)
            df1 = df1.transpose()
            return df1

    def package_sec_annually(self):
        '''package all annual info from incomestatement, blanacesheet and cashflow into a pandas
        dataframe'''
        isa = pd.DataFrame(self.incomestatement_annual)
        bsa = pd.DataFrame(self.balancesheet_annual)
        csa = pd.DataFrame(self.cashflow_annual)
        df = pd.merge(isa, bsa, on='endofperiod')
        df1 = pd.merge(df, csa, on='endofperiod')
        df1.set_index('endofperiod', inplace=True)
        df1 = df1.transpose()
        return df1

    def package_sec_quarterly(self):
        '''package all quarterly info from incomestatement, blanacesheet and cashflow into a pandas
        dataframe'''
        isa = pd.DataFrame(self.incomestatement_quarterly)
        bsa = pd.DataFrame(self.balancesheet_quarterly)
        csa = pd.DataFrame(self.cashflow_quarterly)
        df = pd.merge(isa, bsa, on='endofperiod')
        df1 = pd.merge(df, csa, on='endofperiod')
        df1.set_index('endofperiod', inplace=True)
        df1 = df1.transpose()
        return df1

