from flightforesight_api import create_app

def main():
    """run script for flightforesight_api package."""
    # init app
    app = create_app()

    # run app
    app.run(port=app.config["PORT"])


if __name__ == "__main__":
    main()