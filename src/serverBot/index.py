from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Finnace management server",
    description="Web server for telegram mini app bot",
    version="0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["DELETE", "GET", "POST", "PUT", "PATCH"],
    allow_headers=["*"],
)

from .routes.operations import *
from .routes.reminders import *
from .routes.categories import *
from .routes.cashAccount import *
from .routes.account import *
from .routes.currencies import *

@app.get('/api/status', tags=['info'])
def getApiHealth():
  return "Ok"
