from typing import List

from sqlalchemy import ForeignKey, Text, TIMESTAMP, Float, String, BIGINT, Integer, text, LargeBinary, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base, str_uniq, int_pk, str_null_true
from datetime import datetime
import uuid


# Модель транзакций
class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int_pk] = mapped_column(Integer, primary_key=True, index=True)
    amount: Mapped[float] = mapped_column(Float)
    category: Mapped[str] = mapped_column(String(50))
    mcc_code: Mapped[str] = mapped_column(String(10))
    description: Mapped[str] = mapped_column(String(255))  # Новое поле для описания
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("users.user_id"))  # Добавлено поле user_id

    # Определяем отношение с документами
    documents: Mapped[List["Document"]] = relationship("Document", back_populates="transaction")

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"amount={self.amount}, "
                f"category={self.category!r}, "
                f"mcc_code={self.mcc_code!r}), "
                f"description={self.description!r}, "
                f"user_id={self.user_id})")  # Добавлено user_id

    def __repr__(self):
        return str(self)


# Модель логов
class Log(Base):
    __tablename__ = "logs"

    log_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, index=True)
    timestamp: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    service_name: Mapped[str] = mapped_column(String(100))
    log_level: Mapped[str] = mapped_column(String(20))
    message: Mapped[str] = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("users.user_id"))
    request_id: Mapped[str] = mapped_column(String(36), default=str(uuid.uuid4()))  # UUID как строка
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.document_id"))

    # Определяем отношение с документами
    document: Mapped["Document"] = relationship("Document", back_populates="logs")
    user: Mapped["User"] = relationship("User", back_populates="logs")  # Исправлено

    def __str__(self):
        return (f"{self.__class__.__name__}(log_id={self.log_id}, "
                f"service_name={self.service_name!r}, "
                f"log_level={self.log_level!r}, "
                f"message={self.message!r})")

    def __repr__(self):
        return str(self)


# Модель документов
class Document(Base):
    __tablename__ = "documents"

    document_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    document_type: Mapped[str] = mapped_column(String(50))
    filename: Mapped[str] = mapped_column(String(255))
    upload_date: Mapped[datetime] = mapped_column(TIMESTAMP)
    status: Mapped[str] = mapped_column(String(20))
    transaction_id: Mapped[int] = mapped_column(ForeignKey("transactions.id"))

    # Определяем отношения
    transaction: Mapped["Transaction"] = relationship("Transaction", back_populates="documents")
    logs: Mapped[List["Log"]] = relationship("Log", back_populates="document")

    def __str__(self):
        return (f"{self.__class__.__name__}(document_id={self.document_id}, "
                f"document_type={self.document_type!r}, "
                f"filename={self.filename!r}, "
                f"upload_date={self.upload_date})")

    def __repr__(self):
        return str(self)

# Модель авторизации
class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255))  # Зашифрованный пароль
    first_name: Mapped[str] = mapped_column(String(50))  # Имя пользователя
    last_name: Mapped[str] = mapped_column(String(50))  # Фамилия пользователя
    coins: Mapped[float] = mapped_column(Float, default=0)  # Поле для хранения результата
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Определяем отношение с логами
    logs: Mapped[List["Log"]] = relationship("Log", back_populates="user")

    def __str__(self):
        return (f"{self.__class__.__name__}(user_id={self.user_id}, "
                f"username={self.username!r}, "
                f"email={self.email!r}, "
                f"first_name={self.first_name!r}, "
                f"last_name={self.last_name!r}, "
                f"coins={self.coins}, "
                f"created_at={self.created_at})")

    def __repr__(self):
        return str(self)