
#Importing libraries
import numpy as np
import pandas as pd
import seaborn as sns
#reading data
df = pd.read_csv("taedata.txt",header = None)
df.head()
# # Dataset Preparation 
#adding features name to the data
data=pd.DataFrame(df.values, columns = ["englishSpeaker", "CourseInstructor", "Course", "Semester","Classsize","grade"])
data.head()
data1=pd.DataFrame(data,columns={"CourseInstructor","Course"})
data2= pd.get_dummies(data1.Course,prefix='Course',drop_first=True)
data2.head()
data3 = pd.get_dummies(data1.CourseInstructor, prefix='CourseInstructor',drop_first=True)
data3.head()
data4=pd.DataFrame(data,columns={"englishSpeaker"})
englishSpeaker1=[]
for i in data4.englishSpeaker:
    if i==1:
        englishSpeaker1.append(0)
    else :
        englishSpeaker1.append(1)
data4['englishSpeaker1']=englishSpeaker1
data4.head()
data5=pd.DataFrame(data,columns={"Semester"})
data5=pd.DataFrame(data,columns={"Semester"})
Semester1=[]
for i in data5.Semester:
    if i==1:
        Semester1.append(0)
    else :
        Semester1.append(1)
data5['Semester1']=Semester1
data5.head()
data6= pd.concat([data4, data5],axis=1)
data6.head()
data7=pd.DataFrame(data6,columns={"englishSpeaker1","Semester1"})
data7.head()
data8= pd.concat([data2, data3],axis=1)
data8.head()
data10= pd.concat([data8, data7],axis=1)
data10.head()
data9=pd.DataFrame(data,columns={"Classsize"})
data9.head()
# # Feature Scaling
#from sklearn.preprocessing import StandardScaler
#sc= StandardScaler()
from sklearn.preprocessing import MinMaxScaler
sc= MinMaxScaler()
classsize= sc.fit_transform(data9)
data11=pd.DataFrame(classsize, columns=['classsize']) 
data11.head()
X= pd.concat([data11, data10],axis=1)
X.head()
y=data['grade']
y.head()
# # Model Creation
from numpy import loadtxt
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
# split data into train and test sets
seed = 7
test_size = 0.10
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=seed)
# fit model no training data
model = XGBClassifier()
model.fit(X_train, y_train)
print(model)
# make predictions for test data
y_pred = model.predict(X_test)
predictions = [round(value) for value in y_pred]
#evaluate predictions
accuracy = accuracy_score(y_test, predictions)
print("Accuracy: %.2f%%" % (accuracy * 100.0))
from sklearn.model_selection import cross_val_score
score=cross_val_score(model,X,y,cv=40)
score
score.mean()

# # Hyperparameter optimization
from datetime import datetime
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold
from xgboost import XGBClassifier
import numpy as np
from sklearn.model_selection import RandomizedSearchCV
# Number of trees in random forest
n_estimators = [int(x) for x in np.linspace(start = 200, stop = 2000, num = 10)]
# Number of features to consider at every split
max_features = ['auto', 'sqrt','log2']
# Maximum number of levels in tree
max_depth = [int(x) for x in np.linspace(10, 1000,10)]
# Minimum number of samples required to split a node
min_samples_split = [2, 5, 10,14]
# Minimum number of samples required at each leaf node
min_samples_leaf = [1, 2, 4,6,8]
# Create the random grid
random_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
              'criterion':['entropy','gini']}
print(random_grid)
rf=XGBClassifier()
rf_randomcv=RandomizedSearchCV(estimator=rf,param_distributions=random_grid,n_iter=100,cv=5,verbose=2,
                               random_state=100,n_jobs=-1)
### fit the randomized model
rf_randomcv.fit(X_train,y_train)
rf_randomcv.best_params_
rf_randomcv
best_random_grid=rf_randomcv.best_estimator_
from sklearn.metrics import confusion_matrix,classification_report,accuracy_score
from sklearn.metrics import accuracy_score
y_pred=best_random_grid.predict(X_test)
print(confusion_matrix(y_test,y_pred))
print("Accuracy Score {}".format(accuracy_score(y_test,y_pred)))
print("Classification report: {}".format(classification_report(y_test,y_pred)))

