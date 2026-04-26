import pandas as pd, numpy as np

#Импортируем аналитическую витрину, созданную в SQL
df = pd.read_csv("D:\\PET_PROJECT\\data_mart.csv", sep=',',encoding='cp1251')

#Считаем относительные метрики и коэффициенты
df['Sales_per_sqm'] = df['sales'] / df['store_area']
df['Profit per Sqm'] = (df['sales'] - df['expenses']) / df['store_area']
df['Net Ros'] = (df['sales'] - df['expenses']) * 100 / df['sales']
df['Expense Ratio'] = df['expenses'] / df['sales']
df['avg_receipt'] = df['sales'] / df['num_transactions']
df['frequency of purchases'] = df['num_transactions'] / df['num_customers']
df['Profit'] = df['sales'] - df['expenses']

#Импортируем агрегированные данные по прибыли, расходам и выручке и считаем разницу в среденей прибыли
df_profit = pd.read_csv("D:\\PET_PROJECT\\Profit 5 years.csv", sep=',')
max_profit = df_profit.nlargest(10, 'profit')
min_profit = df_profit.nsmallest(10, 'profit')
avg_max = max_profit['profit'].mean()
avg_min = min_profit['profit'].mean()
#print((avg_max - avg_min) * 100 / avg_min)
#print(max_profit)
#print(min_profit)

#Создаем таблицу агрегированную по филиалам, где некоторые показатели суммируются, а для некоторых считается среднее
df_group1 = df.groupby('branch_id')[['Profit', 'num_customers', 'num_transactions', 'sales', 'expenses']].sum()
df_group2 = df.groupby('branch_id')[['discount_rate', 'Sales_per_sqm', 'Profit per Sqm', 'Net Ros', 'avg_receipt', 'frequency of purchases']].mean()
df_join = df_group1.join(df_group2)

#Здесь присоединяем данные, которые не меняются от года к году
df_join = df_join.join(df[df['report_year'] == 2020].set_index('branch_id')[['Work_experiens','Work_period']])
#Сортируем, округляем
df_join = df_join.sort_values(by='Profit', ascending=False)
df_join = df_join.apply(lambda x: x.round(2), axis =1)

#Выводим топ-10 оучших и хучших по разным показателям, сравниваем и анализируем
#print(df_join.iloc[:10, [0, 9]])
#print(df_join.iloc[40:, [0, 9]])

#След. строчка нужна для корректного формата вывода средних данных
pd.set_option('display.float_format', '{:.2f}'.format)
#Рассчитываем среднее рахличных показателей по топ-10 лучшим и худшим
#print((df_join.iloc[:10, [0,9]].mean() - df_join.iloc[40:, [0,9]].mean()) * 100 / df_join.iloc[40:, [0,9]].mean())
print(df_join.iloc[:10, [10,11,12]].mean())
print(df_join.iloc[40:, [10,11,12]].mean())
# Рассчет коэффициента вариации
#k = df.groupby('branch_id')[['Sales_per_sqm', 'Profit per Sqm', 'Net Ros', 'avg_receipt', 'frequency of purchases']].std() * 100 / df.groupby('branch_id')[['Sales_per_sqm', 'Profit per Sqm', 'Net Ros', 'avg_receipt', 'frequency of purchases']].mean()
#print(k.mean())
#df.to_csv("D:\\PET_PROJECT\\df.csv")

#Коэффициент вариации, показывает, что данные рваные и неравномерные (потоиу что они учебный)
#Я попробовал использовать медиану вместо среднего, но коэффициенты вариации стали еще хуже, поэтому было принято оставить метод mean()

#Созраняем таблицу с рассчитанными показателями
#df_join.to_excel("D:\\PET_PROJECT\\df_join.xlsx")


