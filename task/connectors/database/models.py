from sqlalchemy import Column, Integer, String, Float, Sequence
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CurrencyConversionPLN(Base):
    __tablename__ = "converted_price_pln"

    id = Column(Integer, Sequence(""), primary_key=True)
    currency = Column(String(10), nullable=False)
    rate = Column(Float, nullable=False)
    date = Column(String(50), nullable=False)
    price_in_pln = Column(Float, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "currency": self.currency,
            "rate": self.rate,
            "date": self.date,
            "price_in_pln": self.price_in_pln,
        }
