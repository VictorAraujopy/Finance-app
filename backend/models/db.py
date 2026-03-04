import sqlite3

def init_db():
    conn = sqlite3.connect('financas.db')
    cursor = conn.cursor()

    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS gastos (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                valor       REAL,
                categoria   TEXT,
                descricao   TEXT,
                data        DATE,
                criado_em   DATETIME
            )
        ''')
    except Exception as e:
        print(f"Erro na tabela gastos: {e}")

    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categorias (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                nome        TEXT,
                cor         TEXT,
                icone       TEXT
            )
        ''')
    except Exception as e:
        print(f"Erro na tabela categorias: {e}")

    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS config (
                chave       TEXT PRIMARY KEY,
                valor       TEXT
            )
        ''')
    except Exception as e:
        print(f"Erro na tabela config: {e}")

    conn.commit()
    conn.close()
    print("Tabelas verificadas com sucesso")


init_db()