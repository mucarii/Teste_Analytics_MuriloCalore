# Importando as bibliotecas necessárias
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configurando o estilo dos gráficos
sns.set(style="whitegrid")

# Carregando o dataset limpo
df_clean = pd.read_csv("data/data_clean.csv", parse_dates=["Data"])

# Calculando o total de vendas por registro
df_clean["Total_Vendas"] = df_clean["Quantidade"] * df_clean["Preço"]

# Extraindo o mês e o ano da coluna 'Data' para análise mensal
df_clean["Ano_Mes"] = df_clean["Data"].dt.to_period("M")

# Agrupando os dados por Ano_Mes para calcular o total de vendas mensais
vendas_mensais = (
    df_clean.groupby("Ano_Mes")
    .agg(Total_Vendas=pd.NamedAgg(column="Total_Vendas", aggfunc="sum"))
    .reset_index()
)

# Convertendo 'Ano_Mes' para string para melhor visualização no gráfico
vendas_mensais["Ano_Mes"] = vendas_mensais["Ano_Mes"].astype(str)

# 1. Gráfico de Linha: Tendência de Vendas Mensais
plt.figure(figsize=(12, 6))
sns.lineplot(
    data=vendas_mensais, x="Ano_Mes", y="Total_Vendas", marker="o", color="blue"
)
plt.title("Tendência de Vendas Mensais em 2023")
plt.xlabel("Mês")
plt.ylabel("Total de Vendas (R$)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 2. Insights

# Mês com Maior Total de Vendas
mes_maior_vendas = vendas_mensais.loc[vendas_mensais["Total_Vendas"].idxmax()]
print(
    f"\nO mês com maior total de vendas foi {mes_maior_vendas['Ano_Mes']} com R${mes_maior_vendas['Total_Vendas']:.2f}."
)

print(
    " Insight 1: Setembro de 2023 foi o mes com maior desempenho de venda, atingindo um total de R$131579.67."
)

# Produto com Maior Quantidade Vendida
vendas_por_produto = (
    df_clean.groupby("Produto")
    .agg(
        Total_Vendas=pd.NamedAgg(column="Total_Vendas", aggfunc="sum"),
        Total_Quantidade=pd.NamedAgg(column="Quantidade", aggfunc="sum"),
    )
    .reset_index()
)

produto_mais_quantidade = vendas_por_produto.loc[
    vendas_por_produto["Total_Quantidade"].idxmax()
]
print(
    f"\nO produto com maior quantidade vendida foi {produto_mais_quantidade['Produto']} com {produto_mais_quantidade['Total_Quantidade']} unidades vendidas."
)

print(
    " Insight 2: O produto D é o mais popular entre os clientes, com uma quantidade vendida significativamente maior que os demais produtos."
)

# Total de Vendas e Quantidades por Categoria
vendas_por_categoria = (
    df_clean.groupby("Categoria")
    .agg(
        Total_Vendas=pd.NamedAgg(column="Total_Vendas", aggfunc="sum"),
        Total_Quantidade=pd.NamedAgg(column="Quantidade", aggfunc="sum"),
    )
    .reset_index()
)
print("\nTotal de Vendas e Quantidades Vendidas por Categoria:")
print(vendas_por_categoria.to_string(index=False))

print(
    " Insight 3: A categoria 3 lidera  Total de Vendas depois vem a categoria 1, 2 e 4. A categoria 3 tambem lidera em quantidade vendida porem a categoria 2 tem uma quantidade de maior que a 1 mesmo tendo menos vendas e a 4 tem menos vendas em geral."
)

# Média de Preço por Produto
media_preco_produto = df_clean.groupby("Produto")["Preço"].mean().reset_index()
media_preco_produto.rename(columns={"Preço": "Preco_Medio"}, inplace=True)
print("\nMédia de Preço por Produto:")
print(media_preco_produto.to_string(index=False))

print(
    "Insight 4: O produto E possui a maior média de preço, seguido por Produto C, Produto A, Produto B, e Produto D."
)

# Total de Vendas por Trimestre
df_clean["Trimestre"] = df_clean["Data"].dt.to_period("Q").astype(str)
vendas_trimestrais = (
    df_clean.groupby("Trimestre")
    .agg(Total_Vendas=pd.NamedAgg(column="Total_Vendas", aggfunc="sum"))
    .reset_index()
)
print("\nTotal de Vendas por Trimestre:")
print(vendas_trimestrais.to_string(index=False))

print(
    "Insight 5: O terceiro trimestre foi o trimestre com maior total de vendas, seguido pelo primeiro, segundo, e quarto."
)
