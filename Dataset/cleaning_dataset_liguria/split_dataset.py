import pandas as pd

df = pd.read_csv('infortuni_Liguria.csv')
size_2000 = pd.DataFrame(columns = df.columns)
size_4000 = pd.DataFrame(columns = df.columns)
size_6000 = pd.DataFrame(columns = df.columns)

size_2000 = df.iloc[0:2000]
size_4000 = df.iloc[0:4000]
size_6000 = df.iloc[0:6000]

size_2000.to_csv("infortuni_Liguria_2000.csv", index = False)
size_4000.to_csv("infortuni_Liguria_4000.csv", index = False)
size_6000.to_csv("infortuni_Liguria_6000.csv", index = False)