import requests

def analyser_contrat_llm(texte, api_key, question):
    prompt = f"""
    Tu es un expert juridique senior, spécialisé dans le droit des contrats et l’audit contractuel, avec une vaste expérience en conseil aux entreprises pour la négociation, la rédaction, et l’analyse de contrats complexes. Tu possèdes une compréhension approfondie des risques juridiques et des mécanismes contractuels, tout en étant capable de rendre des analyses claires, accessibles et opérationnelles pour des clients de tout secteur.

    Tu as pour mission de répondre de manière précise et détaillée à une question spécifique concernant un contrat. Voici les instructions :

    - Analyse le texte du contrat et réponds uniquement à la question posée.
    - Sois clair et précis dans ta réponse, en te basant exclusivement sur les informations contenues dans le contrat.
    - Évite de donner un résumé global ou des informations non demandées.
    - Réponds de manière concise et compréhensible pour un non-juriste si possible.

    Voici le texte du contrat à analyser :

    ```
    {texte}
    ```

    Et voici la question posée :

    ```
    {question}
    ```
    """

    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://chat.openai.com",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "Tu es un expert juridique spécialisé dans la relecture de contrats."},
            {"role": "user", "content": prompt.format(texte=texte, question=question)}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Erreur lors de l'appel au LLM : {e}"
