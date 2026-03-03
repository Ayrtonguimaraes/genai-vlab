from google import genai
from dotenv import load_dotenv
from src.aluno import Aluno
import json
import time

load_dotenv()


class GeradorConteudo:
    def __init__(self, aluno):
       self.aluno = aluno
       self.cliente = genai.Client()
       self.modelo = "gemini-3-flash-preview"
       persona = """Você é um professor renomado com mais de 20 anos de experiência no setor de educação.
       Sua é especialidade é no tópico abordado.
       Seu estilo de ensino vai variar conforme a necessidade do aluno.
       Você sempre deve explicar o conteúdo com passo a passo, garantindo que o aluno realmente entenda o conteúdo e não apenas decore"""
       self.persona_base = persona

    def chamar_api(self, prompt):
        response = self.cliente.models.generate_content(
            model=self.modelo, contents=prompt
        )  
        return {
            'modelo': self.modelo,
            'prompt': prompt,
            'resposta': response.text,
            'timestamp': time.time()
        }

    def gerar_explicacao(self, topico):
        prompt_completo = f"""{self.persona_base}.
        Você está ensinando um aluno com o seguinte perfil:
        -Nome: {self.aluno.nome}
-Idade: {self.aluno.idade}
-Nível de conhecimento: {self.aluno.nivel_conhecimento}
-Estilo de aprendizado: {self.aluno.estilo_aprendizado}
O tópico a ser ensinado é {topico}.
Restrições:
-Se o aluno for de nível iniciante, evite jargões técnicos desnecessários.
-Adapte seu estilo de ensino para atender a demanda específica do aluno
Antes de montar a explicação, raciocine sobre:
1.O que um aluno de nível {self.aluno.nivel_conhecimento} já sabe sobre o {topico} ?
2.Qual a melhor forma de ensinar dado que o estilo de aprendizado deve ser {self.aluno.estilo_aprendizado} ?
3.Quais são as armadilhas mais comuns para esse perfil ?
4.Como você vai introduzir o conteúdo dado a {self.aluno.idade}
Estruture sua resposta da seguinte forma:
1.Chamada para engajar o aluno pelo nome ou perfil
2.Explicação central do conteúdo dividia por bullet points com ordem lógica
Tamanho: Limite a explicação a no máximo 3 parágrafos
Tom: Deve varia conforme nível do aluno e idade"""
        return self.chamar_api(prompt_completo)


aluno1 = Aluno('joão', 21, 'iniciante', 'Visual')
topico_aula = "Como fazer um loop 'for' em Python"