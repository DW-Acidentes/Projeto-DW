import pandas as pd
import numpy as np

df1 = pd.read_csv('../../acidentes2017_reduzido.csv',low_memory=False, encoding='ISO-8859-1', sep=';')
df2 = pd.read_csv('../docs/acidentes2017_teste.csv',low_memory=False, sep=';')

df1 = df1.dropna()
df2 = df2.dropna()

df1.to_csv('../../acidentes2017_reduzido_not_Null.csv', ';', encoding = "ISO-8859-1")
df2.to_csv('../docs/acidentes2017_teste_not_Null.csv', ';', encoding = "ISO-8859-1")

#Abrir a Planilha e Apagar (manualmente) a coluna dos indices criada
                       