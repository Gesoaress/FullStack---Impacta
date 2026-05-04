from src.Application.Controllers.user_controller import UserController
from src.Application.Controllers.auth_controller import AuthController
from src.Application.Controllers.product_controller import ProductController
from src.Application.Controllers.sale_controller import SaleController
from flask import jsonify, make_response

def init_routes(app):
    @app.route('/api', methods=['GET'])
    def health():
        return make_response(jsonify({
            "mensagem": "API - OK; Docker - Up",
        }), 200)

    # ── Sellers ──────────────────────────────────────────────
    @app.route('/api/sellers', methods=['POST'])
    def register_user():
        return UserController.register_user()

    @app.route('/api/sellers/activate', methods=['POST'])
    def activate_user():
        return UserController.activate_user()

    @app.route('/api/sellers/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        return UserController.get_user(user_id)

    @app.route('/api/sellers/<int:user_id>', methods=['PUT'])
    def update_user(user_id):
        return UserController.update_user(user_id)

    @app.route('/api/sellers/<int:user_id>/inactivate', methods=['PATCH'])
    def inactivate_user(user_id):
        return UserController.inactivate_user(user_id)

    @app.route('/api/auth/login', methods=['POST'])
    def login():
        return AuthController.login()

    @app.route('/api/products', methods=['POST'])
    def create_product():
        return ProductController.create_product()

    @app.route('/api/products', methods=['GET'])
    def list_products():
        return ProductController.list_products()

    @app.route('/api/products/<int:product_id>', methods=['GET'])
    def get_product(product_id):
        return ProductController.get_product(product_id)

    @app.route('/api/products/<int:product_id>', methods=['PUT'])
    def update_product(product_id):
        return ProductController.update_product(product_id)

    @app.route('/api/products/<int:product_id>/inactivate', methods=['PATCH'])
    def inactivate_product(product_id):
        return ProductController.inactivate_product(product_id)

    @app.route('/api/sales', methods=['POST'])
    def create_sale():
        return SaleController.create_sale()

    @app.route('/api/sales', methods=['GET'])
    def list_sales():
        return SaleController.list_sales()

    @app.route('/api/sales/<int:sale_id>', methods=['GET'])
    def get_sale(sale_id):
        return SaleController.get_sale(sale_id)