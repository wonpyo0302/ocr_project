import pandas as pd
df = pd.read_csv('../../df_file.csv',encoding="utf-8")
print(df['Text'].head(5))
df = df.replace({r'\r':'', r'\n':''}, regex=True)
print(df['Text'].head(5))

df['Label'] = df['Label'].replace([0,1,2,3,4],['Politics','Sport','Technology','Entertainment','Business'])
# print(df)
df['Text'] = df['Text'].str.replace('횂짙','$')

for idx , data in df.iterrows():
    if idx == 1 :    
        print(idx, data.Text, data.Label)