from flask import Flask, request, jsonify, Blueprint
from api.models import db, Servicio, Capa, Ambiente, Dominio, SistemaOperativo, Estatus, Servidor
from flask_cors import CORS
from flask_cors import cross_origin
from datetime import datetime

api = Blueprint('api', __name__)
CORS(api)

### **Funciones auxiliares**
def update_record(record, data):
    """ Actualiza los campos de un registro y su fecha de modificación """
    for key, value in data.items():
        if hasattr(record, key):
            setattr(record, key, value)
    record.fecha_modificacion = datetime.utcnow()
    db.session.commit()
    return record.serialize()

def delete_record(record):
    """ Borrado lógico de un registro """
    if not record:
        return jsonify({"msg": f"{record.__class__.__name__} no encontrado"}), 404
    if not record.activo:
        return jsonify({"msg": f"{record.__class__.__name__} ya está eliminado"}), 400

    record.activo = False
    record.fecha_modificacion = datetime.utcnow()
    db.session.commit()
    return jsonify({"msg": f"{record.__class__.__name__} eliminado correctamente", "fecha_modificacion": record.fecha_modificacion.isoformat()}), 200

def create_generic(model):
    """ Crear un nuevo registro, reutilizando nombres eliminados """
    data = request.get_json()
    registro_existente = model.query.filter_by(nombre=data['nombre']).first()
    if registro_existente and not registro_existente.activo:
        registro_existente.activo = True
        registro_existente.descripcion = data.get('descripcion', registro_existente.descripcion)
        registro_existente.fecha_modificacion = datetime.utcnow()
        db.session.commit()
        return jsonify(registro_existente.serialize()), 200
    nuevo_registro = model(
        nombre=data['nombre'],
        descripcion=data.get('descripcion'),
        activo=True,
        fecha_creacion=datetime.utcnow()
    )
    db.session.add(nuevo_registro)
    db.session.commit()
    return jsonify(nuevo_registro.serialize()), 201

def update_generic(model, record_id):
    """ Actualizar un registro existente """
    record = model.query.get(record_id)
    if not record:
        return jsonify({"msg": f"{model.__name__} con ID {record_id} no encontrado"}), 404
    if not record.activo:
        return jsonify({"msg": f"{model.__name__} con ID {record_id} está inactivo y no puede ser actualizado"}), 400

    return jsonify(update_record(record, request.get_json())), 200

def get_generic(model):
    """ Obtener todos los registros, con opción de incluir inactivos """
    incluir_inactivos = request.args.get('incluir_inactivos', 'false').lower() == 'true'
    records = model.query.all() if incluir_inactivos else model.query.filter_by(activo=True).all()
    return jsonify([record.serialize() for record in records]), 200

def get_generic_by_id(model, record_id):
    """ Obtener un registro por su ID """
    record = model.query.get(record_id)
    if not record:
        return jsonify({"msg": f"{model.__name__} con ID {record_id} no encontrado"}), 404
    return jsonify(record.serialize()), 200

def delete_generic(model, record_id):
    """ Borrado lógico de un registro """
    record = model.query.get(record_id)
    return delete_record(record)
# --- Rutas CRUD genéricas para cada modelo ---
@api.route("/servicios", methods=["GET"])
def get_servicios():
    return get_generic(Servicio)

@api.route("/servicios/<int:record_id>", methods=["GET"])
def get_servicio_by_id(record_id):
    return get_generic_by_id(Servicio, record_id)

@api.route("/servicios", methods=["POST"])
def create_servicio():
    return create_generic(Servicio)

@api.route("/servicios/<int:record_id>", methods=["PUT"])
def update_servicio(record_id):
    return update_generic(Servicio, record_id)

@api.route("/servicios/<int:record_id>", methods=["DELETE"])
def delete_servicio(record_id):
    return delete_generic(Servicio, record_id)

# Repite lo mismo para Capa, Ambiente, Dominio, SistemaOperativo, Estatus, Servidor...
# Ejemplo para Capa:
@api.route("/capas", methods=["GET"])
def get_capas():
    return get_generic(Capa)

@api.route("/capas/<int:record_id>", methods=["GET"])
def get_capa_by_id(record_id):
    return get_generic_by_id(Capa, record_id)

@api.route("/capas", methods=["POST"])
def create_capa():
    return create_generic(Capa)

@api.route("/capas/<int:record_id>", methods=["PUT"])
def update_capa(record_id):
    return update_generic(Capa, record_id)

@api.route("/capas/<int:record_id>", methods=["DELETE"])
def delete_capa(record_id):
    return delete_generic(Capa, record_id)

# ...continúa igual para Ambiente, Dominio, SistemaOperativo, Estatus, Servidor

# Ejemplo para Ambiente:
@api.route("/ambientes", methods=["GET"])
def get_ambientes():
    return get_generic(Ambiente)

@api.route("/ambientes/<int:record_id>", methods=["GET"])
def get_ambiente_by_id(record_id):
    return get_generic_by_id(Ambiente, record_id)

@api.route("/ambientes", methods=["POST"])
def create_ambiente():
    return create_generic(Ambiente)

@api.route("/ambientes/<int:record_id>", methods=["PUT"])
def update_ambiente(record_id):
    return update_generic(Ambiente, record_id)

@api.route("/ambientes/<int:record_id>", methods=["DELETE"])
def delete_ambiente(record_id):
    return delete_generic(Ambiente, record_id)

# Ejemplo para Dominio:
@api.route("/dominios", methods=["GET"])
def get_dominios():
    return get_generic(Dominio)

@api.route("/dominios/<int:record_id>", methods=["GET"])
def get_dominio_by_id(record_id):
    return get_generic_by_id(Dominio, record_id)

@api.route("/dominios", methods=["POST"])
def create_dominio():
    return create_generic(Dominio)

@api.route("/dominios/<int:record_id>", methods=["PUT"])
def update_dominio(record_id):
    return update_generic(Dominio, record_id)

@api.route("/dominios/<int:record_id>", methods=["DELETE"])
def delete_dominio(record_id):
    return delete_generic(Dominio, record_id)

# Ejemplo para SistemaOperativo:
@api.route("/sistemas_operativos", methods=["GET"])
def get_sistemas_operativos():
    return get_generic(SistemaOperativo)

@api.route("/sistemas_operativos/<int:record_id>", methods=["GET"])
def get_sistema_operativo_by_id(record_id):
    return get_generic_by_id(SistemaOperativo, record_id)

@api.route("/sistemas_operativos", methods=["POST"])
def create_sistema_operativo():
    data = request.get_json()

    if not data or "nombre" not in data or "version" not in data:
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    nuevo_sistema = SistemaOperativo(
        nombre=data["nombre"],
        version=data["version"].strip(),
        descripcion=data.get("descripcion", "")
    )

    db.session.add(nuevo_sistema)
    db.session.commit()

    return jsonify(nuevo_sistema.serialize()), 201

@api.route("/sistemas_operativos/<int:record_id>", methods=["PUT"])
def update_sistema_operativo(record_id):
    return update_generic(SistemaOperativo, record_id)

@api.route("/sistemas_operativos/<int:record_id>", methods=["DELETE"])
def delete_sistema_operativo(record_id):
    return delete_generic(SistemaOperativo, record_id)

# Ejemplo para Estatus:
@api.route("/estatus", methods=["GET"])
def get_estatus():
    return get_generic(Estatus)

@api.route("/estatus/<int:record_id>", methods=["GET"])
def get_estatus_by_id(record_id):
    return get_generic_by_id(Estatus, record_id)

@api.route("/estatus", methods=["POST"])
def create_estatus():
    return create_generic(Estatus)

@api.route("/estatus/<int:record_id>", methods=["PUT"])
def update_estatus(record_id):
    return update_generic(Estatus, record_id)

@api.route("/estatus/<int:record_id>", methods=["DELETE"])
def delete_estatus(record_id):
    return delete_generic(Estatus, record_id)

# Ejemplo para Servidor:
@api.route("/servidores", methods=["GET"])
def get_servidores():
    try:
        query = Servidor.query.filter_by(activo=True)
        servidores = query.all()
        return jsonify([servidor.serialize() for servidor in servidores]), 200
    except Exception as e:
        print("ERROR EN GET SERVIDORES:", e)
        return jsonify({"error": str(e)}), 500

@api.route("/servidores/<int:record_id>", methods=["GET"])
def get_servidor_by_id(record_id):
    return get_generic_by_id(Servidor, record_id)

@api.route("/servidores", methods=["POST"])
def create_servidor():
    try:
        data = request.get_json()
        print("DATOS RECIBIDOS:", data)

        required_fields = [
            "nombre", "tipo", "ip", "servicio_id", "capa_id", "ambiente_id", 
            "dominio_id", "sistema_operativo_id", "estatus_id"
        ]
        missing_fields = [field for field in required_fields if field not in data or not data[field]]

        if missing_fields:
            return jsonify({"error": f"Faltan datos obligatorios: {', '.join(missing_fields)}"}), 400

        if Servidor.query.filter_by(nombre=data["nombre"]).first():
            return jsonify({"msg": "Ya existe un servidor con ese nombre"}), 400

        if Servidor.query.filter_by(ip=data["ip"]).first():
            return jsonify({"msg": "Ya existe un servidor con esa IP"}), 400

        data["estatus_id"] = data.get("estatus_id", 1)

        nuevo_servidor = Servidor(
            nombre=data["nombre"], tipo=data["tipo"], ip=data["ip"],
            balanceador=data.get("balanceador", ""), vlan=data.get("vlan", ""),
            link=data.get("link", ""), descripcion=data.get("descripcion", ""),
            servicio_id=data["servicio_id"], capa_id=data["capa_id"],
            ambiente_id=data["ambiente_id"], dominio_id=data["dominio_id"],
            sistema_operativo_id=data["sistema_operativo_id"], estatus_id=data["estatus_id"],
            activo=True, fecha_creacion=datetime.utcnow(), fecha_modificacion=datetime.utcnow()
        )

        db.session.add(nuevo_servidor)
        db.session.commit()

        response = jsonify(nuevo_servidor.serialize())
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 201

    except Exception as e:
        db.session.rollback()
        print("ERROR AL GUARDAR SERVIDOR:", e)
        return jsonify({"error": f"Error interno: {str(e)}"}), 500

@api.route("/servidores/<int:record_id>", methods=["PUT"])
def update_servidor(record_id):
    try:
        servidor = Servidor.query.get(record_id)
        if not servidor:
            return jsonify({"error": "Servidor no encontrado"}), 404

        data = request.get_json()
        
        for key, value in data.items():
            if hasattr(servidor, key):
                setattr(servidor, key, value)

        servidor.fecha_modificacion = datetime.utcnow()
        db.session.commit()

        return jsonify(servidor.serialize()), 200
    except Exception as e:
        print("ERROR EN ACTUALIZACIÓN:", e)
        return jsonify({"error": str(e)}), 500

@api.route("/servidores/<int:record_id>", methods=["DELETE"])
def delete_servidor(record_id):
    try:
        servidor = Servidor.query.get(record_id)
        if not servidor:
            return jsonify({"error": "Servidor no encontrado"}), 404

        servidor.activo = False
        db.session.commit()

        return jsonify({"message": "Servidor marcado como eliminado"}), 200
    except Exception as e:
        print("ERROR EN ELIMINACIÓN:", e)
        return jsonify({"error": str(e)}), 500

from api.models import TipoServidorEnum

@api.route("/servidores/busqueda", methods=["GET"])
def buscar_servidores():
    try:
        query = Servidor.query.filter_by(activo=True)

        if request.args.get("nombre"): query = query.filter(Servidor.nombre.ilike(f"%{request.args['nombre']}%"))
        if request.args.get("tipo"):
            try:
                tipo_val = TipoServidorEnum[request.args["tipo"]]
                query = query.filter(Servidor.tipo == tipo_val)
            except KeyError: pass
        if request.args.get("ip"): query = query.filter(Servidor.ip.ilike(f"%{request.args['ip']}%"))
        if request.args.get("balanceador"): query = query.filter(Servidor.balanceador.ilike(f"%{request.args['balanceador']}%"))
        if request.args.get("vlan"): query = query.filter(Servidor.vlan.ilike(f"%{request.args['vlan']}%"))
        if request.args.get("link"): query = query.filter(Servidor.link.ilike(f"%{request.args['link']}%"))
        if request.args.get("descripcion"): query = query.filter(Servidor.descripcion.ilike(f"%{request.args['descripcion']}%"))
        
        if request.args.getlist("servicios"): query = query.filter(Servidor.servicio_id.in_(request.args.getlist("servicios")))
        if request.args.getlist("capas"): query = query.filter(Servidor.capa_id.in_(request.args.getlist("capas")))
        if request.args.getlist("ambientes"): query = query.filter(Servidor.ambiente_id.in_(request.args.getlist("ambientes")))
        if request.args.getlist("dominios"): query = query.filter(Servidor.dominio_id.in_(request.args.getlist("dominios")))
        if request.args.getlist("sistemas_operativos"): query = query.filter(Servidor.sistema_operativo_id.in_(request.args.getlist("sistemas_operativos")))
        if request.args.getlist("estatus"): query = query.filter(Servidor.estatus_id.in_(request.args.getlist("estatus")))

        servidores = query.all()
        return jsonify([servidor.serialize() for servidor in servidores]), 200
    except Exception as e:
        print("ERROR EN BUSQUEDA:", e)
        return jsonify({"error": str(e)}), 500

# --- NUEVA RUTA DE VALIDACIÓN ---
@api.route("/servidores/validar-actualizaciones", methods=["POST"])
def validar_actualizaciones():
    data = request.get_json()
    if not data or "validaciones" not in data:
        return jsonify({"error": "Petición inválida"}), 400

    validaciones = data["validaciones"]
    errores_detalle = []

    for v in validaciones:
        servidor_id = v.get("id")
        
        # Validar Nombre si se está cambiando
        if v.get("nombre"):
            conflicto_nombre = Servidor.query.filter(
                Servidor.nombre == v["nombre"],
                Servidor.id != servidor_id
            ).first()
            if conflicto_nombre:
                errores_detalle.append(f"El nombre '{v['nombre']}' ya está en uso.")

        # Validar IP si se está cambiando
        if v.get("ip"):
            conflicto_ip = Servidor.query.filter(
                Servidor.ip == v["ip"],
                Servidor.id != servidor_id
            ).first()
            if conflicto_ip:
                errores_detalle.append(f"La IP '{v['ip']}' ya está en uso.")

        # Validar Link si se está cambiando
        if v.get("link"):
            conflicto_link = Servidor.query.filter(
                Servidor.link == v["link"],
                Servidor.id != servidor_id
            ).first()
            if conflicto_link:
                errores_detalle.append(f"El Link '{v['link']}' ya está en uso.")

    if errores_detalle:
        return jsonify({"detalles": errores_detalle}), 400

    return jsonify({"msg": "Validación exitosa"}), 200

