from google import genai
from dotenv import load_dotenv
from aluno import Aluno
import json
import time
import os

load_dotenv()


class GeradorConteudo:
    def __init__(self, aluno):
       self.aluno = aluno
       self.cliente = genai.Client()
       self.modelo = "gemini-3-flash-preview"
       self.persona_base = """Você é um professor renomado com mais de 20 anos de experiência no setor de educação.
       Sua é especialidade é no tópico abordado.
       """
       self.persona_explicacao = f"""{self.persona_base}.
       Você deve agir como um guia paciente e didático, garantindo a compreensão do aluno."""
       self.persona_exemplo = f"""{self.persona_base}.
       Você deve atuar com analogias, conectando o assunto com a realidade do aluno"""
       self.persona_questoes = f"""{self.persona_base}.
       Você deve pensar no design da questão para causar reflexão"""
       self.persona_mapa_mental = f"""{self.persona_base}.
       Você deve quebrar o conteúdo em uma sequência lógica"""
       self.contexto_aluno = f"""Você está ensinando um aluno com o seguinte perfil:
-Nome: {self.aluno.nome}
-Idade: {self.aluno.idade}
-Nível de conhecimento: {self.aluno.nivel_conhecimento}
-Estilo de aprendizado: {self.aluno.estilo_aprendizado}"""

    def chamar_api(self, prompt):
        try:
            response = self.cliente.models.generate_content(
                model=self.modelo, contents=prompt
            )

            return {
            'modelo': self.modelo,
            'prompt': prompt,
            'resposta': response.text,
            'timestamp': time.time(),
            'erro': False,
        }
        except Exception as e:
            return {
                'modelo': self.modelo,
                'prompt': prompt,
                'timestamp': time.time(),
                'erro': True,
                'erro_mensagem': str(e),
                'erro_tipo': type(e).__name__
            }
    
    def salvar_resultados(self, resposta_api, topico, persona, persona_prompt):
        pasta = f'resultados/{self.aluno.nome}'
        os.makedirs(pasta, exist_ok=True)
        caminho_arquivo = f'{pasta}/{topico}.json'
        resposta_api['persona'] = persona
        resposta_api['persona_prompt'] = persona_prompt
        resposta_api['dados_aluno'] = self.aluno.dados_aluno
        resposta_api['topico'] = topico
        if os.path.exists(caminho_arquivo):
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                historico_execucao = json.load(f)
        else:
            historico_execucao = []

        historico_execucao.append(resposta_api)
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            json.dump(historico_execucao, f, indent=4, ensure_ascii=False)

    def gerar_explicacao(self, topico):
        prompt_completo = f"""{self.persona_explicacao}.
        {self.contexto_aluno}.
O tópico a ser ensinado é {topico}.
Você sempre deve explicar o conteúdo com passo a passo, garantindo que o aluno realmente entenda o conteúdo e não apenas decore.
Restrições:
-Se o aluno for de nível iniciante, evite jargões técnicos desnecessários.
-Adapte seu estilo de ensino para atender a demanda específica do aluno
Antes de montar a explicação, raciocine sobre:
1.O que um aluno de nível {self.aluno.nivel_conhecimento} já sabe sobre o {topico} ?
2.Qual a melhor forma de ensinar dado que o estilo de aprendizado deve ser {self.aluno.estilo_aprendizado} ?
3.Quais são as armadilhas mais comuns para esse perfil ?
4.Como você vai escrever a explicação dado a idade do aluno: {self.aluno.idade}
Estruture sua resposta da seguinte forma:
1.Chamada para engajar o aluno pelo nome ou perfil
2.Explicação central do conteúdo dividia por bullet points com ordem lógica
Tamanho: Limite a explicação a no máximo 3 parágrafos
Tom: Deve variar conforme nível do aluno e idade"""
        resultado = self.chamar_api(prompt_completo)

        if not resultado['erro']:
            self.salvar_resultados(resultado, topico, 'persona_explicacao', self.persona_explicacao)
        else:
            print(f"Erro ao gerar os dados -> {resultado['erro_mensagem']}")
        return resultado
    
    def gerar_exemplos(self, topico):
        prompt_completo = f"""{self.persona_exemplo}.
        {self.contexto_aluno}.
O tópico a ser ensinado é {topico}.
Você deve gerar exemplos para que o aluno consiga fixar o conteúdo, fazendo com que ele realmente aprenda e não apenas decore.
Os exemplos devem ter ser pensadas de tal maneira que aborde todo o conteúdo ou os principais pontos.
Restrições:
-Os exemplos devem estar de acordo com o nível do estudante: {self.aluno.nivel_conhecimento}
-Os exemplos devem ser criados para ajudar a visualizar melhor o conteúdo. Sempre leve em consideração a idade do aluno: {self.aluno.idade}
-Adapte seu estilo de ensino para atender a demanda específica do aluno
Antes de montar a explicação, raciocine sobre:
1.O que um aluno de nível {self.aluno.nivel_conhecimento} já sabe sobre o {topico} ?
2.Qual a melhor forma de gerar exemplos dado que o estilo de aprendizado deve ser {self.aluno.estilo_aprendizado} ?
3.Quais são as armadilhas mais comuns para esse perfil ?
4.Como você vai escrever os exemplos dado a idade do aluno: {self.aluno.idade}
Estruture sua resposta da seguinte forma:
1.Chamada para engajar o aluno pelo nome ou perfil
2.Os exemplos que foram pensados.
3.Perguntar se o aluno deseja novos exemplos ou se está pronto para fazer exercícios práticos (adicionar uma call to action)
Tamanho: Limite os exemplos a no máximo 5 exemplos
Tom: Deve variar conforme nível do aluno e idade"""
        resultado = self.chamar_api(prompt_completo)
        if not resultado['erro']:
            self.salvar_resultados(resultado, topico, 'persona_exemplo', self.persona_explicacao)
        else:
            print(f"Erro ao gerar os dados -> {resultado['erro_mensagem']}")
        return resultado
    
    def gerar_questoes(self, topico):
        prompt_completo = f"""{self.persona_questoes}.
        {self.contexto_aluno}.
O tópico a ser ensinado é {topico}.
Você deve gerar questões para que o aluno consiga praticar o conteúdo a ser ensinado.
As questões devem ter ser pensadas de tal maneira que aborde todo o conteúdo ou os principais pontos.
Restrições:
-Se o aluno for de nível iniciante, as questões devem ter um nível mais fácil para não desencorajar o aprendizado.
-Adapte seu estilo de ensino para atender a demanda específica do aluno
Antes de montar as questões, raciocine sobre:
1.O que um aluno de nível {self.aluno.nivel_conhecimento} já sabe sobre o {topico} ?
2.Qual a melhor forma de gerar questões dado que o estilo de aprendizado deve ser {self.aluno.estilo_aprendizado} ?
3.Quais são as armadilhas mais comuns para esse perfil ?
4.Como você vai escrever as questões dado a idade do aluno: {self.aluno.idade}
Estruture sua resposta da seguinte forma:
1.Chamada para engajar o aluno pelo nome ou perfil
2.As questões que foram pensadas.
3.Encorajar o aluno a tentar realizar as questões sozinho e falar que estar disponível para ajudar a realizar a atividade.
Tamanho: Limite as questões a no máximo 5 perguntas
Tom: Deve variar conforme nível do aluno e idade"""
        resultado = self.chamar_api(prompt_completo)
        if not resultado['erro']:
            self.salvar_resultados(resultado, topico, 'persona_questoes', self.persona_explicacao)
        else:
            print(f"Erro ao gerar os dados -> {resultado['erro_mensagem']}")
        return resultado
    
    def gerar_mapa_mental(self, topico):
        prompt_completo = f"""{self.persona_mapa_mental}.
        {self.contexto_aluno}.
O tópico a ser ensinado é {topico}.
Você deve gerar um mapa mental no formato de diagrama para que o aluno consiga fixar os conteúdos principais do tópico: {topico}.
Restrições:
- A profundidade da árvore e o vocabulário dos nós devem refletir o nível: {self.aluno.nivel_conhecimento} e a idade: {self.aluno.idade} anos do aluno
Antes de montar o mapa mental, raciocine sobre:
1.O que um aluno de nível {self.aluno.nivel_conhecimento} já sabe sobre o {topico} ?
2.Qual a melhor forma de gerar uma mapa mental dado que o estilo de aprendizado deve ser {self.aluno.estilo_aprendizado} ?
3.Quais são as armadilhas mais comuns para esse perfil ?
Estruture sua resposta da seguinte forma:
1.Chamada para engajar o aluno pelo nome ou perfil
2.Um diagrama no formato de árvore estruturada.
2.1.Exemplo de padrão a ser seguido no diagrama:
Sistema Principal
├── Módulo A
│   ├── Submódulo A1
│   │   ├── Componente A1.1
│   │   └── Componente A1.2
│   ├── Submódulo A2
│   │   └── Componente A2.1
│
├── Módulo B
│   ├── Submódulo B1
│   │   ├── Componente B1.1
│   │   └── Componente B1.2
│   └── Submódulo B2
│
└── Módulo C
    ├── Submódulo C1
    └── Submódulo C2
        ├── Componente C2.1
        └── Componente C2.2
3.Uma call to action para engajar o aluno a exercitar os conteúdos revisados
"""
        resultado = self.chamar_api(prompt_completo)
        if not resultado['erro']:
            self.salvar_resultados(resultado, topico, 'persona_mapa_mental', self.persona_explicacao)
        else:
            print(f"Erro ao gerar os dados -> {resultado['erro_mensagem']}")
        return resultado