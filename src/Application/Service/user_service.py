from src.Domain.user import UserDomain
from src.Infrastructure.Model.user import User
from src.Infrastructure.http.whats_app import generate_code, send_whatsapp_code
from src.config.data_base import db

class UserService:
    @staticmethod
    def create_user(name, cnpj, email, phone, password):

        if User.query.filter_by(email=email).first():
            raise ValueError("E-mail já cadastrado")

        if User.query.filter_by(cnpj=cnpj).first():
            raise ValueError("CNPJ já cadastrado")

        code = generate_code()

        user = User(
            name=name,
            cnpj=cnpj,
            email=email,
            phone=phone,
            status="INACTIVE",
            activation_code=code
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        send_whatsapp_code(phone, code)

        return UserDomain(
            id=user.id,
            name=user.name,
            cnpj=user.cnpj,
            email=user.email,
            phone=user.phone,
            password=user.password,
            status=user.status
        )

    @staticmethod
    def activate_user(phone, code):
        user = User.query.filter_by(phone=phone, activation_code=code).first()

        if not user:
            raise ValueError("Código inválido")

        if user.status == "ACTIVE":
            raise ValueError("Seller já está ativo")

        user.status = "ACTIVE"
        user.activation_code = None
        db.session.commit()

        return UserDomain(
            id=user.id,
            name=user.name,
            cnpj=user.cnpj,
            email=user.email,
            phone=user.phone,
            password=user.password,
            status=user.status
        )

    @staticmethod
    def get_user(user_id):
        user = User.query.get(user_id)

        if not user:
            raise ValueError("Seller não encontrado")

        return UserDomain(
            id=user.id,
            name=user.name,
            cnpj=user.cnpj,
            email=user.email,
            phone=user.phone,
            password=user.password,
            status=user.status
        )

    @staticmethod
    def update_user(user_id, name=None, email=None, phone=None, password=None):
        user = User.query.get(user_id)

        if not user:
            raise ValueError("Seller não encontrado")

        # Atualiza só os campos que vieram
        if name:
            user.name = name
        if email:
            if User.query.filter_by(email=email).first():
                raise ValueError("E-mail já cadastrado")
            user.email = email
        if phone:
            user.phone = phone
        if password:
            user.set_password(password)

        db.session.commit()

        return UserDomain(
            id=user.id,
            name=user.name,
            cnpj=user.cnpj,
            email=user.email,
            phone=user.phone,
            password=user.password,
            status=user.status
        )

    @staticmethod
    def inactivate_user(user_id):
        user = User.query.get(user_id)

        if not user:
            raise ValueError("Seller não encontrado")

        if user.status == "INACTIVE":
            raise ValueError("Seller já está inativo")

        user.status = "INACTIVE"
        db.session.commit()

        return UserDomain(
            id=user.id,
            name=user.name,
            cnpj=user.cnpj,
            email=user.email,
            phone=user.phone,
            password=user.password,
            status=user.status
        )