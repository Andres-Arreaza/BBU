"""
Este módulo gestiona el inicio del servidor API, la carga de la base de datos y la adición de los endpoints.
"""
import os
from flask import Flask, request, jsonify, url_for, send_from_directory
from flask_migrate import Migrate
from flask_swagger import swagger
from api.utils import APIException, generate_sitemap
from api.models import db, SistemaOperativo, Servidor
from api.routes import api
from api.admin import setup_admin
from api.commands import setup_commands
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import datetime

# Configuración de entorno
ENV = "development" if os.getenv("FLASK_DEBUG") == "1" else "production"
static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../public/')
app = Flask(__name__)
app.url_map.strict_slashes = False

# Configuración de base de datos
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db, compare_type=True)
db.init_app(app)

# Configuración de JWT
app.config["JWT_SECRET_KEY"] = "super-secret"  # Cambia esto!
jwt = JWTManager(app)

# Habilitar CORS para todas las rutas
CORS(app, origins=["http://localhost:3000"], supports_credentials=True)

# Inicialización de componentes
setup_admin(app)
setup_commands(app)
app.register_blueprint(api, url_prefix='/api')

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, error.status_code

@app.route('/')
def sitemap():
    if ENV == "development":
        return generate_sitemap(app)
    return send_from_directory(static_file_dir, 'index.html')

@app.route('/<path:path>', methods=['GET'])
def serve_any_other_file(path):
    if not os.path.isfile(os.path.join(static_file_dir, path)):
        path = 'index.html'
    response = send_from_directory(static_file_dir, path)
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.cache_control.max_age = 0  # Evita la caché en memoria
    return response

# # 🔹 Ruta para obtener sistemas operativos
# @app.route('/api/sistemas_operativos', methods=['GET'])
# def get_sistemas_operativos():
#     try:
#         sistemas = SistemaOperativo.query.all()
#         response = jsonify([sistema.serialize() for sistema in sistemas])
#         response.headers.add("Access-Control-Allow-Origin", "*")
#         return response, 200
#     except Exception as e:
#         return jsonify({"error": f"Error obteniendo sistemas operativos: {str(e)}"}), 500

# # 🔹 Ruta para obtener todos los servidores
# @app.route('/api/servidores', methods=['GET'])
# def get_servidores():
#     try:
#         servidores = Servidor.query.all()
#         response = jsonify([servidor.serialize() for servidor in servidores])
#         response.headers.add("Access-Control-Allow-Origin", "*")
#         return response, 200
#     except Exception as e:
#         return jsonify({"error": f"Error obteniendo servidores: {str(e)}"}), 500

# # 🔹 Ruta para crear un nuevo servidor
# @app.route('/api/servidores', methods=['POST'])
# def create_servidor():
#     try:
#         data = request.get_json()

#         # 🔹 Validar que los datos necesarios están presentes
#         required_fields = [
#             "nombre", "tipo", "ip", "balanceador", "vlan", "descripcion",
#             "link", "servicio_id", "capa_id", "ambiente_id", "dominio_id",
#             "sistema_operativo_id", "estatus_id"
#         ]
#         for field in required_fields:
#             if field not in data or data[field] == "":
#                 return jsonify({"error": f"Campo '{field}' faltante o vacío"}), 400

#         nuevo_servidor = Servidor(**data)
#         db.session.add(nuevo_servidor)
#         db.session.commit()

#         response = jsonify(nuevo_servidor.serialize())
#         response.headers.add("Access-Control-Allow-Origin", "*")
#         return response, 201
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"error": f"Error al guardar servidor: {str(e)}"}), 500

# # 🔹 Ruta para actualizar un servidor
# @app.route("/api/servidores/<int:servidor_id>", methods=["PUT"])
# def update_servidor(servidor_id):
#     servidor = Servidor.query.get(servidor_id)
#     if not servidor:
#         return jsonify({"error": "Servidor no encontrado"}), 404

#     data = request.get_json()
#     campos_actualizables = [
#         "nombre", "tipo", "ip", "balanceador", "vlan", "descripcion", "link",
#         "servicio_id", "capa_id", "ambiente_id", "dominio_id", "sistema_operativo_id", "estatus_id"
#     ]
#     for key in campos_actualizables:
#         if key in data:
#             setattr(servidor, key, data[key])

#     servidor.fecha_modificacion = datetime.utcnow()
#     db.session.commit()

#     response = jsonify({"mensaje": "Servidor actualizado correctamente", "servidor": servidor.serialize()})
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response, 200

# # 🔹 Ruta para eliminar un servidor
# @app.route("/api/servidores/<int:servidor_id>", methods=["DELETE"])
# def delete_servidor(servidor_id):
#     servidor = Servidor.query.get(servidor_id)
#     if not servidor:
#         return jsonify({"error": "Servidor no encontrado"}), 404

#     db.session.delete(servidor)
#     db.session.commit()

#     response = jsonify({"mensaje": "Servidor eliminado correctamente"})
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response, 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=PORT, debug=True)