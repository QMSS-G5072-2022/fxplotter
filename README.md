# fxplotter

A package to to import foreign exchange currency series and plot them.

## Installation

```bash
$ pip install -i https://test.pypi.org/simple/ fxplotter==1.0.0 --no-dependencies
```

## Usage

- You will need to set your api key first:
```python
from fxplotter import fxplotter
fxplotter.api_key = ''
```

- You can access the available currencies with:
```python
fxplotter.get_series()
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`fxplotter` was created by Ahmet Besiroglu. It is licensed under the terms of the MIT license.

## Credits

`fxplotter` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
