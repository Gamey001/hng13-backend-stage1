# app/main.py
from fastapi import FastAPI, Depends, HTTPException, Query, status
from typing import Optional
from sqlmodel import Session, select
from .database import init_db, get_session
from .models import StringRow
from .crud import create_string, get_by_value, delete_by_value
from .utils import from_json

app = FastAPI(title="String Analyzer API (PostgreSQL)")

@app.on_event("startup")
def on_startup():
    init_db()

@app.post("/strings", status_code=status.HTTP_201_CREATED)
def analyze_string(payload: dict, session: Session = Depends(get_session)):
    if "value" not in payload:
        raise HTTPException(status_code=400, detail="Missing 'value'")
    row, props = create_string(session, payload["value"])
    return {
        "id": row.sha256_hash,
        "value": row.value,
        "properties": props,
        "created_at": row.created_at
    }

@app.get("/strings/{string_value}")
def get_string(string_value: str, session: Session = Depends(get_session)):
    row, props = get_by_value(session, string_value)
    return {
        "id": row.sha256_hash,
        "value": row.value,
        "properties": props,
        "created_at": row.created_at
    }

@app.delete("/strings/{string_value}", status_code=204)
def delete_string(string_value: str, session: Session = Depends(get_session)):
    delete_by_value(session, string_value)
    return

@app.get("/strings")
def list_strings(
    is_palindrome: Optional[bool] = Query(None),
    min_length: Optional[int] = Query(None),
    max_length: Optional[int] = Query(None),
    word_count: Optional[int] = Query(None),
    contains_character: Optional[str] = Query(None),
    session: Session = Depends(get_session)
):
    statement = select(StringRow)
    rows = session.exec(statement).all()

    results = []
    for row in rows:
        props = from_json(row.properties)
        ok = True
        if is_palindrome is not None and props["is_palindrome"] != is_palindrome:
            ok = False
        if min_length is not None and props["length"] < min_length:
            ok = False
        if max_length is not None and props["length"] > max_length:
            ok = False
        if word_count is not None and props["word_count"] != word_count:
            ok = False
        if contains_character and contains_character not in row.value:
            ok = False
        if ok:
            results.append({
                "id": row.sha256_hash,
                "value": row.value,
                "properties": props,
                "created_at": row.created_at
            })
    return {"data": results, "count": len(results)}
