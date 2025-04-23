from asyncio.log import logger
from sqlalchemy import select, text
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
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
            logger.error(f"{str(e)}")
            return None
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при проверки пользователя: {str(e)}")
            return None

    @staticmethod
    def getUserById(session: Session, id: int) -> Account:
        try:
            query = select(Account).where(Account.id == id)
            result = session.execute(query)
            return result.scalar()
        except Exception as e:
            logger.error(f"{str(e)}")
            return None

    @staticmethod
    def create(session: Session, tg_id: int) -> Account:
        try:
            account = Account(id=tg_id)
            session.add(account)
            session.commit()
            return account
        except Exception as e:
            logger.error(f"{str(e)}")
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
            logger.error(f"{str(e)}")
            return None
        
    @staticmethod
    def getAccountSixMonthOverview(session: Session, tg_id: int):
        try:
            query = text("""
                WITH date_range AS (
                    SELECT 
                        DATE_TRUNC('month', CURRENT_DATE - INTERVAL '5 months') AS start_month,
                        DATE_TRUNC('month', CURRENT_DATE) AS end_month
                ),
                monthly_totals AS (
                    SELECT 
                        DATE_TRUNC('month', created_at) AS month,
                        SUM(CASE WHEN type = 'INCOME' THEN amount ELSE -amount END) AS monthly_balance
                    FROM operations
                    WHERE account_id = :account_id
                    GROUP BY DATE_TRUNC('month', created_at)
                ),
                all_months AS (
                    SELECT 
                        generate_series(
                            (SELECT start_month FROM date_range),
                            (SELECT end_month FROM date_range),
                            INTERVAL '1 month'
                        )::date AS month
                )
                SELECT 
                    TO_CHAR(am.month, 'YYYY-MM') AS month_year,
                    COALESCE(SUM(mt.monthly_balance) OVER (ORDER BY am.month), NULL) AS cumulative_balance
                FROM all_months am
                LEFT JOIN monthly_totals mt ON am.month = mt.month
                ORDER BY am.month;
            """)
            
            return session.execute(query, {'account_id': tg_id}).fetchall()
        except Exception as e:
            logger.error(f"{str(e)}")
            return None
        
    @staticmethod
    def getAccountOverview(session: Session, tg_id: int):
        try:
            allCashAccount = session.query(CashAccount).filter(CashAccount.account_id == tg_id, CashAccount.main == True).all()
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
            logger.error(f"{str(e)}")
            return None
