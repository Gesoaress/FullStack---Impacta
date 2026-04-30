from src.config.data_base import db
from src.Domain.sale import SaleDomain
from src.Infrastructure.Model.sale import Sale
from src.Infrastructure.Model.product import Product
from src.Infrastructure.Model.user import User


class SaleService:

    @staticmethod
    def create_sale(seller_id, product_id, quantidade):
        # 1. Verifica se o seller existe e está ativo
        seller = User.query.get(seller_id)
        if not seller:
            raise ValueError("Seller não encontrado")
        if seller.status != "ACTIVE":
            raise ValueError("Seller inativo não pode realizar vendas")

        # 2. Verifica se o produto existe e pertence ao seller
        product = Product.query.filter_by(id=product_id, seller_id=seller_id).first()
        if not product:
            raise ValueError("Produto não encontrado")

        # 3. Verifica se o produto está ativo
        if product.status != "ACTIVE":
            raise ValueError("Não é possível vender um produto inativo")

        # 4. Verifica se a quantidade solicitada está disponível no estoque
        if quantidade <= 0:
            raise ValueError("A quantidade deve ser maior que zero")
        if quantidade > product.stock_quantity:
            raise ValueError(
                f"Estoque insuficiente. Disponível: {product.stock_quantity}, Solicitado: {quantidade}"
            )

        # 5. Captura o preço do produto no momento da venda
        preco_unitario = product.price

        # 6. Cria o registro da venda
        sale = Sale(
            product_id=product_id,
            seller_id=seller_id,
            quantidade=quantidade,
            preco_unitario=preco_unitario
        )

        # 7. Deduz a quantidade do estoque automaticamente
        product.stock_quantity -= quantidade

        # 8. Persiste venda e atualização do estoque na mesma transação
        db.session.add(sale)
        db.session.commit()

        return SaleDomain(
            id=sale.id,
            product_id=sale.product_id,
            seller_id=sale.seller_id,
            quantidade=sale.quantidade,
            preco_unitario=sale.preco_unitario,
            created_at=sale.created_at
        )

    @staticmethod
    def list_sales(seller_id):
        sales = Sale.query.filter_by(seller_id=seller_id).order_by(Sale.created_at.desc()).all()
        return [
            SaleDomain(
                id=s.id,
                product_id=s.product_id,
                seller_id=s.seller_id,
                quantidade=s.quantidade,
                preco_unitario=s.preco_unitario,
                created_at=s.created_at
            )
            for s in sales
        ]

    @staticmethod
    def get_sale(sale_id, seller_id):
        sale = Sale.query.filter_by(id=sale_id, seller_id=seller_id).first()
        if not sale:
            raise ValueError("Venda não encontrada")
        return SaleDomain(
            id=sale.id,
            product_id=sale.product_id,
            seller_id=sale.seller_id,
            quantidade=sale.quantidade,
            preco_unitario=sale.preco_unitario,
            created_at=sale.created_at
        )