#TREZOR Core API

Syntax used below is a valid Python function declaration with type hints defined in [PEP 0484](https://www.python.org/dev/peps/pep-0484/).


## Settings

### APPS

`APPS` is list with python packages that reside in './apps/' in your package. If you want to disable some app or enable you can do it easily by just specyfing which package should be lodaded at boot

### START_APP

`START_APP` is an dict which app should be lodaded and example
```

START_APP = {
    'app': 'homescreen',
    'view': 'layout_homescreen'
}

if no view is specified then it will look for default_view in app
