# app/crud.py
from sqlmodel import select, Session
from fastapi import HTTPException, status
from .models import StringRow
from .utils import compute_properties, sha256_of, to_json, from_json, iso_now

def create_string(session: Session, value: str):
    if not isinstance(value, str):
        raise HTTPException(status_code=422, detail="value must be a string")
    props = compute_properties(value)
    sha = props["sha256_hash"]

    existing = session.exec(select(StringRow).where(StringRow.sha256_hash == sha)).first()
    if existing:
        raise HTTPException(status_code=409, detail="String already exists")

    row = StringRow(
        sha256_hash=sha,
        value=value,
        properties=to_json(props),
        created_at=iso_now()
    )
    session.add(row)
    session.commit()
    return row, props

def get_by_value(session: Session, value: str):
    sha = sha256_of(value)
    row = session.exec(select(StringRow).where(StringRow.sha256_hash == sha)).first()
    if not row:
        raise HTTPException(status_code=404, detail="String not found")
    return row, from_json(row.properties)

def delete_by_value(session: Session, value: str):
    sha = sha256_of(value)
    row = session.exec(select(StringRow).where(StringRow.sha256_hash == sha)).first()
    if not row:
        raise HTTPException(status_code=404, detail="String not found")
    session.delete(row)
    session.commit()
