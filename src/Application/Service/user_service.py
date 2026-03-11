from src.Domain.user import UserDomain
from src.Infrastructure.Model.user import User
from src.config.data_base import db 

class UserService:
    @staticmethod
    def create_user(name, cnpj, email, phone, password):

        user = User(
            name=name,
            cnpj=cnpj,
            email=email,
            phone=phone,
            password=password,
            status="INACTIVE"
        )

        db.session.add(user)
        db.session.commit()

        return UserDomain(
            user.id,
            user.name,
            user.cnpj,
            user.email,
            user.phone,
            user.password,
            user.status
        )