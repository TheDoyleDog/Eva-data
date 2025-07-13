from pymongo import MongoClient


def validaUsuario(usuario,password):
    permiso=False
    # Dirección y puerto del servidor MongoDB
    client = MongoClient('mongodb://localhost:27017/')

    # Nombre de la base de datos
    db = client['mi_bd_ejemplo']

    # Nombre de la colección
    collection = db['usuarios']

    # Ejemplo de inserción de un documento
    #nuevo_documento = {"nombre": "Ejemplo", "valor": 123}
    #collection.insert_one(nuevo_documento)

    # Ejemplo de búsqueda de un documento
    data_usr = collection.find_one({"usuario": usuario,'password':password})
    print(data_usr)

    if not data_usr is None:
        permiso=True
    # Cerrar la conexión (opcional, se cierra automáticamente al salir del contexto)
    client.close()

    return permiso