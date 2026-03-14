from flask import Flask
from flask_cors import CORS
from routes.cotacoes import cotacoes_bp
from routes.gastos import gastos_bp
from models.db import init_db 
app = Flask(__name__)

CORS(app)

init_db()

app.register_blueprint(cotacoes_bp)
app.register_blueprint(gastos_bp)

if __name__ == '__main__':
    app.run(debug=True)
    

