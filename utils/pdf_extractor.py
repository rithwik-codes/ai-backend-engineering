import logging

from pypdf import PdfReader


def extract_text_from_pdf(file):

    logging.info("Starting PDF text extraction")

    try:

        reader = PdfReader(file)

        extracted_text = []

        for page in reader.pages:

            text = page.extract_text()

            if text:
                extracted_text.append(text)

        resume_text = "\n".join(
            extracted_text
        ).strip()

        if not resume_text:

            logging.warning(
                "No text extracted from PDF"
            )

            raise ValueError(
                "Could not extract text from PDF"
            )

        logging.info(
            "PDF text extracted successfully"
        )

        return resume_text

    except Exception as e:

        logging.error(
            f"PDF extraction failed: {e}"
        )

        raise