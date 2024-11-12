from sqlalchemy import create_engine, Column, Integer, String, Float, TIMESTAMP, BIGINT, TEXT, ForeignKey
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import uuid

DATABASE_URL = "postgresql://username:password@localhost/dbname"

# Создание SQLAlchemy базы данных
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Модель транзакций
class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(BIGINT, primary_key=True, index=True)
    amount = Column(Float)
    category = Column(String)
    mcc_code = Column(String)
    # Определяем здесь отношение
    documents = relationship("Document", order_by="Document.document_id", back_populates="transaction")

class Log(Base):
    __tablename__ = "logs"

    log_id = Column(BIGINT, primary_key=True, index=True)
    timestamp = Column(TIMESTAMP)
    service_name = Column(String(100))
    log_level = Column(String(20))
    message = Column(TEXT)
    user_id = Column(BIGINT)
    request_id = Column(String(36), default=str(uuid.uuid4()))  # UUID as string
    document_id = Column(Integer, ForeignKey("documents.document_id"))

    document = relationship("Document", back_populates="logs")

class Document(Base):
    __tablename__ = "documents"

    document_id = Column(Integer, primary_key=True, index=True)
    document_type = Column(String(50))
    filename = Column(String(255))
    upload_date = Column(TIMESTAMP)
    file_data = Column(BYTEA)
    status = Column(String(20))
    transaction_id = Column(BIGINT, ForeignKey("transactions.id"))

    transaction = relationship("Transaction", back_populates="documents")
    logs = relationship("Log", back_populates="document")

# Создание таблиц
Base.metadata.create_all(bind=engine)