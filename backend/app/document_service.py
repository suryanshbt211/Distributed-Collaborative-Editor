from sqlalchemy import select, func
from .database import SessionLocal
from .models import Document, DocumentVersion


class DocumentService:

    @staticmethod
    async def get_or_create_document(document_id: str):

        async with SessionLocal() as session:

            result = await session.execute(
                select(Document).where(Document.id == document_id)
            )

            document = result.scalar_one_or_none()

            if document is None:

                document = Document(
                    id=document_id,
                    content="",
                    version="0"
                )

                session.add(document)

                await session.commit()

            return document

    @staticmethod
    async def save_document(document_id: str, content: str):

        async with SessionLocal() as session:

            result = await session.execute(
                select(Document).where(Document.id == document_id)
            )

            document = result.scalar_one_or_none()

            if document:

                # Update current document
                document.content = content

                # Get latest version number
                version_result = await session.execute(
                    select(func.max(DocumentVersion.version_number))
                    .where(DocumentVersion.document_id == document_id)
                )

                latest_version = version_result.scalar()

                if latest_version is None:
                    latest_version = 0

                new_version = DocumentVersion(
                    document_id=document_id,
                    content=content,
                    version_number=latest_version + 1
                )

                session.add(new_version)

                await session.commit()

    @staticmethod
    async def rollback_document(document_id: str, version_number: int):

        async with SessionLocal() as session:

            # Get requested version
            result = await session.execute(
                select(DocumentVersion)
                .where(DocumentVersion.document_id == document_id)
                .where(DocumentVersion.version_number == version_number)
            )

            version = result.scalar_one_or_none()

            if version is None:
                return None

            # Update main document
            doc_result = await session.execute(
                select(Document)
                .where(Document.id == document_id)
            )

            document = doc_result.scalar_one_or_none()

            if document:
                document.content = version.content
                await session.commit()

            return version.content
