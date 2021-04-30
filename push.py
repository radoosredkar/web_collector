import http.client, urllib
import sys
from flask import current_app as app
from config import settings


def push(message: str):
    app.logger.info("Push started")
    message = f"environment: {settings.env_type}\n" + message
    try:
        conn = http.client.HTTPSConnection(
            settings.url.push
        )
        conn.request(
            "GET", "/HomesPushover?" + urllib.parse.urlencode({"message": message}),
        )
        response = conn.getresponse()
        app.logger.info("Push result:%s %s", response.status, response.reason)
    except:
        e = sys.exc_info()[0]
        app.logger.info(e)
