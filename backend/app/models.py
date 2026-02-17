from sqlalchemy import Column, String, Text
from .database import Base
import uuid


class Document(Base):

    __tablename__ = "documents"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    content = Column(
        Text,
        default=""
    )

    version = Column(
        String,
        default="0"
    )
from sqlalchemy import Integer


class DocumentVersion(Base):

    __tablename__ = "document_versions"

    id = Column(Integer, primary_key=True, autoincrement=True)

    document_id = Column(String)

    content = Column(Text)

    version_number = Column(Integer)
