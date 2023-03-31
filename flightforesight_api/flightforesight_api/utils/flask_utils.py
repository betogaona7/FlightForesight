from flask import Flask, url_for
from flask_restx import Api


def flask_server(name: str = None, default_config: object = None) -> Flask:
    """create a Flask app instance.

    Args:
        name (str, optional): name of the application. Defaults to None.
        default_config (object, optional): default configuration object to use. Defaults to None.

    Returns:
        Flask: a Flask app instance
    """
    # get server name
    server_name = name if name is not None else __name__

    # create instance
    app = Flask(server_name)

    # load config
    app.config.from_object(default_config)

    return app


def restx_api(**kwargs) -> Api:
    """create a Flask_restx app instance.

    Returns:
        Api: flask_restx app instance.
    """

    # create instance
    api = Api(**kwargs)

    # check for https
    if kwargs.get("enable_https", False):
        @property
        def specs_url(self):
            return url_for(self.endpoint("specs"), _external=True, _scheme="https")

        # noinspection PyPropertyAccess
        api.specs_url = specs_url

    return api
