from typing import Union
from fastapi import FastAPI, Form, Request, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from pydantic import BaseModel
import models 
from models import aihitdataUK, User, company_info, company_employee, company_contact, company_benefits, company_change, SessionLocal


app = FastAPI()


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


#ไปหน้า dashborDashTotalComTestadtset
@app.get("/DashTotalComTest", response_class=HTMLResponse)
async def get_totals(request: Request, db: Session = Depends(get_db)):
    # คำนวณผลรวมของคอลัมน์ โดยใช้คำสั่ง GROUP BY โดยใช้ฟังก์ชัน sum()
    total_people_count = db.query(func.sum(models.aihitdataUK.people_count)).scalar()
    total_senior_people_count = db.query(func.sum(models.aihitdataUK.senior_people_count)).scalar()
    total_emails_count = db.query(func.sum(models.aihitdataUK.emails_count)).scalar()
    total_personal_emails_count = db.query(func.sum(models.aihitdataUK.personal_emails_count)).scalar()
    total_phones_count = db.query(func.sum(models.aihitdataUK.phones_count)).scalar()
    total_addresses_count = db.query(func.sum(models.aihitdataUK.addresses_count)).scalar()
    total_investors_count = db.query(func.sum(models.aihitdataUK.investors_count)).scalar()
    total_clients_count = db.query(func.sum(models.aihitdataUK.clients_count)).scalar()
    total_partners_count = db.query(func.sum(models.aihitdataUK.partners_count)).scalar()
    total_changes_count = db.query(func.sum(models.aihitdataUK.changes_count)).scalar()
    total_people_changes_count = db.query(func.sum(models.aihitdataUK.people_changes_count)).scalar()
    total_contact_changes_count = db.query(func.sum(models.aihitdataUK.contact_changes_count)).scalar()
    # ส่งผลรวมไปยัง template HTML
    return templates.TemplateResponse("DashTotalComTest.html", {
        "request": request,
        "total_people_count": total_people_count,
        "total_senior_people_count": total_senior_people_count,
        "total_emails_count": total_emails_count,
        "total_personal_emails_count": total_personal_emails_count,
        "total_phones_count": total_phones_count,
        "total_addresses_count": total_addresses_count,
        "total_investors_count": total_investors_count,
        "total_clients_count": total_clients_count,
        "total_partners_count": total_partners_count,
        "total_changes_count": total_changes_count,
        "total_people_changes_count": total_people_changes_count,
        "total_contact_changes_count": total_contact_changes_count

    })

def to_dict(obj):
    """แปลง SQLAlchemy object เป็น dictionary"""
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns} if obj else {}

@app.post("/DashTotalComTest", response_class=HTMLResponse)
async def search_company(request: Request, company_id: int = Form(...), db: Session = Depends(get_db)):
    # ค้นหาในตารางโดยใช้ company_id และมีการ join ระหว่าง ตาราง company_info และ ตาราง aihitdataUK ใน Database โดยการใช้ Foreign Key
    CompanyInfo = db.query(models.company_info).filter(models.company_info.company_idUK == company_id).first()
    CompanyEmployee = to_dict(db.query(models.company_employee).filter(models.company_employee.id == company_id).first())
    CompanyContact = to_dict(db.query(models.company_contact).filter(models.company_contact.id == company_id).first())
    CompanyBenefits = to_dict(db.query(models.company_benefits).filter(models.company_benefits.id == company_id).first())
    CompanyChange = to_dict(db.query(models.company_change).filter(models.company_change.id == company_id).first())
    return templates.TemplateResponse("Dashboradtest.html", {"request": request, 
                                                            "CompanyInfo": CompanyInfo, 
                                                            "CompanyEmployee": CompanyEmployee, 
                                                            "CompanyContact": CompanyContact, 
                                                            "CompanyBenefits": CompanyBenefits, 
                                                            "CompanyChange": CompanyChange})


# Route แสดงฟอร์ม Login

@app.get("/", response_class=HTMLResponse)
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
    return RedirectResponse(url="/DashTotalComTest", status_code=303)




@app.get("/table", response_class=HTMLResponse)
async def read_items(request: Request, db: Session = Depends(get_db)):
    items = db.query(models.aihitdataUK).all()  # ดึงข้อมูลทั้งหมดจากตาราง
    return templates.TemplateResponse("test.html", {"request": request, "items": items})

# top 10 company ที่มีนักลงทุน
@app.get("/top10", response_class=HTMLResponse)
async def get_top10_investors(request: Request, db: Session = Depends(get_db)):
    top_10investors = (
        db.query(models.aihitdataUK)
        .order_by(desc(models.aihitdataUK.investors_count))  # เรียงลำดับจากมากไปน้อย
        .limit(10)  # จำกัดผลลัพธ์ที่ 10 รายการ
        .all()
    )
    return templates.TemplateResponse("top10.html", {"request": request, "top_10investors": top_10investors})

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
    new_CompanyInfo = models.company_info(company_idUK=id, url=url, name=name, website=website, description_short=description_short)
    new_CompanyEmployee = models.company_employee(id=id, people_count=people_count, senior_people_count=senior_people_count)
    new_CompanyContactm = models.company_contact(id=id,emails_count=emails_count, personal_emails_count=personal_emails_count, phones_count=phones_count, addresses_count=addresses_count)
    new_CompanyBenefits = models.company_benefits (id=id, investors_count=investors_count, clients_count=clients_count, partners_count=partners_count)
    new_CompanyChange = models.company_change(id=id, changes_count=changes_count, people_changes_count=people_changes_count, contact_changes_count=contact_changes_count)

    db.add_all([new_company, new_CompanyInfo, new_CompanyEmployee, new_CompanyContactm, new_CompanyBenefits, new_CompanyChange])
    db.commit()
    return RedirectResponse(url="/create", status_code=303)

@app.get("/register", response_class=HTMLResponse)
async def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
async def register_company(
    username: str = Form(...),
    hashed_password: str = Form(...),
    db: Session = Depends(get_db)
):
    new_Account = models.User(username=username, hashed_password=hashed_password )
    db.add(new_Account)
    db.commit()
    return RedirectResponse(url="/register", status_code=303)

#function-----------------------------------------------------------------------------------ตารางฐานข้อมูล

