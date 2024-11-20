# Importando as bibliotecas
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Definindo uma seed para reprodutibilidade
random.seed(15)
np.random.seed(15)

# 1. Criação do Dataset de Vendas


# Função para gerar datas
def gerar_datas(inicio, fim, n):
    inicio_dt = datetime.strptime(inicio, "%d/%m/%Y")
    fim_dt = datetime.strptime(fim, "%d/%m/%Y")
    delta = fim_dt - inicio_dt
    return [inicio_dt + timedelta(days=random.randint(0, delta.days)) for _ in range(n)]


# Listas de produtos e categorias
produtos = ["Produto A", "Produto B", "Produto C", "Produto D", "Produto E"]
categorias = ["Categoria 1", "Categoria 2", "Categoria 3", "Categoria 4"]

# Número de registros
n_registros = 200

# Gerando os dados
dados = {
    "ID": range(1, n_registros + 1),
    "Data": gerar_datas("01/01/2023", "31/12/2023", n_registros),
    "Produto": [random.choice(produtos) for _ in range(n_registros)],
    "Categoria": [random.choice(categorias) for _ in range(n_registros)],
    "Quantidade": [random.randint(1, 50) for _ in range(n_registros)],
    "Preço": [round(random.uniform(10.0, 500.0), 2) for _ in range(n_registros)],
}

# Criando o DataFrame
df = pd.DataFrame(dados)

# Introduzindo valores faltantes aleatoriamente (5% de cada coluna)
for coluna in ["Produto", "Categoria", "Quantidade", "Preço"]:
    df.loc[df.sample(frac=0.05, random_state=42).index, coluna] = np.nan

# Introduzindo duplicatas (10% dos dados)
duplicatas = df.sample(frac=0.10, random_state=42)
df = pd.concat([df, duplicatas], ignore_index=True)

# Salvando o dataset simulado
df.to_csv("data/vendas_dataset.csv", index=False)

# 2. Limpeza dos Dados

# Carregando o dataset
df_limpo = pd.read_csv("data/vendas_dataset.csv")

# Tratamento de valores faltantes
df_limpo.dropna(inplace=True)  # Removemos as linhas com valore faltantes

# Remoção de duplicatas
df_limpo.drop_duplicates(inplace=True)

# Conversão de tipos de dados
# Garantindo que a coluna 'Data' esteja no formato datetime
df_limpo["Data"] = pd.to_datetime(df_limpo["Data"], format="%Y-%m-%d")

# Garantindo que 'Quantidade' seja inteiro e 'Preço' seja float
df_limpo["Quantidade"] = df_limpo["Quantidade"].astype(int)
df_limpo["Preço"] = df_limpo["Preço"].astype(float)

# Salvando o dataset limpo
df_limpo.to_csv("data/data_clean.csv", index=False)

# 3. Análise dos Dados Limpos

# Carregando o dataset limpo
df_clean = pd.read_csv("data/data_clean.csv")

# Calculando o total de vendas por produto
df_clean["Total_Vendas"] = df_clean["Quantidade"] * df_clean["Preço"]
vendas_por_produto = df_clean.groupby("Produto")["Total_Vendas"].sum().reset_index()

# Identificando o produto com o maior número de vendas totais
produto_mais_vendido = vendas_por_produto.loc[
    vendas_por_produto["Total_Vendas"].idxmax()
]

# Exibindo os resultados
print("\nTotal de Vendas por Produto:")
print(vendas_por_produto.to_string(index=False))

print(
    f"\nProduto com o maior total de vendas: {produto_mais_vendido['Produto']}, Total de Vendas: R${produto_mais_vendido['Total_Vendas']:.2f}"
)
