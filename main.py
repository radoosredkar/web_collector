import ipdb
from flask import Flask
from flask import request
from flask_graphql import GraphQLView
from flask_cors import CORS, cross_origin
from web_collector import schemas
import scrappy
from web_collector.scrapper import ParserBolha as bolha
from web_collector.scrapper import ParserNepremicnine as nepremicnine

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from web_collector import log
from config import settings

sentry_sdk.init(
    dsn=settings.sentry.dsn,
    integrations=[FlaskIntegration(), SqlalchemyIntegration()],
    traces_sample_rate=1.0,
)

app = Flask(__name__)
cors = CORS(app)
# cors = CORS(app, resources={r"/*": {"origins": "http://localhost:8080/"}})
app.logger.info(cors)
app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql", schema=schemas.schema, graphiql=True),
)
app.add_url_rule(
    "/graphql/batch",
    view_func=GraphQLView.as_view(
        "graphqlb", schema=schemas.schema, batch=True, method="POST"
    ),
)


@app.route("/")
def root():
    return f"App is online ..."

@app.route("/refresh")
def refresh():
    return scrappy.refresh()


if __name__ == "__main__":
    # app.logging.getLogger("flask_cors").level = app.logging.DEBUG
    # app.logging.getLogger("flask").level = app.logging.DEBUG
    # app.logging.info("test")

    app.run(debug=True, host="127.0.0.1", port=8080)


# @app.before_request
def log_request_info():
    if request:
        app.logger.debug("Headers: %s", request.headers)
        app.logger.debug("Body: %s", request.get_data())


# @app.after_request
def add_headers(response):
    pass
