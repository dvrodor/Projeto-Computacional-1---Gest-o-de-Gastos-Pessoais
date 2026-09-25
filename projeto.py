import json
from pathlib import Path
from datetime import datetime
from enum import Enum


# ============================================================
# ENUMERAÇÃO DE CATEGORIAS
# ============================================================

class Categoria(Enum):

    ALIMENTACAO = "Alimentação"
    TRANSPORTE = "Transporte"
    MORADIA = "Moradia"
    LAZER = "Lazer"
    SAUDE = "Saúde"
    EDUCACAO = "Educação"
    OUTROS = "Outros"

    @classmethod
    def listar(cls):
        return list(cls)


# ============================================================
# CLASSE DESPESA
# ============================================================

class Despesa:

    def __init__(
        self,
        id,
        descricao,
        valor,
        categoria,
        data
    ):

        self.id = id
        self.descricao = descricao
        self.valor = valor
        self.categoria = categoria
        self.data = data

        self.validar()

    # --------------------------------------------------------
    # VALIDAÇÃO
    # --------------------------------------------------------

    def validar(self):

        if not self.descricao.strip():
            raise ValueError(
                "A descrição não pode ficar vazia."
            )

        if self.valor <= 0:
            raise ValueError(
                "O valor deve ser maior que zero."
            )

        if not isinstance(self.categoria, Categoria):
            raise ValueError(
                "Categoria inválida."
            )

        try:

            datetime.strptime(
                self.data,
                "%d/%m/%Y"
            )

        except ValueError:

            raise ValueError(
                "Data inválida. Use DD/MM/AAAA."
            )

    # --------------------------------------------------------
    # CONVERTER PARA DICIONÁRIO
    # --------------------------------------------------------

    def to_dict(self):

        return {
            "id": self.id,
            "descricao": self.descricao,
            "valor": self.valor,
            "categoria": self.categoria.value,
            "data": self.data
        }

    # --------------------------------------------------------
    # CRIAR OBJETO A PARTIR DE DICIONÁRIO
    # --------------------------------------------------------

    @classmethod
    def from_dict(cls, dados):

        categoria = Categoria(dados["categoria"])

        return cls(
            id=dados["id"],
            descricao=dados["descricao"],
            valor=float(dados["valor"]),
            categoria=categoria,
            data=dados["data"]
        )

    # --------------------------------------------------------
    # REPRESENTAÇÃO DA DESPESA
    # --------------------------------------------------------

    def __str__(self):

        return (
            f"ID: {self.id} | "
            f"{self.descricao} | "
            f"R$ {self.valor:.2f} | "
            f"{self.categoria.value} | "
            f"{self.data}"
        )


# ============================================================
# CLASSE REPOSITORY
# ============================================================

class DespesaRepository:

    def __init__(
        self,
        arquivo="despesas.json"
    ):

        self.arquivo = Path(arquivo)

        self.dados = []

        self.carregar()

    # --------------------------------------------------------
    # CARREGAR DADOS
    # --------------------------------------------------------

    def carregar(self):

        if not self.arquivo.exists():

            self.dados = []

            return

        try:

            with open(
                self.arquivo,
                "r",
                encoding="utf-8"
            ) as arquivo:

                dados = json.load(arquivo)

            self.dados = [
                Despesa.from_dict(item)
                for item in dados
            ]

        except (
            json.JSONDecodeError,
            FileNotFoundError,
            KeyError,
            ValueError
        ):

            self.dados = []

    # --------------------------------------------------------
    # SALVAR DADOS
    # --------------------------------------------------------

    def salvar(self):

        dados = [
            despesa.to_dict()
            for despesa in self.dados
        ]

        with open(
            self.arquivo,
            "w",
            encoding="utf-8"
        ) as arquivo:

            json.dump(
                dados,
                arquivo,
                ensure_ascii=False,
                indent=4
            )

    # --------------------------------------------------------
    # ADICIONAR
    # --------------------------------------------------------

    def adicionar(self, despesa):

        self.dados.append(despesa)

        self.salvar()

    # --------------------------------------------------------
    # LISTAR
    # --------------------------------------------------------

    def listar(self):

        return self.dados.copy()

    # --------------------------------------------------------
    # BUSCAR POR ID
    # --------------------------------------------------------

    def buscar_por_id(self, id):

        for despesa in self.dados:

            if despesa.id == id:
                return despesa

        return None

    # --------------------------------------------------------
    # ATUALIZAR
    # --------------------------------------------------------

    def atualizar(self, despesa):

        for indice, item in enumerate(self.dados):

            if item.id == despesa.id:

                self.dados[indice] = despesa

                self.salvar()

                return True

        return False

    # --------------------------------------------------------
    # REMOVER
    # --------------------------------------------------------

    def remover(self, id):

        despesa = self.buscar_por_id(id)

        if despesa is None:
            return False

        self.dados.remove(despesa)

        self.salvar()

        return True


# ============================================================
# CLASSE DE VALIDAÇÃO
# ============================================================

class Validacao:

    # --------------------------------------------------------
    # VALIDAR VALOR
    # --------------------------------------------------------

    @staticmethod
    def valor(valor):

        try:

            valor = float(
                str(valor).replace(",", ".")
            )

            if valor <= 0:
                return False

            return True

        except ValueError:

            return False

    # --------------------------------------------------------
    # VALIDAR DATA
    # --------------------------------------------------------

    @staticmethod
    def data(data):

        try:

            datetime.strptime(
                data,
                "%d/%m/%Y"
            )

            return True

        except ValueError:

            return False

    # --------------------------------------------------------
    # VALIDAR ID
    # --------------------------------------------------------

    @staticmethod
    def id(id):

        try:

            return int(id) > 0

        except ValueError:

            return False


# ============================================================
# CLASSE CONTROLE DE DESPESAS
# ============================================================

class ControleDespesas:

    def __init__(self):

        self.repository = DespesaRepository()

    # --------------------------------------------------------
    # CADASTRAR DESPESA
    # --------------------------------------------------------

    def cadastrar_despesa(
        self,
        descricao,
        valor,
        categoria,
        data
    ):

        if not Validacao.valor(valor):

            raise ValueError(
                "Valor inválido."
            )

        if not Validacao.data(data):

            raise ValueError(
                "Data inválida."
            )

        novo_id = self._gerar_id()

        despesa = Despesa(
            id=novo_id,
            descricao=descricao,
            valor=float(valor),
            categoria=categoria,
            data=data
        )

        self.repository.adicionar(
            despesa
        )

        return despesa

    # --------------------------------------------------------
    # GERAR ID
    # --------------------------------------------------------

    def _gerar_id(self):

        despesas = self.repository.listar()

        if not despesas:

            return 1

        return max(
            despesa.id
            for despesa in despesas
        ) + 1

    # --------------------------------------------------------
    # LISTAR DESPESAS
    # --------------------------------------------------------

    def listar_despesas(self):

        return self.repository.listar()

    # --------------------------------------------------------
    # EDITAR DESPESA
    # --------------------------------------------------------

    def editar_despesa(
        self,
        id,
        descricao,
        valor,
        categoria,
        data
    ):

        despesa = self.repository.buscar_por_id(id)

        if despesa is None:

            return False

        nova_despesa = Despesa(
            id=id,
            descricao=descricao,
            valor=float(valor),
            categoria=categoria,
            data=data
        )

        return self.repository.atualizar(
            nova_despesa
        )

    # --------------------------------------------------------
    # REMOVER DESPESA
    # --------------------------------------------------------

    def remover_despesa(self, id):

        return self.repository.remover(id)

    # --------------------------------------------------------
    # CALCULAR TOTAL
    # --------------------------------------------------------

    def calcular_total(self):

        return sum(
            despesa.valor
            for despesa
            in self.repository.listar()
        )

    # --------------------------------------------------------
    # CALCULAR TOTAL POR CATEGORIA
    # --------------------------------------------------------

    def calcular_por_categoria(self):

        resultado = {}

        for categoria in Categoria:

            resultado[categoria.value] = 0

        for despesa in self.repository.listar():

            resultado[
                despesa.categoria.value
            ] += despesa.valor

        return resultado

    # --------------------------------------------------------
    # FILTRAR POR PERÍODO
    # --------------------------------------------------------

    def filtrar_por_periodo(
        self,
        data_inicial,
        data_final
    ):

        if not Validacao.data(data_inicial):

            raise ValueError(
                "Data inicial inválida."
            )

        if not Validacao.data(data_final):

            raise ValueError(
                "Data final inválida."
            )

        inicio = datetime.strptime(
            data_inicial,
            "%d/%m/%Y"
        )

        fim = datetime.strptime(
            data_final,
            "%d/%m/%Y"
        )

        if inicio > fim:

            raise ValueError(
                "A data inicial não pode "
                "ser maior que a final."
            )

        resultado = []

        for despesa in self.repository.listar():

            data_despesa = datetime.strptime(
                despesa.data,
                "%d/%m/%Y"
            )

            if inicio <= data_despesa <= fim:

                resultado.append(despesa)

        return resultado

    # --------------------------------------------------------
    # FILTRAR POR CATEGORIA
    # --------------------------------------------------------

    def filtrar_por_categoria(
        self,
        categoria
    ):

        return [
            despesa
            for despesa
            in self.repository.listar()
            if despesa.categoria == categoria
        ]

    # --------------------------------------------------------
    # GERAR RESUMO
    # --------------------------------------------------------

    def gerar_resumo(self):

        despesas = self.repository.listar()

        total = self.calcular_total()

        quantidade = len(despesas)

        if quantidade > 0:

            media = total / quantidade

        else:

            media = 0

        return {
            "quantidade": quantidade,
            "total": total,
            "media": media,
            "por_categoria":
                self.calcular_por_categoria()
        }


# ============================================================
# FUNÇÕES DA INTERFACE
# ============================================================

def mostrar_menu():

    print()
    print("=" * 60)
    print("        SISTEMA DE CONTROLE DE DESPESAS")
    print("=" * 60)

    print("1. Cadastrar despesa")
    print("2. Listar despesas")
    print("3. Editar despesa")
    print("4. Remover despesa")
    print("5. Filtrar por categoria")
    print("6. Filtrar por período")
    print("7. Resumo financeiro")
    print("0. Sair")

    print("=" * 60)


# ============================================================
# ESCOLHER CATEGORIA
# ============================================================

def escolher_categoria():

    categorias = Categoria.listar()

    print("\nCategorias:")

    for indice, categoria in enumerate(
        categorias,
        start=1
    ):

        print(
            f"{indice}. {categoria.value}"
        )

    while True:

        try:

            opcao = int(
                input(
                    "\nEscolha uma categoria: "
                )
            )

            if 1 <= opcao <= len(categorias):

                return categorias[
                    opcao - 1
                ]

            print(
                "Escolha uma opção válida."
            )

        except ValueError:

            print(
                "Digite apenas números."
            )


# ============================================================
# CADASTRAR
# ============================================================

def cadastrar(controle):

    print("\n")
    print("=" * 60)
    print("CADASTRAR DESPESA")
    print("=" * 60)

    descricao = input(
        "Descrição: "
    ).strip()

    if not descricao:

        print(
            "A descrição não pode ficar vazia."
        )

        return

    while True:

        valor = input(
            "Valor: R$ "
        ).strip()

        if Validacao.valor(valor):

            valor = float(
                valor.replace(",", ".")
            )

            break

        print(
            "Digite um valor válido."
        )

    categoria = escolher_categoria()

    while True:

        data = input(
            "Data (DD/MM/AAAA): "
        ).strip()

        if Validacao.data(data):

            break

        print(
            "Data inválida."
        )

    try:

        despesa = controle.cadastrar_despesa(
            descricao,
            valor,
            categoria,
            data
        )

        print()
        print(
            f"Despesa cadastrada com sucesso!"
        )

        print(
            f"ID: {despesa.id}"
        )

    except ValueError as erro:

        print(
            f"Erro: {erro}"
        )


# ============================================================
# LISTAR
# ============================================================

def listar(controle):

    despesas = (
        controle.listar_despesas()
    )

    print("\n")
    print("=" * 80)
    print("LISTA DE DESPESAS")
    print("=" * 80)

    if not despesas:

        print(
            "Nenhuma despesa cadastrada."
        )

        return

    for despesa in despesas:

        print(despesa)

    print("=" * 80)

    print(
        f"Total: "
        f"R$ {controle.calcular_total():.2f}"
    )


# ============================================================
# EDITAR
# ============================================================

def editar(controle):

    print("\n")
    print("=" * 60)
    print("EDITAR DESPESA")
    print("=" * 60)

    try:

        id = int(
            input(
                "Digite o ID da despesa: "
            )
        )

    except ValueError:

        print(
            "ID inválido."
        )

        return

    despesas = (
        controle.listar_despesas()
    )

    despesa = None

    for item in despesas:

        if item.id == id:

            despesa = item

            break

    if despesa is None:

        print(
            "Despesa não encontrada."
        )

        return

    print("\nDados atuais:")

    print(
        f"Descrição: "
        f"{despesa.descricao}"
    )

    print(
        f"Valor: "
        f"R$ {despesa.valor:.2f}"
    )

    print(
        f"Categoria: "
        f"{despesa.categoria.value}"
    )

    print(
        f"Data: "
        f"{despesa.data}"
    )

    print(
        "\nDigite os novos dados."
    )

    print(
        "Pressione ENTER para manter "
        "o valor atual."
    )

    descricao = input(
        f"Descrição [{despesa.descricao}]: "
    ).strip()

    if not descricao:

        descricao = despesa.descricao

    valor = input(
        f"Valor [{despesa.valor:.2f}]: "
    ).strip()

    if valor:

        if not Validacao.valor(valor):

            print(
                "Valor inválido."
            )

            return

        valor = float(
            valor.replace(",", ".")
        )

    else:

        valor = despesa.valor

    alterar = input(
        "\nDeseja alterar a categoria? "
        "(S/N): "
    ).strip().upper()

    if alterar == "S":

        categoria = escolher_categoria()

    else:

        categoria = despesa.categoria

    data = input(
        f"Data [{despesa.data}]: "
    ).strip()

    if not data:

        data = despesa.data

    if not Validacao.data(data):

        print(
            "Data inválida."
        )

        return

    try:

        sucesso = controle.editar_despesa(
            id,
            descricao,
            valor,
            categoria,
            data
        )

        if sucesso:

            print(
                "\nDespesa atualizada com sucesso!"
            )

        else:

            print(
                "\nNão foi possível atualizar."
            )

    except ValueError as erro:

        print(
            f"Erro: {erro}"
        )


# ============================================================
# REMOVER
# ============================================================

def remover(controle):

    print("\n")
    print("=" * 60)
    print("REMOVER DESPESA")
    print("=" * 60)

    try:

        id = int(
            input(
                "Digite o ID da despesa: "
            )
        )

    except ValueError:

        print(
            "ID inválido."
        )

        return

    despesa = None

    for item in controle.listar_despesas():

        if item.id == id:

            despesa = item

            break

    if despesa is None:

        print(
            "Despesa não encontrada."
        )

        return

    print()
    print(despesa)

    confirmacao = input(
        "\nDeseja realmente remover? "
        "(S/N): "
    ).strip().upper()

    if confirmacao == "S":

        sucesso = (
            controle.remover_despesa(id)
        )

        if sucesso:

            print(
                "\nDespesa removida com sucesso!"
            )

        else:

            print(
                "\nErro ao remover despesa."
            )

    else:

        print(
            "\nOperação cancelada."
        )


# ============================================================
# FILTRAR POR CATEGORIA
# ============================================================

def filtrar_categoria(controle):

    print("\n")
    print("=" * 60)
    print("FILTRAR POR CATEGORIA")
    print("=" * 60)

    categoria = escolher_categoria()

    despesas = (
        controle.filtrar_por_categoria(
            categoria
        )
    )

    if not despesas:

        print(
            "\nNenhuma despesa encontrada."
        )

        return

    total = 0

    print()
    print(
        f"Despesas de "
        f"{categoria.value}:"
    )

    print("-" * 60)

    for despesa in despesas:

        print(despesa)

        total += despesa.valor

    print("-" * 60)

    print(
        f"Total: R$ {total:.2f}"
    )


# ============================================================
# FILTRAR POR PERÍODO
# ============================================================

def filtrar_periodo(controle):

    print("\n")
    print("=" * 60)
    print("FILTRAR POR PERÍODO")
    print("=" * 60)

    data_inicial = input(
        "Data inicial (DD/MM/AAAA): "
    ).strip()

    data_final = input(
        "Data final (DD/MM/AAAA): "
    ).strip()

    try:

        despesas = (
            controle.filtrar_por_periodo(
                data_inicial,
                data_final
            )
        )

    except ValueError as erro:

        print(
            f"\nErro: {erro}"
        )

        return

    if not despesas:

        print(
            "\nNenhuma despesa encontrada."
        )

        return

    total = 0

    print()
    print(
        f"Despesas entre "
        f"{data_inicial} e {data_final}:"
    )

    print("-" * 80)

    for despesa in despesas:

        print(despesa)

        total += despesa.valor

    print("-" * 80)

    print(
        f"Total do período: "
        f"R$ {total:.2f}"
    )


# ============================================================
# RESUMO FINANCEIRO
# ============================================================

def resumo(controle):

    print("\n")
    print("=" * 60)
    print("RESUMO FINANCEIRO")
    print("=" * 60)

    dados = (
        controle.gerar_resumo()
    )

    print(
        f"Quantidade de despesas: "
        f"{dados['quantidade']}"
    )

    print(
        f"Total gasto: "
        f"R$ {dados['total']:.2f}"
    )

    print(
        f"Média das despesas: "
        f"R$ {dados['media']:.2f}"
    )

    print("\nGastos por categoria:")

    print("-" * 60)

    for categoria, valor in (
        dados["por_categoria"].items()
    ):

        print(
            f"{categoria}: "
            f"R$ {valor:.2f}"
        )

    print("=" * 60)


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():

    controle = ControleDespesas()

    while True:

        mostrar_menu()

        opcao = input(
            "Escolha uma opção: "
        ).strip()

        if opcao == "1":

            cadastrar(controle)

        elif opcao == "2":

            listar(controle)

        elif opcao == "3":

            editar(controle)

        elif opcao == "4":

            remover(controle)

        elif opcao == "5":

            filtrar_categoria(
                controle
            )

        elif opcao == "6":

            filtrar_periodo(
                controle
            )

        elif opcao == "7":

            resumo(controle)

        elif opcao == "0":

            print()
            print(
                "Sistema encerrado."
            )

            break

        else:

            print(
                "\nOpção inválida."
            )

        input(
            "\nPressione ENTER para continuar..."
        )


# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":

    main()
