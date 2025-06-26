from fastapi import FastAPI , HTTPException 
from pydantic import BaseModel
app = FastAPI()

items = []

class Item(BaseModel):
    text: str 
    is_done : bool = False #

@app.get("/")
def root():
    return { "message": "Welcome to the FastAPI application to manage your TODO list"}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id < len(items):
        items[item_id] = item
        return items[item_id]
    else:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id < len(items):
        del items[item_id]
        return {"message": f"Item {item_id} deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")

@app.post("/items")
def create_item(item: Item):
    items.append(item)
    return items

@app.get("/items", response_model=list[Item])
def list_items(limit:int =10 ):
    return items[0:limit]



@app.get("/items/{item_id}" , response_model=Item)
def get_item(item_id: int ) -> Item:
   if item_id < len(items):
       return items[item_id]
   else:
       raise HTTPException (status_code=404, detail=f"Item {item_id} not found" )