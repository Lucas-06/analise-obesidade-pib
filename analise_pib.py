import pandas as pd
import numpy as np


def processar_gdp(caminho_arquivo):
    # 1. Carregar os dados
    df = pd.read_csv(caminho_arquivo)

    # Limpar nomes das colunas (remove espaços como ' GDP_pp ')
    df.columns = df.columns.str.strip()

    # 2. Limpeza dos Dados
    # Converter 'Year' (1/1/1901 -> 1901)
    df['Year'] = df['Year'].astype(str).str.split('/').str[-1].astype(int)

    # Limpar 'GDP_pp': remover vírgulas e espaços, depois converter para float
    df['GDP_pp'] = df['GDP_pp'].astype(str).str.replace(',', '').str.strip()
    df['GDP_pp'] = pd.to_numeric(df['GDP_pp'], errors='coerce')

    # Remover linhas com valores fundamentais nulos
    df = df.dropna(subset=['Country', 'Year', 'GDP_pp'])

    # --- PERGUNTA: Primeiro valor registrado de cada país ---
    primeiros_registros = df.sort_values('Year').groupby('Country').first().reset_index()

    # --- PERGUNTA: Regiões com maiores crescimentos no século passado (1901-2000) ---
    df_xx = df[(df['Year'] >= 1901) & (df['Year'] <= 2000)]
    # Agrupamos por Região e Ano para média regional
    regiao_ano = df_xx.groupby(['Region', 'Year'])['GDP_pp'].mean().reset_index()

    crescimento_list = []
    for region in regiao_ano['Region'].unique():
        reg_data = regiao_ano[regiao_ano['Region'] == region].sort_values('Year')
        if len(reg_data) > 1:
            inicio = reg_data.iloc[0]['GDP_pp']
            fim = reg_data.iloc[-1]['GDP_pp']
            if inicio > 0:
                variacao = ((fim - inicio) / inicio) * 100
                crescimento_list.append({'Region': region, 'Crescimento_%': variacao})

    df_crescimento_reg = pd.DataFrame(crescimento_list).sort_values(by='Crescimento_%', ascending=False)

    # --- PERGUNTA: Preencher anos ausentes (Interpolação) ---
    def preencher_lacunas(group):
        group = group.sort_values('Year')
        todos_anos = pd.DataFrame({'Year': range(group['Year'].min(), group['Year'].max() + 1)})
        # Mescla os anos existentes com a sequência completa
        interp = pd.merge(todos_anos, group, on='Year', how='left')
        interp['Country'] = interp['Country'].ffill().bfill()
        interp['Region'] = interp['Region'].ffill().bfill()
        # Interpola os valores de PIB
        interp['GDP_pp_Estimado'] = interp['GDP_pp'].interpolate(method='linear')
        return interp

    df_completo = df.groupby('Country', group_keys=False).apply(preencher_lacunas)

    # --- LOG DE RESULTADOS ---
    print("=== 1. PRIMEIROS REGISTROS (AMOSTRA) ===")
    print(primeiros_registros[['Country', 'Year', 'GDP_pp']].head())

    print("\n=== 2. CRESCIMENTO POR REGIÃO (1901-2000) ===")
    print(df_crescimento_reg.to_string(index=False))

    print("\n=== 3. AMOSTRA DE ANOS ESTIMADOS (EX: 1902, 1903...) ===")
    # Mostra linhas que não existiam no CSV original
    print(df_completo[df_completo['GDP_pp'].isna()].head())

    return df_completo


# Executar
df_final = processar_gdp("datasets/gdp.csv")