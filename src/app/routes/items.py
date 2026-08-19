from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.deps import get_db
from app.models.item import Item

router = APIRouter(prefix="/items", tags=["items"])


class ItemIn(BaseModel):
    name: str


class ItemOut(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


@router.post("", response_model=ItemOut, status_code=201)
def create_item(payload: ItemIn, db: Session = Depends(get_db)) -> Item:
    item = Item(name=payload.name)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("", response_model=list[ItemOut])
def list_items(db: Session = Depends(get_db)) -> list[Item]:
    return db.query(Item).all()


@router.get("/{item_id}", response_model=ItemOut)
def get_item(item_id: int, db: Session = Depends(get_db)) -> Item:
    item = db.get(Item, item_id)
    if item is None:
        raise HTTPException(404, "item not found")
    return item
