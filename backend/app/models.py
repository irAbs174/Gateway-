from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base
from sqlalchemy import String, Integer, ForeignKey, Text

Base = declarative_base()

class Provider(Base):
    __tablename__ = "providers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    base_url: Mapped[str] = mapped_column(Text, nullable=False)
    credentials: Mapped["Credential"] = relationship(back_populates="provider", uselist=False)

class Credential(Base):
    __tablename__ = "credentials"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    provider_id: Mapped[int] = mapped_column(ForeignKey("providers.id"), unique=True)
    token_encrypted: Mapped[str] = mapped_column(Text, nullable=False)
    provider: Mapped["Provider"] = relationship(back_populates="credentials")
