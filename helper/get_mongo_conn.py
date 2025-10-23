import configparser
import os
import pymongo

def create_parser(config_path):
    parser = configparser.ConfigParser()
    if not os.path.exists(config_path):
        raise FileNotFoundError("Config file doesn't exists!")
    parser.read(config_path)
    return parser

def get_mongo_credentials(parser, config_name):
    conn_string = parser.get(config_name,"mongodb_connection")
    return conn_string

def mongo_connect(conn_string, database, table):
    client = pymongo.MongoClient(conn_string)
    mongo_db = client[database]
    collection = mongo_db[table]
    print(f"Connection to {database} successfully made!")
    return client,collection