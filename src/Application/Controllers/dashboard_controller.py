from flask import jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.Infrastructure.Model.product import Product
from src.Infrastructure.Model.sale import Sale
from src.config.data_base import db
from datetime import datetime, timedelta
from sqlalchemy import func

class DashboardController:

    @staticmethod
    @jwt_required()
    def get_dashboard():
        seller_id = get_jwt_identity()

        try:
            produtos_ativos = Product.query.filter_by(seller_id=seller_id, status="ACTIVE").all()
            total_produtos = len(produtos_ativos)
            total_estoque = sum(p.quantity for p in produtos_ativos)
            baixo_estoque = sum(1 for p in produtos_ativos if p.quantity <= 5)

            vendas = Sale.query.filter_by(seller_id=seller_id).all()
            total_vendido = sum(s.quantidade * s.preco_unitario for s in vendas)
            num_vendas = len(vendas)

            hoje = datetime.utcnow().date()
            vendas_por_dia = []
            for i in range(6, -1, -1):
                dia = hoje - timedelta(days=i)
                total_dia = sum(
                    s.quantidade * s.preco_unitario
                    for s in vendas
                    if s.created_at and s.created_at.date() == dia
                )
                vendas_por_dia.append({"dia": str(dia), "total": round(total_dia, 2)})

            produtos_vendidos = {}
            for s in vendas:
                produto = Product.query.get(s.product_id)
                nome = produto.name if produto else f"Produto {s.product_id}"
                produtos_vendidos[nome] = produtos_vendidos.get(nome, 0) + s.quantidade

            top_produtos = sorted(
                [{"nome": k, "quantidade": v} for k, v in produtos_vendidos.items()],
                key=lambda x: x["quantidade"],
                reverse=True
            )[:5]

            vendas_por_categoria = {}
            for s in vendas:
                produto = Product.query.get(s.product_id)
                cat = (produto.categoria or "Outros") if produto else "Outros"
                vendas_por_categoria[cat] = round(vendas_por_categoria.get(cat, 0) + s.quantidade * s.preco_unitario, 2)

            vendas_por_categoria_list = sorted(
                [{"categoria": k, "total": v} for k, v in vendas_por_categoria.items()],
                key=lambda x: x["total"],
                reverse=True
            )

            return make_response(jsonify({
                "total_produtos": total_produtos,
                "total_estoque": total_estoque,
                "total_vendido": round(total_vendido, 2),
                "num_vendas": num_vendas,
                "baixo_estoque": baixo_estoque,
                "vendas_por_dia": vendas_por_dia,
                "top_produtos": top_produtos,
                "vendas_por_categoria": vendas_por_categoria_list
            }), 200)

        except Exception as e:
            return make_response(jsonify({"erro": "Erro interno no servidor"}), 500)
