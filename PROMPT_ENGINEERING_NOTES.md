# Prompt Engineering Notes 🧠

Este documento descreve as estratégias de engenharia de prompt utilizadas na Plataforma Educativa IA, explicando as decisões técnicas e pedagógicas por trás de cada escolha.

---

## Técnicas Utilizadas

### 1. Persona Prompting

**O que é:** Atribuir uma identidade específica ao modelo antes de fazer a pergunta, filtrando o espaço de respostas para aquelas que um determinado perfil produziria.

**Como foi aplicado:** O projeto define uma `persona_base` compartilhada por todas as funções, estendida por uma persona específica para cada tipo de conteúdo. Isso garante consistência geral sem perder a especialização por tarefa.

```
persona_base → comportamento comum a todas as funções
    └── persona_explicacao  → guia paciente e didático
    └── persona_exemplo     → usa analogias conectadas à realidade do aluno
    └── persona_questoes    → foca no design da questão para causar reflexão
    └── persona_mapa_mental → quebra o conteúdo em sequência lógica
```

**Por que personas diferentes por função:** Um professor adota posturas distintas dependendo do objetivo pedagógico. Explicar um conceito exige paciência e didática; criar questões exige pensar em como estimular reflexão; montar um mapa mental exige organização hierárquica. Usar a mesma persona para todas as funções produziria respostas genéricas.

---

### 2. Context Setting

**O que é:** Fornecer ao modelo todas as informações de fundo necessárias antes de fazer a pergunta, evitando que ele preencha lacunas com suposições genéricas.

**Como foi aplicado:** Um bloco `contexto_aluno` é montado uma única vez no `__init__` da classe `GeradorConteudo` e reutilizado em todas as funções, injetando o perfil completo do aluno em cada prompt:

```
- Nome: {aluno.nome}
- Idade: {aluno.idade}
- Nível de conhecimento: {aluno.nivel_conhecimento}
- Estilo de aprendizado: {aluno.estilo_aprendizado}
```

**Decisão de design:** O contexto é definido no `__init__` porque o perfil do aluno não muda durante a sessão. Isso evita repetição de código (princípio DRY) e garante consistência entre todas as chamadas.

**Restrições pedagógicas por função:** Além do perfil, cada função define restrições específicas baseadas no contexto. Por exemplo:
- `gerar_explicacao` → evita jargões para iniciantes
- `gerar_exemplos` → exemplos alinhados à idade e nível
- `gerar_questoes` → dificuldade calibrada para não desencorajar iniciantes
- `gerar_mapa_mental` → profundidade da árvore reflete o nível do aluno

---

### 3. Chain-of-Thought (CoT)

**O que é:** Instruir o modelo a raciocinar explicitamente antes de gerar a resposta, melhorando a qualidade ao forçar etapas intermediárias de pensamento.

**Como foi aplicado:** Todas as funções incluem um bloco de raciocínio com 3-4 perguntas pedagógicas que o modelo deve responder antes de montar o conteúdo:

```
Antes de montar a explicação, raciocine sobre:
1. O que um aluno de nível {nivel} já sabe sobre {topico}?
2. Qual a melhor forma de ensinar dado o estilo {estilo}?
3. Quais são as armadilhas mais comuns para esse perfil?
4. Como adaptar o conteúdo para a idade {idade}?
```

**Por que funciona:** Cada pergunta do CoT conecta uma variável do perfil do aluno a uma decisão pedagógica concreta. O modelo não apenas recebe os dados do aluno — ele é forçado a usá-los ativamente no raciocínio antes de responder.

**Evidência na prática:** As respostas geradas mostram o raciocínio explícito antes do conteúdo, comprovando que o modelo está aplicando as perguntas do CoT. Isso também permite auditar a qualidade do raciocínio antes de aceitar a resposta.

---

### 4. Output Formatting

**O que é:** Especificar explicitamente como a resposta deve ser estruturada — formato, tamanho, tom e convenções visuais.

**Como foi aplicado:** Cada função define uma seção de output com estrutura, tamanho e tom específicos:

| Função | Estrutura | Tamanho | Tom |
|---|---|---|---|
| `gerar_explicacao` | Chamada + bullet points lógicos | Máx. 3 parágrafos | Varia com nível e idade |
| `gerar_exemplos` | Chamada + exemplos + call to action | Máx. 5 exemplos | Varia com nível e idade |
| `gerar_questoes` | Chamada + questões + encorajamento | Máx. 5 perguntas | Varia com nível e idade |
| `gerar_mapa_mental` | Chamada + árvore ASCII + call to action | Sem limite rígido | Varia com nível e idade |

**Decisão especial para o mapa mental:** Para garantir consistência no formato ASCII, o prompt inclui um exemplo visual concreto do padrão esperado com os caracteres `├──`, `└──` e `│`. Descrever o formato em palavras seria ambíguo — mostrar um exemplo elimina a variação entre chamadas.

```
Sistema Principal
├── Módulo A
│   ├── Submódulo A1
│   └── Submódulo A2
└── Módulo B
    └── Submódulo B1
```

---

## Arquitetura dos Prompts

Cada prompt segue uma estrutura consistente de 4 camadas:

```
[PERSONA ESPECÍFICA]
    ↓
[CONTEXTO DO ALUNO]
    ↓
[CHAIN-OF-THOUGHT — raciocínio pedagógico]
    ↓
[OUTPUT FORMATTING — estrutura da resposta]
```

Essa ordem é intencional: a persona define quem responde, o contexto define o cenário, o CoT força o raciocínio antes da resposta, e o output formatting garante que a entrega seja utilizável.

---

## Decisões de Engenharia

### Personas como atributos do objeto
As personas são definidas no `__init__` como atributos (`self.persona_explicacao`, etc.), não dentro de cada função. Isso permite:
- Reutilização sem repetição
- Fácil modificação para comparação de versões de prompt
- Rastreabilidade — o campo `persona_prompt` no JSON de saída registra exatamente qual persona foi usada

### Restrições com critério, não com receita
As restrições dos prompts usam critérios gerais em vez de regras específicas por caso:

```
# ❌ Receita (frágil):
Se iniciante: use 2 níveis na árvore, sem termos técnicos
Se avançado: use 4 níveis, termos técnicos liberados

# ✅ Critério (flexível):
A profundidade e o vocabulário devem refletir o nível {nivel} do aluno
```

O modelo já sabe o que caracteriza cada nível — dar o critério e deixar ele decidir produz resultados mais naturais e adaptados.

### Histórico de execuções
Cada resultado é salvo em `resultados/{nome_aluno}/{topico}.json` com os campos `persona`, `persona_prompt`, `dados_aluno` e `topico`. Isso permite comparar como diferentes personas ou versões de prompt afetam a qualidade da resposta para o mesmo aluno e tópico.

---

## Exemplos de Output

A pasta [`/samples`](./samples) contém exemplos reais de outputs 
gerados para diferentes perfis de alunos e tópicos.