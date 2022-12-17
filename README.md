# fxplotter

A package to to import foreign exchange currency series and plot them.

## Installation

```bash
$ pip install -i https://test.pypi.org/simple/ fxplotter==1.0.0 --no-dependencies
```

## Usage
- First get your API key from evds website https://evds2.tcmb.gov.tr/index.php?/evds/login  by creating an account. 

- You will need to set your api key first to run the package:
```python
from fxplotter import fxplotter
fxplotter.api_key = ''
```

- You can access to the available currencies with the following:

```python
fxplotter.get_series()
```

- You can get the historical data for the specified list of currencies and a date window:

```python
fxplotter.get_series()
```

- You can also plot them interactively. For example:

```python
fxplotter.plot_data(['USD', 'EUR', 'JPY'],startdate="01-01-2018", enddate="01-12-2022")
```

- Or, you can also plot them in a normalized fashion:

```python
fxplotter.plot_normalized_data(['USD', 'EUR', 'JPY'],startdate="01-01-2018", enddate="01-12-2022")
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`fxplotter` was created by Ahmet Besiroglu. It is licensed under the terms of the MIT license.

## Credits

`fxplotter` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
