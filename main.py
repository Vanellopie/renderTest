# from typing import Optional

# from fastapi import FastAPI

# app = FastAPI()


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Optional[str] = None):
#     return {"item_id": item_id, "q": q}


from supabase import create_client, Client
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# https://docs.render.com/deploy-fastapi

url: str = "https://pudktqwdyxdtkyxgxqzj.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB1ZGt0cXdkeXhkdGt5eGd4cXpqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTAzODE1MzMsImV4cCI6MjAyNTk1NzUzM30._MzX-DYB7YOtSKrJPxUxXDSQFmS6HVBj0AdJJ6ShfWE"

supabase: Client = create_client(url, key)

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str = None

@app.post("/items/")
def create_item(item: Item):
    data = supabase.table("tasks").insert(item.dict()).execute()
    if data.data:
        return data.data
    else:
        raise HTTPException(status_code=400, detail="Item could not be created")
    

@app.get("/items/")
def read_items():
    data = supabase.table("tasks").select("*").execute()
    if data.data:
        return data.data
    else:
        raise HTTPException(status_code=404, detail="Items not found")
    

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    data = supabase.table("tasks").update(item.dict()).eq("id", item_id).execute()
    if data.data:
        return data.data
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    data = supabase.table("tasks").delete().eq("id", item_id).execute()
    if data.data:
        return {"message": "Item deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Item not found")
    
