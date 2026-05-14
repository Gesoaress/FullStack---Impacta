from flask import Flask
from flask_cors import CORS
from src.config.data_base import init_db
from src.routes import init_routes
import os

def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='/static')

    CORS(app)

    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB

    init_db(app)
    init_routes(app)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)