import psycopg2
from sqlalchemy import create_engine

def conexao():
    db_name = "Reposicao"
    db_user = "postgres"
    db_password = "ssckCdSzGtlUyXkAylAqNVpaVJzKVRdh"
    db_host = "roundhouse.proxy.rlwy.net"
    portbanco = "21990"

    return psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host, port=portbanco)


def Funcao_Inserir (df_tags, tamanho,tabela, metodo):
    # Configurações de conexão ao banco de dados
    database = "railway"
    user = "postgres"
    password = "ssckCdSzGtlUyXkAylAqNVpaVJzKVRdh"
    host = "roundhouse.proxy.rlwy.net"
    port = "21990"

# Cria conexão ao banco de dados usando SQLAlchemy
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')

    # Inserir dados em lotes
    chunksize = tamanho
    for i in range(0, len(df_tags), chunksize):
        df_tags.iloc[i:i + chunksize].to_sql(tabela, engine, if_exists=metodo, index=False , schema='Reposicao')


def conexaoJohn():
    db_name = "railway"
    db_user = "postgres"
    db_password = "ssckCdSzGtlUyXkAylAqNVpaVJzKVRdh"
    db_host = "roundhouse.proxy.rlwy.net"
    portbanco = "21990"

    return psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host, port=portbanco)

def conexaoEngine():
    db_name = "railway"
    db_user = "postgres"
    db_password = "ssckCdSzGtlUyXkAylAqNVpaVJzKVRdh"
    db_host = "roundhouse.proxy.rlwy.net"
    portbanco = "21990"


    if not all([db_name, db_user, db_password, db_host]):
        raise ValueError("One or more environment variables are not set")

    connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{portbanco}/{db_name}"
    return create_engine(connection_string)