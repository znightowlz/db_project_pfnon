import models 
from models import aihitdataUK, User, company_info, company_employee, company_contact, company_benefits, company_change, SessionLocal

def copy_data_to_company_info():
    # ดึงข้อมูลจากตาราง aihitdataUK
    db = SessionLocal()
    aihitdataUK1 = db.query(aihitdataUK.id, aihitdataUK.url, aihitdataUK.name, aihitdataUK.website, aihitdataUK.description_short).all()
    
    # เพิ่มข้อมูลที่คัดลอกไปยังตาราง company_info
    current_id = 1
    try:
        for company in aihitdataUK1:
            new_company_info = company_info(
                id = current_id,
                company_id=company.id,
                url=company.url,
                name=company.name,
                website=company.website,
                description_short=company.description_short
            )
            db.add(new_company_info)
            current_id += 1
    
    # บันทึกข้อมูลลงในตาราง company_info
        db.commit()
    finally:
        # ปิด session หลังจากใช้งานเสร็จ
        db.close()
#------------------------------------------------------------------------------------------------------------------------------
def copy_data_to_company_employee():
    # ดึงข้อมูลจากตาราง aihitdataUK
    db = SessionLocal()
    aihitdataUK1 = db.query(aihitdataUK.id, aihitdataUK.people_count, aihitdataUK.senior_people_count).all()
    
    # เพิ่มข้อมูลที่คัดลอกไปยังตาราง company_employee
    try:
        for company in aihitdataUK1:
            new_company = company_employee(
                id=company.id,
                people_count=company.people_count,
                senior_people_count=company.senior_people_count,              
            )
            db.add(new_company)
    
    # บันทึกข้อมูลลงในตาราง company_employee
        db.commit()
    finally:
        # ปิด session หลังจากใช้งานเสร็จ
        db.close()
#------------------------------------------------------------------------------------------------------------------------------
def copy_data_to_company_contact():
    # ดึงข้อมูลจากตาราง aihitdataUK
    db = SessionLocal()
    aihitdataUK1 = db.query(aihitdataUK.id, aihitdataUK.emails_count, aihitdataUK.personal_emails_count, aihitdataUK.phones_count, aihitdataUK.addresses_count).all()
    
    # เพิ่มข้อมูลที่คัดลอกไปยังตาราง company_contact
    try:
        for company in aihitdataUK1:
            new_company = company_contact(
                id=company.id,
                emails_count=company.emails_count,
                personal_emails_count=company.personal_emails_count,
                phones_count=company.phones_count,
                addresses_count=company.addresses_count
            )
            db.add(new_company)
    
    # บันทึกข้อมูลลงในตาราง company_contact
        db.commit()
    finally:
        # ปิด session หลังจากใช้งานเสร็จ
        db.close()
#------------------------------------------------------------------------------------------------------------------------------
def copy_data_to_company_benefits():
    # ดึงข้อมูลจากตาราง aihitdataUK
    db = SessionLocal()
    aihitdataUK1 = db.query(aihitdataUK.id, aihitdataUK.investors_count, aihitdataUK.clients_count, aihitdataUK.partners_count).all()
    
    # เพิ่มข้อมูลที่คัดลอกไปยังตาราง company_benefits
    try:
        for company in aihitdataUK1:
            new_company = company_benefits(
                id=company.id,
                investors_count=company.investors_count,
                clients_count=company.clients_count,
                partners_count=company.partners_count,
            )
            db.add(new_company)
    
    # บันทึกข้อมูลลงในตาราง company_benefits
        db.commit()
    finally:
        # ปิด session หลังจากใช้งานเสร็จ
        db.close()    
#------------------------------------------------------------------------------------------------------------------------------
def copy_data_to_company_change():
    # ดึงข้อมูลจากตาราง aihitdataUK
    db = SessionLocal()
    aihitdataUK1 = db.query(aihitdataUK.id, aihitdataUK.changes_count, aihitdataUK.people_changes_count, aihitdataUK.contact_changes_count).all()
    
    # เพิ่มข้อมูลที่คัดลอกไปยังตาราง company_change
    try:
        for company in aihitdataUK1:
            new_company = company_change(
                id=company.id,
                changes_count=company.changes_count,
                people_changes_count=company.people_changes_count,
                contact_changes_count=company.contact_changes_count,
            )
            db.add(new_company)
    
    # บันทึกข้อมูลลงในตาราง company_change
        db.commit()
    finally:
        # ปิด session หลังจากใช้งานเสร็จ
        db.close() 

#------------------------------------------------------------------------------------------------------------------------------
