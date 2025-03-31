from fastapi import Query, Request
from fastapi.responses import JSONResponse
from src.db.models.Reminder import ReminderCreateDTO, ReminderUpdateDTO
from src.modules.reminders.remindersRepository import RemindersRepository
from src.db.index import DB
from src.modules.finance.cashAccounts.cashAccountRepository import CashAccountRepository
from src.modules.finance.operations.operationsRepository import OperationsRepository
from ..index import app

@app.get('/api/notifies/all', tags=['Notifies'])
def getAllNotifies():
  try:
    with DB.getSession() as session:
      reminders = RemindersRepository.getAll(session)
      reminders_data = [
        {
          'id': r.id,
          'day_of_week': r.day_of_week.name, 
          'time': str(r.time),
          'next_time': str(r.next_time),
          'is_acitve': r.is_acitve,
          'created_at': str(r.created_at),
        }
        for r in reminders 
      ]
      return JSONResponse(
        status_code=200,
        content={"success": True, "reminders": reminders_data}
      )
  except Exception as e:
    return JSONResponse(
        status_code=500,
        content={"success": False, "error": str(e)}
    )

@app.post('/api/notifies/create', tags=['Notifies'])
def createNotify(data: ReminderCreateDTO):
  try:
    with DB.getSession() as session:
      newReminder = RemindersRepository.create(session, data)
      reminderData = {
        'id': newReminder.id,
        'account_id': newReminder.account_id,
        'day_of_week': newReminder.day_of_week.name,
        'time': str(newReminder.time),
        'next_time': str(newReminder.next_time),
        'is_acitve': newReminder.is_acitve,
        'created_at': str(newReminder.created_at),
      }
      return JSONResponse(
        status_code=200,
        content={"success": True, "reminder": reminderData}
      )
  except Exception as e:
    return JSONResponse(
        status_code=500,
        content={"success": False, "error": str(e)}
    )

@app.patch('/api/notifies/update', tags=['Notifies'])
def updateNotify(data: ReminderUpdateDTO):
  try:
    with DB.getSession() as session:
      reminders = RemindersRepository.update(session, data)
      print(reminders)
      if not reminders: raise Exception('Failed to update')

      reminderData = {
        'id': reminders.id,
        'account_id': reminders.account_id,
        'day_of_week': reminders.day_of_week.name,
        'time': str(reminders.time),
        'next_time': str(reminders.next_time),
        'is_acitve': reminders.is_acitve,
        'created_at': str(reminders.created_at),
      }
      return JSONResponse(
        status_code=200,
        content={"success": True, "reminder": reminderData}
      )
  except Exception as e:
    return JSONResponse(
        status_code=500,
        content={"success": False, "error": str(e)}
    )
@app.delete('/api/notifies/delete', tags=['Notifies'])
def deleteNotify(id: int = Query(None)):
  try:
    with DB.getSession() as session:
      deleted = RemindersRepository.delete(session, id)
      if not deleted: raise Exception('Failed to delete')
      return JSONResponse(
        status_code=200,
        content={"success": True}
      )
  except Exception as e:
    return JSONResponse(
        status_code=500,
        content={"success": False, "error": str(e)}
    )
