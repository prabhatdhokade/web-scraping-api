from fastapi import HTTPException, Header
from config.settings import API_TOKEN


def verify_token(x_token: str = Header(...)):
    if x_token != API_TOKEN:
        raise HTTPException(status_code=400, detail="Invalid API Token")
    return x_token
