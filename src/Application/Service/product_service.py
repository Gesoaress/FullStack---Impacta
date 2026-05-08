from src.Domain.product import ProductDomain
from src.Infrastructure.Model.product import Product
from src.config.data_base import db

def _to_domain(p):
    return ProductDomain(id=p.id, seller_id=p.seller_id, name=p.name, price=p.price, quantity=p.quantity, status=p.status, img=p.img, categoria=p.categoria or "Outros")

class ProductService:

    @staticmethod
    def create_product(seller_id, name, price, quantity, img=None, status="ACTIVE", categoria="Outros"):
        product = Product(seller_id=seller_id, name=name, price=price, quantity=quantity, status=status, img=img, categoria=categoria)
        db.session.add(product)
        db.session.commit()
        return _to_domain(product)

    @staticmethod
    def list_products(seller_id):
        products = Product.query.filter_by(seller_id=seller_id).all()
        return [_to_domain(p) for p in products]

    @staticmethod
    def get_product(seller_id, product_id):
        product = Product.query.filter_by(id=product_id, seller_id=seller_id).first()
        if not product:
            raise ValueError("Produto não encontrado")
        return _to_domain(product)

    @staticmethod
    def update_product(seller_id, product_id, name=None, price=None, quantity=None, img=None, status=None, categoria=None):
        product = Product.query.filter_by(id=product_id, seller_id=seller_id).first()
        if not product:
            raise ValueError("Produto não encontrado")
        if name: product.name = name
        if price is not None: product.price = price
        if quantity is not None: product.quantity = quantity
        if img: product.img = img
        if status: product.status = status
        if categoria: product.categoria = categoria
        db.session.commit()
        return _to_domain(product)

    @staticmethod
    def inactivate_product(seller_id, product_id):
        product = Product.query.filter_by(id=product_id, seller_id=seller_id).first()
        if not product:
            raise ValueError("Produto não encontrado")
        if product.status == "INACTIVE":
            raise ValueError("Produto já está inativo")
        product.status = "INACTIVE"
        db.session.commit()
        return _to_domain(product)

    @staticmethod
    def activate_product(seller_id, product_id):
        product = Product.query.filter_by(id=product_id, seller_id=seller_id).first()
        if not product:
            raise ValueError("Produto não encontrado")
        if product.status == "ACTIVE":
            raise ValueError("Produto já está ativo")
        product.status = "ACTIVE"
        db.session.commit()
        return _to_domain(product)

    @staticmethod
    def delete_product(seller_id, product_id):
        product = Product.query.filter_by(id=product_id, seller_id=seller_id).first()
        if not product:
            raise ValueError("Produto não encontrado")
        db.session.delete(product)
        db.session.commit()
