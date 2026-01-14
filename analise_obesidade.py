import pandas as pd
import matplotlib.pyplot as plt


def processar_analise_obesidade(caminho_arquivo):
    # Carregar os dados
    df = pd.read_csv(caminho_arquivo)

    # 2. Limpeza: Extrair apenas o valor numérico da coluna 'Obesity (%)'
    df['Obesity_Value'] = df['Obesity (%)'].str.split(' ').str[0]
    df['Obesity_Value'] = pd.to_numeric(df['Obesity_Value'], errors='coerce')

    # Remover linhas sem dados (NaN)
    df = df.dropna(subset=['Obesity_Value'])

    # --- PERGUNTA 1: Top 5 países com maior e menor taxa de aumento ---
    df_growth = df[df['Sex'] == 'Both sexes'].copy()

    growth_results = []
    for country in df_growth['Country'].unique():
        country_data = df_growth[df_growth['Country'] == country].sort_values('Year')
        if len(country_data) > 1:
            inicio = country_data.iloc[0]['Obesity_Value']
            fim = country_data.iloc[-1]['Obesity_Value']
            aumento_total = fim - inicio
            growth_results.append({'Country': country, 'Aumento': aumento_total})

    df_aumento = pd.DataFrame(growth_results)
    top_5_maior_aumento = df_aumento.sort_values(by='Aumento', ascending=False).head(5)
    top_5_menor_aumento = df_aumento.sort_values(by='Aumento', ascending=True).head(5)

    # --- PERGUNTA 2: Maiores e menores níveis em 2015 ---
    df_2015 = df[(df['Year'] == 2015) & (df['Sex'] == 'Both sexes')]
    top_5_2015 = df_2015.sort_values(by='Obesity_Value', ascending=False).head(5)
    bottom_5_2015 = df_2015.sort_values(by='Obesity_Value', ascending=True).head(5)

    # --- PERGUNTA 3: Diferença média entre sexos no Brasil ---
    df_brazil = df[df['Country'] == 'Brazil']
    # Pivotar para ter colunas Male e Female por ano
    pivot_brazil = df_brazil.pivot(index='Year', columns='Sex', values='Obesity_Value')
    if 'Male' in pivot_brazil.columns and 'Female' in pivot_brazil.columns:
        pivot_brazil['Diff'] = pivot_brazil['Female'] - pivot_brazil['Male']
        media_dif_brasil = pivot_brazil['Diff'].mean()
    else:
        media_dif_brasil = "Dados de sexo não encontrados para o Brasil"

    # --- LOG DE RESULTADOS ---
    print("=== 1. TAXA DE AUMENTO (TODO O PERÍODO) ===")
    print("\nMaiores Aumentos (Pontos Percentuais):")
    print(top_5_maior_aumento.to_string(index=False))
    print("\nMenores Aumentos (ou Reduções):")
    print(top_5_menor_aumento.to_string(index=False))

    print("\n=== 2. NÍVEIS DE OBESIDADE EM 2015 ===")
    print("\nPaíses com MAIOR Obesidade:")
    print(top_5_2015[['Country', 'Obesity_Value']].to_string(index=False))
    print("\nPaíses com MENOR Obesidade:")
    print(bottom_5_2015[['Country', 'Obesity_Value']].to_string(index=False))

    print("\n=== 3. DIFERENÇA MÉDIA NO BRASIL ===")
    print(f"A diferença média (Mulheres - Homens) ao longo dos anos foi de: {media_dif_brasil:.2f}%")

    # --- PERGUNTA 4: Gráfico de Evolução Mundial ---
    world_evolution = df.groupby(['Year', 'Sex'])['Obesity_Value'].mean().unstack()

    world_evolution.plot(figsize=(10, 6), linewidth=2)
    plt.title('Evolução Média da Obesidade no Mundo por Sexo', fontsize=14)
    plt.ylabel('Prevalência de Obesidade (%)')
    plt.xlabel('Ano')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(title='Sexo')
    plt.show()


# Para rodar, certifique-se que o caminho do arquivo está correto
processar_analise_obesidade("datasets/obesity_cleaned.csv")