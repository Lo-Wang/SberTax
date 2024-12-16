from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import TIMESTAMP, String, Integer, LargeBinary, Float
from datetime import datetime
from app.database import Base

class Document(Base):
    __tablename__ = "documents"

    document_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    document_type: Mapped[str] = mapped_column(String(50))
    filename: Mapped[str] = mapped_column(String(255))
    upload_date: Mapped[datetime] = mapped_column(TIMESTAMP)
    status: Mapped[str] = mapped_column(String(20))
    amount: Mapped[float] = mapped_column(Float, nullable=False)  # Поле для суммы
    category: Mapped[str] = mapped_column(String(50))  # Поле для категории
    mcc_code: Mapped[str] = mapped_column(String(10))  # Поле для кода MCC
    description: Mapped[str] = mapped_column(String(255))  # Новое поле для описания

    def __str__(self):
        return (f"{self.__class__.__name__}(document_id={self.document_id}, "
                f"document_type={self.document_type!r}, "
                f"filename={self.filename!r}, "
                f"upload_date={self.upload_date}, "
                f"amount={self.amount}, "
                f"category={self.category}, "
                f"mcc_code={self.mcc_code}, "
                f"description={self.description})")  # Добавлено описание

    def __repr__(self):
        return str(self)