from fxplotter import fxplotter
import pandas


# _param_generator
def test_param_generator():
    params = fxplotter._param_generator({'salih': 'benli', 'ahmet': 'besir'})
    assert params == 'salih=benli&ahmet=besir'

# _make_request
def test_make_request():
    request_content = fxplotter._make_request('https://reqres.in/api/200')
    assert type(request_content) == bytes

# get_data

def test_get_data():
    data = fxplotter.get_data(['USD','EUR'],startdate="01-01-2019", enddate="01-01-2020")
    assert type(data) == pandas.core.frame.DataFrame






