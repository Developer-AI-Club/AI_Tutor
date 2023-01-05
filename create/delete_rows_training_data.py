import pandas as pd


df = pd.read_csv('./data/training_data.csv')
df =  df[df.Tag == ''] 

# df.column_name != whole string from the cell
# now, all the rows with the column: Name and Value: "dog" will be deleted

df.to_csv('./data/training_data.csv', index=False)