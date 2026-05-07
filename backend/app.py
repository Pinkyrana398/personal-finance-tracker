from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    CORS(app, supports_credentials=True, origins="*")

    from routes.auth_routes import auth_bp
    from routes.transaction_routes import transaction_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(transaction_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)