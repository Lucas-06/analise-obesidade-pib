# 🌍 Global Health & Economy: GDP vs. Obesity Analysis

Este projeto consiste em uma análise de dados exploratória (EDA) que investiga a correlação entre o desenvolvimento econômico de um país (**PIB per Capita**) e a saúde de sua população, especificamente focando nas taxas de **Obesidade**.

O objetivo é responder à pergunta: *"Países mais ricos tendem a ser mais obesos?"*

---

## 📊 Principais Resultados

A análise dos dados combinados (1975-2016) revelou:

1.  **Correlação Positiva Moderada (~0.38):** Existe uma tendência de aumento da obesidade conforme o PIB cresce, mas não é uma regra absoluta.
2.  **Relação Logarítmica:** O impacto do aumento de renda na obesidade é muito mais forte em países em desenvolvimento. Em economias ricas, a curva tende a estabilizar.
3.  **Outliers Interessantes:**
    * **Japão:** Um outlier de saúde (PIB alto, obesidade baixíssima).
    * **Nauru e Kuwait:** PIB alto impulsionado por recursos específicos, com taxas de obesidade extremas (>40%).
    * **Brasil e México:** Países de renda média com tendências de alta na obesidade, aproximando-se de países desenvolvidos.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.11**
* **Pandas:** Para manipulação, limpeza e junção (merge) de datasets.
* **Matplotlib:** Para visualização de dados estática.
* **NumPy:** Para cálculos matemáticos e linhas de tendência (regressão polinomial).
* **Pillow (PIL):** Para geração de mapas animados (GIFs).

---

## 📂 Estrutura do Projeto

```text
├── datasets/
│   ├── gdp.csv              # Dados brutos do PIB per capita
│   └── obesity_cleaned.csv  # Dados brutos de obesidade global
├── plots/                   # Imagens e GIFs gerados
│   ├── correlation_plot.png
│   └── animacao_debug.gif
├── analysis_script.py       # Script principal de análise e visualização
└── README.md