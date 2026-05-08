from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.Application.Service.product_service import ProductService

class ProductController:

    @staticmethod
    @jwt_required()
    def create_product():
        seller_id = get_jwt_identity()
        data = request.get_json()

        name = data.get('nome') or data.get('name')
        price = data.get('preco') if data.get('preco') is not None else data.get('price')
        quantity = data.get('quantidade') if data.get('quantidade') is not None else data.get('quantity')
        image = data.get('img') or data.get('image')
        status_raw = data.get('status', 'Ativo')
        status = 'ACTIVE' if status_raw == 'Ativo' else 'INACTIVE'
        categoria = data.get('categoria', 'Outros')

        if not name or price is None or quantity is None:
            return make_response(jsonify({"erro": "Campos obrigatórios faltando"}), 400)

        try:
            product = ProductService.create_product(seller_id, name, price, quantity, image, status, categoria)
            return make_response(jsonify({
                "mensagem": "Produto cadastrado com sucesso",
                "produto": product.to_dict()
            }), 201)
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 409)
        except Exception as e:
            return make_response(jsonify({"erro": "Erro interno no servidor"}), 500)

    @staticmethod
    @jwt_required()
    def list_products():
        seller_id = get_jwt_identity()

        try:
            products = ProductService.list_products(seller_id)
            return make_response(jsonify({
                "produtos": [p.to_dict() for p in products]
            }), 200)
        except Exception as e:
            return make_response(jsonify({"erro": "Erro interno no servidor"}), 500)

    @staticmethod
    @jwt_required()
    def get_product(product_id):
        seller_id = get_jwt_identity()

        try:
            product = ProductService.get_product(seller_id, product_id)
            return make_response(jsonify({
                "produto": product.to_dict()
            }), 200)
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 404)
        except Exception as e:
            return make_response(jsonify({"erro": "Erro interno no servidor"}), 500)

    @staticmethod
    @jwt_required()
    def update_product(product_id):
        seller_id = get_jwt_identity()
        data = request.get_json()

        name = data.get('nome') or data.get('name')
        price = data.get('preco') if data.get('preco') is not None else data.get('price')
        quantity = data.get('quantidade') if data.get('quantidade') is not None else data.get('quantity')
        image = data.get('img') or data.get('image')
        status_raw = data.get('status')
        status = ('ACTIVE' if status_raw == 'Ativo' else 'INACTIVE') if status_raw else None
        categoria = data.get('categoria')

        try:
            product = ProductService.update_product(seller_id, product_id, name, price, quantity, image, status, categoria)
            return make_response(jsonify({
                "mensagem": "Produto atualizado com sucesso",
                "produto": product.to_dict()
            }), 200)
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 400)
        except Exception as e:
            return make_response(jsonify({"erro": "Erro interno no servidor"}), 500)

    @staticmethod
    @jwt_required()
    def inactivate_product(product_id):
        seller_id = get_jwt_identity()

        try:
            product = ProductService.inactivate_product(seller_id, product_id)
            return make_response(jsonify({
                "mensagem": "Produto inativado com sucesso",
                "produto": product.to_dict()
            }), 200)
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 400)
        except Exception as e:
            return make_response(jsonify({"erro": "Erro interno no servidor"}), 500)

    @staticmethod
    @jwt_required()
    def activate_product(product_id):
        seller_id = get_jwt_identity()

        try:
            product = ProductService.activate_product(seller_id, product_id)
            return make_response(jsonify({
                "mensagem": "Produto ativado com sucesso",
                "produto": product.to_dict()
            }), 200)
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 400)
        except Exception as e:
            return make_response(jsonify({"erro": "Erro interno no servidor"}), 500)

    @staticmethod
    @jwt_required()
    def delete_product(product_id):
        seller_id = get_jwt_identity()

        try:
            ProductService.delete_product(seller_id, product_id)
            return make_response(jsonify({"mensagem": "Produto deletado com sucesso"}), 200)
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 404)
        except Exception as e:
            return make_response(jsonify({"erro": "Erro interno no servidor"}), 500)