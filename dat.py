import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Função para obter dados da API SGS do Banco Central do Brasil
def obter_dados_bcb(codigo_serie, data_inicial):
    url = f'http://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo_serie}/dados?formato=json&dataInicial={data_inicial}&dataFinal=2023-12-31'
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data)
    df['data'] = pd.to_datetime(df['data'], dayfirst=True)
    df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
    return df

# Obter dados da taxa Selic (código da série: 432)
data_inicial = '1980-01-01'
df_juros = obter_dados_bcb(432, data_inicial)
df_juros.rename(columns={'valor': 'taxa_juros'}, inplace=True)

# Obter dados do IPCA (código da série: 433)
df_inflacao = obter_dados_bcb(433, data_inicial)
df_inflacao.rename(columns={'valor': 'inflacao'}, inplace=True)

# Mesclar os dados em um único DataFrame
df = pd.merge(df_juros, df_inflacao, on='data', how='inner')

# Filtrar os últimos 500 dados
df = df.sort_values('data', ascending=False).head(500).sort_values('data')

# Salvar os dados em um arquivo CSV
df.to_csv('dados_juros_inflacao_brasil.csv', index=False)

print("Dados coletados e salvos em 'dados_juros_inflacao_brasil.csv'")

# Criar gráficos de regressão linear simples
plt.figure(figsize=(12, 6))
sns.regplot(x='inflacao', y='taxa_juros', data=df)
plt.title('Regressão Linear Simples: Taxa de Juros vs Inflação')
plt.xlabel('Inflação (%)')
plt.ylabel('Taxa de Juros (%)')
plt.grid(True)
plt.show()

