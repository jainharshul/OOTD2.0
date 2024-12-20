from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from firebase_setup import db

app = FastAPI()

# Pydantic Model for Item
class Item(BaseModel):
    name: str
    description: str
    price: float

# Create an item in Firestore
@app.post("/items/")
async def create_item(item: Item):
    try:
        doc_ref = db.collection("items").document()
        doc_ref.set(item.dict())
        return {"message": "Item created successfully!", "id": doc_ref.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get all items
@app.get("/items/")
async def get_items():
    try:
        items_ref = db.collection("items")
        docs = items_ref.stream()
        items = [{**doc.to_dict(), "id": doc.id} for doc in docs]
        return {"items": items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get an item by ID
@app.get("/items/{item_id}")
async def get_item(item_id: str):
    try:
        doc_ref = db.collection("items").document(item_id)
        doc = doc_ref.get()
        if not doc.exists:
            raise HTTPException(status_code=404, detail="Item not found")
        return {"item": doc.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Delete an item
@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    try:
        doc_ref = db.collection("items").document(item_id)
        doc_ref.delete()
        return {"message": "Item deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
