import uvicorn

if __name__ == "__main__":
    uvicorn.run("src.serverBot.index:app", port=9000, log_level="info", host='127.0.0.1')