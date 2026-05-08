from src.config.data_base import db
from datetime import datetime

class SaleOrder(db.Model):
    __tablename__ = 'sale_orders'

    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship('Sale', backref='order', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "seller_id": self.seller_id,
            "total": round(self.total, 2),
            "created_at": str(self.created_at),
            "itens": [i.to_dict() for i in self.items]
        }
