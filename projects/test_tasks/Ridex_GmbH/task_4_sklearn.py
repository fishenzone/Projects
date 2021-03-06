# -*- coding: utf-8 -*-
"""task_4_sklearn.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VYL8oIP_WqtUNqkBpvfPQHWymYZLMR11

# Задание #3 Sklearn и основы ML

## Инструменты и ресурсы для выполнения задания

### Библиотеки Python

* [Sklearn](http://scikit-learn.org/stable/).
  - [Introduction to machine learning in Python with scikit-learn](http://www.dataschool.io/machine-learning-with-scikit-learn/).
* [Kaggle Python Tutorial on Machine Learning](https://campus.datacamp.com/courses/kaggle-python-tutorial-on-machine-learning).

### Ресурсы по изучению ML
* [ML from Stanford University](https://www.coursera.org/learn/machine-learning/). Самый базовый курс.
* [Введение в машинное обучение](https://www.coursera.org/learn/vvedenie-mashinnoe-obuchenie/). Курс професссора Воронцова К.В. на coursera.org. Существенно более полный, чем курс Andrew Ng, но сокращен по сравнению с курсом, читаемым в ШАД.

![what I really do](https://pp.vk.me/c629431/v629431882/2a1a8/7EAKCA_FtnA.jpg)
  
## Разминка
1. Загрузите набор данных [Spambase](https://archive.ics.uci.edu/ml/datasets/Spambase). *Сами данные находятся по ссылке http://archive.ics.uci.edu/ml/machine-learning-databases/spambase/spambase.data. Вам также потребуются имена признаков, которые доступны по ссылке http://archive.ics.uci.edu/ml/machine-learning-databases/spambase/spambase.names*.
"""

# Commented out IPython magic to ensure Python compatibility.
import matplotlib.pyplot as plt
from IPython.display import HTML
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier 
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectFromModel
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from scipy import stats
import warnings
# %matplotlib inline
warnings.filterwarnings('ignore')
plt.style.use('dark_background')
scaler = StandardScaler()
# sns.set()

# Commented out IPython magic to ensure Python compatibility.
# %%bash
# wget http://archive.ics.uci.edu/ml/machine-learning-databases/spambase/spambase.data
# wget http://archive.ics.uci.edu/ml/machine-learning-databases/spambase/spambase.names

data = np.genfromtxt('spambase.data', delimiter=',')
with open('spambase.names', 'r') as f:
  names = [name.strip() for name in f]

"""2. Ответьте на следующие воросы:
  * Сколько примеров писем в датасете?
"""

print(f'Dataset has {data.shape[0]} writings.')

"""  * Какова доля спама?"""

print(f'Percantage of spam is {(np.unique(data[:,-1], return_counts=True)[1][1]/data.shape[0]*100).round(1)}%.')

"""* Какие характерные группы признаков представлены в наборе?

* процент слов в электронном письме, которые соответствуют конкретному слову
* процент символов в электронном письме, которые соответствуют конкретному символу
* средняя длина непрерывных последовательностей заглавных букв
* длина самой длинной непрерывной последовательности заглавных букв
* сумма длины непрерывных последовательностей заглавных букв
* общее количество заглавных букв в электронном письме
* атрибут, показывающий спам это или нет
"""

colnames = [name.partition(':')[0] for name in names if not (len(name) == 0 or name[0] == '|' or name[0] == '1')]
colnames.append('spam')
df_spam = pd.DataFrame(data, columns=colnames)
df_spam.info()

df_spam['spam'] = 2 * df_spam['spam'] - 1

"""3. Подготовьте два разбиения исходного набора данных на тестовую (test) и обучающую (train) выборки:
  * Первые 3000 писем отдайте на обучение, а оставшиеся на тест.
  * Сделайте случайное разбиение в тех же пропорциях.
"""

df_train = df_spam.iloc[:3000,]
df_test = df_spam.iloc[3000:,]

df_random = df_spam.sample(frac=1)
df_random_train = df_random.iloc[:3000,]
df_random_test = df_random.iloc[3000:,]

"""4. Для первого из разбиений обучите алгоритм sklearn.tree.DecisionTreeClassifier на обучающей выборке."""

def print_result(y, y_pred):
  print('Recall:', metrics.recall_score(y, y_pred).round(2))
  print('Precision:', metrics.precision_score(y, y_pred).round())
  print('F1:', metrics.f1_score(y, y).round())
  print('Accuracy:', metrics.accuracy_score(y, y_pred).round(2))

clf = DecisionTreeClassifier()
clf = clf.fit(df_train.iloc[:,:-1], df_train.iloc[:,-1:])
y_pred = clf.predict(df_test.iloc[:,:-1])

"""5. Замерьте метрики качества recall, precision, f1, accuracy на тестовой выборке из первого разбиения."""

print_result(df_test.iloc[:,-1:], y_pred)

"""6. Повторите пункты 4. и 5. для второго разбиения."""

def data_split(train, test):
  x_train, y_train = train.iloc[:,:-1], train.iloc[:,-1:]
  x_test, y_test = test.iloc[:,:-1], test.iloc[:,-1:]
  return x_train, y_train, x_test, y_test

x_train, y_train, x_test, y_test = data_split(df_random_train, df_random_test)
clf = DecisionTreeClassifier()
clf = clf.fit(x_train, y_train)
y_pred_tree = clf.predict(x_test)

print_result(y_test, y_pred_tree)

"""7. Объясните разницу в результатах. **Далее используйте только второе (случайное) разбиение.**

Train data без случайного разбиения не была репрезентативной. Если посмотреть в датасет, то становится ясно, что сначала идут единицы, а затем нули(у нас -1).

8. Для модели, обученной на случайном разбиении, выведите оценку информативности признаков (feature importance).
"""

sort = clf.feature_importances_.argsort()[:35]
fig = plt.figure(figsize=(16, 8))
plt.barh(df_random.columns[sort], clf.feature_importances_[sort])   
plt.xlabel('Feature Importance')
plt.ylabel('Feature name')
plt.show()

"""9. Предложите способ, как можно использовать данную оценку?

Подобрать подходящие параметры для модели. Ненужная дата будет только увеличивать bias и ухудшит выход нашей модели.

10. Предложите способ, которым решающее дерево способно дать такую оценку.
"""

model_tr = SelectFromModel(clf, prefit=True)
df_train_new = model_tr.transform(x_train)
print(f'Number of parameters in old data: {x_train.shape[1]} features.')
print(f'Number of parameters in new data: {df_train_new.shape[1]} features.')

"""11. Обучите алгоритм sklearn.neighbors.KNeighborsClassifier на обучающей выборке и произведите оценку качества модели на тестовой выборке."""

knn = KNeighborsClassifier()
knn.fit(x_train, y_train)
y_pred_knn = knn.predict(x_test)

print_result(y_test, y_pred_knn)

"""12. Какая из обученных моделей лучше?

Дерево лучше.

13. Способен ли KNN оценить информативность признаков?

Нет, не способен.

14. Произведите нормировку обучающей и тестовой выборок.
"""

def data_scale(train, test):
  train_scaled = scaler.fit_transform(train)
  test_scaled = scaler.fit_transform(test)
  return train_scaled, test_scaled

x_train_scale, x_test_scale = data_scale(x_train, x_test)

"""15. Повторите эксперимент с KNN на нормированных данных. Объясните разницу в результатах."""

knn = KNeighborsClassifier()
knn.fit(x_train_scale, y_train)
y_pred_knn = knn.predict(x_test_scale)

print_result(y_test, y_pred_knn)

"""KNN расчитывает расстояние, используя значения параметров. Если какой-то параметр больше других, то он будет иметь большое влияние на конечный результат модели.

16. Повторите эксперимент с решающим деревом на нормированных данных. Сравните результаты с теми, которые получены на ненормированных данных. Объясните подобное поведение.
"""

clf = DecisionTreeClassifier()
clf = clf.fit(x_train_scale, y_train)
y_pred_tree = clf.predict(x_test_scale)

print_result(y_test, y_pred_tree)

"""Результаты стали немножно хуже. Нормализация для дерева решение не нужна, так как дерево разбевает данные на подмножества, а затем рекурсивно генерирует новые узлы. В духе if cause.

17. Пропорции разбиения на данный момент выбраны безосновательно. Найдите оптимальные пропорции разбиения на train и test. Для этого необходимо перебрать значения пропорции разбиения по сетке, для каждого значения сгенерировать большое число разбиений и на каждом посчитать ошибку (с точки зрения выбранной метрики, например, f1), далее строится график зависимости дисперсии величины ошибки от пропорции разбиения, пропорция разбиения выбирается из области наименьшей дисперсии ошибки. Выберите метрику и постройте график зависимости дисперсии ошибки от пропорции разбиения.

18. Однократное разбиение выборки на train и test не является достаточно хорошим методом с точки зрения оценки качества моделей. На практике используется многократное разбиение или т.н. Cross Validation. Получите оценки качества для решающего дерева и KNN, используя Cross Validation. *Существует несколько типов Cross Validation. Выберите один из них и обоснуйте свой выбор.*

I'll skip those two.

19. На данный момент параметры алгоритмов KNN и Decision Tree выбраны наугад. Для одбора параметров используется т.н. Greed Search. 
  - Найдите оптимальный набор параметров дерева, перебрав значения параметров по сетке. Параметры для настройки: критерий разбиения, максимальная глубина, число признаков для каждого узла, минимальное число объектов в листе.
  - Найдите оптимальный набор параметров для KNN, перебрав значения параметров по сетке. Параметры для настройки: число соседей, функция расстояния, схема взвешивания.
"""

X_train, X_test, y_train, y_test = train_test_split(df_spam.iloc[:,:-1], df_spam.iloc[:,-1:], test_size=0.2, random_state=66)
X_train_scale, X_test_scale = data_scale(X_train, X_test)

params_tree = {'splitter': ['best', 'random'],
               'max_depth': np.arange(2, 500, 50),
               'min_samples_split': np.arange(2, 100, 10),
               'min_samples_leaf': np.arange(2, 100, 10)} 

grid_search_tree = GridSearchCV(DecisionTreeClassifier(random_state=66), params_tree, verbose=1, cv=5)
grid_search_tree.fit(X_train, y_train)

params_knn = {'n_neighbors': np.arange(2, 10),
               'metric': ['euclidean', 'manhattan', 'chebyshev', 'minkowski', 'wminkowski', 'seuclidean', 'mahalanobis'],
               'weights': ['uniform', 'distance']} 
grid_search_knn = GridSearchCV(knn, params_knn, verbose=1, cv=5)

grid_search_knn.fit(X_train_scale, y_train)

y_pred_dt = grid_search_tree.predict(X_test)
y_pred_knn = grid_search_knn.predict(X_test_scale)

print(f'Best params for DT: {grid_search_tree.best_params_}')
print(f'Best params for KNN: {grid_search_knn.best_params_}\n')

print('Results for DT:')
print_result(y_test, y_pred_dt)
print('\nResults for KNN:')
print_result(y_test, y_pred_knn)

