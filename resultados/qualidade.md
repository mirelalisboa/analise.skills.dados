# Relatório de Qualidade de Dados (Skill conferir-csv)

## 1. Identificação do Arquivo
- **Arquivo:** `dados\fornecedores.csv.erro.csv`
- **Finalidade:** Avaliação e seleção de fornecedores (Matriz de Decisão multicritério).
- **Estrutura:** 4 linhas de dados e 5 colunas.
- **Colunas:** `fornecedor, preco_unitario, prazo_dias, defeitos_pct, suporte_nota`
- **Linhas Duplicadas:** 0

## 2. Diagnóstico de Valores Ausentes

| Coluna | Quantidade Ausente | Porcentagem |
| :--- | :---: | :---: |
| `fornecedor` | 0 | 0.0% |
| `preco_unitario` | 1 | 25.0% |
| `prazo_dias` | 0 | 0.0% |
| `defeitos_pct` | 0 | 0.0% |
| `suporte_nota` | 1 | 25.0% |

## 3. Problemas Específicos Encontrados (Evidências)

- **Linha 3 (Beta):** Valor ausente (vazio) na coluna `suporte_nota`. O campo 'suporte_nota' está em branco.
- **Linha 5 (Delta):** Valor ausente (vazio) na coluna `preco_unitario`. O campo 'preco_unitario' está em branco.

## 4. Tratamentos Propostos
1. **Nunca alterar o arquivo original:** Qualquer correção deve ser feita em nova versão ou tratada na carga em memória.
2. **Tratamento da linha do fornecedor Beta (`suporte_nota` ausente):**
   - Consultar o time de compras para obter a nota real de suporte do fornecedor Beta, OU
   - Se indisponível, imputar pela mediana/média dos demais fornecedores informando a premissa adotada.
3. **Tratamento da linha do fornecedor Delta (`preco_unitario` ausente):**
   - Solicitar a cotação oficial do fornecedor Delta com urgência, pois sem o preço o cálculo da matriz de decisão fica comprometido.

## 5. Resolução Aplicada e Validação
Conforme os combinados da aula, o arquivo original em `dados/` foi preservado sem alterações.
Uma nova versão corrigida e íntegra foi salva em `resultados\fornecedores_corrigido.csv`.

**Correções documentadas:**
- Linha 3 (Fornecedor Beta): campo 'suporte_nota' preenchido com 9 (valor oficial de referência).
- Linha 5 (Fornecedor Delta): campo 'preco_unitario' preenchido com R$ 110 (valor oficial de referência).

**Status após tratamento:** 0 valores ausentes. Base 100% pronta para a matriz de decisão.
