from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.Application.Service.sale_service import SaleService

class SaleController:

    @staticmethod
    @jwt_required()
    def create_order():
        seller_id = get_jwt_identity()
        data = request.get_json()
        items = data.get('items', [])

        if not items:
            return make_response(jsonify({"erro": "Nenhum item informado"}), 400)

        try:
            order = SaleService.create_order(seller_id, items)
            return make_response(jsonify({
                "mensagem": "Venda realizada com sucesso",
                "pedido": order.to_dict()
            }), 201)
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 400)
        except Exception as e:
            return make_response(jsonify({"erro": "Erro interno no servidor"}), 500)

    @staticmethod
    @jwt_required()
    def list_orders():
        seller_id = get_jwt_identity()
        try:
            orders = SaleService.list_orders(seller_id)
            return make_response(jsonify({"pedidos": orders}), 200)
        except Exception as e:
            return make_response(jsonify({"erro": "Erro interno no servidor"}), 500)
