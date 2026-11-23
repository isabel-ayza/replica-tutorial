import os
import certifi
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError

load_dotenv()

def conectar_base_de_datos():
    base_de_datos = None
    try:
        cliente = MongoClient(
            os.getenv("MONGO_URI"),
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=5000
        )
        cliente.admin.command("ping")
        base_de_datos = cliente["dbb_products_app"]
        print("Conexión exitosa a MongoDB")
    except PyMongoError as error:
        print("Error de conexión a MongoDB:", error)
    return base_de_datos