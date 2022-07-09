# -*- coding: utf-8 -*-
"""task_2_pandas.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lgP4i_Nvr6UpphSLNQeJfCgxyUmJJ2qc
"""

# Commented out IPython magic to ensure Python compatibility.
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from scipy import stats
import warnings
warnings.filterwarnings('ignore')
# %matplotlib inline
plt.style.use('dark_background')

"""# Задание #2 Pandas

## Инструменты и ресурсы для выполнения задания

### Библиотеки Python

  * [Pandas](http://pandas.pydata.org/)
    - [Tutorials](http://pandas.pydata.org/pandas-docs/stable/tutorials.html)
    - [Easier data analysis in Python with pandas](http://www.dataschool.io/easier-data-analysis-with-pandas/)

### Ресурсы по Titanic dataset
  * [Сам конкурс](https://www.kaggle.com/c/titanic)
  * [Пример решения конкурса](http://nbviewer.jupyter.org/github/agconti/kaggle-titanic/blob/master/Titanic.ipynb)
  * [Еще пример](https://habrahabr.ru/company/mlclass/blog/270973/)
  
## Разминка
**Как и в предыдущем задании здесь запрещено использовать циклы, если это специально не оговорено.**
1. Скачайте Titanic dataset и загрузите его в pandas.DataFrame; выведите первые 5 записей в ноутбук. Как можно интерпретировать данную таблицу?
"""

# Commented out IPython magic to ensure Python compatibility.
# %%bash
# kaggle competitions download -c titanic
# unzip -q './titanic.zip' -d './data'

df = pd.read_csv('data/train.csv')
df.head()

"""2. Получите имена столбцов."""

df.columns

"""Oops! That's a for loop"""

for i in df.columns:
    print(i)

"""3. Перемешайте строки в случайном порядке."""

df_shuffle = df.sample(frac=1).reset_index(drop=True)

"""4. Получите случайную подвыборку данных с возвращением и без."""

df_random_with_seed = df.sample(frac=0.6, random_state=66)
df_random_without_seed = df.sample(frac=0.6)

"""5. Разбейте данные случайным образом на две непересекающиеся подвыборки."""

random_number = int(666*np.random.rand(1))
first_part, second_part = df_shuffle.iloc[:random_number,:], df_shuffle.iloc[random_number,:]

"""6. Проверьте, является ли признак **Name** уникальным для каждого пассажира, если да, то сделайте его новым индексом данных."""

print(df.Name.nunique() == len(df.Name))
df.Name.is_unique

df = df.set_index('Name')

"""7. Проверьте, содержат ли данные пропуски, если да, то заполните их."""

def display_null(df):
  df_null_series = df.isnull().sum()
  df_null = pd.DataFrame(data=df_null_series, columns=['Num of nan'])
  df_null['% of nan'] = round((df.isnull().sum() / df.shape[0]) * 100)
  display(df_null)

display_null(df)

"""![](https://vignette.wikia.nocookie.net/titanic/images/f/f9/Titanic_side_plan.png/revision/latest?cb=20180322183733)"""

df['Cabin_new'] = df.Cabin.apply(lambda x: x[0] if pd.notnull(x) else 'M')
df['Cabin_new'] = df['Cabin_new'].replace(['A', 'B', 'C', 'T'], 'ABCT')
df['Cabin_new'] = df['Cabin_new'].replace(['D', 'E'], 'DE')
df['Cabin_new'] = df['Cabin_new'].replace(['F', 'G'], 'FG')
df['Age'] = df.groupby(['Sex', 'Pclass'])['Age'].apply(lambda x: x.fillna(x.median()))

"""Embarked is a categorical feature and there are only 2 missing values in whole data set. Both of those passengers are female, upper class and they have the same ticket number. This means that they know each other and embarked from the same port together. """

df[df['Embarked'].isnull()]

"""When I googled Stone, Mrs. George Nelson (Martha Evelyn), I found that she embarked from S (Southampton) with her maid Amelie Icard, in this page [Martha Evelyn Stone: Titanic Survivor](https://www.encyclopedia-titanica.org/titanic-survivor/martha-evelyn-stone.html)."""

df['Embarked'] = df['Embarked'].fillna('S')
df.drop(['Cabin'], axis=1, inplace=True)
display_null(df)

"""8. Определите, как много пассажиров ехало первым классом."""

first_class = df.Pclass.value_counts()
print(f'The total number of first class passengers on a sinking ship: {first_class[1]}')

"""9. Постройте гистограмму возрастов пассажиров."""

plt.rc('figure', figsize=(15, 10))
df_age = df['Age']
plt.title('Passengers by Age Group')
plt.xlabel('Age')
plt.ylabel('Count')
max_age = max(df['Age'])
plt.hist([df_age],
         bins=8,
         range=(1, max_age),
         stacked=True)
plt.show()

"""10. Определите средний возраст пассажиров, медианный возраст, дисперсию."""

print(f'Mean age: {int(df.Age.mean())}')
print(f'Median age: {int(df.Age.median())}')
print(f'Standard deviation: {int(df.Age.std())}\n')
df['Age'].describe()

"""11. Добавьте признак, который показывает, какой процент пассажиров имели возраст строго меньше, чем данный пассажир."""

df['PerYounger'] = df['Age'].apply(lambda x: (df.Age[df.Age < x].count() / df.shape[0] * 100))
df.head()

"""12. Коррелируют ли число братьев/сестер с числом родителей/детей?"""

df['SibSp'].corr(df['Parch'])

"""SibSp and Parch features are positively correlated(moderate correlation) which are both indicative of the number of family members accompanying passenger

14. Есть ли зависимость между классом и номером билета?
"""

df['Ticket_freq'] = df.groupby('Ticket')['Ticket'].transform('count')
df['Pclass'].corr(df['Ticket_freq'])

"""Well that wasn't smart. I guess not.

15. Какой части пассажиров удалось выжить?
"""

df_per = df[df['Survived'] == 1].count().values[1] / df.shape[0] * 100
print(f'The percentage of survived people: {int(df_per)}%.')

"""16. Сделайте визуализацию, позволяющую ответить на вопросы:
  * Верно ли, что женщины выживали чаще мужчин?

Yes, that's true.
"""

survival_rate = df.groupby(['Sex']).mean()[['Survived']]
male_rate = survival_rate.loc['male']
female_rate = survival_rate.loc['female']
display(survival_rate)

male_pos = np.random.uniform(0, male_rate, len(df[(df['Sex']=='male') & (df['Survived']==1)]))
male_neg = np.random.uniform(male_rate, 1, len(df[(df['Sex']=='male') & (df['Survived']==0)]))
female_pos = np.random.uniform(0, female_rate, len(df[(df['Sex']=='female') & (df['Survived']==1)]))
female_neg = np.random.uniform(female_rate, 1, len(df[(df['Sex']=='female') & (df['Survived']==0)]))

fig, ax = plt.subplots(1, 1, figsize=(9, 7))
np.random.seed(66)
ax.scatter(np.random.uniform(-0.3, 0.3, len(male_pos)), male_pos, color='#FF00FF', edgecolor='lightgray', label='Male(Survived=1)')
ax.scatter(np.random.uniform(-0.3, 0.3, len(male_neg)), male_neg, color='#FF00FF', edgecolor='lightgray', alpha=0.2, label='Male(Survived=0)')
ax.scatter(1+np.random.uniform(-0.3, 0.3, len(female_pos)), female_pos, color='#00FFFF', edgecolor='lightgray', label='Female(Survived=1)')
ax.scatter(1+np.random.uniform(-0.3, 0.3, len(female_neg)), female_neg, color='#00FFFF', edgecolor='lightgray', alpha=0.2, label='Female(Survived=0)')
ax.set_xlim(-0.5, 2.0)
ax.set_ylim(-0.03, 1.1)
ax.set_xticks([0, 1])
ax.set_xticklabels(['Male', 'Female'], fontweight='bold', fontfamily='serif', fontsize=13)
ax.set_yticks([], minor=False)
for s in ["top","right","left", 'bottom']: #I'm trully sorry
    ax.spines[s].set_visible(False)

fig.text(0.1, 1, 'Distribution of Survivors by Gender', fontweight='bold', fontfamily='serif', fontsize=15)    
fig.text(0.1, 0.96, 'As is known, the survival rate for female is high, with 19% of male and 74% of female.', fontweight='light', fontfamily='serif', fontsize=12)    

ax.legend(loc=(0.8, 0.5), edgecolor='None')
plt.tight_layout()
plt.show()

"""  * Верно ли, что чаще выживали пассажиры с более дорогими билетами?"""

survivor_count = df['Survived'].sum()
def get_survival_rate(df, col):
    by_col = df.groupby(col)
    count_by_col = by_col['Survived'].sum()
    survival_rate = count_by_col / survivor_count * 100
    print('Survival rates:', survival_rate, '\n \n', 'Counts: ', count_by_col)
    return survival_rate, count_by_col
def class_count(df, num):
  num_class_count = (df['Pclass'] == num).sum()
  num_class = num_class_count / df.shape[0] * 100
  return round(num_class, 2), num_class_count

first_class, second_class, third_class = class_count(df, 1), class_count(df, 2), class_count(df, 3)

print('First class percentage = ', first_class[0], ' | Count: ', first_class[1])
print('Second class percentage = ', second_class[0], ' | Count: ', second_class[1])
print('Third class percentage = ', third_class[0], ' | Count: ', third_class[1])

"""We see that:



*   the first class represents about a quarter of the passengers on board (≈ 24%)
*   the second class represents a little less than a quarter of the passengers on board (≈ 20%)
*   the third class represents more than half of the passengers onboard (≈ 55%)

Let's now compare these percentages with the survival ones.
"""

get_survival_rate(df, 'Pclass')

"""With these survival rates, we can see that:

*   The first class represents ≈ 24% of the passengers, but ≈ 40% of the survivors
*   The second class represents ≈ 20% of the passengers, but ≈ 25% of the survivors
*   The third class representes ≈ 55% of the passengers, but ≈ 34% of the survivors

Let's visualize these results to get a better understanding.
"""

def get_counts(df, col, num, status):
    target = df[col].where(df[col] == num)
    class_count = target.where(df['Survived'] == status).count()
    return class_count
def gen_plot(survival_array, death_array, by_factor, x_ticks):
    abs_survival_list = np.array(survival_array)
    abs_death_list = np.array(death_array)
    N = len(abs_survival_list)
    ind = np.arange(N)
    width = 1 / N

    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
    ax1.bar(ind, abs_survival_list, width, color='#00FFFF', label='Survival', alpha=0.8)
    ax1.bar(ind, abs_death_list, width, color='#FF00FF', label='Death', alpha=0.8, bottom=abs_survival_list)
    plt.sca(ax1)
    plt.xticks(ind, x_ticks)
    ax1.set_title('Absolute count ' + by_factor)
    ax1.set_ylabel('Count')
    ax1.legend(loc='upper left')
    plt.setp(plt.gca().get_xticklabels(), rotation=45)

    per_survival_list = (abs_survival_list / (abs_survival_list + abs_death_list)) * 100
    per_death_list = (abs_death_list / (abs_survival_list + abs_death_list)) * 100

    ax2.bar(ind, per_survival_list, width, color='#00FFFF', label='Survival percentage', alpha=0.8)
    ax2.bar(ind, per_death_list, width, color='#FF00FF', label='Death percentage', alpha=0.8, bottom=per_survival_list)
    plt.sca(ax2)
    plt.xticks(ind, x_ticks)
    ax2.set_title('Percentage ' + by_factor)
    ax2.set_ylabel('Percentage')
    plt.setp(plt.gca().get_xticklabels(), rotation=45)

    return plt.show()
    
class1_survival_count = get_counts(df, 'Pclass', 1, 1)
class2_survival_count = get_counts(df, 'Pclass', 2, 1)
class3_survival_count = get_counts(df, 'Pclass', 3, 1)
class1_death_count = get_counts(df, 'Pclass', 1, 0)
class2_death_count = get_counts(df, 'Pclass', 2, 0)
class3_death_count = get_counts(df, 'Pclass', 3, 0)

gen_plot([class1_survival_count, class2_survival_count, class3_survival_count],
         [class1_death_count, class2_death_count, class3_death_count],
         'by ticket class',
         ['First class', 'Second class', 'Third class'])

"""We can see that there is a clear correlation between death and ticket class: the higher your ticket class, the higher your chances of survival."""