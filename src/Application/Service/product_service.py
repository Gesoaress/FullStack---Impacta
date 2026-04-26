from src.Domain.product import ProductDomain
from src.Infrastructure.Model.product import Product
from src.config.data_base import db


class ProductService:

    @staticmethod
    def create_product(seller_id, name, price, quantity, img=None):
        product = Product(
            seller_id=seller_id,
            name=name,
            price=price,
            quantity=quantity,
            status="ACTIVE",
            img=img
        )
        db.session.add(product)
        db.session.commit()
        return ProductDomain(id=product.id, seller_id=product.seller_id, name=product.name, price=product.price, quantity=product.quantity, status=product.status, img=product.img)

    @staticmethod
    def list_products(seller_id):
        products = Product.query.filter_by(seller_id=seller_id).all()
        return [ProductDomain(id=p.id, seller_id=p.seller_id, name=p.name, price=p.price, quantity=p.quantity, status=p.status, img=p.img) for p in products]

    @staticmethod
    def get_product(seller_id, product_id):
        product = Product.query.filter_by(id=product_id, seller_id=seller_id).first()
        if not product:
            raise ValueError("Produto não encontrado")
        return ProductDomain(id=product.id, seller_id=product.seller_id, name=product.name, price=product.price, quantity=product.quantity, status=product.status, img=product.img)

    @staticmethod
    def update_product(seller_id, product_id, name=None, price=None, quantity=None, img=None):
        product = Product.query.filter_by(id=product_id, seller_id=seller_id).first()
        if not product:
            raise ValueError("Produto não encontrado")
        if name: product.name = name
        if price is not None: product.price = price
        if quantity is not None: product.quantity = quantity
        if img: product.img = img
        db.session.commit()
        return ProductDomain(id=product.id, seller_id=product.seller_id, name=product.name, price=product.price, quantity=product.quantity, status=product.status, img=product.img)

    @staticmethod
    def inactivate_product(seller_id, product_id):
        product = Product.query.filter_by(id=product_id, seller_id=seller_id).first()
        if not product:
            raise ValueError("Produto não encontrado")
        if product.status == "INACTIVE":
            raise ValueError("Produto já está inativo")
        product.status = "INACTIVE"
        db.session.commit()
        return ProductDomain(id=product.id, seller_id=product.seller_id, name=product.name, price=product.price, quantity=product.quantity, status=product.status, img=product.img)
