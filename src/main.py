import json
import os
from aluno import Aluno
from gerar_conteudo import GeradorConteudo
from rich.console import Console
from rich.markdown import Markdown

console = Console()

def carregar_alunos(caminho='data/dados_alunos.json'):
    if not os.path.exists(caminho):
        print("Arquivo de alunos não encontrado. Execute: python criar_alunos.py")
        exit(1)
    with open(caminho, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    # Recria os objetos Aluno a partir do JSON
    return [Aluno(a['nome'], a['idade'], a['nivel_de_conhecimento'], a['estilo_de_aprendizado']) for a in dados]

def exibir_alunos(alunos):
    console.print("\n[bold cyan]=== Alunos disponíveis ===[/bold cyan]")
    for i, aluno in enumerate(alunos):
        print(f"[{i+1}] {aluno.nome} | {aluno.nivel_conhecimento} | {aluno.estilo_aprendizado}")

TIPOS_CONTEUDO = {
    '1': ('Explicação', 'gerar_explicacao'),
    '2': ('Exemplos',   'gerar_exemplos'),
    '3': ('Questões',   'gerar_questoes'),
    '4': ('Mapa Mental','gerar_mapa_mental'),
}

def exibir_tipos():
    console.print("\n[bold cyan]=== Tipos de conteúdo ===[/bold cyan]")
    for chave, (nome, _) in TIPOS_CONTEUDO.items():
        print(f"[{chave}] {nome}")
    print("Escolha um ou mais separados por vírgula (ex: 1,3)")


def main():
    alunos = carregar_alunos()
    
    while True:
        exibir_alunos(alunos)
        escolha = input("\nEscolha um aluno (ou 'sair'): ").strip()
        
        if escolha.lower() == 'sair':
            print("Até logo!")
            break
        
        # Validar se a escolha é válida
        if not escolha.isdigit() or not (1 <= int(escolha) <= len(alunos)):
            print("Opção inválida!")
            continue
            
        aluno = alunos[int(escolha) - 1]  # -1 porque lista começa em 0
        gerador = GeradorConteudo(aluno)
        topico = input(f"\nDigite o tópico para {aluno.nome}: ").strip()
        
        exibir_tipos()
        tipos_escolhidos = input("Escolha: ").strip().split(',')
        
        for tipo in tipos_escolhidos:
            tipo = tipo.strip()
            if tipo in TIPOS_CONTEUDO:
                nome, metodo = TIPOS_CONTEUDO[tipo]
                print(f"\n⏳ Gerando {nome}...")
                resultado = getattr(gerador, metodo)(topico)
                console.print(f"\n[bold green]=== {nome} ===[/bold green]")
                resposta = resultado.get('resposta', resultado.get('erro_mensagem'))
                if metodo == 'gerar_mapa_mental':
                    console.print(f"\n[bold green]=== {nome} ===[/bold green]")
                    console.print(resposta)  # sem Markdown()
                else:
                    console.print(f"\n[bold green]=== {nome} ===[/bold green]")
                    console.print(Markdown(resposta))
            else:
                print(f"Tipo '{tipo}' inválido, ignorando.")

if __name__ == '__main__':
    main()