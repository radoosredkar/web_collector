from flask import request
from flask_graphql import GraphQLView
from flask_cors import CORS, cross_origin
from web_collector import schemas
import scrappy
from web_collector.scrapper import ParserBolha as bolha
from web_collector.scrapper import ParserNepremicnine as nepremicnine
from app import app

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from web_collector import log
from config import settings
from flask import jsonify
import flask
import web_collector.db_firestore as db_firestore
import json

# sentry_sdk.init(
#   dsn=settings.sentry.dsn,
#   integrations=[FlaskIntegration(), SqlalchemyIntegration()],
#   traces_sample_rate=1.0,
# )

cors = CORS(app)
# cors = CORS(app, resources={r"/*": {"origins": "*"}})
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
@cross_origin()
def root():
    return f"App is online ..."


@app.route("/homes/<string:record_id>", methods=["PATCH"])
@cross_origin()
def update(record_id):
    doc_ref = db_firestore.get_document_ref(settings.collections.homes, record_id)
    app.logger.info(doc_ref)
    if request.method == "PATCH":
        db_firestore.update_document(doc_ref, request.form)
        document = doc_ref.get()
        response = flask.jsonify(document.to_dict())
        app.logger.info(response)
        # response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    else:
        app.logger.error("Document {record_id} not found")
    app.logger.info(record_id)
    return f"{record_id} {request.get_data()} {request.method}"

@app.route('/latest_refresh')
def latest_refresh():
    return  flask.jsonify(db_firestore.get_latest_refresh(settings.collections.logs))

@app.route("/refresh", defaults={'client':'url'})
@app.route("/refresh/<client>")
@cross_origin()
def refresh(client):
    all_changed_items = scrappy.refresh(client)
    # return {"all_changed_item": scrappy.refresh()}
    app.logger.info(f"Refresh finished {all_changed_items}")
    return {"all_changed_items": all_changed_items}

@app.route("/archieve")
@cross_origin()
def archieve():
    all_changed_items = scrappy.archieve()
    app.logger.info(f"Refresh finished {all_changed_items}")
    return {"all_changed_items": all_changed_items}


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


@app.after_request
def add_headers(response):
    # response.headers.add("Access-Control-Allow-Origin", "*")
    return response
