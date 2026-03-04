# Plataforma Educativa IA 🎓

> Plataforma que gera conteúdo educativo personalizado usando engenharia de prompt avançada com a API do Google Gemini.

## Sobre o Projeto

Este projeto foi desenvolvido como parte de um desafio técnico de Estágio em IA e Engenharia de Prompt. O objetivo é demonstrar como técnicas avançadas de engenharia de prompt — como Persona Prompting, Context Setting, Chain-of-Thought e Output Formatting — podem melhorar significativamente a qualidade de respostas geradas por modelos de linguagem disponíveis no free tier da API.

A plataforma recebe o perfil de um aluno (nome, idade, nível de conhecimento e estilo de aprendizado) e um tópico, e gera 4 tipos de conteúdo educativo personalizado: explicação conceitual, exemplos práticos, questões de reflexão e mapa mental.

## Tecnologias

- Python 3.11.9
- [Google Gemini API](https://ai.google.dev/) — modelo `gemini-3-flash-preview`
- [google-genai](https://pypi.org/project/google-genai/) — SDK oficial do Google
- [python-dotenv](https://pypi.org/project/python-dotenv/) — gerenciamento de variáveis de ambiente
- [rich](https://pypi.org/project/rich/) — formatação de output no terminal

## Estrutura do Projeto

```
./
├── .env                        # Variáveis de ambiente (não commitado)
├── .env.example                # Exemplo de variáveis necessárias
├── .gitignore
├── criar_alunos.py             # Script para gerar data/dados_alunos.json
├── requirements.txt
├── README.md
├── PROMPT_ENGINEERING_NOTES.md # Documentação das estratégias de prompt
├── data/
│   └── dados_alunos.json       # Perfis dos alunos
├── resultados/                 # Outputs gerados (histórico por aluno/tópico)
├── samples/                    # Exemplos de outputs JSON
└── src/
    ├── aluno.py                # Classe Aluno com validações
    ├── gerar_conteudo.py       # Motor de engenharia de prompt
    └── main.py                 # CLI da aplicação
```

## Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/Ayrtonguimaraes/genai-vlab.git
cd genai-vlab
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Copie o arquivo de exemplo e adicione sua chave de API:

```bash
cp .env.example .env
```

Edite o `.env` com sua chave:

```
GEMINI_API_KEY=sua_chave_aqui
```

Você pode obter uma chave gratuita em [Google AI Studio](https://aistudio.google.com/).

### 5. Gere os perfis de alunos

```bash
python criar_alunos.py
```

## Como Usar

Execute o CLI a partir da raiz do projeto:

```bash
python src/main.py
```

O sistema vai guiar você por 3 etapas:

**1. Selecione um aluno:**
```
=== Alunos disponíveis ===
[1] João | intermediário | leitura-escrita
[2] Maria | iniciante | auditivo
[3] Pedro | iniciante | visual
[4] Carol | avançado | cinestésico
[5] José | avançado | leitura-escrita

Escolha um aluno (ou 'sair'):
```

**2. Digite o tópico:**
```
Digite o tópico para João: Como fazer um loop 'for' em Python
```

**3. Escolha o(s) tipo(s) de conteúdo:**
```
=== Tipos de conteúdo ===
[1] Explicação
[2] Exemplos
[3] Questões
[4] Mapa Mental
Escolha um ou mais separados por vírgula (ex: 1,3):
```

Os resultados são exibidos no terminal com formatação rica e salvos automaticamente em `resultados/{nome_aluno}/{topico}.json`.

## Técnicas de Engenharia de Prompt

O projeto aplica 4 técnicas em cada prompt gerado:

| Técnica | O que faz |
|---|---|
| **Persona Prompting** | Define um professor especialista com postura específica para cada tipo de conteúdo |
| **Context Setting** | Injeta o perfil completo do aluno (nome, idade, nível, estilo) como contexto |
| **Chain-of-Thought** | Solicita raciocínio pedagógico explícito antes de gerar o conteúdo |
| **Output Formatting** | Especifica estrutura, tamanho e tom esperados para cada tipo de resposta |

Cada uma das 4 funções de geração usa uma persona distinta, adaptada ao seu objetivo pedagógico. Veja detalhes completos em [PROMPT_ENGINEERING_NOTES.md](./PROMPT_ENGINEERING_NOTES.md).

## Exemplos de Output

A pasta [`/samples`](./samples) contém exemplos reais de outputs gerados para diferentes perfis de alunos e tópicos.

## Variáveis de Ambiente

| Variável | Descrição |
|---|---|
| `GEMINI_API_KEY` | Chave de API do Google Gemini (obrigatória) |