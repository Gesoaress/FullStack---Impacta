from src.Application.Controllers.user_controller import UserController
from src.Application.Controllers.auth_controller import AuthController
from src.Application.Controllers.product_controller import ProductController
from src.Application.Controllers.sale_controller import SaleController
from src.Application.Controllers.dashboard_controller import DashboardController
from src.Application.Controllers.admin_controller import AdminController
from flask import jsonify, make_response

def init_routes(app):
    @app.route('/api', methods=['GET'])
    def health():
        return make_response(jsonify({
            "mensagem": "API - OK; Docker - Up",
        }), 200)

    # Sellers
    @app.route('/api/sellers', methods=['POST'])
    def register_user():
        return UserController.register_user()

    @app.route('/api/sellers/activate', methods=['POST'])
    def activate_user():
        return UserController.activate_user()

    @app.route('/api/auth/login', methods=['POST'])
    def login():
        return AuthController.login()

    @app.route('/api/sellers/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        return UserController.get_user(user_id)

    @app.route('/api/sellers/<int:user_id>', methods=['PUT'])
    def update_user(user_id):
        return UserController.update_user(user_id)

    @app.route('/api/sellers/<int:user_id>/inactivate', methods=['PATCH'])
    def inactivate_user(user_id):
        return UserController.inactivate_user(user_id)

    # Products
    @app.route('/api/products', methods=['GET'])
    def list_products():
        return ProductController.list_products()

    @app.route('/api/products', methods=['POST'])
    def create_product():
        return ProductController.create_product()

    @app.route('/api/products/<int:product_id>', methods=['GET'])
    def get_product(product_id):
        return ProductController.get_product(product_id)

    @app.route('/api/products/<int:product_id>', methods=['PUT'])
    def update_product(product_id):
        return ProductController.update_product(product_id)

    @app.route('/api/products/<int:product_id>/inactivate', methods=['PATCH'])
    def inactivate_product(product_id):
        return ProductController.inactivate_product(product_id)

    @app.route('/api/products/<int:product_id>/activate', methods=['PATCH'])
    def activate_product(product_id):
        return ProductController.activate_product(product_id)

    @app.route('/api/products/<int:product_id>', methods=['DELETE'])
    def delete_product(product_id):
        return ProductController.delete_product(product_id)

    # Sales
    @app.route('/api/sales', methods=['POST'])
    def create_order():
        return SaleController.create_order()

    @app.route('/api/sales', methods=['GET'])
    def list_orders():
        return SaleController.list_orders()

    # Dashboard
    @app.route('/api/dashboard', methods=['GET'])
    def get_dashboard():
        return DashboardController.get_dashboard()

    # Admin
    @app.route('/api/admin/register', methods=['POST'])
    def register_admin():
        return AdminController.register_admin()

    @app.route('/api/admin/sellers', methods=['GET'])
    def admin_list_sellers():
        return AdminController.list_sellers()

    @app.route('/api/admin/sellers/<int:seller_id>', methods=['DELETE'])
    def admin_delete_seller(seller_id):
        return AdminController.delete_seller(seller_id)

    @app.route('/api/admin/sellers/<int:seller_id>/toggle', methods=['PATCH'])
    def admin_toggle_seller(seller_id):
        return AdminController.toggle_seller(seller_id)