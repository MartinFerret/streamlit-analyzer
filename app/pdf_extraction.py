import fitz

def extract_text_from_pdf(uploaded_file):
    pdf_bytes = uploaded_file.read()
    try:
        return fitz.open(stream=pdf_bytes, filetype="pdf")
    except Exception as e:
        raise Exception("Erreur lors de l'ouverture du PDF. Veuillez vérifier le fichier.")
