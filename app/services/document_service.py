from pathlib import Path

from app.services.pdf_services import PDFService
from app.services.text_service import TXTService
from app.services.docx_service import DOCXService


class DocumentService:

    @staticmethod
    def extract_text(
        file_path: str
    ) -> str:

        extension = (
            Path(file_path)
            .suffix
            .lower()
        )

        if extension == ".pdf":
            return PDFService.extract_text(
                file_path
            )

        if extension == ".txt":
            return TXTService.extract_text(
                file_path
            )

        if extension == ".docx":
            return DOCXService.extract_text(
                file_path
            )

        raise ValueError(
            f"Unsupported file type: {extension}"
        )