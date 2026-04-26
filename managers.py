import pandas as pd

#Импортируем аналитискую витрину с показателями, рассчитанными на предыдущем шаге
df = pd.read_csv("D:\\PET_PROJECT\\df.csv")

#Функция для преобразования длинного ФИО в формат Фамилия И.О.
def short_fio(row):
    l = row['fio'].split()
    if len(l) == 3:
        return l[0] + ' ' + l[1][0] + '.' +  l[2][0] + '.'
    elif len(l) == 2:
        return l[0] + ' ' + l[1][0] + '.'
    else:
        return l[0]
df['short_fio'] = df.apply(short_fio, axis=1)

#Группируем по менеджерам и смотрим показатели филиалов под их руководством за последний отчетный год
df_2024 = df[df['report_year'] == 2024]
df_group1 = df_2024.groupby('short_fio')[['Profit', 'Work_experiens']].sum()
df_group2 = df_2024.groupby('short_fio')[['Net Ros', 'Profit per Sqm', 'avg_receipt', 'frequency of purchases','num_transactions', 'num_customers',  'discount_rate']].mean()
df_join = df_group1.join(df_group2)
group_size = (df_2024.groupby('short_fio').size()).rename('group_size')
df_join = df_join.join(group_size)

#Считаем взвешенную прибыль и стаж
df_join['profit per manager'] = df_join['Profit'] / df_join['group_size']
df_join['Work_exp'] = df_join['Work_experiens'] / df_join['group_size']
df_join = df_join.drop('Work_experiens', axis=1)

#След. строчка нужна для корректного формата вывода средних данных
pd.set_option('display.float_format', '{:.2f}'.format)

#Сортируем, выводим анализируем
df_join.sort_values(by='profit per manager', ascending=False, inplace=True)
print(df_join.iloc[:, [2, 3, 9]])
print(df_join.iloc[:, [2]].median(), df_join.iloc[9, [2]])
#print(df_join.iloc[:, [3]].median())

#Рассчитываем коэф. корреляции
corr = df_join['profit per manager'].corr(df_join['discount_rate'])
print(corr)