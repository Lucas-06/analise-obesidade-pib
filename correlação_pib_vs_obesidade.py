import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. Carregar e Cruzar Dados
df_ob = pd.read_csv("datasets/obesity_cleaned.csv")
df_ob['Obesity_Value'] = pd.to_numeric(df_ob['Obesity (%)'].str.split(' ').str[0], errors='coerce')
df_ob = df_ob[df_ob['Sex'] == 'Both sexes']

df_gdp = pd.read_csv("datasets/gdp.csv")
df_gdp.columns = df_gdp.columns.str.strip()
df_gdp['Year'] = df_gdp['Year'].astype(str).str.split('/').str[-1].astype(int)
df_gdp['GDP_pp'] = pd.to_numeric(df_gdp['GDP_pp'].astype(str).str.replace(',', '').str.strip(), errors='coerce')

df = pd.merge(df_ob, df_gdp, on=['Country', 'Year'], how='inner')

# 2. Filtrar Ano Recente
ano_recente = df['Year'].max()
df_plot = df[df['Year'] == ano_recente].copy()

# 3. Escolher quem destacar
destaques_lista = [
    'Brazil', 'China', 'India', 'Japan', 'Germany', 'France',
    'Mexico', 'Qatar', 'Kuwait', 'Nauru', 'Bangladesh'
]
# Adiciona também o mais rico e o mais pobre automaticamente
destaques_lista.append(df_plot.loc[df_plot['GDP_pp'].idxmax()]['Country'])
destaques_lista.append(df_plot.loc[df_plot['GDP_pp'].idxmin()]['Country'])

# 4. Plotar
plt.figure(figsize=(12, 8))

# Todos os países em cinza
plt.scatter(df_plot['GDP_pp'], df_plot['Obesity_Value'],
            alpha=0.4, c='gray', s=30, label='Mundo')

# Destaques em vermelho
df_dest = df_plot[df_plot['Country'].isin(destaques_lista)]
plt.scatter(df_dest['GDP_pp'], df_dest['Obesity_Value'],
            c='red', s=70, edgecolors='black', label='Países Selecionados')

# Escrever os nomes
for _, row in df_dest.iterrows():
    plt.text(row['GDP_pp'], row['Obesity_Value'] + 1.5, row['Country'],
             fontsize=10, fontweight='bold', ha='center')

plt.xscale('log') # Escala Log para o PIB
plt.xlabel('PIB per Capita (USD) - Escala Log')
plt.ylabel('Taxa de Obesidade (%)')
plt.title(f'Mapa de Dispersão: Riqueza vs Peso ({ano_recente})')
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.show()