
#Importing libraries
import numpy as np
import pandas as pd
import seaborn as sns
#reading data
df = pd.read_csv("taedata.txt",header = None)
df.head()
# # Dataset Preparation
data=pd.DataFrame(df.values, columns = ["englishSpeaker", "CourseInstructor", "Course", "Semester","Classsize","grade"])
data.head()
#separating Categorical features from dataframe
data1=pd.DataFrame(data,columns={"CourseInstructor","Course"})
#applying one-hot encoding
data2= pd.get_dummies(data1.Course,prefix='Course',drop_first=True)
data2.head()
#applying one-hot encoding on CourseInstructor
data3 = pd.get_dummies(data1.CourseInstructor, prefix='CourseInstructor',drop_first=True)
data3.head()
#converting binary features into 0 and 1
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
#converting binary features into 0 and 1
data5=pd.DataFrame(data,columns={"Semester"})
Semester1=[]
for i in data5.Semester:
    if i==1:
        Semester1.append(0)
    else :
        Semester1.append(1)
data5['Semester1']=Semester1
data5.head()
#combining the features
data6= pd.concat([data4, data5],axis=1)
data6.head()
data7=pd.DataFrame(data6,columns={"englishSpeaker1","Semester1"})
data7.head()
data8= pd.concat([data2, data3],axis=1)
data8.head()
data10=pd.concat([data8, data7],axis=1)
data10.head()
data9=pd.DataFrame(data,columns={"Classsize"})
data9.head()
# # Feature Scaling (both StandardScaler and Min-max tried)
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
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix,classification_report
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state = 0)
from sklearn.svm import SVC 
svm_model_linear = SVC(kernel = 'linear', C = 1).fit(X_train, y_train) 
svm_predictions = svm_model_linear.predict(X_test) 
# model accuracy for X_test   
accuracy = svm_model_linear.score(X_test, y_test) 
print("The accuracy is ::::",accuracy)  
# creating a confusion matrix 
cm = confusion_matrix(y_test, svm_predictions) 
print(cm)
rbf = SVC(kernel='rbf', gamma=1, C=8).fit(X_train, y_train)
rbf_predictions = rbf.predict(X_test) 
  
# model accuracy for X_test   
accuracy_rbf = rbf.score(X_test, y_test) 
print(accuracy_rbf)
# creating a confusion matrix 
cm = confusion_matrix(y_test, rbf_predictions) 
print(cm)
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.cm import rainbow
get_ipython().run_line_magic('matplotlib', 'inline')
import warnings
warnings.filterwarnings('ignore')
svc_scores = []
kernels = ['linear', 'poly', 'rbf', 'sigmoid']
for i in range(len(kernels)):
    svc_classifier = SVC(kernel = kernels[i])
    svc_classifier.fit(X_train, y_train)
    svc_scores.append(svc_classifier.score(X_test, y_test))
colors = rainbow(np.linspace(0, 1, len(kernels)))
plt.bar(kernels, svc_scores, color = colors)
for i in range(len(kernels)):
    plt.text(i, svc_scores[i], svc_scores[i])
plt.xlabel('Kernels')
plt.ylabel('Scores')
plt.title('Support Vector Classifier scores for different kernels')
print("The score for Support Vector Classifier is {}% with {} kernel.".format(svc_scores[0]*100, 'Linear'))
# # Decision Tree Classifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
dt_scores = []
for i in range(1, len(X.columns) + 1):
    dt_classifier = DecisionTreeClassifier(max_features = i, random_state = 0)
    dt_classifier.fit(X_train, y_train)
    dt_scores.append(dt_classifier.score(X_test, y_test))
dt_scores
plt.plot([i for i in range(1, len(X.columns) + 1)], dt_scores, color = 'green')
for i in range(1, len(X.columns) + 1):
    plt.text(i, dt_scores[i-1], (i, dt_scores[i-1]))
plt.xticks([i for i in range(1, len(X.columns) + 1)])
plt.xlabel('Max features')
plt.ylabel('Scores')
plt.title('Decision Tree Classifier scores for different number of maximum features')
print("The score for Decision Tree Classifier is {}% with {} maximum features.".format(dt_scores[5]*100,6)
dt_scores[21]
# # Random Forest Classifier
rf_scores = []
estimators = [1500, 100, 200, 500, 1000]
for i in estimators:
    rf_classifier = RandomForestClassifier(n_estimators = i, random_state = 0)
    rf_classifier.fit(X_train, y_train)
    rf_scores.append(rf_classifier.score(X_test, y_test))
colors = rainbow(np.linspace(0, 1, len(estimators)))
plt.bar([i for i in range(len(estimators))], rf_scores, color = colors, width = 0.8)
for i in range(len(estimators)):
    plt.text(i, rf_scores[i], rf_scores[i])
plt.xticks(ticks = [i for i in range(len(estimators))], labels = [str(estimator) for estimator in estimators])
plt.xlabel('Number of estimators')
plt.ylabel('Scores')
plt.title('Random Forest Classifier scores for different number of estimators')
print("The score for Random Forest Classifier is {}% with {} estimators.".format(rf_scores[4]*100, [1500, 500]))
rf_classifier = RandomForestClassifier(n_estimators =1500, random_state = 0)
rf_classifier.fit(X_train, y_train)
y_pred=rf_classifier.predict(X_test)
from sklearn.metrics import accuracy_score,roc_auc_score
print("Accuracy_score: {}".format(accuracy_score(y_test,y_pred)))
print(confusion_matrix(y_test, y_pred))
print("=== Classification Report ===")
print(classification_report(y_test, y_pred))


# # K Neighbors Classifier
knn_scores = []
for k in range(1,21):
    knn_classifier = KNeighborsClassifier(n_neighbors = k)
    knn_classifier.fit(X_train, y_train)
    knn_scores.append(knn_classifier.score(X_test, y_test))
plt.plot([k for k in range(1, 21)], knn_scores, color = 'red')
for i in range(1,21):
    plt.text(i, knn_scores[i-1], (i, knn_scores[i-1]))
plt.xticks([i for i in range(1, 21)])
plt.xlabel('Number of Neighbors (K)')
plt.ylabel('Scores')
plt.title('K Neighbors Classifier scores for different K values')
print("The score for K Neighbors Classifier is {}% with {} nieghbors.".format(knn_scores[0]*100, 0))


# # SVM Hyperparameter using Use GridsearchCV
from sklearn.model_selection import GridSearchCV 
  
# defining parameter range 
param_grid = {'C': [0.1, 1, 10, 100, 500,1000],  
              'gamma': [1, 0.1, 0.01, 0.001, 0.0001,0.002], 
              'kernel': ['sigmoid']}  
  
grid = GridSearchCV(SVC(), param_grid, refit = True, verbose = 3) 
  
# fitting the model for grid search 
grid.fit(X_train, y_train) 
# print best parameter after tuning 
print(grid.best_params_) 
  
# print how our model looks after hyper-parameter tuning 
print(grid.best_estimator_) 
grid_predictions = grid.predict(X_test) 
# print classification report 
print(classification_report(y_test, grid_predictions)) 

