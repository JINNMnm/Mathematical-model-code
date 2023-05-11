import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn import tree

# Read the data
data = pd.read_csv('titanic.csv')
inputs = data.drop(['Name','Cabin','Ticket','Embarked','PassengerId'], axis='columns')
inputs = inputs.dropna(axis = 0)
target = inputs['Survived']
inputs = inputs.drop(['Survived'], axis='columns')

le = LabelEncoder()

inputs['Pclass_n'] = le.fit_transform(inputs['Pclass'])
inputs['Sex_n'] = le.fit_transform(inputs['Sex'])
inputs['SibSp_n'] = le.fit_transform(inputs['SibSp'])
inputs['Parch_n'] = le.fit_transform(inputs['Parch'])
inputs_n = inputs.drop(['Pclass','Sex','SibSp','Parch','Fare'], axis='columns')

# Create and train the model
model = tree.DecisionTreeClassifier()
model.fit(inputs_n,target)
print(model.predict([[1,1,0,0,0]]))
print(model.score(inputs_n,target))

