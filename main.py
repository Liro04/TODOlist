from fastapi.templating import Jinja2Templates
from fastapi import Request, FastAPI, HTTPException, Form
from fastapi.responses import RedirectResponse           
from pydantic import BaseModel
from auth import router as auth_router

app = FastAPI()
app.include_router(auth_router)

templates = Jinja2Templates(directory="templates")
items = []

class Item(BaseModel):
    text: str
    is_done: bool = False

@app.post("/add")
def add_item(request: Request, text: str = Form(...)):
    items.append(Item(text=text))
    return RedirectResponse(url="/todo", status_code=303)

@app.get("/todo")
def read_todo(request: Request):
    return templates.TemplateResponse("todo.html", {"request": request, "app_name": "My TODO App", "items": items})

@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI application to manage your TODO list"}

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
def list_items(limit: int = 10):
    return items[0:limit]

@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int) -> Item:
    if item_id < len(items):
        return items[item_id]
    else:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")