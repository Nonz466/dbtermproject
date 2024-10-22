from typing import Union
from fastapi import FastAPI, Form, Request, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models

app = FastAPI()


#@app.get("/")
#def read_root():
    #return {"Hello": "World"}


#@app.get("/items/{item_id}")
#def read_item(item_id: int, q: Union[str, None] = None):
    #return {"item_id": item_id, "q": q}
# สร้าง FastAPI instance
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
# กำหนดตำแหน่งของโฟลเดอร์ที่เก็บไฟล์ HTML
templates = Jinja2Templates(directory="templates")

# สร้าง dependency สำหรับการเชื่อมต่อฐานข้อมูล
def get_db():
    db = models.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model สำหรับรับข้อมูลจากผู้ใช้
class ItemCreate(BaseModel):
    name: str
    description: str
# สร้าง route ที่ render หน้า HTML
@app.get("/login/", response_class=HTMLResponse)
async def read_index(request: Request):
     context = {
         'request': request,
         #'value': '/static/document/test2.pdf',
     }
     return templates.TemplateResponse("index.html", context)

@app.get("/test/", response_class=HTMLResponse)
async def read_index(request: Request):
     context = {
         'request': request,
         #'value': '/static/document/test2.pdf',
     }
     return templates.TemplateResponse("index.html", context)

@app.get("/items/{item_id}")
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.aihitdataUK).filter(models.aihitdataUK.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item