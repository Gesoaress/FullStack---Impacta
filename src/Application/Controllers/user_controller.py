from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
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

    @staticmethod
    def activate_user():
        data = request.get_json()

        phone = data.get('phone')
        code = data.get('code')

        if not phone or not code:
            return make_response(jsonify({"erro": "Campos obrigatórios faltando"}), 400)

        try:
            user = UserService.activate_user(phone, code)
            return make_response(jsonify({
                "mensagem": "Mini mercado ativado com sucesso",
                "usuario": user.to_dict()
            }), 200)
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 400)
        except Exception as e:
            return make_response(jsonify({"erro": "Erro interno no servidor"}), 500)

    @staticmethod
    @jwt_required()
    def get_user(user_id):
        try:
            user = UserService.get_user(user_id)
            return make_response(jsonify({
                "usuario": user.to_dict()
            }), 200)
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 404)
        except Exception as e:
            return make_response(jsonify({"erro": "Erro interno no servidor"}), 500)

    @staticmethod
    @jwt_required()
    def update_user(user_id):
        # Garante que só o próprio seller pode editar seus dados
        current_user_id = get_jwt_identity()
        if str(user_id) != str(current_user_id):
            return make_response(jsonify({"erro": "Sem permissão para editar outro seller"}), 403)

        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        password = data.get('password')

        try:
            user = UserService.update_user(user_id, name, email, phone, password)
            return make_response(jsonify({
                "mensagem": "Seller atualizado com sucesso",
                "usuario": user.to_dict()
            }), 200)
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 400)
        except Exception as e:
            return make_response(jsonify({"erro": "Erro interno no servidor"}), 500)

    @staticmethod
    @jwt_required()
    def inactivate_user(user_id):
        # Garante que só o próprio seller pode se inativar
        current_user_id = get_jwt_identity()
        if str(user_id) != str(current_user_id):
            return make_response(jsonify({"erro": "Sem permissão para inativar outro seller"}), 403)

        try:
            user = UserService.inactivate_user(user_id)
            return make_response(jsonify({
                "mensagem": "Seller inativado com sucesso",
                "usuario": user.to_dict()
            }), 200)
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 400)
        except Exception as e:
            return make_response(jsonify({"erro": "Erro interno no servidor"}), 500)