import pandas as pd
import numpy as np
import sklearn
from sklearn import linear_model
from sklearn.utils import shuffle

data = pd.read_csv('./data/student-mat.csv', sep=';')

data = data[
    ['G1', 'G2', 'G3', 'studytime', 'failures', 'absences']
    ]

predict_label = 'G3'

x = np.array(data.drop([predict_label], 1))
y = np.array(data[predict_label])

x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.1)

linear = linear_model.LinearRegression()

linear.fit(x_train, y_train)
accuracy = linear.score(x_test, y_test)
print('Model accuracy', accuracy)

print('Co-efficient: \n', linear.coef_)
print('Intercept: \n', linear.intercept_)

predictions = linear.predict(x_test)

for x in range(len(predictions)):
    print('Predicted grade: ', predictions[x])
    print('Input data: ', x_test[x], 'Actual grade: ', y_test[x])