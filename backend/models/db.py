import sqlite3

def init_db():
    conn = sqlite3.connect('financas.db')
    cursor = conn.cursor()

    try:
        cursor.execute('DROP TABLE IF EXISTS lancamento')
        cursor.execute('''
            CREATE TABLE lancamento (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo        TEXT,
                valor       REAL,
                categoria   TEXT,
                descricao   TEXT,
                data        DATE,
                criado_em   DATETIME
            )
        ''')
    except Exception as e:
        print(f"Erro na tabela lancamento: {e}")

    try:
        cursor.execute('DROP TABLE IF EXISTS categorias')
        cursor.execute('''
                    CREATE TABLE categorias (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                nome        TEXT,
                cor         TEXT,
                icone       TEXT
            )
        ''')
    except Exception as e:
        print(f"Erro na tabela categorias: {e}")

    try:
        cursor.execute('DROP TABLE IF EXISTS config')
        cursor.execute('''
                    CREATE TABLE config (
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