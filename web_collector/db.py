from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
import sqlalchemy
import os
from config import settings
import MySQLdb
from google.cloud import secretmanager

basedir = os.path.abspath(os.path.dirname(__file__))
file_path = os.path.abspath(basedir + f"/{settings.db.path}/{settings.db.name}")
# engine = create_engine("sqlite:///" + file_path, echo=False)
# engine = create_engine(settings.db.url)
db_socket_dir = os.environ.get("DB_SOCKET_DIR", "/cloudsql")
cloud_sql_connection_name = "web-collector-deploy-303917:europe-west1:db"

#Read from secret POC
if os.environ.get("DEVELOPMENT"):
    engine = create_engine(settings.db.url)
else:
    client = secretmanager.SecretManagerServiceClient()
    secret_name = "web-collector-db_password"
    project_id = "web-collector-deploy-303917"
    request = {"name": f"projects/533861754708/secrets/web-collector-db_password/versions/1"}
    response = client.access_secret_version(request)
    db_password = response.payload.data.decode("UTF-8")

    engine = create_engine(
        # Equivalent URL:
        # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=<socket_path>/<cloud_sql_instance_name>
        sqlalchemy.engine.url.URL(
            drivername="mysql+pymysql",
            username=settings.db.user,  # e.g. "my-database-user"
            password=db_password,  # e.g. "my-database-password"
            database="web_collector",  # e.g. "my-database-name"
            query={
                "unix_socket": "{}/{}".format(
                    db_socket_dir, cloud_sql_connection_name  # e.g. "/cloudsql"
                )  # i.e "<PROJECT-NAME>:<INSTANCE-REGION>:<INSTANCE-NAME>"
            },
        ),
    )


Sesson = scoped_session(sessionmaker(bind=engine))
