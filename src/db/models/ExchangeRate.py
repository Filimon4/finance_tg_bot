from sqlalchemy import Column, ForeignKey, Integer, Numeric, TIMESTAMP, func
from ..index import Base


class ExchangeRate(Base):
    __tablename__ = "exchange_rate"

    id = Column(Integer, primary_key=True, autoincrement=True)

    from_currency_id = Column(
        Integer, ForeignKey("currency.id"), nullable=False
    )
    to_currency_id = Column(Integer, ForeignKey("currency.id"), nullable=False)

    rate = Column(Numeric(15, 2))
    created_at = Column(TIMESTAMP, default=func.now())
