"""Flask Namespace for FlightForesight

Available endpoints:
    - predict/ (GET): endpoint to predict if a flight can be delayed or not.
    - preload/ (GET): loads the ML learning model creating a single instance of it for inference.
"""

from flask_restx import Resource, fields, Namespace
from ..utils import routes_utils as rutils
import time
from datetime import datetime, timedelta
from typing import Dict, Tuple
from flask_restx.reqparse import RequestParser
import pickle
import numpy as np
import os

from ..utils import data_headers_dict

MODEL_PATH = (
    os.path.join(os.getcwd(), "assets/models/model.pkl")
)

ns = Namespace(
    name="FlightForesight Delay Flight Predictor",
    description="collection of API endpoints",
)

_delay_prediction_model = None

delay_response_model = ns.model(
    "Delay Response Model",
    {
        "can_be_delayed": fields.String(),
        "load_time": fields.String(),
        "compute_time": fields.String(),
    },
)

delay_error_response = ns.model(
    "Delay Error Response Model", {"message": fields.String()}
)


def delay_prediction_error(e: Exception):
    """error handling for FlightForesight API endpoints

    Args:
        e (Exception): raised exception

    Returns:
        Tuple(Dict, int): response body, error status code
    """
    return {"message": e}, 400


@ns.route("/preload")
class FFPreloadApi(Resource):
    # define structure
    preload_mlmodel_response = ns.model(
        "Preload Response", {"load_time": fields.String()}
    )

    @ns.response(200, "Success", preload_mlmodel_response)
    @ns.response(500, "Failure", delay_error_response)
    def get(self):
        try:
            _, load_time = get_delay_prediction_model()
        except Exception as e:
            raise Exception(f"ML model preload failed {e}")

        response_output = {"load_time": load_time}
        return response_output


@ns.route("/predict")
class FFPredictDelay(Resource):
    # define structure
    predict_delay_response = ns.model(delay_response_model.name, delay_response_model)

    parser = RequestParser()
    parser = rutils.add_flight_arguments(parser)

    @ns.expect(parser)
    @ns.response(200, "Success", predict_delay_response)
    @ns.response(400, "Failure", delay_error_response)
    def get(self):
        flight_args = self.parser.parse_args()
        response_output, _ = predict_flight_delay(flight_args)
        return response_output


def predict_flight_delay(flight_args: Dict) -> Tuple[Dict, timedelta]:
    """predict whether the flight is going to be delayed or not

    Args:
        flight_args (Dict): request arguments

    Returns:
        Tuple[Dict, timedelta]: output response, compute time
    """
    response_output = {}

    # start timer
    t0 = time.time()

    # get model instance
    try:
        model, load_time = get_delay_prediction_model()
    except Exception as e:
        raise Exception(f"Model fetch failed. {e}")

    # predict
    try:
        # create new data input
        new_data = data_headers_dict.copy()

        # update numerical dict values
        new_data["DIA"] = flight_args["DIA"]
        new_data["MES"] = flight_args["MES"]
        new_data["temporada_alta"] = flight_args["temporada_alta"]

        # update categorical dict values
        cat_vars_names = [
            "DIANOM_" + str(flight_args["DIANOM"]),
            "TIPOVUELO_" + str(flight_args["TIPOVUELO"]),
            "OPERA_" + str(flight_args["OPERA"]),
            "SIGLAORI_" + str(flight_args["SIGLAORI"]),
            "SIGLADES_" + str(flight_args["SIGLADES"]),
            "periodo_dia_" + str(flight_args["periodo_dia"]),
        ]

        for name in cat_vars_names:
            if name in new_data:
                new_data[name] = 1

        # convert to one-hot encoded vector
        x = np.array(list(new_data.values())).reshape(1, -1)

        # make inference
        prediction = model.predict(x)

        # update response
        response_output["can_be_delayed"] = "yes" if prediction else "no"
    except Exception as e:
        raise Exception(f"Prediction failed. {e}")

    # end timer
    t1 = time.time()
    total_time = datetime.fromtimestamp(t1) - datetime.fromtimestamp(t0)
    total_time = f"{total_time.total_seconds():.3f} seconds"

    response_output["load_time"] = load_time
    response_output["compute_time"] = total_time

    return response_output, total_time


def get_delay_prediction_model():
    """Singleton to create a model instance

    Returns:
        Tuple[gxboost, timedelta]: model, compute time
    """
    global _delay_prediction_model

    if not _delay_prediction_model:
        t0 = time.time()
        with open(MODEL_PATH, "rb") as file:
            _delay_prediction_model = pickle.load(file)
        t1 = time.time()
        total_time = datetime.fromtimestamp(t1) - datetime.fromtimestamp(t0)
        total_time = f"{total_time.total_seconds():.3f} seconds"
    else:
        total_time = "Model was already loaded"

    return _delay_prediction_model, total_time
