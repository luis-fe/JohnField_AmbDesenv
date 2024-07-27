from flask import Blueprint, jsonify, request
from functools import wraps
from Service.OrdemProd import detalhamentoOP

DetalhamentoOPJohn = Blueprint('DetalhamentoOPJohn', __name__) # Esse é o nome atribuido para o conjunto de rotas envolvendo usuario

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token == 'Easy445277888':  # Verifica se o token é igual ao token fixo
            return f(*args, **kwargs)
        return jsonify({'message': 'Acesso negado'}), 401

    return decorated_function


@DetalhamentoOPJohn.route('/api/JonhField/DetalhaOPEncerrada', methods=['GET'])
@token_required
def getDetalhaOPEncerrada():

    codOP = request.args.get('codOP', '')
    codCliente = request.args.get('codCliente', '')


    consulta = detalhamentoOP.DetalharOPEncerrada(codOP, codCliente)
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