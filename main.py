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
import web_collector.db_firestore as db_firestore
import json

#sentry_sdk.init(
#   dsn=settings.sentry.dsn,
#   integrations=[FlaskIntegration(), SqlalchemyIntegration()],
#   traces_sample_rate=1.0,
#)

cors = CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
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

@app.route("/homes/<string:record_id>", methods=['PATCH', 'GET'])
def comment(record_id):
    doc_ref = db_firestore.get_document_ref(settings.collections.homes, record_id)
    if request.method == "PATCH":
        data = request.get_data()
        db_firestore.update_document(doc_ref, json.loads(data)) 
        document = doc_ref.get()
        return document.to_dict()
    else:
        app.logger.error("Document {record_id} not found")
    app.logger.info(record_id)
    return f"{record_id} {request.get_data()} {request.method}"

@app.route("/refresh")
def refresh():
    all_changed_items = scrappy.refresh()
    #return {"all_changed_item": scrappy.refresh()}
    app.logger.info(f"Refresh finished {all_changed_items}")
    return {"all_changed_items":all_changed_items}


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
