import constants
import requests
import ast
from datetime import datetime

API_KEY = constants.API_KEY  # Alpha Vantage API key
ticker = 'FCN'


def get_data(ticker, function, data1=None, period=None, data2=None):
    """Retrieve data from Alpha Vantage
    args:
        ticker (str): ticker or symbol for company.
        function (str): API function, e.g. 'OVERVIEW', 'EARNINGS'.
        data1 (str, optional): data field to request (Level 1). Defaults to None.
        data2 (str, optional): data field to request (Level 2). Defaults to None.
        period (int, optional): period to request (relative to today). Defaults to None.

    returns: Alpha Vantage API data
    rtype: dict, str or int
    """

    url = 'https://www.alphavantage.co/query?function=' + function + '&symbol=' + \
        ticker + '&apikey=' + API_KEY

    response = requests.request("GET", url)

    # If no particular datapoint has been specified, return the whole dictionary
    if data1 == None and data2 == None:
        return ast.literal_eval(response.text)
    # If a particular Level 1 datapoint has been specified, return that datapoint
    elif data2 == None:
        return ast.literal_eval(response.text)[data1][period]
    # If a particular Level 2 datapoint has been specified, return that datapoint
    else:
        return ast.literal_eval(response.text)[data1][period][data2]


def get_data_at_date(ticker, function, data1=None, data2=None, date=None):

    # work out the quarter ending on or before the date
    # if quarter is Q1, take prior full year, less prior Q1, plus current Q1
    # if quarter is Q2, take prior full year, less prior Q1 and Q2, plus current Q1 and Q2
    # if quarter is Q3, take prior year Q4 statement, current full year, less current q4
    # if quarter is Q4, take current full year

    return None


print(get_data('TSCO', "INCOME_STATEMENT", "annualReports", 0, "totalRevenue"))
print(get_data('TSCO', "OVERVIEW", "Description"))
