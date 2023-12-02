
## Stock Price Prediction Api using LSTM

### ABSTRACT :
Stock price prediction is the most significantly used in the financial sector. Stock market is volatile in nature, so it is difficult to predict stock prices. This is a time series problem. Stock price prediction is a difficult task where there are no rules to predict the price of the stock in the stock market. There are so many existing methods for predicting stock prices. The prediction methods are Logistic Regression Model, SVM, ARCH model, RNN, CNN, Backpropagation, Naïve Bayes, ARIMA model, etc. In these models, Long Short-Term Memory (LSTM) is the most suitable algorithm for time series problems. The main objective is to forecast the current market trends and could predict the stock prices accurately. We use LSTM recurrent neural networks to predict the stock prices accurately. 


###  DATA COLLECTION : 



![Data](https://cdn.sanity.io/images/l2tpt56d/production/890a48ede0462bb1e278723bf12977201914cd50-1824x542.png)

For the experimental study, we downloaded live datasets namely google, nifty, reliance, etc. from the Yahoo Finance website (https://finance.yahoo.com/).



### METHODOLOGIES : 
LSTM uses the RNN approach which has the ability to memorize. Each LSTM cell has three gates i.e. input, forget and output gates. While the data that enters the LSTM’s network, the data that is required is kept and the unnecessary data will be forgotten by the forget gate.

![LSTM](https://cdn.sanity.io/images/l2tpt56d/production/1d93ac59a3daab25a14549e6b4b86cec0ac49739-1236x680.png)


Forget Gate:

A forget gate will remove unnecessary data from the cell state.
- The information that is less important or not required for the LSTM to understand things is removed by performing multiplication of hidden state by a sigmoid function.
- This step is necessary to optimize the performance of the model.
- It takes two inputs i.e., h(t-1) and xt, where h(t-1) is the previous cell hidden state
output and xt is the current cell input.
Ft =σ(Wfx *Xt+Wfh *ht-1 +bf)

![Forget Gate](https://cdn.sanity.io/images/l2tpt56d/production/fab06435ef98f93f6c71c5df5e10cfdf7c46c0fc-1216x124.png)


Input Gate:
- This cell is responsible for regulating the data that is added to the cell from the input. Forget gate is used to filter some input.
- A vector is created by adding all the possible values from the previous cell hidden state h(t-1) and current cell input Xt by using the tanh function. The output of the tanh function in the ranges of [-1, 1].
- Finally, the outputs of sigmoid and tanh functions are multiplied and the output is added to the cell state.

![Input Gate](https://cdn.sanity.io/images/l2tpt56d/production/6a4c8fe150f30a482efc0745c3ba76edcd39f6cb-1230x118.png)

Output Gate:
 - Tanh function is applied to the cell state to create a vector with all possible values.
 - Sigmoid function is applied to previous cell hidden state h(t-1) and current cell input xt to filter necessary data from the previous cell.
 - Now, the outputs of sigmoid and tanh functions are multiplied and this output is sent as a hidden state of the next cell.

![Output Gate](https://cdn.sanity.io/images/l2tpt56d/production/4b46ef5bac6c1a989a4781108af8c8b5d993b3d7-862x120.png
)

### SYSTEM ARCHITECTURE : 

![System Architecture](https://cdn.sanity.io/images/l2tpt56d/production/36b95a3689d6e5f228ddff87bfe9f2640dc8fe6e-1496x598.png)

### Data Selection: 
The first step is to select data for an organization and split the data into training and testing. we have used 75% for training and 25% for testing purposes.
### Pre-processing of data: 
In pre-processing, we are selecting attributes required for the algorithm and the remaining attributes are neglected. The selected attributes are Trade Open, Trade High, Trade Low, Trade Close, Trade Volume. In pre-processing, we are using normalization to get values in a particular range.
### Prediction using LSTM: 
In this system, we are using the LSTM algorithm for predicting stock values. Initially, the training data is passed through the system and train the model. Then in the testing phase, the predicted values are compared with the actual values.
### Evaluation: 
In the evaluation phase we are calculating the Accuracy, Mean Square Error (MSE) and Root Mean Square Error (RMSE) values for comparison.