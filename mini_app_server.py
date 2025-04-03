import os
import uvicorn
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env', verbose=True, override=True)

app_host = None

if os.getenv('APP_HOST'):
    app_host = app_host
else:
    app_host = '127.0.0.1'

if __name__ == "__main__":
    uvicorn.run("src.serverBot.index:app", port=9000, log_level="info", host=os.getenv('APP_HOST'))