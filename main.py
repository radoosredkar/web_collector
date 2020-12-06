from flask import Flask
from flask_graphql import GraphQLView
from schemas import schema
from flask_cors import CORS, cross_origin
import scrappy
import ParserBolha as bolha
import ParserNepremicnine as nepremicnine
import logging

import sentry_sdk

sentry_sdk.init(
    "https://007e055e5fe64e35b55b36140bf6b18d@o371271.ingest.sentry.io/5363923"
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
    return scrappy.refresh()


if __name__ == "__main__":
    logging.getLogger("flask_cors").level = logging.DEBUG
    logging.getLogger("flask").level = logging.DEBUG
    logging.info("test")

    app.run(debug=True, host="0.0.0.0")


@app.before_request
def log_request_info():
    print(1342)
    app.logger.debug("Headers: %s", request.headers)
    app.logger.debug("Body: %s", request.get_data())


@app.after_request
def add_headers(response):
    print(1342)
