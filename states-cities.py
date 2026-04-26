import pandas as pd

#Импортируем аналитискую витрину с показателями, рассчитанными на предыдущем шаге
df = pd.read_csv("D:\\PET_PROJECT\\df.csv")

#Создаем новую таблицу агрегированную по регионам
df_group1 = df.groupby('region')[['Profit', 'sales', 'expenses', 'num_customers', 'num_transactions']].sum()
df_group2 = df.groupby('region')[['avg_receipt', 'frequency of purchases']].mean()
group_size = (df.groupby('region').size() / 5).rename('group_size')
df_join = df_group1.join(group_size).sort_values(by='Profit', ascending=False)

#След. строчка нужна для корректного формата вывода средних данных
pd.set_option('display.float_format', '{:.2f}'.format)

#Считаем разницу в прибыли
#print((df_join.iloc[0,:] - df_join.iloc[5,:]) * 100 / df_join.iloc[5,:])

#Рассчитываем взвешанные показатели
df_join['Avg Profit per Branch'] = df_join['Profit'] / df_join['group_size']
df_join['Avg Sales per Branch'] = df_join['sales'] / df_join['group_size']
df_join = df_join.join(df_group2)

#Выводим получившуюся таблицу, счиатем разницу, анализируем
print(df_join.iloc[:, [6, 8, 9]].sort_values(by='Avg Profit per Branch', ascending=False))
print((df_join.loc['Центральный федеральный округ'] - df_join.loc['Приволжский федеральный округ']) * 100 / df_join.loc['Приволжский федеральный округ'])

#Группируем уже по городам
df_group3 = df.groupby('city')[['Profit', 'sales', 'expenses', 'num_customers', 'num_transactions']].sum()
df_group4 = df.groupby('city')[['avg_receipt', 'frequency of purchases', 'Profit per Sqm']].mean()
group_size1 = (df.groupby('city').size() / 5).rename('group_size1')
df_join1 = df_group3.join(group_size1).sort_values(by='Profit', ascending=False)
pd.set_option('display.float_format', '{:.2f}'.format)

#Также расчитываем новые взвешанные показатели
df_join1['Avg Profit per Branch'] = df_join1['Profit'] / df_join1['group_size1']
df_join1['Avg Sales per Branch'] = df_join1['sales'] / df_join1['group_size1']
df_join1['Avg customers per Branch'] = df_join1['num_customers'] / df_join1['group_size1']
df_join1['Avg transactions per Branch'] = df_join1['num_transactions'] / df_join1['group_size1']
df_join1 = df_join1.join(df_group4)
df1 = df_join1[['Avg Profit per Branch']].sort_values(by='Avg Profit per Branch')
print(df1)

#Выводим результаты, анализируем
#print(df_join1.iloc[:, [0, 10]])
#print(df_join1.iloc[:, [0, 6, 7]].sort_values(by='Avg Profit per Branch', ascending=False))
#print((df_join1.loc['Москва'] - df_join1.loc['Омск']) * 100 / df_join1.loc['Омск'])

