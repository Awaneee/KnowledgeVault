from docx import Document


class DOCXService:

    @staticmethod
    def extract_text(
        file_path: str
    ) -> str:

        document = Document(
            file_path
        )

        paragraphs = [
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ]

        return "\n".join(
            paragraphs
        )