import streamlit as st
import fitz
import re
import io

def extract_text_from_pdf(uploaded_file):
    # On s'assure que le fichier est bien un PDF
    pdf_bytes = uploaded_file.read()
    try:
        return fitz.open(stream=pdf_bytes, filetype="pdf")
    except Exception as e:
        st.error("Erreur lors de l'ouverture du PDF. Veuillez vérifier le fichier.")
        raise e

def highlight_pdf(pdf, keywords_or_phrases):
    page_summary = {}
    for page_num, page in enumerate(pdf):
        for keyword_or_phrase in keywords_or_phrases:
            # S'assurer que les mots-clés ou phrases sont correctement échappés et ne contiennent pas de caractères malveillants
            safe_keyword = re.escape(keyword_or_phrase)
            matches = [match for match in re.finditer(safe_keyword, page.get_text("text"), flags=re.IGNORECASE)]
            for match in matches:
                text_dict = page.get_text("dict")
                for block in text_dict["blocks"]:
                    if 'lines' in block:
                        for line in block["lines"]:
                            for span in line["spans"]:
                                if re.search(safe_keyword, span["text"], flags=re.IGNORECASE):
                                    rect = fitz.Rect(span["bbox"])
                                    highlight = page.add_highlight_annot(rect)
                                    highlight.set_colors(stroke=(0.7, 0.9, 1), fill=(0.9, 1, 1))
                                    highlight.update()

                                    if keyword_or_phrase not in page_summary:
                                        page_summary[keyword_or_phrase] = []
                                    page_summary[keyword_or_phrase].append({
                                        'page': page_num + 1,
                                        'text': span['text']
                                    })
    return pdf, page_summary

def generate_pdf_bytes(pdf):
    output_stream = io.BytesIO()
    pdf.save(output_stream)
    output_stream.seek(0)
    return output_stream

st.title("📄 Analyse de Contrat - OAD")

with st.expander("Instructions", expanded=False):
    st.markdown("""
        1. Téléchargez votre contrat au format PDF en utilisant le bouton ci-dessous.
        2. Entrez les mots-clés ou phrases que vous souhaitez rechercher dans le contrat. Séparez-les par des virgules.
        3. Le PDF sera analysé et les mots-clés seront surlignés. Un résumé des résultats apparaîtra avec des liens pour chaque occurrence.
        4. Vous pouvez télécharger le PDF annoté en cliquant sur le bouton de téléchargement.
    """)

uploaded_file = st.file_uploader("Télécharge ton contrat (PDF)", type="pdf")

input_text = st.text_area(
    "Entrez les mots-clés et phrases à rechercher, séparés par des virgules (ex: duration, ownership, obligations of the first party)",
    value="duration, ownership, payment, paris est magique, obligations of the first party",
    height=100
)

keywords_or_phrases = [item.strip() for item in input_text.split(',') if item.strip()]

# Validation des mots-clés
if not keywords_or_phrases:
    st.error("Veuillez entrer des mots-clés ou phrases à rechercher.")
else:
    # Assurer la sécurité des expressions régulières
    try:
        re.compile('|'.join(map(re.escape, keywords_or_phrases)))  # Tester la validité des expressions régulières
    except re.error:
        st.error("Erreur dans les mots-clés. Veuillez vérifier leur format.")
        keywords_or_phrases = []

if uploaded_file is not None and keywords_or_phrases:
    with st.spinner('Analyse en cours...'):
        pdf = extract_text_from_pdf(uploaded_file)
        original_texts = [page.get_text("text") for page in pdf]

        found_any = False
        not_found = []

        for phrase in keywords_or_phrases:
            phrase_found = any(re.search(re.escape(phrase), text, flags=re.IGNORECASE) for text in original_texts)
            if not phrase_found:
                not_found.append(phrase)
            else:
                found_any = True

        if not_found:
            st.badge("Need review", icon="⚠️", color="orange")
            with st.expander("⚠️ Mots-clés non trouvés", expanded=False):
                st.markdown(f"Aucun résultat pour les mots-clés suivants : {', '.join(not_found)}")

        if found_any:
            highlighted_pdf, page_summary = highlight_pdf(pdf, keywords_or_phrases)
            pdf_bytes = generate_pdf_bytes(highlighted_pdf)

            st.download_button(
                label="📥 Télécharger le PDF annoté",
                data=pdf_bytes,
                file_name="contrat_annoté.pdf",
                mime="application/pdf"
            )

            st.badge("Success", icon=":material/check:", color="green")
            with st.expander("✅ Mots-clés trouvés", expanded=False):
                for keyword, occurrences in page_summary.items():
                    st.markdown(f"### {keyword.capitalize()}")
                    for entry in occurrences:
                        st.markdown(
                            f"**Page {entry['page']}**: {entry['text']}"
                        )
        else:
            st.warning("Aucun mot ou phrase trouvé pour le surlignage dans le contrat.")
