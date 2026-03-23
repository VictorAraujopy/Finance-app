from flask import Blueprint, request, jsonify
import sqlite3
gastos_bp = Blueprint('gastos', __name__)   

DB = "financas.db"


@gastos_bp.route('/api/gastos', methods=['POST'])
def adicionar_gasto():
    try:

        data = request.get_json()
        tipo = data.get('tipo')
        valor = data.get('valor')
        categoria = data.get('categoria')
        descricao = data.get('descricao')
        data_lancamento = data.get('data')

        if not tipo or not valor:
            return jsonify({'error': 'tipo e valor são obrigatórios'}), 400

        with sqlite3.connect(DB) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO lancamento (tipo, valor, categoria, descricao, data, criado_em)
                VALUES (?, ?, ?, ?, ?, datetime('now'))
            ''', (tipo, valor, categoria, descricao, data_lancamento))
            conn.commit()
            return jsonify({'message': 'Gasto adicionado com sucesso'}), 201
        
    except Exception as e:
        print(f"Erro ao adicionar gasto: {e}")  
    return jsonify({'error': str(e)}), 500


@gastos_bp.route('/api/gastos', methods=['GET'])
def listar_gastos():
    try:
        with sqlite3.connect(DB) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, tipo, valor, categoria, descricao, data FROM lancamento ORDER BY criado_em DESC')            
            gastos = cursor.fetchall()
        return jsonify({'gastos': gastos}), 200

    except Exception as e:
        print(f"Erro ao listar gastos: {e}")
        return jsonify({'error': str(e)}), 500

@gastos_bp.route('/api/gastos/<int:id>', methods=['PUT'])
def atualizar_gasto(id):
    try:
        data = request.get_json()
        tipo = data.get('tipo')
        valor = data.get('valor')
        categoria = data.get('categoria')
        descricao = data.get('descricao')
        data_lancamento = data.get('data')

        if not tipo or not valor:
            return jsonify({'error': 'tipo e valor são obrigatórios'}), 400

        with sqlite3.connect(DB) as conn:
            cursor = conn.cursor()
            cursor.execute('''
             UPDATE lancamento
                SET tipo=?, valor=?, categoria=?, descricao=?, data=?
                WHERE id=?
            ''', (tipo, valor, categoria, descricao, data_lancamento, id))
            conn.commit()
            return jsonify({'message': 'Gasto editado com sucesso'}), 200

    except Exception as e:
        print(f"Erro ao atualizar gasto: {e}")
        return jsonify({'error': str(e)}), 500

