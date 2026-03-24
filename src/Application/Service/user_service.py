from src.Domain.user import UserDomain
from src.Infrastructure.Model.user import User
from src.Infrastructure.http.whats_app import generate_code, send_whatsapp_code
from src.config.data_base import db

class UserService:
    @staticmethod
    def create_user(name, cnpj, email, phone, password):

        # Verifica duplicidade antes de tentar salvar
        if User.query.filter_by(email=email).first():
            raise ValueError("E-mail já cadastrado")

        if User.query.filter_by(cnpj=cnpj).first():
            raise ValueError("CNPJ já cadastrado")

        # Gera o código de ativação
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

        # Envia o código via WhatsApp
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
        # Busca o seller pelo celular
        user = User.query.filter_by(phone=phone).first()

        if not user:
            raise ValueError("Seller não encontrado")

        if user.activation_code != code:
            raise ValueError("Código inválido")

        if user.status == "ACTIVE":
            raise ValueError("Seller já está ativo")

        # Ativa o seller
        user.status = "ACTIVE"
        user.activation_code = None  # limpa o código após ativar
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