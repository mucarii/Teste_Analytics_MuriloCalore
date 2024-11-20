-- Consulta 1: Listar o nome do produto, categoria e a soma total de vendas para cada produto.
-- Ordenar o resultado pelo valor total de vendas em ordem decrescente.

SELECT 
    Produto,
    Categoria,
    SUM(Quantidade * Preço) AS Total_Vendas
FROM 
    vendas
GROUP BY 
    Produto, 
    Categoria
ORDER BY 
    Total_Vendas DESC;

-- Explicação da Lógica:
-- 1. Selecionamos as colunas 'Produto' e 'Categoria' para identificar cada produto e sua categoria.
-- 2. Calculamos a soma total de vendas multiplicando 'Quantidade' por 'Preço' para cada registro e agrupamos por 'Produto' e 'Categoria'.
-- 3. Ordenamos os resultados pelo 'Total_Vendas' em ordem decrescente para identificar os produtos com maior desempenho de vendas.

------------------------------------------------------------------

-- Consulta 2: Identificar os produtos que venderam menos no mês de junho de 2024.

SELECT 
    Produto,
    SUM(Quantidade * Preço) AS Total_Vendas_Junho_2024
FROM 
    vendas
WHERE 
    YEAR(Data) = 2024 AND MONTH(Data) = 6
GROUP BY 
    Produto
HAVING 
    SUM(Quantidade * Preço) = (
        SELECT MIN(Sub_Total_Vendas)
        FROM (
            SELECT 
                Produto, 
                SUM(Quantidade * Preço) AS Sub_Total_Vendas
            FROM 
                vendas
            WHERE 
                YEAR(Data) = 2024 AND MONTH(Data) = 6
            GROUP BY 
                Produto
        ) AS Sub_Query
    );

-- Explicação da Lógica:
-- 1. Filtramos os registros de vendas ocorridas em junho de 2024 usando as funções YEAR() e MONTH().
-- 2. Agrupamos os dados por 'Produto' e calculamos o 'Total_Vendas_Junho_2024' para cada produto.
-- 3. Utilizamos a cláusula HAVING para selecionar apenas os produtos cujo 'Total_Vendas_Junho_2024' é igual ao valor mínimo de vendas desse mês.
-- 4. A subconsulta dentro do HAVING encontra o menor total de vendas entre todos os produtos vendidos em junho de 2024.
-- 5. O resultado será os produtos que tiveram o menor desempenho de vendas nesse período específico.
