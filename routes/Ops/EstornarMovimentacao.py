from flask import Blueprint, jsonify, request
from functools import wraps
from Service import Fase_OP_JohnField, estornarOP
EstornoOP_routesJohn = Blueprint('EstornarOPJohn', __name__) # Esse é o nome atribuido para o conjunto de rotas envolvendo usuario

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token == 'Easy445277888':  # Verifica se o token é igual ao token fixo
            return f(*args, **kwargs)
        return jsonify({'message': 'Acesso negado'}), 401

    return decorated_function



@EstornoOP_routesJohn.route('/api/JonhField/EstornarMovOP', methods=['POST'])
@token_required
def EstornarMovOP():
    data = request.get_json()
    idUsuario = data.get('idUsuario')
    codOP = data.get('codOP')
    codCliente = data.get('codCliente')


    consulta = estornarOP.EstornoOP(codOP, codCliente, idUsuario)
    # Obtém os nomes das colunas
    column_names = consulta.columns
    # Monta o dicionário com os cabeçalhos das colunas e os valores correspondentes
    consulta_data = []
    for index, row in consulta.iterrows():
        consulta_dict = {}
        for column_name in column_names:
            consulta_dict[column_name] = row[column_name]
        consulta_data.append(consulta_dict)
    return jsonify(consulta_data)



@EstornoOP_routesJohn.route('/api/JonhField/EstornoOPEncerrada', methods=['DELETE'])
@token_required
def delete_EstornoOPEncerrada():
    data = request.get_json()
    idUsuario = data.get('idUsuario')
    codOP = data.get('codOP')
    codCliente = data.get('codCliente')


    consulta = estornarOP.EstornoOPEncerrada(codOP, codCliente, idUsuario)
    # Obtém os nomes das colunas
    column_names = consulta.columns
    # Monta o dicionário com os cabeçalhos das colunas e os valores correspondentes
    consulta_data = []
    for index, row in consulta.iterrows():
        consulta_dict = {}
        for column_name in column_names:
            consulta_dict[column_name] = row[column_name]
        consulta_data.append(consulta_dict)
    return jsonify(consulta_data)