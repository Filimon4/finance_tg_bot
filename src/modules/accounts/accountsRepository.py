from sqlalchemy import select, text
from sqlalchemy.orm import Session
from src.modules.finance.cashAccounts.cashAccountRepository import CashAccountRepository
from src.db.models.Operations import Operations
from src.db.models.CashAccount import CashAccount
from src.db.models.Account import Account
from pydantic import BaseModel

class AccountCreateDTO(BaseModel):
    id: int

class AccountRepository:
    @staticmethod
    def getOrCreateUserById(session: Session, id: int) -> Account:
        try:
            user = AccountRepository.getUserById(session, id)
            if not user:
                user = AccountRepository.create(session, id)
            return user
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def getUserById(session: Session, id: int) -> Account:
        try:
            query = select(Account).where(Account.id == id)
            result = session.execute(query)
            return result.scalar()
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def create(session: Session, tg_id: int) -> Account:
        try:
            account = Account(id=tg_id)
            session.add(account)
            session.commit()
            return account
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def delete(session: Session, tg_id: int) -> Account:
        try:
            account = AccountRepository.getUserById(session, tg_id)
            if not account:
                raise "There is not such account"
            session.delete(account)
            session.commit()
            return True
        except Exception as e:
            print(e)
            return False
        
    @staticmethod
    def getAccountOverview(session: Session, tg_id: int):
        try:
            allCashAccount = session.query(CashAccount).filter(CashAccount.account_id == tg_id).all()
            
            account_overview = {
                "total_income": float(0),
                "total_expenses": float(0)
            }

            for cashAccount in allCashAccount:
                cashAccountBalance = CashAccountRepository.getCashAccountOverview(session, cashAccount.id)
                if not cashAccountBalance: continue
                account_overview["total_income"] += float(cashAccountBalance["total_income"])
                account_overview["total_expenses"] += float(cashAccountBalance["total_expenses"])

            return {
                "balance": float(account_overview["total_income"] - account_overview["total_expenses"]),
                "total_income": account_overview["total_income"],
                "total_expenses": account_overview["total_expenses"]
            }
        except Exception as e:
            print(e)
            return None
