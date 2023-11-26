
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
data10= pd.concat([data7, data8],axis=1)
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


# # ANN Model Creation
# Importing the Keras libraries and packages
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LeakyReLU,PReLU,ELU
from keras.layers import Dropout
from keras.optimizers import SGD
#In ANN , if the target variable is categorivcal , we need to perform one hot encoding
y= pd.get_dummies(y)
y.head()
# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)
# Initialising the ANN
classifier = Sequential()
# Adding the input layer and the first hidden layer
#we are giving output_dim=6,input_dim=11 as we have 11 input features
#we are using init='he_uniform'initialization,we are using activation='relu',generally relu performs well
classifier.add(Dense(output_dim =26, init = 'he_uniform',activation='relu',input_dim = X_train.shape[1]))
# Adding the second hidden layer
classifier.add(Dense(output_dim =26, init = 'he_uniform',activation='relu'))
# Adding the second hidden layer
classifier.add(Dense(output_dim =26, init = 'he_uniform',activation='relu'))
# Adding the output layer
#as output layer will be 1 so we are using output_dim=1
#In output layer case , we are using activation function=sigmoid
classifier.add(Dense(output_dim = 3, init = 'he_uniform', activation = 'softmax'))
opt = SGD(lr=0.2, momentum=0.7)
# Compiling the ANN
#here we are uisng opimizer=Adamax,loss=binary_crossentropy as it is binary classification
#metrics=accuracy
classifier.compile(optimizer = opt, loss = 'categorical_crossentropy', metrics = ['accuracy'])
# Fitting the ANN to the Training set
#we are making model
model_history=classifier.fit(X_train, y_train,validation_split=0.1, batch_size = 10, nb_epoch = 200)
# evaluate the model
_, train_acc = classifier.evaluate(X_train, y_train, verbose=0)
_, test_acc = classifier.evaluate(X_test, y_test, verbose=0)
print('Train: %.3f, Test: %.3f' % (train_acc, test_acc))

