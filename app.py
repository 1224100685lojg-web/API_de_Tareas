from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración BD
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tareas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo
class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)
    estado = db.Column(db.String(20), nullable=False)  # pendiente, en progreso, completada

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "estado": self.estado
        }

# Crear BD
with app.app_context():
    db.create_all()

# 🔹 CREATE (POST)
@app.route('/tareas', methods=['POST'])
def crear_tarea():
    data = request.get_json()

    if not data or not all(k in data for k in ("titulo", "descripcion", "estado")):
        return jsonify({"error": "Faltan datos"}), 400

    nueva_tarea = Tarea(
        titulo=data["titulo"],
        descripcion=data["descripcion"],
        estado=data["estado"]
    )

    db.session.add(nueva_tarea)
    db.session.commit()

    return jsonify({
        "mensaje": "Tarea creada",
        "tarea": nueva_tarea.to_dict()
    }), 201

# 🔹 READ (GET)
@app.route('/tareas', methods=['GET'])
def obtener_tareas():
    tareas = Tarea.query.all()
    return jsonify([t.to_dict() for t in tareas]), 200

# 🔹 UPDATE (PUT)
@app.route('/tareas/<int:id>', methods=['PUT'])
def actualizar_tarea(id):
    tarea = Tarea.query.get(id)

    if not tarea:
        return jsonify({"error": "Tarea no encontrada"}), 404

    data = request.get_json()

    tarea.titulo = data.get("titulo", tarea.titulo)
    tarea.descripcion = data.get("descripcion", tarea.descripcion)
    tarea.estado = data.get("estado", tarea.estado)

    db.session.commit()

    return jsonify({
        "mensaje": "Tarea actualizada",
        "tarea": tarea.to_dict()
    })

# 🔹 DELETE
@app.route('/tareas/<int:id>', methods=['DELETE'])
def eliminar_tarea(id):
    tarea = Tarea.query.get(id)

    if not tarea:
        return jsonify({"error": "Tarea no encontrada"}), 404

    db.session.delete(tarea)
    db.session.commit()

    return jsonify({"mensaje": "Tarea eliminada"})

if __name__ == '__main__':
    app.run(debug=True)