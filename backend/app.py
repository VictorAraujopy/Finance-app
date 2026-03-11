from flask import Flask
from flask_cors import CORS
from routes.cotacoes import cotacoes_bp

app = Flask(__name__)

CORS(app)
app.register_blueprint(cotacoes_bp)

if __name__ == '__main__':
    app.run(debug=True)
    