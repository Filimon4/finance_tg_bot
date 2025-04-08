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
    allow_methods=["*"],
    allow_headers=["*"],
)

from .routes.operations import *
from .routes.reminders import *
from .routes.categories import *
from .routes.cashAccount import *
from .routes.account import *
from .routes.currencies import *
from .routes.export import *

@app.get('/api/health')
def getApiHealth():
  return "Ok"
