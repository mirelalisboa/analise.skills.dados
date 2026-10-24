import csv
import os
import numpy as np
import matplotlib.pyplot as plt

# 1. Garantir que a pasta resultados/ existe conforme os combinados
os.makedirs("resultados", exist_ok=True)

# 2. Carregar os dados originais (somente leitura de dados/fornecedores.csv.csv)
caminho_dados = os.path.join("dados", "fornecedores.csv.csv")
dados = []

with open(caminho_dados, mode="r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        dados.append({
            "fornecedor": row["fornecedor"],
            "preco": float(row["preco_unitario"]),
            "prazo": float(row["prazo_dias"]),
            "defeitos": float(row["defeitos_pct"]),
            "suporte": float(row["suporte_nota"])
        })

# 3. Critérios e pesos da Matriz de Decisão (Decision-Matrix)
pesos = {
    "preco": 0.25,      # 25%
    "prazo": 0.25,      # 25%
    "qualidade": 0.25,  # 25% (menor taxa de defeitos)
    "suporte": 0.25     # 25% (nota do atendimento)
}

# Referências para normalização (escala de 1 a 10)
melhor_preco = min(d["preco"] for d in dados)
melhor_prazo = min(d["prazo"] for d in dados)
melhor_defeitos = min(d["defeitos"] for d in dados)
melhor_suporte = max(d["suporte"] for d in dados)

# 4. Cálculo das notas normalizadas (1 a 10) e nota ponderada final
resultados = []
for d in dados:
    nota_preco = 10.0 * (melhor_preco / d["preco"])
    nota_prazo = 10.0 * (melhor_prazo / d["prazo"])
    nota_qualidade = 10.0 * (melhor_defeitos / d["defeitos"])
    nota_suporte = 10.0 * (d["suporte"] / melhor_suporte)
    
    pontuacao_total = (
        nota_preco * pesos["preco"] +
        nota_prazo * pesos["prazo"] +
        nota_qualidade * pesos["qualidade"] +
        nota_suporte * pesos["suporte"]
    )
    
    resultados.append({
        "fornecedor": d["fornecedor"],
        "preco_original": d["preco"],
        "prazo_original": d["prazo"],
        "defeitos_original": d["defeitos"],
        "suporte_original": d["suporte"],
        "nota_preco": round(nota_preco, 2),
        "nota_prazo": round(nota_prazo, 2),
        "nota_qualidade": round(nota_qualidade, 2),
        "nota_suporte": round(nota_suporte, 2),
        "pontuacao_total": round(pontuacao_total, 2)
    })

resultados.sort(key=lambda x: x["pontuacao_total"], reverse=True)
for rank, item in enumerate(resultados, 1):
    item["rank"] = rank

melhor = resultados[0]

# Exibição no terminal
print("=== MATRIZ DE DECISÃO - RESULTADO DOS FORNECEDORES ===")
for r in resultados:
    print(f"#{r['rank']} {r['fornecedor']}: Nota Final = {r['pontuacao_total']} "
          f"(Preço: {r['nota_preco']}, Prazo: {r['nota_prazo']}, Qualidade: {r['nota_qualidade']}, Suporte: {r['nota_suporte']})")
print(f"\n>> Fornecedor Vencedor: {melhor['fornecedor']} (Nota: {melhor['pontuacao_total']}/10.0) <<\n")

# 5. Salvar resumo em resultados/melhor_fornecedor.txt
with open(os.path.join("resultados", "melhor_fornecedor.txt"), "w", encoding="utf-8") as f:
    f.write(f"Melhor Fornecedor: {melhor['fornecedor']}\n")
    f.write(f"Pontuação Final Ponderada: {melhor['pontuacao_total']} / 10.0\n")
    f.write(f"Preço Unitário: R$ {melhor['preco_original']:.2f}\n")
    f.write(f"Prazo de Entrega: {melhor['prazo_original']:.0f} dias\n")
    f.write(f"Taxa de Defeitos: {melhor['defeitos_original']:.1f}%\n")
    f.write(f"Nota de Suporte: {melhor['suporte_original']:.1f} / 10.0\n")

# 6. Salvar relatório Markdown em resultados/relatorio_fornecedores.md
with open(os.path.join("resultados", "relatorio_fornecedores.md"), "w", encoding="utf-8") as f:
    f.write("# Relatório de Avaliação de Fornecedores (Decision Matrix)\n\n")
    f.write("## 1. Contexto e Objetivo\n")
    f.write("Seleção do melhor fornecedor utilizando matriz de decisão multicritério e gráficos da skill `chart-image`.\n\n")
    f.write("## 2. Critérios e Pesos\n")
    f.write("- **Preço Unitário (25%):** Menor custo por unidade (R$).\n")
    f.write("- **Prazo de Entrega (25%):** Menor tempo de resposta (dias).\n")
    f.write("- **Qualidade (25%):** Menor índice de defeitos (%).\n")
    f.write("- **Suporte (25%):** Atendimento e assistência técnica (0 a 10).\n\n")
    f.write("## 3. Matriz de Decisão Normalizada\n\n")
    f.write("| Rank | Fornecedor | Preço (25%) | Prazo (25%) | Qualidade (25%) | Suporte (25%) | **Nota Final Ponderada** |\n")
    f.write("| :---: | :--- | :---: | :---: | :---: | :---: | :---: |\n")
    for r in resultados:
        f.write(f"| #{r['rank']} | **{r['fornecedor']}** | {r['nota_preco']} | {r['nota_prazo']} | {r['nota_qualidade']} | {r['nota_suporte']} | **{r['pontuacao_total']}** |\n")
    f.write("\n## 4. Gráficos Gerados\n")
    f.write("- `grafico_fornecedores.png`: Comparativo de notas finais e detalhamento por critério.\n")
    f.write("- `grafico_radar_fornecedores.png`: Gráfico radar/teia de aranha multicritério.\n")
    f.write("- `grafico_tradeoff_fornecedores.png`: Dispersão de Trade-off (Preço vs. Defeitos vs. Prazo).\n")

# ==============================================================================
# APLICAÇÃO DA SKILL CHART-IMAGE: GRÁFICOS DE QUALIDADE PARA PUBLICAÇÃO
# ==============================================================================
# Paleta de cores profissional e consistente
cor_destaque = "#1b5e20"  # Verde escuro para o vencedor
cores_barras = ["#2e7d32", "#1565c0", "#e65100", "#c62828"]
nomes = [r["fornecedor"] for r in resultados]
totais = [r["pontuacao_total"] for r in resultados]

# --- GRÁFICO 1 (MELHORADO): Comparativo Geral + Critérios Lado a Lado ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), dpi=300)

# Subgráfico 1: Barras do Total com destaque no vencedor
barras = ax1.bar(nomes, totais, color=cores_barras, width=0.55, edgecolor="#333333", linewidth=0.8)
for barra in barras:
    yval = barra.get_height()
    ax1.text(barra.get_x() + barra.get_width() / 2, yval + 0.25, f"{yval:.2f}",
             ha="center", va="bottom", fontsize=10, fontweight="bold")

ax1.set_ylim(0, 11.5)
ax1.set_ylabel("Nota Ponderada Final (escala 0 a 10)", fontsize=11, fontweight="bold")
ax1.set_title("A. Ranking Geral Ponderado (Pesos Iguais 25%)", fontsize=12, fontweight="bold", pad=12)
ax1.grid(axis="y", linestyle=":", alpha=0.6)
ax1.axhline(melhor["pontuacao_total"], color="darkgreen", linestyle="--", alpha=0.5, label="Maior Pontuação")
ax1.legend(loc="upper right", frameon=True)

# Subgráfico 2: Desempenho individual por critério
pos = np.arange(len(nomes))
largura = 0.18
ax2.bar(pos - 1.5 * largura, [r["nota_preco"] for r in resultados], largura, label="Preço (R$)", color="#0288d1")
ax2.bar(pos - 0.5 * largura, [r["nota_prazo"] for r in resultados], largura, label="Prazo (dias)", color="#f57c00")
ax2.bar(pos + 0.5 * largura, [r["nota_qualidade"] for r in resultados], largura, label="Qualidade (defeitos %)", color="#388e3c")
ax2.bar(pos + 1.5 * largura, [r["nota_suporte"] for r in resultados], largura, label="Suporte (nota)", color="#7b1fa2")

ax2.set_xticks(pos)
ax2.set_xticklabels(nomes, fontsize=11, fontweight="bold")
ax2.set_ylim(0, 11.5)
ax2.set_ylabel("Nota Normalizada (0 a 10)", fontsize=11, fontweight="bold")
ax2.set_title("B. Notas Individuais por Critério", fontsize=12, fontweight="bold", pad=12)
ax2.grid(axis="y", linestyle=":", alpha=0.6)
ax2.legend(loc="upper right", frameon=True, fontsize=9)

fig.suptitle("Avaliação Integrada de Fornecedores - Matriz de Decisão", fontsize=15, fontweight="bold", y=0.98)
fig.text(0.5, 0.01, "Fonte: dados/fornecedores.csv.csv | Análise segundo metodologia decision-matrix e chart-image",
         ha="center", fontsize=9, color="#555555", style="italic")
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
caminho_g1 = os.path.join("resultados", "grafico_fornecedores.png")
plt.savefig(caminho_g1, dpi=300)
plt.close()

# --- GRÁFICO 2 (NOVO): Gráfico Radar / Teia de Aranha Multicritério ---
categorias = ["Preço", "Prazo", "Qualidade\n(Menos Defeitos)", "Suporte"]
num_vars = len(categorias)
angulos = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
angulos += angulos[:1]  # Fechar o polígono circular

fig_radar, ax_radar = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True), dpi=300)

estilos = [
    {"cor": "#2e7d32", "linha": "-", "marcador": "o"},   # Delta
    {"cor": "#1565c0", "linha": "--", "marcador": "s"},  # Beta
    {"cor": "#e65100", "linha": "-.", "marcador": "^"},  # Alfa
    {"cor": "#c62828", "linha": ":", "marcador": "d"}    # Gama
]

for idx, r in enumerate(resultados):
    valores = [r["nota_preco"], r["nota_prazo"], r["nota_qualidade"], r["nota_suporte"]]
    valores += valores[:1]
    estilo = estilos[idx % len(estilos)]
    ax_radar.plot(angulos, valores, linewidth=2, linestyle=estilo["linha"],
                  marker=estilo["marcador"], label=f"{r['fornecedor']} (Nota {r['pontuacao_total']})", color=estilo["cor"])
    ax_radar.fill(angulos, valores, color=estilo["cor"], alpha=0.10)

ax_radar.set_xticks(angulos[:-1])
ax_radar.set_xticklabels(categorias, fontsize=11, fontweight="bold")
ax_radar.set_ylim(0, 10.5)
ax_radar.set_yticks([2, 4, 6, 8, 10])
ax_radar.set_yticklabels(["2", "4", "6", "8", "10"], fontsize=9, color="#555555")
ax_radar.set_title("Perfil Multidimensional dos Fornecedores (Gráfico Radar)", fontsize=14, fontweight="bold", pad=25)
ax_radar.legend(loc="upper right", bbox_to_anchor=(1.25, 1.1), frameon=True, fontsize=10)

fig_radar.text(0.5, 0.02, "Fonte: dados/fornecedores.csv.csv | Escala normalizada de 0 a 10 (quanto maior a área, melhor o fornecedor)",
               ha="center", fontsize=9, color="#555555", style="italic")
plt.tight_layout()
caminho_g2 = os.path.join("resultados", "grafico_radar_fornecedores.png")
plt.savefig(caminho_g2, dpi=300, bbox_inches="tight")
plt.close()

# --- GRÁFICO 3 (NOVO): Dispersão de Trade-off (Preço vs. Defeitos vs. Prazo) ---
fig_scatter, ax_scatter = plt.subplots(figsize=(9, 6), dpi=300)

for r in resultados:
    # O tamanho da bolha representa o prazo em dias (quanto maior a bolha, maior o prazo de entrega)
    tamanho_bolha = r["prazo_original"] * 65
    cor = "#2e7d32" if r["fornecedor"] == melhor["fornecedor"] else "#1565c0"
    
    ax_scatter.scatter(r["preco_original"], r["defeitos_original"], s=tamanho_bolha,
                       color=cor, alpha=0.7, edgecolors="#222222", linewidth=1.5)
    
    # Rótulo de texto explicativo em cada ponto
    ax_scatter.annotate(
        f"{r['fornecedor']}\n(R$ {r['preco_original']:.0f} | {r['defeitos_original']}% def. | {r['prazo_original']:.0f} dias)",
        xy=(r["preco_original"], r["defeitos_original"]),
        xytext=(0, 14),
        textcoords="offset points",
        ha="center", fontsize=9, fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#cccccc", alpha=0.85)
    )

ax_scatter.set_xlabel("Preço Unitário em R$ (Menor é Melhor ←)", fontsize=11, fontweight="bold")
ax_scatter.set_ylabel("Taxa de Defeitos em % (Menor é Melhor ↓)", fontsize=11, fontweight="bold")
ax_scatter.set_title("Análise de Trade-off: Preço vs. Qualidade (Tamanho da Bolha = Prazo em Dias)",
                     fontsize=13, fontweight="bold", pad=12)

# Região ideal destacada
ax_scatter.axhspan(0, 1.5, xmin=0, xmax=0.5, color="#e8f5e9", alpha=0.5, label="Região Ideal (Baixo Custo & Alta Qualidade)")
ax_scatter.grid(True, linestyle="--", alpha=0.5)
ax_scatter.legend(loc="upper left", frameon=True, fontsize=9)

fig_scatter.text(0.5, 0.01, "Fonte: dados/fornecedores.csv.csv | Bolhas menores indicam entregas mais rápidas.",
                 ha="center", fontsize=9, color="#555555", style="italic")
plt.tight_layout()
caminho_g3 = os.path.join("resultados", "grafico_tradeoff_fornecedores.png")
plt.savefig(caminho_g3, dpi=300, bbox_inches="tight")
plt.close()

print(f"Gráfico 1 (Melhorado) salvo em: {caminho_g1}")
print(f"Gráfico 2 (Radar) salvo em: {caminho_g2}")
print(f"Gráfico 3 (Trade-off) salvo em: {caminho_g3}")
