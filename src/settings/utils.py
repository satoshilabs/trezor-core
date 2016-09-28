import trezor.main
from settings import config


def autodiscover_apps():
    for app in config.APPS:
        module = import_app(app)
        module.boot()


def import_app(name, func='boot'):
    return __import__('apps.{}'.format(name), globals(), locals(), [func], 0)


def setup_default_view():
    app = config.START_APP['app']
    view = config.START_APP.get('view', 'default_view')

    module_app, func = view.split('.')
    module = import_app(app +'.'+ module_app, view)
    trezor.main.run(default_workflow=getattr(module, view.split('.')[-1]))