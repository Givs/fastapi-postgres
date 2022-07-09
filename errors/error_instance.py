from fastapi import HTTPException


def error_instance(status: int, message: str):
    raise HTTPException(status_code=status, detail=message)

