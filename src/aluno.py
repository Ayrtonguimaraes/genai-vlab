class Aluno:
    # Usando constantes para determinar os níveis e estilos permitidos
    NIVEIS_PERMITIDOS = ['iniciante', 'intermediário', 'avançado']
    ESTILOS_PERMITIDOS = ['visual', 'auditivo', 'leitura-escrita', 'cinestésico']

    def __init__(self, nome, idade, nivel_conhecimento, estilo_aprendizado):
        self.nome = nome
        self.idade = idade

        if nivel_conhecimento.lower() not in Aluno.NIVEIS_PERMITIDOS:
            raise ValueError(f'Erro: O nível escolhido deve ser um destes: {Aluno.NIVEIS_PERMITIDOS}')
        self.nivel_conhecimento = nivel_conhecimento.lower()

        if estilo_aprendizado.lower() not in Aluno.ESTILOS_PERMITIDOS:
            raise ValueError(f'Erro: O estilo escolhido deve ser um destes: {Aluno.ESTILOS_PERMITIDOS}')
        self.estilo_aprendizado = estilo_aprendizado.lower()

    @property
    def dados_aluno(self):
        return {
            'nome': self.nome,
            'idade': self.idade,
            'nivel_de_conhecimento': self.nivel_conhecimento,
            'estilo_de_aprendizado': self.estilo_aprendizado
        }

