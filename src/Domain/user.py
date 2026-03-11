class UserDomain:
    def __init__(self, id, name, cnpj, email, phone, status):
        self.id = id
        self.name = name
        self.cnpj = cnpj
        self.email = email
        self.phone = phone
        self.status = status
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "cnpj": self.cnpj,
            "email": self.email,
            "phone": self.phone,
            "status": self.status
        }