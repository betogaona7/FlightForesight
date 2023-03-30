
from flask import Flask 
from .settings import Config
from .utils import flask_server, restx_api

__version__ = "0.0.1"

api = restx_api(title="FlightForesight", version=__version__)

def create_app() -> Flask: 
    """initialise flask app

    Args:
        config_file (str, optional): path to config file. Defaults to None.

    Returns:
        Flask: flask instance
    """
    # load flask app
    app = flask_server(
        name="FlightForesight API", default_config=Config
    )

    # update swagger endpoint 
    if app.config.get("SWAGGER_DOC_URL"):
        api._doc = app.config["SWAGGER_DOC_URL"]

    # update API title
    if app.config.get("ENV"):
        api.title = f'{api.title} ({app.config["ENV"]})'

    # initialize app 
    api.init_app(app)

    # add namespaces 
    with app.app_context():
        from .routes import routes_ns
        if "/foresight/v1" in app.config.get("ENDPOINTS", []):
            api.add_namespace(routes_ns, "/foresight/v1")

        return app

__all__ = ["create_app"]

