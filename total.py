import pandas as pd

#Импортируем аналитискую витрину
df = pd.read_csv("D:\\PET_PROJECT\\data_mart.csv", sep=',',encoding='cp1251')
#Рассчитываем прибыль
df['Profit'] = df['sales'] - df['expenses']
#Группируем по отчетным годам для расчета динамики основных показателей за 5 лет
df = df.groupby('report_year')[['Profit', 'sales', 'expenses', 'num_customers', 'num_transactions']].sum()
#Рассчитываем относительные метрики эффективности по годам
df['Net Ros'] = (df['sales'] - df['expenses']) * 100 / df['sales']
df['avg_receipt'] = df['sales'] / df['num_customers']
df['frequency of purchases'] = df['num_transactions'] / df['num_customers']

#След. строчка нужна для корректного формата вывода средних данных
pd.set_option('display.float_format', '{:.2f}'.format)

#Выводим результаты, считаем, аналзируем
print(df.iloc[:, [0,5,6]])
print((df.iloc[2, [0,5,6]] - df.iloc[:, [0,5,6]].median()) * 100 / df.iloc[2, [0,5,6]])
print(df.iloc[:, [0,5,6]].mean())

#Рассчет коэффициента вариации
k_var = df.std() * 100 / df.mean()
#print(k_var)

