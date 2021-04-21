import http.client, urllib


def push(message:str):
    conn = http.client.HTTPSConnection(
        "europe-west2-web-collector-deploy-303917.cloudfunctions.net"
    )
    conn.request(
        "GET", "/HomesPushover?" + urllib.parse.urlencode({"message": message}),
    )
    response = conn.getresponse()

