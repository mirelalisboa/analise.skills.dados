# Relatório de Avaliação de Fornecedores (Decision Matrix)

## 1. Contexto e Objetivo
Seleção do melhor fornecedor utilizando matriz de decisão multicritério e gráficos da skill `chart-image`.

## 2. Critérios e Pesos
- **Preço Unitário (25%):** Menor custo por unidade (R$).
- **Prazo de Entrega (25%):** Menor tempo de resposta (dias).
- **Qualidade (25%):** Menor índice de defeitos (%).
- **Suporte (25%):** Atendimento e assistência técnica (0 a 10).

## 3. Matriz de Decisão Normalizada

| Rank | Fornecedor | Preço (25%) | Prazo (25%) | Qualidade (25%) | Suporte (25%) | **Nota Final Ponderada** |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| #1 | **Delta** | 7.73 | 10.0 | 10.0 | 10.0 | **9.43** |
| #2 | **Beta** | 8.5 | 8.0 | 5.0 | 9.47 | **7.74** |
| #3 | **Alfa** | 9.44 | 5.0 | 2.5 | 8.42 | **6.34** |
| #4 | **Gama** | 10.0 | 3.33 | 1.25 | 6.32 | **5.22** |

## 4. Gráficos Gerados
- `grafico_fornecedores.png`: Comparativo de notas finais e detalhamento por critério.
- `grafico_radar_fornecedores.png`: Gráfico radar/teia de aranha multicritério.
- `grafico_tradeoff_fornecedores.png`: Dispersão de Trade-off (Preço vs. Defeitos vs. Prazo).
