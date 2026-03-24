from src.Domain.user import UserDomain
from src.Infrastructure.Model.user import User
from src.config.data_base import db

class UserService:
    @staticmethod
    def create_user(name, cnpj, email, phone, password):

        # Verifica duplicidade antes de tentar salvar
        if User.query.filter_by(email=email).first():
            raise ValueError("E-mail já cadastrado")

        if User.query.filter_by(cnpj=cnpj).first():
            raise ValueError("CNPJ já cadastrado")

        user = User(
            name=name,
            cnpj=cnpj,
            email=email,
            phone=phone,
            status="INACTIVE"
        )
        user.set_password(password)  # hash da senha

        db.session.add(user)
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