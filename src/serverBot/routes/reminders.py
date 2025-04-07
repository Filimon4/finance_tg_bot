from fastapi import Query, Request
from fastapi.responses import JSONResponse
from src.db.models.Reminder import ReminderCreateDTO, ReminderUpdateDTO
from src.modules.reminders.remindersRepository import ReminderDeleteData, RemindersRepository
from src.db.index import DB
from src.modules.finance.cashAccounts.cashAccountRepository import CashAccountRepository
from src.modules.finance.operations.operationsRepository import OperationsRepository
from ..index import app

@app.get('/api/reminders/all', tags=['Reminders'])
def getAllNotifies():
  try:
    with DB.get_session() as session:
      reminders = RemindersRepository.getAll(session)
      reminders_data = [
        {
          'id': r.id,
          'day_of_week': r.day_of_week.name, 
          'hour': str(r.hour),
          'next_time': str(r.next_time),
          'is_active': r.is_active,
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
  
@app.get('/api/reminders/users_reminders', tags=['Reminders'])
def getById(tg_id: int = Query(None)):
  try:
    with DB.get_session() as session:
      reminders = RemindersRepository.getAllById(session, tg_id)
      remindersJson = [
        {
          'id': rem.id,
          'day_of_week': rem.day_of_week.name if rem.day_of_week is not None else None,
          'hour': str(rem.hour),
          'next_time': str(rem.next_time),
          'is_active': rem.is_active,
          'created_at': str(rem.created_at),
          'account_id': rem.account_id,
        }
        for rem in reminders
      ]
      return JSONResponse(
        status_code=200,
        content={"success": True, 'reminders': remindersJson}
      )
  except Exception as e:
    return JSONResponse(
        status_code=500,
        content={"success": False, "error": str(e)}
    )
    
@app.get('/api/reminders/one', tags=['Reminders'])
def getById(id: int = Query(None)):
  try:
    with DB.get_session() as session:
      reminder = RemindersRepository.getById(session, id)
      remindersJson = {
        'id': reminder.id,
        'day_of_week': reminder.day_of_week.name if reminder.day_of_week is not None else None,
        'hour': str(reminder.hour),
        'next_time': str(reminder.next_time),
        'is_active': reminder.is_active,
        'created_at': str(reminder.created_at),
        'account_id': reminder.account_id,
      }
      return JSONResponse(
        status_code=200,
        content={"success": True, 'reminder': remindersJson}
      )

  except Exception as e:
    return JSONResponse(
        status_code=500,
        content={"success": False, "error": str(e)}
    )

@app.post('/api/reminders', tags=['Reminders'])
def createNotify(data: ReminderCreateDTO):
  try:
    with DB.get_session() as session:
      newReminder = RemindersRepository.create(session, data)
      reminderData = {
        'id': newReminder.id,
        'account_id': newReminder.account_id,
        'day_of_week': newReminder.day_of_week.name,
        'hour': str(newReminder.hour),
        'next_time': str(newReminder.next_time),
        'is_active': newReminder.is_active,
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

@app.patch('/api/reminders', tags=['Reminders'])
def updateNotify(data: ReminderUpdateDTO):
  try:
    with DB.get_session() as session:
      reminders = RemindersRepository.update(session, data)
      print(reminders)
      if not reminders: raise Exception('Failed to update')

      reminderData = {
        'id': reminders.id,
        'account_id': reminders.account_id,
        'day_of_week': reminders.day_of_week.name,
        'hour': str(reminders.hour),
        'next_time': str(reminders.next_time),
        'is_active': reminders.is_active,
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
@app.delete('/api/reminders', tags=['Reminders'])
def deleteNotify(data: ReminderDeleteData):
  try:
    with DB.get_session() as session:
      deleted = RemindersRepository.delete(session, data.id)
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
