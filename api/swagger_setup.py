# Copyright (c) 2024 by Jonathan AW

#swagger_setup.py
from flask import send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint

def init_swagger_ui(app):
    """
    Initialize Swagger UI and serve OpenAPI documentation.
    """
    SWAGGER_URL = '/swagger'
    API_URL = '/openapi.yaml'  # URL to access the OpenAPI YAML file

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,  # Swagger UI endpoint
        API_URL,      # OpenAPI spec file path
        config={       # Swagger UI config overrides
            'app_name': "FundSage API Documentation"
        }
    )

    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    @app.route('/openapi.yaml', methods=['GET'])
    def serve_openapi_yaml():
        """
        Serve the OpenAPI specification YAML file.
        """
        return send_from_directory('../docs', 'openapi.yaml')

