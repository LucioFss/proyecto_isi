#BLUEPRINT PARA LA VERFICACION DE EL ESTADO DE LA APLICACION

# Se importa la clase de blueprint para la creacion y gestion de blueprints, y jsonfy, para convertir datos de python
from flask import Blueprint, jsonify


health_bp = Blueprint('health',__name__)

@health_bp.route('/health')
def health_check():
    #Se retorna por ahora un
    return jsonify({
        "status" : "ok",
        "message" : "El servicio esta funcionando correctamente"
    }), 200
