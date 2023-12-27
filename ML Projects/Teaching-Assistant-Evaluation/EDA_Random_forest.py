
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
# # Checking null value
data.isnull().sum()
# # Summary Statistics for numerical features(Classsize)
#Classsize is the numerical feature so we are finding summary stattistics for this feature
data.Classsize.describe()
data.info()
# # Exploratory Data Analysis for Numerical features(EDA)
#Univariate Analysis
sns.distplot(data['Classsize'])
# # Checking classsize is gaussian distributed or not
##QQ-plot
import statsmodels.api as sm 
import pylab as py 
sm.qqplot(data.Classsize,line='s') 
py.show() 
# # The feature Classsize follows Gaussian distribution

# # Outliers in Numerical Features
figure=data.boxplot(column="Classsize")
# * Outliers are present in Classsize feature
# * We need to remove outliers from the feature
# * 3 sigma technique is used to remove outliers as the feature follows Gaussian distribution

# # Outlier Detection
uppper_boundary=data['Classsize'].mean() + 3* data['Classsize'].std()
lower_boundary=data['Classsize'].mean() - 3* data['Classsize'].std()
print(lower_boundary), print(uppper_boundary),print(data['Classsize'].mean())
data.loc[data['Classsize']>=66,'Classsize']=60
data.head()
#Outlier removal
figure=data.boxplot(column="Classsize")
# # Checking the balance of the class
sns.countplot('grade',data=data)
data_grade=data['grade'].value_counts()
data_grade
# * The class is balance

# # Bar graph for Categorical features
#checking for all categorical features
sns.countplot('englishSpeaker',data=data)
data_englishSpeaker=data['englishSpeaker'].value_counts()
data_englishSpeaker
#Checking for CourseInstructor
sns.countplot('CourseInstructor',data=data)
data_CourseInstructor=data['CourseInstructor'].value_counts()
data_CourseInstructor.head()
#Checking for Course
sns.countplot('Course',data=data)
data_Course=data['Course'].value_counts()
data_Course.head()
#checking for Semester
sns.countplot('Semester',data=data)
data_Semester=data['Semester'].value_counts()
data_Semester.head()
# # Summer Semester and Regular Semester Analysis
# # Summer semester data
summerSemesterdata=data[data['Semester']==1]
summerSemesterdata.head()
summerSemesterdata.shape
# # Regular semester data
#Regular semester data
regularSemesterdata=data[data['Semester']==2]
regularSemesterdata.head()
regularSemesterdata.shape
# # Feature Important
from sklearn.ensemble import ExtraTreesRegressor
import matplotlib.pyplot as plt
model=ExtraTreesRegressor()
X_data=data.iloc[:,:5]
y_data=data['grade']
model.fit(X_data,y_data)
feature_importances=pd.Series(model.feature_importances_,index=X_data.columns)
feature_importances.nlargest(5).plot(kind='barh')
# # Hypothesis testing

# * Pearson’s correlation can not be used for categorical features. So we are using Chi-squared test.
# * Hypothesis testing is performed on categorical feature using Chi-Squared test.

# # Contingency Table showing correlation between CourseInstructor and Course
#contigency table
data_courseInstructor = pd.crosstab(data['Course'], 
                            data['CourseInstructor'],  
                               margins = False) 
data_courseInstructor.head()
# * 22 Instructor has taught 3 times course 1
# 
# * 3 Instructor has taught 2 times course 2
# 
# * Course X-axis,CourseInstructor Y-axis
#Heat Map for contigency table
sns.heatmap(pd.crosstab(data.Course, data.CourseInstructor),
            cmap="YlGnBu", annot=True, cbar=True)
#contigency table
data_englishSpeaker= pd.crosstab([data.CourseInstructor,data.Course], 
                            data['englishSpeaker'],  
                               margins = False) 
data_englishSpeaker.head()


# * CourseInstructor 1 has taught courses 8 and 15 and he is english non-speaker,course 15 has been taught by other 2 courseInstructor which were also english non-speaker 
#Heat Map for contigency table
sns.heatmap(pd.crosstab([data.CourseInstructor,data.Course], data.englishSpeaker),
            cmap="YlGnBu", annot=True, cbar=True)
#contigency table
data_englishSpeaker= pd.crosstab([data.CourseInstructor,data.Course], 
                            [data.englishSpeaker,data.Semester],  
                               margins = False) 
data_englishSpeaker.head(10)
#Heat Map for contigency table
sns.heatmap(pd.crosstab([data.CourseInstructor,data.Course], [data.englishSpeaker,data.Semester]),
            cmap="YlGnBu", annot=True, cbar=True)
# # Hypothesis Sample

# H0: The features CourseInstructor and Course are independent (which means they are not associated).
# 
# H1: CourseInstructor and Course are not independent (which means they are associated).
# 
# H0: All CourseInstructor are not englishSpeaker
# 
# H1: All CourseInstructor are englishSpeaker(Rejecting null hypothesis)
from scipy.stats import chi2_contingency
from scipy.stats import chi2
stat, p, dof, expected = chi2_contingency(data_courseInstructor)
print('dof=%d' % dof)
#print(expected)
# interpret test-statistic
prob = 0.95
critical = chi2.ppf(prob, dof)
print('probability=%.3f, critical=%.3f, stat=%.3f' % (prob, critical, stat))
if abs(stat) >= critical:
	print('H0: The features CourseInstructor and Course are independent')
else:
	print('H1: CourseInstructor and Course are not independent (which means they are associated).')
# interpret p-value
alpha = 1.0 - prob
print('significance=%.3f, p=%.3f' % (alpha, p))
if p <= alpha:
	print('H0: The features CourseInstructor and Course are independent')
else:
	print('H1: CourseInstructor and Course are not independent (which means they are associated)')
stat, p, dof, expected = chi2_contingency(data_englishSpeaker)
print('dof=%d' % dof)
#print(expected)
# interpret test-statistic
prob = 0.95
critical = chi2.ppf(prob, dof)
print('probability=%.3f, critical=%.3f, stat=%.3f' % (prob, critical, stat))
if abs(stat) >= critical:
	print('H0:All CourseInstructor are not englishSpeaker')
else:
	print('H1:All CourseInstructor are englishSpeaker(Rejecting null hypothesis)')
# interpret p-value
alpha = 1.0 - prob
print('significance=%.3f, p=%.3f' % (alpha, p))
if p <= alpha:
	print('H0:All CourseInstructor are not englishSpeaker')
else:
	print('H1:All CourseInstructor are englishSpeaker(Rejecting null hypothesis)')


# # Preprocessing and Feature Engineering

# The quality of data is checked. The data has no missing value
# 
# The data has two categorical features: CourseInstructor and course.
# 
# CourseInstructor has 25 categories
# 
# Course has 26 categories

# # Handling Categorical Features

# #  1. One hot encoding
# 
# One hot encoding is performed on CourseInstructor and Course.
# 
# Dummy variable trap is handled.
# 
# We have 52 independent features.
# 
# Binary features Semester and englishInstructor are handled by replacing 1 as 0 and 2 as 1.
data1=pd.DataFrame(data,columns={"CourseInstructor","Course"})
#performing one hot encoding on the feature Course
data2= pd.get_dummies(data1.Course,prefix='Course',drop_first=True)
data2.head()
#performing one hot encoding on the feature CourseInstructor
data3 = pd.get_dummies(data1.CourseInstructor, prefix='CourseInstructor',drop_first=True)
data3.head()
# As the feature englishSpeaker is binary we need to convert in 0 and 1 to get good accuracy
data4=pd.DataFrame(data,columns={"englishSpeaker"})
englishSpeaker1=[]
for i in data4.englishSpeaker:
    if i==1:
        englishSpeaker1.append(0)
    else :
        englishSpeaker1.append(1)
data4['englishSpeaker1']=englishSpeaker1
data4.head()
# As the feature Semester is binary we need to convert in 0 and 1 to get good accuracy
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
#Combining the dataframe
data6= pd.concat([data4, data5],axis=1)
data6.head()
#taking englishSpeaker1 and Semester1
data7=pd.DataFrame(data6,columns={"englishSpeaker1","Semester1"})
data7.head()
#combining the features
data8= pd.concat([data2, data3],axis=1)
data8.head()
#combining the features
data10=pd.concat([data8, data7],axis=1)
data10.head()
#Storing the feature Classsize in a seperate dataframe
data9=pd.DataFrame(data,columns={"Classsize"})
data9.head()
# # Feature Scaling
#from sklearn.preprocessing import StandardScaler
#sc= StandardScaler()
from sklearn.preprocessing import MinMaxScaler
sc= MinMaxScaler()
classsize = sc.fit_transform(data9)
data11=pd.DataFrame(classsize, columns=['classsize']) 
data11.head()
X= pd.concat([data11, data10],axis=1)
X.head()
y=data['grade']
y.head()
# # Model Creation
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.1, random_state = 0)
classifier=RandomForestClassifier()
classifier.fit(X_train,y_train)
y_pred=classifier.predict(X_test)
y_pred1=classifier.predict_proba(X_test)
from sklearn.metrics import accuracy_score,roc_auc_score
print("Accuracy_score: {}".format(accuracy_score(y_test,y_pred)))
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
confusion_matrix(y_test, y_pred)
print("=== Classification Report ===")
print(classification_report(y_test, y_pred))
# This means that all your positive samples are classified as positive samples and none of the positive samples are classified incorrectly.
# 
# While precision refers to the percentage of your results which are relevant, recall refers to the percentage of total relevant results correctly classified by your algorithm. ... For problems where both precision and recall are important, one can select a model which maximizes this F-1 score

# # Hyperparameter Optimization

# # Randomized Search Cv
import numpy as np
from sklearn.model_selection import RandomizedSearchCV
# Number of trees in random forest
n_estimators = [int(x) for x in np.linspace(start = 200, stop = 2000, num = 10)]
# Number of features to consider at every split
max_features = ['auto', 'sqrt','log2']
# Maximum number of levels in tree
max_depth = [int(x) for x in np.linspace(10, 1000,10,1500)]
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
rf=RandomForestClassifier()
rf_randomcv=RandomizedSearchCV(estimator=rf,param_distributions=random_grid,n_iter=100,cv=5,verbose=2,
                               random_state=100,n_jobs=-1)
### fit the randomized model
rf_randomcv.fit(X_train,y_train)
rf_randomcv.best_params_
rf_randomcv
best_random_grid=rf_randomcv.best_estimator_
from sklearn.metrics import accuracy_score
y_pred=best_random_grid.predict(X_test)
print(confusion_matrix(y_test,y_pred))
print("Accuracy Score {}".format(accuracy_score(y_test,y_pred)))
print("Classification report: {}".format(classification_report(y_test,y_pred)))
# # Performed one-hot encoding on most 5 frequent categories and put 0 for remaining.
kdddata=data.copy()
kdddata1=pd.DataFrame(kdddata,columns={"CourseInstructor","Course"})
#Checking the categories in the dataset
for i in kdddata1.columns:
    print(i,":",len(kdddata1[i].unique()),"labels")
kdddata1.CourseInstructor.value_counts().sort_values(ascending=False).head(10)
kdddata1.Course.value_counts().sort_values(ascending=False).head(10)
#print top 10 features for CourseInstructor_10
CourseInstructor_10=kdddata1.CourseInstructor.value_counts().sort_values(ascending=False).head(10).index
CourseInstructor_10=list(CourseInstructor_10)
CourseInstructor_10
#print top 10 features for Course
Course_10=kdddata1.Course.value_counts().sort_values(ascending=False).head(10).index
Course_10=list(Course_10)
Course_10
import numpy as np
for categories in CourseInstructor_10:
    kdddata1[categories]=np.where(kdddata1['CourseInstructor']==categories,1,0)
kdddata1.head()
kdddata1 = kdddata1.add_suffix('CourseInstructor')
kdddata1.head()
for categories in Course_10:
    kdddata1[categories]=np.where(kdddata1['CourseCourseInstructor']==categories,1,0)
kdddata1.head()
kdddata2=kdddata1.iloc[:,2:22]
kdddata2.head()
kdddata2.shape
#combining the features
kdddata3=pd.concat([data7, kdddata2],axis=1)
kdddata3.head()
X_kddata= pd.concat([data11, kdddata3],axis=1)
X_kddata.head()
ykddata=data['grade']
X_trainkdd, X_testdd, y_traindd, y_testdd = train_test_split(X_kddata, ykddata, test_size = 0.1, random_state = 0)
classifierkdd=RandomForestClassifier()
classifierkdd.fit(X_trainkdd,y_traindd)
y_predkdd=classifierkdd.predict(X_testdd)
y_pred1kdd=classifierkdd.predict_proba(X_testdd)
from sklearn.metrics import accuracy_score,roc_auc_score
print("Accuracy_score: {}".format(accuracy_score(y_testdd,y_predkdd)))
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
confusion_matrix(y_testdd, y_predkdd)
print("=== Classification Report ===")
print(classification_report(y_testdd, y_predkdd))
# # Conclusion
# As we can see from the result that method one for one-hot encoding is giving better result in our case.
