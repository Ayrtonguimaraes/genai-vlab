from google import genai
from dotenv import load_dotenv
from src.aluno import Aluno
import json
import time

load_dotenv()

aluno1 = Aluno('joão', 21, 'iniciante', 'Visual')
topico_aula = "Como fazer um loop 'for' em Python"

prompt_simples = f"""
Atue como um professor.
Ensine sobre o tópico: {topico_aula}.
O aluno se chama {aluno1.nome} e tem {aluno1.idade}.
{aluno1.nome} está no nível {aluno1.nivel_conhecimento} e prefere aprender no estilo {aluno1.estilo_aprendizado}.
Crie uma explicação simples e direta para {aluno1.nome}.
"""

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client()

modelo = "gemini-3-flash-preview"
response = client.models.generate_content(
    model=modelo, contents=prompt_simples
)

dado = {
    'modelo': modelo,
    'resposta': response.text,
    'timestamp': time.time()
}

with open ('resposta_da_api.json', 'w', encoding='utf-8') as f:
    json.dump(dado, f, indent=2, ensure_ascii=False)