from sqlalchemy import Column, Integer, String, create_engine, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

# สร้างฐานข้อมูลและเชื่อมต่อกับ SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# สร้าง Base สำหรับ ORM
Base = declarative_base()

# สร้าง SessionLocal สำหรับการเชื่อมต่อกับฐานข้อมูล
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# สร้างโมเดล (Table) สำหรับจัดเก็บข้อมูล
class aihitdataUK(Base):
    __tablename__ = "aihitdataUK"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True)
    name = Column(String, index=True)
    website = Column(String, index=True)
    people_count = Column(Integer, index=True)
    senior_people_count = Column(Integer, index=True)
    emails_count = Column(Integer, index=True)
    personal_emails_count = Column(Integer, index=True)
    phones_count = Column(Integer, index=True)
    addresses_count = Column(Integer, index=True)
    investors_count = Column(Integer, index=True)
    clients_count = Column(Integer, index=True)
    partners_count = Column(Integer, index=True)
    changes_count = Column(Integer, index=True)
    people_changes_count = Column(Integer, index=True)
    contact_changes_count = Column(Integer, index=True)
    description_short = Column(String, index=True)

    company_info = relationship("company_info", back_populates="aihitdataUK", cascade="all, delete-orphan")
class company_info(Base):
    __tablename__ = "company_info"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True)
    name = Column(String, index=True)
    website = Column(String, index=True)
    description_short = Column(String, index=True)
    company_idUK = Column(Integer, ForeignKey("aihitdataUK.id", ondelete="CASCADE"))

    aihitdataUK = relationship("aihitdataUK", back_populates="company_info")

class company_employee(Base):
    __tablename__ = "company_employee"

    id = Column(Integer, primary_key=True, index=True)
    people_count = Column(Integer, index=True)
    senior_people_count = Column(Integer, index=True)

class company_contact(Base):
    __tablename__ = "company_contact"

    id = Column(Integer, primary_key=True, index=True)
    emails_count = Column(Integer, index=True)
    personal_emails_count = Column(Integer, index=True)
    phones_count = Column(Integer, index=True)
    addresses_count = Column(Integer, index=True)
 
class company_benefits(Base):
    __tablename__ = "company_benefits"

    id = Column(Integer, primary_key=True, index=True)
    investors_count = Column(Integer, index=True)
    clients_count = Column(Integer, index=True)
    partners_count = Column(Integer, index=True)
 
class company_change(Base):
    __tablename__ = "company_change"

    id = Column(Integer, primary_key=True, index=True)
    changes_count = Column(Integer, index=True)
    people_changes_count = Column(Integer, index=True)
    contact_changes_count = Column(Integer, index=True)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

# สร้างตารางในฐานข้อมูล
Base.metadata.create_all(bind=engine)

