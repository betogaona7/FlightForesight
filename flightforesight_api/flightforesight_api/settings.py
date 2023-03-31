class Config(object):
    """default configurations"""

    ENV: str = "development"
    DEBUG: bool = False
    TESTING: bool = False
    PORT: int = 8081
    MAX_RETRIES: int = 5
    SWAGGER_DOC_URL: str = "/ff_docs/"
    SWAGGER_DOC_NAME: str = "ff_swagger.json"
    ENDPOINTS: str = ["/foresight/v1"]
