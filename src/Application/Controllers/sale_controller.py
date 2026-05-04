from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.Application.Service.sale_service import SaleService

class SaleController:

    @staticmethod
    @jwt_required()
    def create_sale():
        seller_id = get_jwt_identity()
        data = request.get_json()
        product_id = data.get('product_id')
        quantidade = data.get('quantity')

        if not product_id or not quantidade:
            return make_response(jsonify({"erro": "Campos obrigatórios faltando"}), 400)

        try:
            sale = SaleService.create_sale(seller_id, product_id, quantidade)
            return make_response(jsonify({
                "mensagem": "Venda realizada com sucesso",
                "venda": sale.to_dict()
            }), 201)
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 400)
        except Exception as e:
            return make_response(jsonify({"erro": "Erro interno no servidor"}), 500)

    @staticmethod
    @jwt_required()
    def list_sales():
        seller_id = get_jwt_identity()
        try:
            sales = SaleService.list_sales(seller_id)
            return make_response(jsonify({
                "vendas": [s.to_dict() for s in sales]
            }), 200)
        except Exception as e:
            return make_response(jsonify({"erro": "Erro interno no servidor"}), 500)

    @staticmethod
    @jwt_required()
    def get_sale(sale_id):
        seller_id = get_jwt_identity()
        try:
            sale = SaleService.get_sale(sale_id, seller_id)
            return make_response(jsonify({
                "venda": sale.to_dict()
            }), 200)
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 404)
        except Exception as e:
            return make_response(jsonify({"erro": "Erro interno no servidor"}), 500)