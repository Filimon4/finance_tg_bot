from sqlalchemy.orm import Session
from ..cashAccounts.accountRepository import AccountRepository
from ..categories.categoriesRepository import CategoryRepository
from .operationsRepository import OperationRepository


class OperationService:
    @classmethod
    async def createOperation(
        cls, db: Session, command: str, account_id: int = None
    ):
        try:
            parts = command.strip().split(maxsplit=2)
            if len(parts) != 3:
                return {
                    "success": False,
                    "message": "Неверный формат. Используйте: (+ или -; сумма; категория)",
                }

            operation_type, amount_str, category_name = parts

            if operation_type not in ("+", "-"):
                return {
                    "success": False,
                    "message": "Тип операции должен быть '+' или '-'",
                }

            try:
                amount = float(amount_str)
                if amount <= 0:
                    return {
                        "success": False,
                        "message": "Сумма должна быть положительным числом",
                    }
            except ValueError:
                return {"success": False, "message": "Сумма должна быть числом"}

            if account_id is not None:
                account = AccountRepository.get(db, account_id)
                if not account:
                    return {
                        "success": False,
                        "message": f"Аккаунт с ID {account_id} не найден",
                    }
            else:
                account = AccountRepository.create(db)
                if not account:
                    return {
                        "success": False,
                        "message": "Ошибка при создании аккаунта",
                    }
                account_id = account.id

            category = CategoryRepository.get_by_name(db, category_name)
            if not category:
                category = CategoryRepository.create(
                    db,
                    name=category_name,
                    base_type=None,
                    account_id=account_id,
                )
                if not category:
                    return {
                        "success": False,
                        "message": "Ошибка при создании категории",
                    }

            operation = OperationRepository.create(
                db,
                account_id=account_id,
                to_account_id=None,
                category_id=category.id,
                amount=amount,
                type=operation_type,
                description=f"Операция: {category_name}",
            )

            if not operation:
                return {
                    "success": False,
                    "message": "Ошибка при создании операции",
                }

            return {
                "success": True,
                "message": f"Операция успешно создана: {operation_type}{amount} ({category_name})",
                "operation_id": operation.id,
                "account_id": account_id,
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"Ошибка обработки команды: {str(e)}",
            }
