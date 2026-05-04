class ProductDomain:
    def __init__(self, id, seller_id, name, price, quantity, status, img=None):
        self.id = id
        self.seller_id = seller_id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.status = status
        self.img = img

    def to_dict(self):
        return {
            "id": self.id,
            "seller_id": self.seller_id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "status": self.status,
            "img": self.img
        }