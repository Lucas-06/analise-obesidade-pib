import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import io
import numpy as np
import os


def criar_mapa_animado(csv_path, col_valor, titulo):
    # 1. Verifica se o arquivo existe
    if not os.path.exists(csv_path):
        print(f"ERRO: O arquivo '{csv_path}' não foi encontrado.")
        return

    # Cria pasta de output
    pasta_output = 'plots'
    if not os.path.exists(pasta_output):
        os.makedirs(pasta_output)

    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()  # Remove espaços extras nos nomes das colunas

    print("Colunas encontradas:", df.columns.tolist())  # Debug para ver nomes das colunas

    # Limpeza de Ano e Valores
    try:
        # Tenta converter o ano. Ajuste conforme seu CSV real
        df['Year'] = df['Year'].astype(str).str.extract(r'(\d{4})').astype(int)

        # Limpeza robusta de números (remove vírgulas e pega o primeiro valor numérico)
        df[col_valor] = pd.to_numeric(
            df[col_valor].astype(str).str.replace(',', '').str.extract(r'(\d+\.?\d*)')[0],
            errors='coerce'
        )
    except Exception as e:
        print(f"Erro ao processar colunas: {e}")
        return

    df = df.dropna(subset=['Country', 'Year', col_valor])

    # --- DICA: Para um mapa real, use a biblioteca 'geopandas'.
    # Aqui expandi um pouco a lista, mas o ideal é ter todos os países.
    coords = {
        'Brazil': (-14.2, -51.9), 'China': (35.8, 104.2), 'United States': (37.1, -95.7),
        'Afghanistan': (33.9, 67.7), 'France': (46.2, 2.2), 'India': (20.5, 78.9),
        'Germany': (51.1, 10.4), 'Russia': (61.5, 105.3), 'Japan': (36.2, 138.2),
        'United Kingdom': (55.3, -3.4), 'Italy': (41.8, 12.5), 'Canada': (56.1, -106.3),
        'Australia': (-25.2, 133.7), 'South Africa': (-30.5, 22.9)
    }

    frames = []
    anos = sorted(df['Year'].unique())[::5]  # Pula de 5 em 5 anos para ser mais rápido

    print(f"Processando {len(anos)} anos...")

    for ano in anos:
        df_year = df[df['Year'] == ano].copy()

        # Mapeia coordenadas
        df_year['lat'] = df_year['Country'].map(lambda x: coords.get(x, (None, None))[0])
        df_year['lon'] = df_year['Country'].map(lambda x: coords.get(x, (None, None))[1])

        # Verifica quantos países sobraram após o filtro de coordenadas
        total_paises = len(df_year)
        df_year = df_year.dropna(subset=['lat', 'lon'])
        paises_com_coords = len(df_year)

        if df_year.empty:
            print(f"Ano {ano}: Nenhum país encontrado na lista de coordenadas. Pulando.")
            continue

        # Debug visual no terminal
        # print(f"Ano {ano}: Plotando {paises_com_coords}/{total_paises} países.")

        fig, ax = plt.subplots(figsize=(10, 6))

        # Carrega um mapa mundi simples de fundo (opcional, mas ajuda na visualização)
        # Se não quiser instalar 'cartopy' ou 'geopandas', mantemos apenas os limites
        ax.set_xlim(-180, 180)
        ax.set_ylim(-60, 85)
        ax.grid(True, alpha=0.3, linestyle='--')  # Grade para ajudar a ver que é um mapa

        scatter = ax.scatter(df_year['lon'], df_year['lat'],
                             s=np.sqrt(df_year[col_valor]) * 5,  # Aumentei o tamanho da bolha
                             c=df_year[col_valor],
                             cmap='viridis',
                             alpha=0.7,
                             edgecolors='black')  # Borda para destacar

        plt.colorbar(scatter, ax=ax, label=col_valor)
        ax.set_title(f"{titulo} - {ano}")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")

        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100)
        buf.seek(0)
        frames.append(Image.open(buf))
        plt.close()

    if frames:
        caminho_final = os.path.join(pasta_output, 'animacao_debug.gif')
        frames[0].save(caminho_final, save_all=True, append_images=frames[1:], duration=300, loop=0)
        print(f"Sucesso! GIF salvo em: {caminho_final}")
    else:
        print(
            "FALHA: Nenhum frame foi gerado. Verifique se os nomes dos países no CSV batem com o dicionário 'coords'.")


# Teste
criar_mapa_animado("datasets/gdp.csv", "GDP_pp", "Evolução do PIB per Capita")