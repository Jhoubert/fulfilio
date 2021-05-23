import os

import yaml
cfg = yaml.safe_load(open("config.yml"))

user = cfg.get("db").get("user") if "DB_USER" not in os.environ else os.environ.get("DB_USER")
password = cfg.get("db").get("password") if "DB_PASSWORD" not in os.environ else os.environ.get("DB_PASSWORD")
host = cfg.get("db").get("host") if "DB_HOST" not in os.environ else os.environ.get("DB_HOST")
port = cfg.get("db").get("port") if "DB_PORT" not in os.environ else os.environ.get("DB_PORT")
dbname = cfg.get("db").get("name") if "DB_NAME" not in os.environ else os.environ.get("DB_NAME")

database_string = 'postgresql://%s:%s@%s:%s/%s' % (user, password, host, port, dbname)

