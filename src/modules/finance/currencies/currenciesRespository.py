from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from src.db.models.Currency import Currency

class CurrenciesRepository:

  @staticmethod
  def getAll(session: Session):
    try:
      return session.query(Currency).all()
    except SQLAlchemyError as e:
      raise Exception(e)
    except Exception as e:
      raise Exception(e)
