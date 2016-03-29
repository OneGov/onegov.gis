import pytest

from morepath import setup
from onegov.core import Framework
from onegov.core.utils import scan_morepath_modules
from onegov.gis import MapboxApp
from webtest import TestApp as Client


def test_no_secret_keys(es_url):

    class App(Framework, MapboxApp):
        pass

    app = App()

    with pytest.raises(AssertionError):
        app.configure_application(mapbox_token='sk.asdf')


def test_mapbox_token_tween(es_url):

    config = setup()

    class App(Framework, MapboxApp):
        testing_config = config

    @App.path(path='')
    class Root(object):
        pass

    @App.html(model=Root)
    def view_root(self, request):
        return '<body></body>'

    scan_morepath_modules(App, config)
    config.commit()

    app = App()

    app.configure_application()
    assert '<body>' in Client(app).get('/')

    app.configure_application(mapbox_token='pk.asdf')
    assert '<body data-mapbox-token="pk.asdf"></body>'
