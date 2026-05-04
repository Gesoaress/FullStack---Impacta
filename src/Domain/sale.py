class SaleDomain:
    def __init__(self, id, product_id, seller_id, quantidade, preco_unitario, created_at=None):
        self.id = id
        self.product_id = product_id
        self.seller_id = seller_id
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario
        self.created_at = created_at

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "seller_id": self.seller_id,
            "quantidade": self.quantidade,
            "preco_unitario": self.preco_unitario,
            "created_at": str(self.created_at) if self.created_at else None
        }