# Importação das bibliotecas básicas

!pip install plotly --upgrade

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly
import plotly.express as px
import plotly.graph_objs as go
import datetime

"""#TESTE COVID"""

#montando nome do arquivo, com base na data atual
today = datetime.datetime.now() + datetime.timedelta(days=-1)

d1 = today.strftime("%d/%m/%Y")
ano = today.strftime("%Y")
mes = today.strftime("%m")
dia = today.strftime("%d")

#selecionando colunas necessárias para o estudo
columns = ['SEXO','IDADE','DATA_OBITO','CIDADE','COR','COMORBIDADE1','COMORBIDADE2','COMORBIDADE3','COMORBIDADE4','COMORBIDADE5','COMORBIDADE6']
df = pd.read_csv("https://www.saude.ma.gov.br/wp-content/uploads/"+ano+"/"+mes+"/Obitos-Anonimizados-"+dia+mes+".csv", encoding='latin-1', engine = 'python', sep=';', header = None, names = columns)
df # defaulted

#manipulação dos dados
df["IDADE"] = np.where(df["IDADE"].str.contains("MESES"), df["IDADE"].str.extract('(\d+)').astype(float)/12, df["IDADE"].str.extract('(\d+)').astype(float))
df["FAIXA"] = np.where(df["IDADE"] < 20, '20', np.where(df["IDADE"] < 40, '40', np.where(df["IDADE"] < 50, '50', np.where(df["IDADE"] < 60, '60', 'ACIMA 60'))))
df["COMORBIDADE1"].fillna("SEM COMORBIDADE", inplace = True)
df["MESANO"] = pd.to_datetime(df['DATA_OBITO'], format="%d/%m/%Y").dt.strftime("%y")+pd.to_datetime(df['DATA_OBITO'], format="%d/%m/%Y").dt.strftime("%m")
df["COMORBIDADE"] = df['COMORBIDADE1']=="SEM COMORBIDADE"

#geração dos gráficos
grafico = px.treemap(df, path=['FAIXA', 'COMORBIDADE1'])
grafico.show()

#data corte 15/05
PREVACINA = df[df['DATA_OBITO']<='15/04/2021']
grafico = px.treemap(PREVACINA, path=['FAIXA', 'COMORBIDADE1', 'SEXO'])
grafico.show()

POSVACINA = df[df['DATA_OBITO']>'15/04/2021']
grafico = px.treemap(POSVACINA, path=['FAIXA', 'COMORBIDADE1', 'SEXO'])
grafico.show()

grafico = px.parallel_categories(df, dimensions=['FAIXA','COMORBIDADE1'])
grafico.show()

sns.countplot(x = df['MESANO']);

plt.hist(x = df['IDADE']);

grafico = px.scatter_matrix(df, dimensions=['FAIXA', 'COMORBIDADE'], color = 'SEXO')
grafico.show()

df = df[df['MESANO']!='2003']

F20 = df[['FAIXA','MESANO']]
F20 = F20[F20['FAIXA']=='20']
F20 = F20.groupby(by=["MESANO"]).count()
F20.rename(columns={'FAIXA': 'F20'}, inplace = True)

F40 = df[['FAIXA','MESANO']]
F40 = F40[df['FAIXA']=='40']
F40 = F40.groupby(by=["MESANO"]).count()
F40.rename(columns={'FAIXA': 'F40'}, inplace = True)

F50 = df[['FAIXA','MESANO']]
F50 = F50[F50['FAIXA']=='50']
F50 = F50.groupby(by=["MESANO"]).count()
F50.rename(columns={'FAIXA': 'F50'}, inplace = True)

F60 = df[['FAIXA','MESANO']]
F60 = F60[F60['FAIXA']=='60']
F60 = F60.groupby(by=["MESANO"]).count()
F60.rename(columns={'FAIXA': 'F60'}, inplace = True)
F60 = F60.sort_values(['MESANO'])

F60M = df[['FAIXA','MESANO']]
F60M = F60M[F60M['FAIXA']=='ACIMA 60']
F60M = F60M.groupby(by=["MESANO"]).count()
F60M.rename(columns={'FAIXA': 'F60M'}, inplace = True)

FAIXAS = pd.concat([F60M, F60, F50, F40, F20], axis=1) #, join="left"
FAIXAS["F60M"].fillna(0, inplace = True)
FAIXAS["F60"].fillna(0, inplace = True)
FAIXAS["F50"].fillna(0, inplace = True)
FAIXAS["F40"].fillna(0, inplace = True)
FAIXAS["F20"].fillna(0, inplace = True)

FAIXAS.plot.line()
plt.grid(True)
plt.xlabel("eixo X")
plt.ylabel("eixo Y")

plt.show()
