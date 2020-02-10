"""
This module contains all database interfacing methods for the MFlix
application. You will be working on this file for the majority of M220P.

Each method has a short description, and the methods you must implement have
docstrings with a short explanation of the task.

Look out for TODO markers for additional help. Good luck!
"""

from flask import current_app, g
from werkzeug.local import LocalProxy
import json
from pymongo import MongoClient, DESCENDING, ASCENDING


def get_db():
    """
    Configuration method to return db instance
    """
    db = getattr(g, "_database", None)
    CMM_DB_HOST = current_app.config["mongo_db_host"]
    CMM_DB_PORT = current_app.config["mongo_db_port"]
    CMM_DB_NAME = current_app.config["mongo_db_name"]
    CMM_DB_AUTH = current_app.config['mongo_db_auth']
    CMM_DB_USER = current_app.config['mongo_db_user']
    CMM_DB_PASSWORD = current_app.config['mongo_db_password']

    if db is None:
        current_app.logger.info(
            "these are the credentials  {0}, {1}, {2},{3},{4},{5}".format(CMM_DB_HOST, CMM_DB_PORT, CMM_DB_NAME,
                                                                          CMM_DB_AUTH, CMM_DB_USER, CMM_DB_PASSWORD))

        current_app.logger.info(
            "these are the credentials  {0}, {1}, {2},{3},{4},{5}".format(type(CMM_DB_HOST), type(CMM_DB_PORT), CMM_DB_NAME,
                                                                          CMM_DB_AUTH, CMM_DB_USER, CMM_DB_PASSWORD))

        current_app.logger.info(
            "these are the credentials  {0}, {1}, {2},{3},{4},{5}".format(type(CMM_DB_HOST), type(CMM_DB_PORT), CMM_DB_NAME,
                                                                          CMM_DB_AUTH, CMM_DB_USER, CMM_DB_PASSWORD))

        db = g._database = MongoClient(
            CMM_DB_HOST,
            int(CMM_DB_PORT),
            maxPoolSize=50,
            wtimeout=2500,
            # connectTimeoutMS=200,
        )
        # user authentication for mongodb
        auth = json.loads(CMM_DB_AUTH.lower())
        if auth:
            db.the_database.authenticate(CMM_DB_USER, CMM_DB_PASSWORD, source=CMM_DB_NAME)

    return db[CMM_DB_NAME]


# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)
