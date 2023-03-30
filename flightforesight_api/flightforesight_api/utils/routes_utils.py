from flask_restx.reqparse import RequestParser


def add_flight_arguments(parser: RequestParser) -> RequestParser:
    """add flight arguments for the FlightForesight API endpoints.

    Args:
        parser (RequestParser): request argument parser

    Returns:
        parser (RequestParser): updated request argument parser
    """
    parser.add_argument(
        "DIA", type=int, help="Día que se tomara el vuelo.", required=True
    )

    parser.add_argument(
        "MES", type=int, help="Mes que se tomara el vuelo.", required=True
    )

    parser.add_argument(
        "temporada_alta",
        type=int,
        help="1 si es temporada alta, 0 si no.",
        required=True,
    )

    parser.add_argument(
        "DIANOM",
        type=str,
        help="Día de la semana de operacion del vuelo.",
        required=True,
    )

    parser.add_argument(
        "TIPOVUELO",
        type=str,
        help="Tipo de vuelo, I = internacional, N = Nacional.",
        required=True,
    )

    parser.add_argument(
        "OPERA", type=str, help="Nombre de aerolinea que opera", required=True
    )

    parser.add_argument(
        "SIGLAORI", type=str, help="Nombre ciudad de origen", required=True
    )

    parser.add_argument(
        "SIGLADES", type=str, help="Nombre ciudad de destino", required=True
    )

    parser.add_argument(
        "periodo_dia", type=str, help="mañana, tarde, noche", required=True
    )

    return parser
