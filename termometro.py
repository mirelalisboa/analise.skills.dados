import os
import matplotlib.pyplot as plt

# 1. Pontos conhecidos: (temperatura, corrente)
# Ponto 1: 0 °C -> 4 mA  (x1, y1)
x1, y1 = 0, 4
# Ponto 2: 100 °C -> 20 mA (x2, y2)
x2, y2 = 100, 20

# 2. Cálculo dos coeficientes da reta (y = a*x + b)
# Inclinação (a)
a = (y2 - y1) / (x2 - x1)
# Coeficiente linear (b)
b = y1 - a * x1

print("=== EQUAÇÃO DA RETA ===")
print(f"Coeficiente a (inclinação): {a}")
print(f"Coeficiente b: {b}")
print(f"Equação: y = {a} * x + {b}\n")

# 3. Ponto de teste para x = 50 graus
temp_teste = 50
corrente = a * temp_teste + b

print(f"=== RESULTADOS PARA X = {temp_teste} °C ===")
print(f"Corrente calculada (y): {corrente} mA")

# 4. Avisos de limites
# Limite de temperatura: 0 a 100 °C
if temp_teste < 0 or temp_teste > 100:
    print(f"[AVISO] Temperatura fora da faixa operacional segura (0 a 100 °C)! Valor: {temp_teste} °C")
else:
    print("[OK] Temperatura dentro da faixa operacional (0 a 100 °C).")

# Limite de corrente: 4 a 20 mA
if corrente < 4 or corrente > 20:
    print(f"[AVISO] Corrente elétrica fora do padrão (4 a 20 mA)! Valor: {corrente} mA")
else:
    print("[OK] Corrente elétrica dentro do padrão (4 a 20 mA).")

# 5. Classificação da temperatura
# Baixa: até 30 graus | Média: até 60 graus | Alta: acima de 60 graus
if temp_teste <= 30:
    classificacao = "Baixa"
elif temp_teste <= 60:
    classificacao = "Média"
else:
    classificacao = "Alta"

print(f"Classificação da temperatura: {classificacao}\n")

# 6. Geração do gráfico com matplotlib
# Valores de temperatura (eixo X) e corrente (eixo Y)
temperaturas = list(range(0, 101, 10))
correntes = [a * t + b for t in temperaturas]

plt.figure(figsize=(8, 5))
plt.plot(temperaturas, correntes, label=f"Reta: y = {a}x + {b}", color="blue", linewidth=2)
plt.plot(temp_teste, corrente, "ro", label=f"Ponto de teste ({temp_teste} °C, {corrente} mA)")

plt.title("Termômetro: Corrente Elétrica vs Temperatura")
plt.xlabel("Temperatura (°C)")           # Eixo X
plt.ylabel("Corrente Elétrica (mA)")     # Eixo Y
plt.grid(True, linestyle="--", alpha=0.7)
plt.legend()

# Salvar o gráfico na pasta resultados/ conforme as regras do projeto
os.makedirs("resultados", exist_ok=True)
caminho_grafico = os.path.join("resultados", "grafico_termometro.png")
plt.savefig(caminho_grafico)
print(f"Gráfico salvo com sucesso em: {caminho_grafico}")
