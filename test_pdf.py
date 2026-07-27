from app.services.pdf_services import PDFService

text = PDFService.extract_text(
    "Statement of Purpose.pdf"
)

print(text[:1000])