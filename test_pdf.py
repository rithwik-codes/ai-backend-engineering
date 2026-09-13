from utils.pdf_extractor import extract_text_from_pdf


with open("resume.pdf", "rb") as file:

    text = extract_text_from_pdf(file)

    print("\n--- EXTRACTED RESUME TEXT ---\n")

    print(text)