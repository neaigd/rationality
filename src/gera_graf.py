import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import math
import json

# Load data from JSON file
with open('data/articles.json', 'r', encoding='utf-8') as f:
    consolidated_data = json.load(f)


# --- Pré-processamento e Criação do DataFrame ---
data_for_df = []
criterios_list = ["A'", "Q'", "C'", "S'", "R'", "V'"]

for article in consolidated_data:
    row = {'article_id': article['article_id']}
    for crit in criterios_list:
        # Mapeia Verdadeiro para 1, Falso para 0
        row[crit] = 1 if article['analise_criterios'][crit]['status'] == 'Verdadeiro' else 0
    # Adiciona status geral (1 para ATENDIDA, 0 para NÃO ATENDIDA)
    row['RC_Geral'] = 1 if 'ATENDIDA' in article['resultado_final_rc']['status_geral'] else 0
    data_for_df.append(row)

df = pd.DataFrame(data_for_df)
df.set_index('article_id', inplace=True)

# --- Geração das Visualizações ---

# 1. Gráfico de Barras: Frequência de Status "Verdadeiro" por Critério
plt.figure(figsize=(10, 6))
status_counts = df[criterios_list].sum() # Soma os 1s (Verdadeiro)
status_counts.plot(kind='bar', color='skyblue')
plt.title('Frequência de Status "Verdadeiro" por Critério Refinado')
plt.xlabel('Critério Refinado')
plt.ylabel('Número de Artigos (Status Verdadeiro)')
plt.xticks(rotation=0)
plt.ylim(0, len(df) + 1) # Ajusta limite do eixo y
for i, count in enumerate(status_counts):
    plt.text(i, count + 0.1, str(count), ha='center')
plt.tight_layout()
plt.savefig('output/status_por_criterio.png')
plt.close()

# 2. Gráfico de Barras: Status Geral da RC
plt.figure(figsize=(6, 4))
rc_geral_counts = df['RC_Geral'].map({1: 'ATENDIDA', 0: 'NÃO ATENDIDA'}).value_counts()
rc_geral_counts.plot(kind='bar', color=['salmon', 'lightgreen'])
plt.title('Status Geral da Racionalidade Científica (RC)')
plt.xlabel('Status RC')
plt.ylabel('Número de Artigos')
plt.xticks(rotation=0)
plt.ylim(0, len(df) + 1)
for i, count in enumerate(rc_geral_counts):
    plt.text(i, count + 0.1, str(count), ha='center')
plt.tight_layout()
plt.savefig('output/status_geral_rc.png')
plt.close()

# 3. Heatmap Comparativo
plt.figure(figsize=(8, 5))
sns.heatmap(df[criterios_list], annot=True, cmap="viridis", cbar=False, linewidths=.5, linecolor='lightgray', fmt='d')
plt.title('Comparativo de Atendimento aos Critérios (1=Verdadeiro, 0=Falso)')
plt.xlabel('Critério Refinado')
plt.ylabel('Artigo ID')
plt.yticks(rotation=0)
plt.savefig('output/heatmap_comparativo.png')
plt.close()


# 4. Gráfico de Radar (Exemplo para um artigo, pode ser adaptado)
def plot_radar_chart(dataframe, article_id_to_plot, title_suffix=""):
    labels = np.array(criterios_list)
    stats = dataframe.loc[article_id_to_plot, criterios_list].values

    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False)
    # Fechar o círculo
    stats = np.concatenate((stats,[stats[0]]))
    angles = np.concatenate((angles,[angles[0]]))

    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, polar=True)
    ax.plot(angles, stats, 'o-', linewidth=2, color='blue')
    ax.fill(angles, stats, alpha=0.25, color='blue')
    ax.set_thetagrids(angles[:-1] * 180/np.pi, labels) # Usa [:-1] para não repetir o primeiro label
    ax.set_title(f"Perfil de Racionalidade: {article_id_to_plot}{title_suffix}")
    ax.set_yticks([0, 1]) # Define os ticks radiais para 0 e 1
    ax.set_yticklabels(["Falso", "Verdadeiro"])
    ax.grid(True)
    plt.savefig(f'output/radar_{article_id_to_plot}.png')
plt.close()

# Gerar gráfico de radar para o primeiro artigo como exemplo
if not df.empty:
    plot_radar_chart(df, df.index[0])
    # Você pode chamar plot_radar_chart(df, 'article_id') para outros artigos
    # plot_radar_chart(df, '2_Moraes') # Exemplo

# 5. Gráfico de Percentual de Atendimento por Critério
plt.figure(figsize=(10, 6))
percent_atendimento = (df[criterios_list].mean() * 100).round(1)
ax = percent_atendimento.plot(kind='bar', color='skyblue')
plt.title('Percentual de Atendimento por Critério')
plt.xlabel('Critério')
plt.ylabel('Percentual de Artigos que Atenderam (%)')
plt.xticks(rotation=0)
plt.ylim(0, 110)

# Adicionar valores nas barras
for p in ax.patches:
    ax.annotate(f'{p.get_height()}%', 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha='center', va='center', 
                xytext=(0, 5), 
                textcoords='offset points')

plt.tight_layout()
plt.savefig('output/percentual_atendimento_criterios.png')
plt.close()

print("\nDataFrame usado para os gráficos:")
print(df)
print("\nPercentual de atendimento por critério:")
print(percent_atendimento)
