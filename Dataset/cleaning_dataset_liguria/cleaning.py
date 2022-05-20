import pandas as pd

df = pd.read_csv('Output.csv', sep=';')
pd.set_option("display.max_rows", None)
#print(df[df['LuogoNascita']=='35'])

cont = 35

index = df.index

for x in index:
    if 'Z' in df.LuogoNascita[x]:
        df.LuogoNascita[x] = str(cont)
        cont+=1
"""
day = df.DataProtocollo[0].split("/", 1)[0]
month = df.DataProtocollo[0].split("/", 2)[1]
year = df.DataProtocollo[0].split("/", 3)[2]
"""

for i in range(len(df.DataProtocollo)):
    day = df.DataProtocollo[i].split("/", 1)[0]
    month = df.DataProtocollo[i].split("/", 2)[1]
    year = df.DataProtocollo[i].split("/", 3)[2]
    df.DataProtocollo[i] = year+month+day

for i in range(len(df.DataAccadimento)):
    day = df.DataAccadimento[i].split("/", 1)[0]
    month = df.DataAccadimento[i].split("/", 2)[1]
    year = df.DataAccadimento[i].split("/", 3)[2]
    df.DataAccadimento[i] = year+month+day
    

df.to_csv("Dataset_Liguria.csv", sep=',', index = False)