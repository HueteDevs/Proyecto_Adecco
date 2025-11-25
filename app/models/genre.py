from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Genre(Base):
    __tablename__ = "genres"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name_genre: Mapped[str] = mapped_column(String(200), nullable=False) 