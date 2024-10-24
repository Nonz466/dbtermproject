from typing import Union
from fastapi import FastAPI, Form, Request, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models 
from models import User


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



# Route แสดงฟอร์ม Login
@app.get("/logintest", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("logintest.html", {"request": request})

# Route สำหรับตรวจสอบ username และ password
@app.post("/logintest")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    # ตรวจสอบว่า username มีอยู่ในฐานข้อมูลหรือไม่
    user = db.query(User).filter(User.username == username).first()
    if not user or not password:
        return templates.TemplateResponse("logintest.html", {"request": request, "error": "Invalid credentials"})
    
    # ถ้า login ผ่าน ให้ redirect ไปยังหน้า index
    return RedirectResponse(url="/table", status_code=303)

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

@app.get("/table", response_class=HTMLResponse)
async def read_items(request: Request, db: Session = Depends(get_db)):
    items = db.query(models.aihitdataUK).all()  # ดึงข้อมูลทั้งหมดจากตาราง
    return templates.TemplateResponse("test.html", {"request": request, "items": items})

@app.get("/create", response_class=HTMLResponse)
async def create_company_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

# Route สำหรับรับข้อมูลจากฟอร์มและบันทึกลงฐานข้อมูล
@app.post("/create")
async def create_company(
    id: int = Form(...),
    url: str = Form(...),
    name: str = Form(...),
    website: str = Form(...),
    people_count: int = Form(...),
    senior_people_count: int = Form(...),
    emails_count: int = Form(...),
    personal_emails_count: int = Form(...),
    phones_count: int = Form(...),
    addresses_count: int = Form(...),
    investors_count: int = Form(...),
    clients_count: int = Form(...),
    partners_count: int = Form(...),
    changes_count: int = Form(...),
    people_changes_count: int = Form(...),
    contact_changes_count: int = Form(...),
    description_short: str = Form(...),
    db: Session = Depends(get_db)
):
    new_company = models.aihitdataUK(id=id, url=url, name=name, website=website, people_count=people_count, senior_people_count=senior_people_count, emails_count=emails_count, personal_emails_count=personal_emails_count,
                                     phones_count=phones_count, addresses_count=addresses_count, investors_count=investors_count, clients_count=clients_count, partners_count=partners_count, changes_count=changes_count,
                                     people_changes_count=people_changes_count, contact_changes_count=contact_changes_count, description_short=description_short)
    db.add(new_company)
    db.commit()
    return RedirectResponse(url="/create", status_code=303)