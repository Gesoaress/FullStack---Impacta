from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.Infrastructure.Model.user import User
from src.config.data_base import db
from werkzeug.security import generate_password_hash
import os

def admin_required(fn):
    from functools import wraps
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != "ADMIN":
            return make_response(jsonify({"erro": "Acesso negado"}), 403)
        return fn(*args, **kwargs)
    return wrapper

class AdminController:

    @staticmethod
    def register_admin():
        data = request.get_json()
        secret = data.get('secret')
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        if secret != os.getenv('ADMIN_SECRET'):
            return make_response(jsonify({"erro": "Chave secreta inválida"}), 403)

        if not name or not email or not password:
            return make_response(jsonify({"erro": "Campos obrigatórios faltando"}), 400)

        if User.query.filter_by(email=email).first():
            return make_response(jsonify({"erro": "E-mail já cadastrado"}), 409)

        admin = User(
            name=name,
            cnpj="00.000.000/0000-00",
            email=email,
            phone="",
            status="ACTIVE",
            role="ADMIN"
        )
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()

        return make_response(jsonify({
            "mensagem": "Admin cadastrado com sucesso",
            "admin": admin.to_dict()
        }), 201)

    @staticmethod
    @admin_required
    def list_sellers():
        sellers = User.query.filter_by(role="SELLER").all()
        return make_response(jsonify({
            "mercados": [s.to_dict() for s in sellers]
        }), 200)

    @staticmethod
    @admin_required
    def delete_seller(seller_id):
        seller = User.query.filter_by(id=seller_id, role="SELLER").first()
        if not seller:
            return make_response(jsonify({"erro": "Mercado não encontrado"}), 404)
        db.session.delete(seller)
        db.session.commit()
        return make_response(jsonify({"mensagem": "Mercado deletado com sucesso"}), 200)

    @staticmethod
    @admin_required
    def toggle_seller(seller_id):
        seller = User.query.filter_by(id=seller_id, role="SELLER").first()
        if not seller:
            return make_response(jsonify({"erro": "Mercado não encontrado"}), 404)
        seller.status = "INACTIVE" if seller.status == "ACTIVE" else "ACTIVE"
        db.session.commit()
        return make_response(jsonify({
            "mensagem": f"Mercado {'ativado' if seller.status == 'ACTIVE' else 'desativado'} com sucesso",
            "mercado": seller.to_dict()
        }), 200)
