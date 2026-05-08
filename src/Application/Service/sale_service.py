from src.config.data_base import db
from src.Infrastructure.Model.sale_order import SaleOrder
from src.Infrastructure.Model.sale import Sale
from src.Infrastructure.Model.product import Product
from src.Infrastructure.Model.user import User

class SaleService:

    @staticmethod
    def create_order(seller_id, items):
        seller = User.query.get(seller_id)
        if not seller:
            raise ValueError("Seller não encontrado")
        if seller.status != "ACTIVE":
            raise ValueError("Seller inativo não pode realizar vendas")

        if not items:
            raise ValueError("Nenhum item na venda")

        total = 0
        sale_items = []

        for item in items:
            product_id = item.get('product_id')
            quantidade = item.get('quantity', 0)

            product = Product.query.filter_by(id=product_id, seller_id=seller_id).first()
            if not product:
                raise ValueError(f"Produto {product_id} não encontrado")
            if product.status != "ACTIVE":
                raise ValueError(f"Produto '{product.name}' está inativo")
            if quantidade <= 0:
                raise ValueError(f"Quantidade inválida para '{product.name}'")
            if quantidade > product.quantity:
                raise ValueError(f"Estoque insuficiente para '{product.name}'. Disponível: {product.quantity}")

            total += product.price * quantidade
            sale_items.append((product, quantidade))

        order = SaleOrder(seller_id=seller_id, total=round(total, 2))
        db.session.add(order)
        db.session.flush()

        for product, quantidade in sale_items:
            sale = Sale(
                order_id=order.id,
                product_id=product.id,
                seller_id=seller_id,
                quantidade=quantidade,
                preco_unitario=product.price
            )
            product.quantity -= quantidade
            db.session.add(sale)

        db.session.commit()
        db.session.refresh(order)
        return order

    @staticmethod
    def list_orders(seller_id):
        orders = SaleOrder.query.filter_by(seller_id=seller_id).order_by(SaleOrder.created_at.desc()).all()
        result = []
        for o in orders:
            d = o.to_dict()
            for item in d['itens']:
                product = Product.query.get(item['product_id'])
                item['product_nome'] = product.name if product else '-'
            result.append(d)
        return result
