from flask import Flask
from flask import request
from flask_graphql import GraphQLView
from flask_cors import CORS, cross_origin
from web_collector.schemas import schema
from web_collector import scrappy
from web_collector import ParserBolha as bolha
from web_collector import ParserNepremicnine as nepremicnine
import logging

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="https://c457a3b783ea4c2ca406263f30086806@o371271.ingest.sentry.io/5556585",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0,
)

app = Flask(__name__)
cors = CORS(app)
# cors = CORS(app, resources={r"/*": {"origins": "http://localhost:8080/"}})
app.logger.info(cors)
app.add_url_rule(
    "/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True)
)
app.add_url_rule(
    "/graphql/batch",
    view_func=GraphQLView.as_view("graphqlb", schema=schema, batch=True, method="POST"),
)


@app.route("/refresh")
def refresh():
    print(1 / 0)
    return scrappy.refresh()


if __name__ == "__main__":
    logging.getLogger("flask_cors").level = logging.DEBUG
    logging.getLogger("flask").level = logging.DEBUG
    logging.info("test")

    # app.run(debug=True, host="0.0.0.0")


# @app.before_request
def log_request_info():
    print(1342)
    if request:
        app.logger.debug("Headers: %s", request.headers)
        app.logger.debug("Body: %s", request.get_data())


# @app.after_request
def add_headers(response):
    print(1342)
