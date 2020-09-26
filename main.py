from flask import Flask
from flask_graphql import GraphQLView
from schemas import schema
from flask_cors import CORS
import scrappy

# import sentry_sdk
# sentry_sdk.init("https://007e055e5fe64e35b55b36140bf6b18d@o371271.ingest.sentry.io/5363923")

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.add_url_rule(
    "/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True)
)
app.add_url_rule(
    "/graphql/batch",
    view_func=GraphQLView.as_view("graphqlb", schema=schema, batch=True, method="POST"),
)

@app.route("/refresh")
def refresh():
    scrappy.scrapp()
    scrappy.scrappNepremicnine()
    scrappy.sesson.commit()
    return f"{str(scrappy.all_changed_items)}"

if __name__ == "__main__":
    app.run(debug=True)


@app.before_request
def log_request_info():
    app.logger.debug("Headers: %s", request.headers)
    app.logger.debug("Body: %s", request.get_data())
