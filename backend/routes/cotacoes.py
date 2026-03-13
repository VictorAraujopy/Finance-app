from flask import Blueprint, jsonify
from services import api_client

cotacoes_bp = Blueprint('cotacoes', __name__)

@cotacoes_bp.route('/api/cotacoes', methods=['GET'])
def get_cotacoes():

    cotacoes = api_client.buscar_cotacoes()
    return jsonify(cotacoes)



