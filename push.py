import http.client, urllib
import sys
from flask import current_app as app


def push(message: str):
    app.logger.info("Push started")
    try:
        conn = http.client.HTTPSConnection(
            "europe-west2-web-collector-deploy-303917.cloudfunctions.net"
        )
        conn.request(
            "GET", "/HomesPushover?" + urllib.parse.urlencode({"message": message}),
        )
        response = conn.getresponse()
        app.logger.info("Push result:%s %s",response.status, response.reason)
    except:
        e = sys.exc_info()[0]
        app.logger.info(e)
