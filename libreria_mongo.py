from pymongo import MongoClient


def validaUsuario(usuario,password):
    permiso=False
    client = MongoClient("mongodb://localhost:27017/")
    db = client["comerciotech_db"]
    collection = db["usuarios"]
    
    data_usr = collection.find_one({"usuario": usuario, "password": password})
    
    if data_usr is not None:
        permiso=True
    
    client.close()
    return permiso

