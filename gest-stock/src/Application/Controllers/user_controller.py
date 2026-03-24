from flask import request, jsonify, make_response
from src.Application.Service.user_service import UserService
 
class UserController:
    @staticmethod
    def register_user():
        data = request.get_json()
 
        name = data.get('name')
        cnpj = data.get('cnpj')
        email = data.get('email')
        phone = data.get('phone')
        password = data.get('password')
 
        if not name or not cnpj or not email or not phone or not password:
            return make_response(jsonify({"erro": "Campos obrigatórios faltando"}), 400)
 
        try:
            user = UserService.create_user(name, cnpj, email, phone, password)
            return make_response(jsonify({
                "mensagem": "Mini mercado cadastrado com sucesso",
                "usuario": user.to_dict()
            }), 201)
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 409)
        except Exception as e:
            return make_response(jsonify({"erro": "Erro interno no servidor"}), 500)