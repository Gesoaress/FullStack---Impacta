from flask import request, jsonify, make_response
from flask_jwt_extended import create_access_token
from src.Infrastructure.Model.user import User

class AuthController:
    @staticmethod
    def login():
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return make_response(jsonify({"erro": "Campos obrigatórios faltando"}), 400)

        try:
            # Busca o seller pelo email
            user = User.query.filter_by(email=email).first()

            if not user:
                return make_response(jsonify({"erro": "E-mail ou senha inválidos"}), 401)

            if not user.check_password(password):
                return make_response(jsonify({"erro": "E-mail ou senha inválidos"}), 401)

            if user.status != "ACTIVE":
                return make_response(jsonify({"erro": "Seller inativo, ative sua conta primeiro"}), 403)

            # Gera o token JWT
            token = create_access_token(identity=str(user.id))

            return make_response(jsonify({
                "mensagem": "Login realizado com sucesso",
                "token": token,
                "usuario": user.to_dict()
            }), 200)

        except Exception as e:
            return make_response(jsonify({"erro": "Erro interno no servidor"}), 500)