import pandas as pd
import requests
import json
import matplotlib.pyplot as plt
import plotly.express as px

api_key = ""
api_base_url = "https://evds2.tcmb.gov.tr/service/evds/"

codebook = {'Date': 'Tarih',
 'USD': 'TP.DK.USD.A.YTL',
 'EUR': 'TP.DK.EUR.A.YTL',
 'ATS': 'TP.DK.ATS.A.YTL',
 'AUD': 'TP.DK.AUD.A.YTL',
 'BEF': 'TP.DK.BEF.A.YTL',
 'BGN': 'TP.DK.BGN.A.YTL',
 'CAD': 'TP.DK.CAD.A.YTL',
 'CHF': 'TP.DK.CHF.A.YTL',
 'CNY': 'TP.DK.CNY.A.YTL',
 'DEM': 'TP.DK.DEM.A.YTL',
 'DKK': 'TP.DK.DKK.A.YTL',
 'ECU': 'TP.DK.ECU.A.YTL',
 'ESP': 'TP.DK.ESP.A.YTL',
 'FIM': 'TP.DK.FIM.A.YTL',
 'FRF': 'TP.DK.FRF.A.YTL',
 'GBP': 'TP.DK.GBP.A.YTL',
 'GRD': 'TP.DK.GRD.A.YTL',
 'IEP': 'TP.DK.IEP.A.YTL',
 'IRR': 'TP.DK.IRR.A.YTL',
 'ITL': 'TP.DK.ITL.A.YTL',
 'JPY': 'TP.DK.JPY.A.YTL',
 'KWD': 'TP.DK.KWD.A.YTL',
 'LUF': 'TP.DK.LUF.A.YTL',
 'NLG': 'TP.DK.NLG.A.YTL',
 'NOK': 'TP.DK.NOK.A.YTL',
 'PKR': 'TP.DK.PKR.A.YTL',
 'PTE': 'TP.DK.PTE.A.YTL',
 'RON': 'TP.DK.RON.A.YTL',
 'RUB': 'TP.DK.RUB.A.YTL',
 'SAR': 'TP.DK.SAR.A.YTL',
 'SEK': 'TP.DK.SEK.A.YTL',
 'XDR': 'TP.DK.XDR.A.YTL',
 'QAR': 'TP.DK.QAR.A.YTL',
 'KRW': 'TP.DK.KRW.A.YTL',
 'AED': 'TP.DK.AED.A.YTL',
 'AZN': 'TP.DK.AZN.A.YTL'}

def _param_generator(param):
    """
    An internal function that generates parameters for the external API calls
    """
    param_text = ""
    for key, value in param.items():
        param_text += str(key) + "=" + str(value)
        param_text += "&"
    return param_text[:-1]



def _make_request(url, params={}):
    """
    An internal function that makes the call to the API
    """

    params = _param_generator(params)

    request = requests.Session().get(url + params)
    if request.status_code == 200:
        return request.content
    else:
        raise ConnectionError(
            "Connection error, please check your request. Url:{}".format(
                request.url
            )
        )
        
def get_series(detail=False, raw=False):
    """
    The function returns dataframe of series which belongs to given data group.
    Because of default detail parameter is False, only return "SERIE_CODE", "SERIE_NAME" and "START_DATE" value.
    """
    series = _make_request('https://evds2.tcmb.gov.tr/service/evds/serieList/',\
                                params = {'key' : api_key, 'type' : 'json', 'code' : 'bie_dkdovytl'})
    series = json.loads(series)
    df = pd.DataFrame(series)
    df = df['SERIE_CODE'].str[6:9].unique()
    return df


def get_data(
    series=get_series(),
    startdate="",
    enddate="",
    aggregation_types="",
    formulas="",
    frequency="",
    raw=False,
):
    """
    The function returns data of the given series data. Series must be typed as list.
    Also, set parameter raw=False to return dictionary format.
    If aggregation_types and formulas,
        - not defined, API returns value aggregated and calculated default aggregations type and formula for the series.
        - defined as a string, given aggregation type and formula applied for all given series
        - defined as a list, given aggregation types and formulas applied for given series respectively.
    Available aggregation types are avg, min, max, first, last, sum.
    Available formulas are the following:
        Percentage change: 1
        Difference: 2
        Yearly percentage change: 3
        Yearly difference: 4
        Percentage change in comparison with end of previous year: 5
        Difference in comparison with end of previous year: 6
        Moving average: 7
        Moving total: 8
    It is possible to set frequency of data. Possible frequencies are the following:
        Daily: 1
        Workday: 2
        Weekly: 3
        Two times in a month: 4
        Monthly: 5
        Quarterly: 6
        Six month: 7
        Yearly: 8
    """
    ticker = series
    print(ticker)
    reverted_dict = dict(zip(codebook.values(), codebook.keys()))
    series = list(map(codebook.get, series))
    
    
    if isinstance(series, list) == False:
        return print("Series type must be list.")

    # For daily data set enddate to startdate, if blank
    if enddate == "":
        enddate = startdate

    series_count = len(series)

    # Set aggregation type
    if aggregation_types == "":
        # Default aggregation method
        aggregation_type_param = ""
    elif isinstance(aggregation_types, list):
        # User defined aggregation per series
        aggregation_type_param = "-".join([str(i) for i in aggregation_types])
    else:
        # User defined aggregation same for all series
        aggregation_type_param = "-".join(
            [str(aggregation_types) for i in range(series_count)]
        )

    # Set formulas
    if formulas == "":
        # Default formula
        formula_param = ""
    elif isinstance(formulas, list):
        # User defined formula per series
        formula_param = "-".join([str(i) for i in formulas])
    else:
        # User defined formula same for all series
        formula_param = "-".join([str(formulas) for i in range(series_count)])

    data = _make_request(
        api_base_url,
        params={
            "series": "-".join(series),
            "startDate": startdate,
            "endDate": enddate,
            "type": "json",
            "key": api_key,
            "formulas": formula_param,
            "frequency": str(frequency),
            "aggregationTypes": aggregation_type_param,
        },
    )
    data = json.loads(data)["items"]
    # If raw is true return only json results.
    if raw:
        return data
    # Numeric values in json data is defined as text. To fix this problem, set dtype="float"
    new_col_names = ['Date'] + ticker
    df = pd.DataFrame(data, dtype="float")

    #df = pd.DataFrame(data, columns = ['Date'] + ticker, dtype="float")
    if "UNIXTIME" in df.columns:
        df.drop(columns=["UNIXTIME"], inplace=True)
    if type(ticker) != list:
        ticker = ticker.tolist()
    df.columns = ['Date'] + ticker
    
    
    return df

def plot_data(
    series=get_series(),
    startdate="",
    enddate="",
    aggregation_types="",
    formulas="",
    frequency="",
    raw=False,
):
    """
    The function returns data of the given series data. Series must be typed as list.
    Also, set parameter raw=False to return dictionary format.
    If end date not defined, end date set as equal to start date
    If aggregation_types and formulas,
        - not defined, API returns value aggregated and calculated default aggregations type and formula for the series.
        - defined as a string, given aggregation type and formula applied for all given series
        - defined as a list, given aggregation types and formulas applied for given series respectively.
    Available aggregation types are avg, min, max, first, last, sum.
    Available formulas are the following:
        Percentage change: 1
        Difference: 2
        Yearly percentage change: 3
        Yearly difference: 4
        Percentage change in comparison with end of previous year: 5
        Difference in comparison with end of previous year: 6
        Moving average: 7
        Moving total: 8
    It is possible to set frequency of data. Possible frequencies are the following:
        Daily: 1
        Workday: 2
        Weekly: 3
        Two times in a month: 4
        Monthly: 5
        Quarterly: 6
        Six month: 7
        Yearly: 8
    """
    
    df = get_data(
    series= series,
    startdate = startdate,
    enddate=enddate,
    aggregation_types=aggregation_types,
    formulas=formulas,
    frequency=frequency,
    raw=raw,
    )
    
  # Convert the first column to a datetime object
    df[df.columns[0]] = pd.to_datetime(df[df.columns[0]],dayfirst=True)

  # Set the date column as the index
    df.set_index(df.columns[0], inplace=True)
    df = df.fillna(method='bfill')
 
    fig = px.line(df, x=df.index, y=df.columns[0:])
    return fig.show()
    
    
def plot_normalized_data(
    series=get_series(),
    startdate="",
    enddate="",
    aggregation_types="",
    formulas="",
    frequency="",
    raw=False,
):
    """
    The function returns data of the given series data

    Parameters
    ----------
    series : pandas.core.frame.DataFrame
      A series of pandas
    startdate : string
      A date string YYYY-MM-DD
    end : string
      A date string YYYY-MM-DD

    Returns
    -------
    number
      A plot to be show()

    Examples
    --------
    >>> from qmsspkg import qmsspkg
    >>> a = pd.Categorical(["character", "hits", "your", "eyeballs"])
    >>> b = pd.Categorical(["but", "integer", "where it", "counts"])
    >>> qmsspkg.catbind(a, b)
    [character, hits, your, eyeballs, but, integer, where it, counts]
    Categories (8, object): [but, character, counts,
    eyeballs, hits, integer, where it, your]

    The function returns data of the given series data. Series must be typed as list.
    Also, set parameter raw=False to return dictionary format.
    If end date not defined, end date set as equal to start date
    If aggregation_types and formulas,
        - not defined, API returns value aggregated and calculated default aggregations type and formula for the series.
        - defined as a string, given aggregation type and formula applied for all given series
        - defined as a list, given aggregation types and formulas applied for given series respectively.
    Available aggregation types are avg, min, max, first, last, sum.
    Available formulas are the following:
        Percentage change: 1
        Difference: 2
        Yearly percentage change: 3
        Yearly difference: 4
        Percentage change in comparison with end of previous year: 5
        Difference in comparison with end of previous year: 6
        Moving average: 7
        Moving total: 8
    It is possible to set frequency of data. Possible frequencies are the following:
        Daily: 1
        Workday: 2
        Weekly: 3
        Two times in a month: 4
        Monthly: 5
        Quarterly: 6
        Six month: 7
        Yearly: 8
    """
    
    df = get_data(
    series= series,
    startdate = startdate,
    enddate=enddate,
    aggregation_types=aggregation_types,
    formulas=formulas,
    frequency=frequency,
    raw=raw,
    )
    
  # Convert the first column to a datetime object
    df[df.columns[0]] = pd.to_datetime(df[df.columns[0]],dayfirst=True)

  # Set the date column as the index
    df.set_index(df.columns[0], inplace=True)
    df = df.fillna(method='bfill')
    
  # Get the first row of the dataframe
    first_row = df.iloc[0]
  
  # Divide all columns except the first one by the value in the first row
    for col in df.columns[0:]:
        df[col] = df[col] / first_row[col]

  # Plot all the columns in the DataFrame
    fig = px.line(df, x=df.index, y=df.columns[0:])
    return fig.show()

class ConnectionError(Exception):
    pass