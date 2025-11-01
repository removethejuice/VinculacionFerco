import pandas as pd

df = pd.read_csv("rotaciones_12_meses.csv", encoding="utf-8-sig")
print (df.head())


print (df.columns)
df_filtrado = df.loc[:, df.columns.str.lower() == "rotaciones"]
print (df_filtrado.head())