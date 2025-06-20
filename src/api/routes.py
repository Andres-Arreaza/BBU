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

    # Validar que los datos no sean `None`
    if not data or "nombre" not in data or "version" not in data:
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    nuevo_sistema = SistemaOperativo(
        nombre=data["nombre"],
        version=data["version"].strip(),  # 🔹 Asegura que no sea None
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
    """Obtiene solo los servidores activos."""
    try:
        query = Servidor.query.filter_by(activo=True)  # 🔹 Solo servidores activos (`True`)
        servidores = query.all()
        return jsonify([servidor.serialize() for servidor in servidores]), 200
    except Exception as e:
        print("ERROR EN GET SERVIDORES:", e)
        return jsonify({"error": str(e)}), 500

@api.route("/servidores/<int:record_id>", methods=["GET"])
def get_servidor_by_id(record_id):
    """Obtiene un servidor por ID con datos completos."""
    return get_generic_by_id(Servidor, record_id)

@api.route("/servidores", methods=["POST"])
def create_servidor():
    """Crea un nuevo servidor con validación de datos y evita duplicados por nombre o IP."""
    try:
        data = request.get_json()
        print("DATOS RECIBIDOS:", data)  # 🔹 Verifica qué datos recibe el backend

        # 🔹 Validación de datos obligatorios
        required_fields = [
            "nombre", "tipo", "ip", "servicio_id", "capa_id", "ambiente_id", 
            "dominio_id", "sistema_operativo_id", "estatus_id"
        ]
        missing_fields = [field for field in required_fields if field not in data or not data[field]]

        if missing_fields:
            return jsonify({"error": f"Faltan datos obligatorios: {', '.join(missing_fields)}"}), 400

        # 🔹 Validación de duplicidad por nombre
        if Servidor.query.filter_by(nombre=data["nombre"]).first():
            return jsonify({"msg": "Ya existe un servidor con ese nombre"}), 400

        # 🔹 Validación de duplicidad por IP
        if Servidor.query.filter_by(ip=data["ip"]).first():
            return jsonify({"msg": "Ya existe un servidor con esa IP"}), 400

        # 🔹 Asegura que `estatus_id` nunca sea `None`
        data["estatus_id"] = data.get("estatus_id", 1)  # 🔹 Valor por defecto si falta

        # 🔹 Crear nuevo servidor
        nuevo_servidor = Servidor(
            nombre=data["nombre"],
            tipo=data["tipo"],
            ip=data["ip"],
            balanceador=data.get("balanceador", ""),
            vlan=data.get("vlan", ""),
            link=data.get("link", ""),
            descripcion=data.get("descripcion", ""),
            servicio_id=data["servicio_id"],
            capa_id=data["capa_id"],
            ambiente_id=data["ambiente_id"],
            dominio_id=data["dominio_id"],
            sistema_operativo_id=data["sistema_operativo_id"],
            estatus_id=data["estatus_id"],
            activo=True,  # 🔹 Se crea como activo (`True`)
            fecha_creacion=datetime.utcnow(),
            fecha_modificacion=datetime.utcnow()
        )

        # 🔹 Guardar en la base de datos
        db.session.add(nuevo_servidor)
        db.session.commit()

        response = jsonify(nuevo_servidor.serialize())
        response.headers.add("Access-Control-Allow-Origin", "*")  # 🔹 Evita bloqueo por CORS
        return response, 201

    except Exception as e:
        db.session.rollback()  # 🔹 Evita datos corruptos si ocurre un error
        print("ERROR AL GUARDAR SERVIDOR:", e)  # 🔹 Mensaje detallado en consola
        return jsonify({"error": f"Error interno: {str(e)}"}), 500

@api.route("/servidores/<int:record_id>", methods=["PUT"])
def update_servidor(record_id):
    """Actualiza un servidor por ID con validación de datos."""
    try:
        servidor = Servidor.query.get(record_id)
        if not servidor:
            return jsonify({"error": "Servidor no encontrado"}), 404

        data = request.get_json()
        def sanitize(value):
            return None if value in ["", None] else value

        servidor.nombre = sanitize(data.get("nombre"))
        servidor.tipo = sanitize(data.get("tipo"))
        servidor.ip = sanitize(data.get("ip"))
        servidor.balanceador = sanitize(data.get("balanceador"))
        servidor.vlan = sanitize(data.get("vlan"))
        servidor.link = sanitize(data.get("link"))
        servidor.descripcion = sanitize(data.get("descripcion"))
        servidor.servicio_id = sanitize(data.get("servicio_id"))
        servidor.capa_id = sanitize(data.get("capa_id"))
        servidor.ambiente_id = sanitize(data.get("ambiente_id"))
        servidor.dominio_id = sanitize(data.get("dominio_id"))
        servidor.sistema_operativo_id = sanitize(data.get("sistema_operativo_id"))
        servidor.estatus_id = sanitize(data.get("estatus_id"))  # <-- AGREGA ESTA LÍNEA
        servidor.activo = sanitize(data.get("activo"))

        servidor.fecha_modificacion = datetime.utcnow()
        db.session.commit()

        return jsonify(servidor.serialize()), 200
    except Exception as e:
        print("ERROR EN ACTUALIZACIÓN:", e)
        return jsonify({"error": str(e)}), 500

@api.route("/servidores/<int:record_id>", methods=["DELETE"])
def delete_servidor(record_id):
    """Marca un servidor como eliminado en lugar de borrarlo físicamente."""
    try:
        servidor = Servidor.query.get(record_id)
        if not servidor:
            return jsonify({"error": "Servidor no encontrado"}), 404

        servidor.activo = False  # 🔹 Marca el servidor como eliminado (`False`)
        db.session.commit()

        return jsonify({"message": "Servidor marcado como eliminado"}), 200
    except Exception as e:
        print("ERROR EN ELIMINACIÓN:", e)
        return jsonify({"error": str(e)}), 500

# Ruta de búsqueda filtrada para servidores
from api.models import TipoServidorEnum

@api.route("/servidores/busqueda", methods=["GET"])
def buscar_servidores():
    try:
        query = Servidor.query.filter_by(activo=True)

        # Filtros simples
        if request.args.get("nombre"):
            query = query.filter(Servidor.nombre.ilike(f"%{request.args['nombre']}%"))
        if request.args.get("tipo"):
            try:
                tipo_val = TipoServidorEnum[request.args["tipo"]]
                query = query.filter(Servidor.tipo == tipo_val)
            except KeyError:
                pass
        if request.args.get("ip"):
            query = query.filter(Servidor.ip.ilike(f"%{request.args['ip']}%"))
        if request.args.get("balanceador"):
            query = query.filter(Servidor.balanceador.ilike(f"%{request.args['balanceador']}%"))
        if request.args.get("vlan"):
            query = query.filter(Servidor.vlan.ilike(f"%{request.args['vlan']}%"))
        if request.args.get("link"):
            query = query.filter(Servidor.link.ilike(f"%{request.args['link']}%"))
        if request.args.get("descripcion"):
            query = query.filter(Servidor.descripcion.ilike(f"%{request.args['descripcion']}%"))

        # Filtros por relación (pueden venir varios valores)
        if request.args.getlist("servicios"):
            query = query.filter(Servidor.servicio_id.in_(request.args.getlist("servicios")))
        if request.args.getlist("capas"):
            query = query.filter(Servidor.capa_id.in_(request.args.getlist("capas")))
        if request.args.getlist("ambientes"):
            query = query.filter(Servidor.ambiente_id.in_(request.args.getlist("ambientes")))
        if request.args.getlist("dominios"):
            query = query.filter(Servidor.dominio_id.in_(request.args.getlist("dominios")))
        if request.args.getlist("sistemas_operativos"):
            query = query.filter(Servidor.sistema_operativo_id.in_(request.args.getlist("sistemas_operativos")))
        if request.args.getlist("estatus"):
            query = query.filter(Servidor.estatus_id.in_(request.args.getlist("estatus")))

        servidores = query.all()
        return jsonify([servidor.serialize() for servidor in servidores]), 200
    except Exception as e:
        print("ERROR EN BUSQUEDA:", e)
        return jsonify({"error": str(e)}), 500

@api.route("/servidores/validar_masivo", methods=["POST"])
def validar_masivo():
    """
    Recibe filas del CSV y devuelve la observación para cada una.
    """
    from api.models import Servicio, Capa, Ambiente, Dominio, SistemaOperativo, Estatus, Servidor, TipoServidorEnum
    data = request.get_json()
    filas = data.get("filas", [])
    if not filas or len(filas) < 2:
        return jsonify([])

    encabezado = filas[0]
    resultado = [encabezado + ["Observación"]]

    # Mapas para buscar por nombre
    servicios = {s.nombre.upper(): s.id for s in Servicio.query.filter_by(activo=True).all()}
    capas = {c.nombre.upper(): c.id for c in Capa.query.filter_by(activo=True).all()}
    ambientes = {a.nombre.upper(): a.id for a in Ambiente.query.filter_by(activo=True).all()}
    dominios = {d.nombre.upper(): d.id for d in Dominio.query.filter_by(activo=True).all()}
    sistemas = {s.nombre.upper(): s.id for s in SistemaOperativo.query.filter_by(activo=True).all()}
    estatuses = {e.nombre.upper(): e.id for e in Estatus.query.filter_by(activo=True).all()}

    for fila in filas[1:]:
        # Ajusta los índices según el orden de tu CSV
        nombre, tipo, ip, servicio, capa, ambiente, balanceador, vlan, dominio, so, estatus, descripcion, link = fila[:13]
        observacion = []

        # Validar nombre e IP duplicados
        if Servidor.query.filter_by(nombre=nombre).first():
            observacion.append("Nombre ya existe")
        if Servidor.query.filter_by(ip=ip).first():
            observacion.append("IP ya existe")

        # Validar existencia de campos relacionados
        if tipo.upper() not in ["FISICO", "FÍSICO", "VIRTUAL"]:
            observacion.append("Tipo no válido")
        if servicio.upper() not in servicios:
            observacion.append("Servicio no existe")
        if capa.upper() not in capas:
            observacion.append("Capa no existe")
        if ambiente.upper() not in ambientes:
            observacion.append("Ambiente no existe")
        if dominio.upper() not in dominios:
            observacion.append("Dominio no existe")
        if so.upper() not in sistemas:
            observacion.append("S.O. no existe")
        if estatus.upper() not in estatuses:
            observacion.append("Estatus no existe")

        if not observacion:
            observacion = ["Servidor listo para guardar"]

        resultado.append(fila + ["; ".join(observacion)])

    return jsonify(resultado)

@api.route("/servidores/carga_masiva", methods=["POST"])
def carga_masiva_servidores():
    """
    Recibe una lista de filas (incluyendo encabezado) y crea los servidores en la base de datos.
    Devuelve éxito o error.
    """
    from api.models import Servicio, Capa, Ambiente, Dominio, SistemaOperativo, Estatus, Servidor
    data = request.get_json()
    filas = data.get("filas", [])
    if not filas or len(filas) < 2:
        return jsonify({"error": "No hay datos para guardar"}), 400

    encabezado = filas[0]
    # Ajusta los índices según el orden de tu CSV
    # nombre, tipo, ip, servicio, capa, ambiente, balanceador, vlan, dominio, so, estatus, descripcion, link
    servidores_creados = []
    errores = []

    # Mapas para buscar por nombre
    servicios = {s.nombre.upper(): s.id for s in Servicio.query.filter_by(activo=True).all()}
    capas = {c.nombre.upper(): c.id for c in Capa.query.filter_by(activo=True).all()}
    ambientes = {a.nombre.upper(): a.id for a in Ambiente.query.filter_by(activo=True).all()}
    dominios = {d.nombre.upper(): d.id for d in Dominio.query.filter_by(activo=True).all()}
    sistemas = {s.nombre.upper(): s.id for s in SistemaOperativo.query.filter_by(activo=True).all()}
    estatuses = {e.nombre.upper(): e.id for e in Estatus.query.filter_by(activo=True).all()}

    for fila in filas[1:]:
        try:
            nombre, tipo, ip, servicio, capa, ambiente, balanceador, vlan, dominio, so, estatus, descripcion, link = fila[:13]
            # Validar duplicados en BD
            if Servidor.query.filter_by(nombre=nombre).first() or Servidor.query.filter_by(ip=ip).first():
                errores.append(f"Servidor duplicado: {nombre} / {ip}")
                continue
            # Validar relaciones
            servicio_id = servicios.get(servicio.upper())
            capa_id = capas.get(capa.upper())
            ambiente_id = ambientes.get(ambiente.upper())
            dominio_id = dominios.get(dominio.upper())
            so_id = sistemas.get(so.upper())
            estatus_id = estatuses.get(estatus.upper())
            if not all([servicio_id, capa_id, ambiente_id, dominio_id, so_id, estatus_id]):
                errores.append(f"Relaciones inválidas para: {nombre}")
                continue
            nuevo_servidor = Servidor(
                nombre=nombre,
                tipo=tipo,
                ip=ip,
                balanceador=balanceador,
                vlan=vlan,
                link=link,
                descripcion=descripcion,
                servicio_id=servicio_id,
                capa_id=capa_id,
                ambiente_id=ambiente_id,
                dominio_id=dominio_id,
                sistema_operativo_id=so_id,
                estatus_id=estatus_id,
                activo=True,
                fecha_creacion=datetime.utcnow(),
                fecha_modificacion=datetime.utcnow()
            )
            db.session.add(nuevo_servidor)
            servidores_creados.append(nombre)
        except Exception as e:
            errores.append(f"Error en {fila}: {str(e)}")
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al guardar en base de datos: {str(e)}"}), 500

    if errores:
        return jsonify({"msg": "Carga masiva finalizada con errores", "errores": errores, "creados": servidores_creados}), 207
    return jsonify({"msg": "Carga masiva exitosa", "creados": servidores_creados}), 201