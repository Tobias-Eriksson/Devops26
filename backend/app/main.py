"""Minimal FastAPI backend for the course template app.

A tiny in-memory "notes" API. Deliberately simple: students extend this
during the course (tests, CI, containers, deployment) without needing to
understand a complex domain model first.
"""
from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Template App API")


class Item(BaseModel):
    id: int
    text: str


class ItemCreate(BaseModel):
    text: str


class Stats(BaseModel):
    count: int
    total_characters: int


# In-memory storage. Resets whenever the container restarts - good enough
# for a teaching app; a real database is out of scope for this template.
_items: list[Item] = []
_next_id = 1

# Running total of characters across all notes, so /api/items/stats stays
# cheap instead of walking the whole list on every request.
_total_characters = 0


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/items")
def list_items() -> list[Item]:
    return _items


@app.get("/api/items/stats")
def item_stats() -> Stats:
    return Stats(count=len(_items), total_characters=_total_characters)


@app.post("/api/items", status_code=201)
def create_item(payload: ItemCreate) -> Item:
    global _next_id, _total_characters
    item = Item(id=_next_id, text=payload.text)
    _items.append(item)
    _next_id += 1
    _total_characters += len(item.text)
    return item


@app.get("/api/items/{item_id}")
def get_item(item_id: int) -> Item:
    for item in _items:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/api/items/{item_id}", status_code=204, response_model=None)
def delete_item(item_id: int) -> None:
    for i, item in enumerate(_items):
        if item.id == item_id:
            del _items[i]
            return
    raise HTTPException(status_code=404, detail="Item not found")
