import csv
import os

# Caminho do arquivo a ser verificado
caminho_arquivo = os.path.join("dados", "fornecedores.csv.erro.csv")

# 1. Carregar dados brutos
linhas = []
with open(caminho_arquivo, mode="r", encoding="utf-8") as f:
    reader = csv.reader(f)
    cabecalho = next(reader)
    for num_linha, row in enumerate(reader, start=2):
        linhas.append((num_linha, row))

total_linhas = len(linhas)
total_colunas = len(cabecalho)

# 2. Verificação de valores ausentes, tipos e inconsistências
valores_ausentes = {col: 0 for col in cabecalho}
problemas = []
linhas_duplicadas = 0
vistos = set()

for num_linha, row in linhas:
    # Checar duplicatas
    tupla_row = tuple(row)
    if tupla_row in vistos:
        linhas_duplicadas += 1
    vistos.add(tupla_row)
    
    # Checar cada coluna
    for i, col in enumerate(cabecalho):
        if i >= len(row):
            valor = ""
        else:
            valor = row[i].strip()
        
        # Ausência: vazio ou apenas espaços
        if valor == "":
            valores_ausentes[col] += 1
            problemas.append({
                "linha": num_linha,
                "fornecedor": row[0] if len(row) > 0 else "Desconhecido",
                "coluna": col,
                "tipo_problema": "Valor ausente (vazio)",
                "detalhes": f"O campo '{col}' está em branco."
            })
        else:
            # Para colunas numéricas, verificar conversão
            if col in ["preco_unitario", "prazo_dias", "defeitos_pct", "suporte_nota"]:
                try:
                    num = float(valor)
                    # Checagens de regras de negócio
                    if col == "preco_unitario" and num <= 0:
                        problemas.append({
                            "linha": num_linha,
                            "fornecedor": row[0],
                            "coluna": col,
                            "tipo_problema": "Valor inválido",
                            "detalhes": f"Preço deve ser maior que zero (valor encontrado: {num})."
                        })
                    if col == "prazo_dias" and num <= 0:
                        problemas.append({
                            "linha": num_linha,
                            "fornecedor": row[0],
                            "coluna": col,
                            "tipo_problema": "Valor inválido",
                            "detalhes": f"Prazo deve ser maior que zero (valor encontrado: {num})."
                        })
                    if col == "defeitos_pct" and (num < 0 or num > 100):
                        problemas.append({
                            "linha": num_linha,
                            "fornecedor": row[0],
                            "coluna": col,
                            "tipo_problema": "Valor fora da faixa",
                            "detalhes": f"Percentual de defeitos deve estar entre 0 e 100% (valor: {num})."
                        })
                    if col == "suporte_nota" and (num < 0 or num > 10):
                        problemas.append({
                            "linha": num_linha,
                            "fornecedor": row[0],
                            "coluna": col,
                            "tipo_problema": "Valor fora da faixa",
                            "detalhes": f"Nota de suporte deve estar entre 0 e 10 (valor: {num})."
                        })
                except ValueError:
                    problemas.append({
                        "linha": num_linha,
                        "fornecedor": row[0],
                        "coluna": col,
                        "tipo_problema": "Tipo incorreto",
                        "detalhes": f"Esperado número, mas encontrado texto: '{valor}'."
                    })

# 3. Exibir no terminal os resultados calculados
print("=== RELATÓRIO DE QUALIDADE (SKILL CONFERIR-CSV) ===")
print(f"Arquivo analisado: {caminho_arquivo}")
print(f"Total de registros: {total_linhas}")
print(f"Total de colunas: {total_colunas} -> {', '.join(cabecalho)}")
print(f"Linhas duplicadas: {linhas_duplicadas}")
print("\nValores ausentes por coluna:")
for col, contagem in valores_ausentes.items():
    print(f" - {col}: {contagem} ausente(s)")

print(f"\nTotal de problemas encontrados: {len(problemas)}")
for p in problemas:
    print(f" [ALERTA] Linha {p['linha']} (Fornecedor: {p['fornecedor']}): {p['tipo_problema']} na coluna '{p['coluna']}' -> {p['detalhes']}")

# 4. Salvar resultados/qualidade.md conforme a regra da skill conferir-csv
os.makedirs("resultados", exist_ok=True)
caminho_qualidade = os.path.join("resultados", "qualidade.md")
with open(caminho_qualidade, "w", encoding="utf-8") as f:
    f.write("# Relatório de Qualidade de Dados (Skill conferir-csv)\n\n")
    f.write("## 1. Identificação do Arquivo\n")
    f.write(f"- **Arquivo:** `{caminho_arquivo}`\n")
    f.write("- **Finalidade:** Avaliação e seleção de fornecedores (Matriz de Decisão multicritério).\n")
    f.write(f"- **Estrutura:** {total_linhas} linhas de dados e {total_colunas} colunas.\n")
    f.write(f"- **Colunas:** `{', '.join(cabecalho)}`\n")
    f.write(f"- **Linhas Duplicadas:** {linhas_duplicadas}\n\n")
    
    f.write("## 2. Diagnóstico de Valores Ausentes\n\n")
    f.write("| Coluna | Quantidade Ausente | Porcentagem |\n")
    f.write("| :--- | :---: | :---: |\n")
    for col, contagem in valores_ausentes.items():
        pct = (contagem / total_linhas) * 100 if total_linhas > 0 else 0
        f.write(f"| `{col}` | {contagem} | {pct:.1f}% |\n")
    
    f.write("\n## 3. Problemas Específicos Encontrados (Evidências)\n\n")
    if problemas:
        for p in problemas:
            f.write(f"- **Linha {p['linha']} ({p['fornecedor']}):** {p['tipo_problema']} na coluna `{p['coluna']}`. {p['detalhes']}\n")
    else:
        f.write("Nenhum problema encontrado nos registros.\n")
        
    f.write("\n## 4. Tratamentos Propostos\n")
    f.write("1. **Nunca alterar o arquivo original:** Qualquer correção deve ser feita em nova versão ou tratada na carga em memória.\n")
    f.write("2. **Tratamento da linha do fornecedor Beta (`suporte_nota` ausente):**\n")
    f.write("   - Consultar o time de compras para obter a nota real de suporte do fornecedor Beta, OU\n")
    f.write("   - Se indisponível, imputar pela mediana/média dos demais fornecedores informando a premissa adotada.\n")
    f.write("3. **Tratamento da linha do fornecedor Delta (`preco_unitario` ausente):**\n")
    f.write("   - Solicitar a cotação oficial do fornecedor Delta com urgência, pois sem o preço o cálculo da matriz de decisão fica comprometido.\n")

print(f"\nResumo de qualidade gravado com sucesso em: {caminho_qualidade}")

