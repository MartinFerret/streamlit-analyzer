import streamlit as st
from app.contract_analysis import analyser_contrat_llm
from app.pdf_extraction import extract_text_from_pdf

st.set_page_config(page_title="Analyseur de Contrat IA", layout="wide")
st.title("📄 Analyse de Contrat assistée par IA")

with st.sidebar:
    st.header("🔑 Clé API OpenRouter")
    api_key = st.text_input("Entre ta clé API OpenRouter", type="password")

uploaded_file = st.file_uploader("📎 Téléverse ton contrat en PDF", type="pdf")

if uploaded_file and api_key:
    with st.spinner("Chargement du contrat..."):
        pdf = extract_text_from_pdf(uploaded_file)
        texte_contrat = "\n".join([page.get_text("text") for page in pdf])

    st.subheader("🧠 Analyse assistée par IA")

    with st.expander("🧠 Analyse assistée par IA", expanded=False):
        if st.checkbox("📄 Résumer automatiquement le contrat"):
            question_resume = "Fournis un résumé du contrat en 5 à 10 points clés, en te concentrant sur ses éléments principaux."
            with st.spinner('Analyse en cours...'):
                resume = analyser_contrat_llm(texte_contrat, api_key, question_resume)
            st.markdown("### ✍️ Résumé du contrat")
            st.write(resume)

        if st.checkbox("📌 Extraire automatiquement les clauses clés"):
            question_clauses = "Liste et explique les clauses clés du contrat, comme la résiliation, la responsabilité, les pénalités, etc."
            with st.spinner('Analyse en cours...'):
                clauses = analyser_contrat_llm(texte_contrat, api_key, question_clauses)
            st.markdown("### 📑 Clauses clés")
            st.write(clauses)

        if st.checkbox("⚖️ Évaluer le niveau de risque juridique"):
            question_risque = "Évalue le niveau de risque juridique du contrat sur une échelle de 1 à 10, en tenant compte des zones floues et des déséquilibres possibles."
            with st.spinner('Analyse en cours...'):
                risque = analyser_contrat_llm(texte_contrat, api_key, question_risque)
            st.markdown("### ⚖️ Évaluation du risque")
            st.markdown(f"Note de risque : {risque}")

    st.markdown("---")
    st.subheader("💬 Analyse personnalisée")
    custom_prompt = st.text_area("Pose ta propre question au sujet du contrat")

    if st.button("Analyser avec l'IA") and custom_prompt.strip():
        with st.spinner('Analyse en cours...'):
            result = analyser_contrat_llm(texte_contrat, api_key, custom_prompt.strip())
            st.markdown("### 🧾 Résultat de l'analyse")
            st.write(result)
            st.download_button("📥 Télécharger l'analyse", result, file_name="analyse_contrat.txt")

else:
    st.info("📝 Téléverse un contrat PDF et saisis ta clé API OpenRouter pour commencer.")
