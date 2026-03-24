from src.Application.Controllers.user_controller import UserController
from src.Application.Controllers.auth_controller import AuthController
from flask import jsonify, make_response

def init_routes(app):
    @app.route('/api', methods=['GET'])
    def health():
        return make_response(jsonify({
            "mensagem": "API - OK; Docker - Up",
        }), 200)

    @app.route('/api/sellers', methods=['POST'])
    def register_user():
        return UserController.register_user()

    @app.route('/api/sellers/activate', methods=['POST'])
    def activate_user():
        return UserController.activate_user()

    @app.route('/api/auth/login', methods=['POST'])
    def login():
        return AuthController.login()