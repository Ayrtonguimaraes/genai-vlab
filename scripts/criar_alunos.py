from src.aluno import Aluno
import os
import json

lista_alunos = [
Aluno('João', 19, 'intermediário', 'leitura-escrita'),
Aluno('Maria', 50, 'iniciante',"auditivo"),
Aluno('Pedro', 13, 'iniciante', 'visual'),
Aluno('Carol', 28, 'avançado', 'cinestésico'),
Aluno('José', 60, 'avançado', 'leitura-escrita') ]

dados = [aluno.dados_aluno for aluno in lista_alunos]
pasta = "data"
os.makedirs(pasta, exist_ok=True)
caminho_arquivo = f'{pasta}/dados_alunos.json'

with open(caminho_arquivo, 'w', encoding='utf-8') as f:
    json.dump(dados, f, indent=4, ensure_ascii=False)