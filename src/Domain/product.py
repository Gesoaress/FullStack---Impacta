class ProductDomain:
    def __init__(self, id, seller_id, name, price, quantity, status, img=None, categoria="Outros"):
        self.id = id
        self.seller_id = seller_id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.status = status
        self.img = img
        self.categoria = categoria

    def to_dict(self):
        status_map = {"ACTIVE": "Ativo", "INACTIVE": "Inativo"}
        return {
            "id": self.id,
            "seller_id": self.seller_id,
            "nome": self.name,
            "preco": self.price,
            "quantidade": self.quantity,
            "status": status_map.get(self.status, self.status),
            "img": self.img,
            "categoria": self.categoria
        }