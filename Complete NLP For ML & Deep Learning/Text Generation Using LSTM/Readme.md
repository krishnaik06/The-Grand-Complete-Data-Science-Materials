# Text-Generation-Using-LSTM

## About the Project
The poem by Robert Frost "Stopping by words on the Snowing Evening" was converted from PDF to text, pre-processed, and tokenized using word indexes. It was transformed into 50-word sequences. An LSTM model with a vocabulary size and vector space of 50 was trained for 200 epochs, achieving 84.83 accuracy. 
![lstm](https://github.com/Mohitraj27/Text-Generation-Using-LSTM/assets/87956374/addf0791-2551-4953-8d63-eead3e8ab6d9)


### Automatic Text Generation
Automatic text generation is the generation of natural language texts by computer. It has applications in automatic documentation systems, automatic letter writing, automatic report generation, etc. In this project, we are going to generate words given a set of input words. We are going to train the LSTM model using Robert Frost poem Stopping by woods in a snowing evenining which is taken in pdf format and then converted into text file.

## Dataset Used
### Download Link
```
https://drive.google.com/file/d/1ZdSH2PJZROCHjz3PYKd7AtnzicbxWSh1/view?usp=sharing
```
```
Stopping by Woods on a Snowy Evening Robert Frost  
 
 Whose woods these are I think I know  
His house is in the village though  
He will not see me stopping here  
To watch his woods fill up with snow  
 
My little horse must think it queer  
To stop without a farmhouse near  
Between the woods and frozen lake  
The darkest evening of the year  
 
He gives his harness bells a shake  
To ask if there is some mistake  
The only other sounds the sweep  
Of easy wind and downy flake  
 
The woods are lovely dark and deep  
But I have promises to keep  
And miles to go before I sleep  
And miles to go before I sleep  
  Admiring Light on a Sunny Day Erika Fitzpatrick  
 
What light this is I may it know  
Its beams barred by finite time though  
He should not mind me pausing now  
To admire this light ere it go  
 
My wearied mind considers how  
There is time enough to allow  
Dead and dilated eyes to gaze  
On light thats not for me endowed  
 
It filters through in timid haze  
For this room its not seen in days  
Dust dances where lighted  day glows  
In mute music and golden rays  
 
Sunlight is happy hope arose  
But I have ssignments to close  
And pages to rove before I doze  
And pages to rove before I doze  
```
### Long Short Term Memory Network (LSTM)
- Long Short-Term Memory (LSTM) networks are a modified version of recurrent neural networks, which makes it easier to remember past data in memory.
- Generally LSTM is composed of a cell (the memory part of the LSTM unit) and three "regulators", usually called gates, of the flow of information inside the LSTM unit: an input gate, an output gate and a forget gate.
- Intuitively, the cell is responsible for keeping track of the dependencies between the elements in the input sequence.
- The input gate controls the extent to which a new value flows into the cell, the forget gate controls the extent to which a value remains in the cell and the output gate controls the extent to which the value in the cell is used to compute the output activation of the LSTM unit.
- The activation function of the LSTM gates is often the logistic sigmoid function.
- There are connections into and out of the LSTM gates, a few of which are recurrent. The weights of these connections, which need to be learned during training, determine how the gates operate.

### Architecture of LSTM
![lstm_working](https://github.com/Mohitraj27/Text-Generation-Using-LSTM/assets/87956374/39a10d23-32df-4162-985a-9403b3a5c0b6)

## Pre- Processing of Dataset
![image](https://github.com/Mohitraj27/Text-Generation-Using-LSTM/assets/87956374/b66e6156-d0e8-41d6-b5fc-7637dd284e2a)

### Removing Stopwards
![stopwords_ani](https://github.com/Mohitraj27/Text-Generation-Using-LSTM/assets/87956374/a50d53c7-7cc3-4ebd-bd77-cc0d6ee26ecb)

### Removing Lemmatization
![lemmatize_ani](https://github.com/Mohitraj27/Text-Generation-Using-LSTM/assets/87956374/614ce7c2-323d-42fe-ad80-4527435dfbdb)

#### Converting texts in form of Tokens
```
['stopping', 'by', 'woods', 'on', 'a', 'snowy', 'evening', 'robert', 'frost', 'whose', 'woods', 'these', 'are', 'i', 'think', 'i', 'know', 'his', 'house', 'is', 'in', 'the', 'village', 'though', 'he', 'will', 'not', 'see', 'me', 'stopping', 'here', 'to', 'watch', 'his', 'woods', 'fill', 'up', 'with', 'snow', 'my', 'little', 'horse', 'must', 'think', 'it', 'queer', 'to', 'stop', 'without', 'a']
```
#### Converting Tokens into text into sequences
Create a unique numerical token for each unique word in the dataset. fit_on_texts() updates internal vocabulary based on a list of texts. texts_to_sequences() transforms each text in texts to a sequence of integers.sequences containes a list of integer values created by tokenizer. Each line in sequences has 51 words. Now we will split each line such
that the first 50 words are in X and the last word is in y.

```
array([112,  36,  11,  17,   9, 136,  35, 134, 133, 132,  11, 131,  33,
         4,  34,   4,  31,  18, 126,   7,  13,   3, 122,  29,  15, 118,
         8, 116,  14, 112, 113,   1, 110,  18,  11, 106, 104, 103, 101,
        27, 100,  98,  97,  34,   6,  94,   1,  92,  90,   9])
```
 Vocab Size is 137 for my dataset
 Sequence Length is of 50


 ### LSTM Model
 A Sequential model is appropriate for a plain stack of layers where each layer has exactly one input tensor and one output tensor.

 #### Embedding Layer

 The Embedding layer is initialized with random weights and will learn an embedding for all of the words in the training dataset. It requires 3 arguments:

- input_dim: This is the size of the vocabulary in the text data which is vocab_size in this case.
- output_dim: This is the size of the vector space in which words will be embedded. It defines the size of the output vectors from this layer for each word.
- input_length: Length of input sequences which is seq_length.

#### LSTM Layer
This is the main layer of the model. It learns long-term dependencies between time steps in time series and sequence data. return_sequence when set to True returns the full sequence as the output.

#### Dense Layer
Dense layer is the regular deeply connected neural network layer. It is the most common and frequently used layer. The rectified linear activation function or relu for short is a piecewise linear function that will output the input directly if it is positive, otherwise, it will output zero.
![relu-2](https://github.com/Mohitraj27/Text-Generation-Using-LSTM/assets/87956374/7e101fc8-e614-4ba9-8103-32dbc8fa3930)

The last layer is also a dense layer with 13009 neurons because we have to predict the probabilties of 13009 words. The activation function used is softmax. Softmax converts a real vector to a vector of categorical probabilities. The elements of the output vector are in range (0, 1) and sum to 1.
![softmax](https://github.com/Mohitraj27/Text-Generation-Using-LSTM/assets/87956374/319e52ca-c49e-4496-b2f2-7eaf30dbfb0a)


## Model Summary 

```
Model: "sequential"
_________________________________________________________________
 Layer (type)                Output Shape              Param #   
=================================================================
 embedding (Embedding)       (None, 50, 50)            6850      
                                                                 
 lstm (LSTM)                 (None, 50, 100)           60400     
                                                                 
 lstm_1 (LSTM)               (None, 100)               80400     
                                                                 
 dense (Dense)               (None, 100)               10100     
                                                                 
 dense_1 (Dense)             (None, 137)               13837     
                                                                 
=================================================================
Total params: 171,587
Trainable params: 171,587
Non-trainable params: 0
_________________________________________________________________
```
## Model Training 
Model is Trained at 200 epochs at batch size of 16 and achieved a accuracy of 84.83 %.
After training the model is saved using h5 extension and is ready for prediction or Text generation.
```
model.fit(X, y, batch_size = 32, epochs = 200)
```
```
Epoch 1/200
6/6 [==============================] - 6s 99ms/step - loss: 4.9193 - accuracy: 0.0169


Epoch 2/200
6/6 [==============================] - 1s 142ms/step - loss: 4.9043 - accuracy: 0.0449


Epoch 3/200
6/6 [==============================] - 1s 252ms/step - loss: 4.8186 - accuracy: 0.0393


Epoch 4/200
6/6 [==============================] - 2s 304ms/step - loss: 4.7181 - accuracy: 0.0449


Epoch 5/200
6/6 [==============================] - 2s 291ms/step - loss: 4.6537 - accuracy: 0.0562


Epoch 6/200
6/6 [==============================] - 2s 249ms/step - loss: 4.6114 - accuracy: 0.0562


Epoch 7/200
6/6 [==============================] - 1s 219ms/step - loss: 4.5836 - accuracy: 0.0393


Epoch 8/200
6/6 [==============================] - 1s 172ms/step - loss: 4.5602 - accuracy: 0.0225


Epoch 9/200
6/6 [==============================] - 1s 215ms/step - loss: 4.5394 - accuracy: 0.0562


Epoch 10/200
6/6 [==============================] - 1s 187ms/step - loss: 4.5183 - accuracy: 0.0562


Epoch 11/200
6/6 [==============================] - 1s 151ms/step - loss: 4.4917 - accuracy: 0.0562


Epoch 12/200
6/6 [==============================] - 1s 94ms/step - loss: 4.4669 - accuracy: 0.0449


Epoch 13/200
6/6 [==============================] - 1s 96ms/step - loss: 4.4229 - accuracy: 0.0506


Epoch 14/200
6/6 [==============================] - 1s 94ms/step - loss: 4.3878 - accuracy: 0.0506


Epoch 15/200
6/6 [==============================] - 1s 96ms/step - loss: 4.3356 - accuracy: 0.0506


Epoch 16/200
6/6 [==============================] - 1s 133ms/step - loss: 4.2711 - accuracy: 0.0562


Epoch 17/200
6/6 [==============================] - 1s 95ms/step - loss: 4.2217 - accuracy: 0.0562


Epoch 18/200
6/6 [==============================] - 1s 94ms/step - loss: 4.1446 - accuracy: 0.0562


Epoch 19/200
6/6 [==============================] - 1s 111ms/step - loss: 4.0780 - accuracy: 0.0899


Epoch 20/200
6/6 [==============================] - 1s 153ms/step - loss: 3.9843 - accuracy: 0.0955


Epoch 21/200
6/6 [==============================] - 1s 157ms/step - loss: 3.9270 - accuracy: 0.0843


Epoch 22/200
6/6 [==============================] - 1s 163ms/step - loss: 3.8681 - accuracy: 0.0955


Epoch 23/200
6/6 [==============================] - 1s 149ms/step - loss: 3.7527 - accuracy: 0.0843


Epoch 24/200
6/6 [==============================] - 1s 159ms/step - loss: 3.6529 - accuracy: 0.1124


Epoch 25/200
6/6 [==============================] - 1s 158ms/step - loss: 3.5730 - accuracy: 0.0843


Epoch 26/200
6/6 [==============================] - 1s 154ms/step - loss: 3.4857 - accuracy: 0.1124


Epoch 27/200
6/6 [==============================] - 1s 94ms/step - loss: 3.3912 - accuracy: 0.1180


Epoch 28/200
6/6 [==============================] - 1s 96ms/step - loss: 3.2802 - accuracy: 0.1124


Epoch 29/200
6/6 [==============================] - 1s 93ms/step - loss: 3.2172 - accuracy: 0.1067


Epoch 30/200
6/6 [==============================] - 1s 98ms/step - loss: 3.1472 - accuracy: 0.1124


Epoch 31/200
6/6 [==============================] - 1s 95ms/step - loss: 3.0373 - accuracy: 0.1124


Epoch 32/200
6/6 [==============================] - 1s 97ms/step - loss: 3.0024 - accuracy: 0.1236


Epoch 33/200
6/6 [==============================] - 1s 95ms/step - loss: 2.9254 - accuracy: 0.1236


Epoch 34/200
6/6 [==============================] - 1s 93ms/step - loss: 2.8419 - accuracy: 0.1461


Epoch 35/200
6/6 [==============================] - 1s 98ms/step - loss: 2.8271 - accuracy: 0.1236


Epoch 36/200
6/6 [==============================] - 1s 94ms/step - loss: 2.7117 - accuracy: 0.1461


Epoch 37/200
6/6 [==============================] - 1s 97ms/step - loss: 2.6796 - accuracy: 0.1461


Epoch 38/200
6/6 [==============================] - 1s 95ms/step - loss: 2.6112 - accuracy: 0.1685


Epoch 39/200
6/6 [==============================] - 1s 96ms/step - loss: 2.5577 - accuracy: 0.1742


Epoch 40/200
6/6 [==============================] - 1s 95ms/step - loss: 2.4924 - accuracy: 0.2022


Epoch 41/200
6/6 [==============================] - 1s 93ms/step - loss: 2.4705 - accuracy: 0.1966


Epoch 42/200
6/6 [==============================] - 1s 101ms/step - loss: 2.4125 - accuracy: 0.1854


Epoch 43/200
6/6 [==============================] - 1s 93ms/step - loss: 2.3626 - accuracy: 0.1910


Epoch 44/200
6/6 [==============================] - 1s 156ms/step - loss: 2.3505 - accuracy: 0.2191


Epoch 45/200
6/6 [==============================] - 1s 149ms/step - loss: 2.3166 - accuracy: 0.2247


Epoch 46/200
6/6 [==============================] - 1s 154ms/step - loss: 2.2827 - accuracy: 0.2079


Epoch 47/200
6/6 [==============================] - 1s 156ms/step - loss: 2.2730 - accuracy: 0.1966



Epoch 48/200
6/6 [==============================] - 1s 157ms/step - loss: 2.2693 - accuracy: 0.2022


Epoch 49/200
6/6 [==============================] - 1s 162ms/step - loss: 2.1978 - accuracy: 0.2247


Epoch 50/200
6/6 [==============================] - 1s 158ms/step - loss: 2.1997 - accuracy: 0.2191


Epoch 51/200
6/6 [==============================] - 1s 111ms/step - loss: 2.1650 - accuracy: 0.2360


Epoch 52/200
6/6 [==============================] - 1s 94ms/step - loss: 2.1340 - accuracy: 0.2191


Epoch 53/200
6/6 [==============================] - 1s 92ms/step - loss: 2.0931 - accuracy: 0.2753


Epoch 54/200
6/6 [==============================] - 1s 95ms/step - loss: 2.0811 - accuracy: 0.2472


Epoch 55/200
6/6 [==============================] - 1s 95ms/step - loss: 2.0293 - accuracy: 0.3090


Epoch 56/200
6/6 [==============================] - 1s 101ms/step - loss: 2.0077 - accuracy: 0.2809


Epoch 57/200
6/6 [==============================] - 1s 94ms/step - loss: 2.0220 - accuracy: 0.2809


Epoch 58/200
6/6 [==============================] - 1s 95ms/step - loss: 1.9995 - accuracy: 0.2865


Epoch 59/200
6/6 [==============================] - 1s 99ms/step - loss: 1.9635 - accuracy: 0.2753


Epoch 60/200
6/6 [==============================] - 1s 96ms/step - loss: 1.9456 - accuracy: 0.2865


Epoch 61/200
6/6 [==============================] - 1s 97ms/step - loss: 1.9000 - accuracy: 0.3090


Epoch 62/200
6/6 [==============================] - 1s 93ms/step - loss: 1.8796 - accuracy: 0.3371


Epoch 63/200
6/6 [==============================] - 1s 98ms/step - loss: 1.8552 - accuracy: 0.3315


Epoch 64/200
6/6 [==============================] - 1s 95ms/step - loss: 1.9291 - accuracy: 0.2865


Epoch 65/200
6/6 [==============================] - 1s 96ms/step - loss: 1.9085 - accuracy: 0.2978


Epoch 66/200
6/6 [==============================] - 1s 98ms/step - loss: 1.8884 - accuracy: 0.3427


Epoch 67/200
6/6 [==============================] - 1s 93ms/step - loss: 1.8393 - accuracy: 0.3371


Epoch 68/200
6/6 [==============================] - 1s 127ms/step - loss: 1.7714 - accuracy: 0.3652


Epoch 69/200
6/6 [==============================] - 1s 152ms/step - loss: 1.7653 - accuracy: 0.3483


Epoch 70/200
6/6 [==============================] - 1s 157ms/step - loss: 1.7249 - accuracy: 0.4326


Epoch 71/200
6/6 [==============================] - 1s 155ms/step - loss: 1.7065 - accuracy: 0.4382


Epoch 72/200
6/6 [==============================] - 1s 158ms/step - loss: 1.7066 - accuracy: 0.3539


Epoch 73/200
6/6 [==============================] - 1s 158ms/step - loss: 1.7310 - accuracy: 0.3820


Epoch 74/200
6/6 [==============================] - 1s 158ms/step - loss: 1.6968 - accuracy: 0.3876


Epoch 75/200
6/6 [==============================] - 1s 140ms/step - loss: 1.6755 - accuracy: 0.4101


Epoch 76/200
6/6 [==============================] - 1s 97ms/step - loss: 1.6827 - accuracy: 0.3708


Epoch 77/200
6/6 [==============================] - 1s 94ms/step - loss: 1.7745 - accuracy: 0.3876


Epoch 78/200
6/6 [==============================] - 1s 97ms/step - loss: 1.7132 - accuracy: 0.3315


Epoch 79/200
6/6 [==============================] - 1s 95ms/step - loss: 1.6812 - accuracy: 0.3315


Epoch 80/200
6/6 [==============================] - 1s 96ms/step - loss: 1.6493 - accuracy: 0.3596


Epoch 81/200
6/6 [==============================] - 1s 95ms/step - loss: 1.6640 - accuracy: 0.3202


Epoch 82/200
6/6 [==============================] - 1s 93ms/step - loss: 1.6891 - accuracy: 0.3483


Epoch 83/200
6/6 [==============================] - 1s 97ms/step - loss: 1.6691 - accuracy: 0.3371


Epoch 84/200
6/6 [==============================] - 1s 94ms/step - loss: 1.6379 - accuracy: 0.3539


Epoch 85/200
6/6 [==============================] - 1s 95ms/step - loss: 1.6103 - accuracy: 0.3539


Epoch 86/200
6/6 [==============================] - 1s 93ms/step - loss: 1.5813 - accuracy: 0.4045


Epoch 87/200
6/6 [==============================] - 1s 99ms/step - loss: 1.5381 - accuracy: 0.3876


Epoch 88/200
6/6 [==============================] - 1s 99ms/step - loss: 1.5375 - accuracy: 0.4270


Epoch 89/200
6/6 [==============================] - 1s 94ms/step - loss: 1.5216 - accuracy: 0.4326


Epoch 90/200
6/6 [==============================] - 1s 96ms/step - loss: 1.4935 - accuracy: 0.4213


Epoch 91/200
6/6 [==============================] - 1s 95ms/step - loss: 1.4759 - accuracy: 0.5112


Epoch 92/200
6/6 [==============================] - 1s 98ms/step - loss: 1.4702 - accuracy: 0.4944


Epoch 93/200
6/6 [==============================] - 1s 157ms/step - loss: 1.4774 - accuracy: 0.4494


Epoch 94/200
6/6 [==============================] - 1s 154ms/step - loss: 1.4802 - accuracy: 0.3876


Epoch 95/200
6/6 [==============================] - 1s 158ms/step - loss: 1.5109 - accuracy: 0.4270


Epoch 96/200
6/6 [==============================] - 1s 155ms/step - loss: 1.4601 - accuracy: 0.4663


Epoch 97/200
6/6 [==============================] - 1s 158ms/step - loss: 1.4627 - accuracy: 0.4494


Epoch 98/200
6/6 [==============================] - 1s 167ms/step - loss: 1.4394 - accuracy: 0.4270


Epoch 99/200
6/6 [==============================] - 1s 159ms/step - loss: 1.5398 - accuracy: 0.3539


Epoch 100/200
6/6 [==============================] - 1s 99ms/step - loss: 1.4874 - accuracy: 0.3933


Epoch 101/200
6/6 [==============================] - 1s 96ms/step - loss: 1.5003 - accuracy: 0.4326


Epoch 102/200
6/6 [==============================] - 1s 99ms/step - loss: 1.4462 - accuracy: 0.4157


Epoch 103/200
6/6 [==============================] - 1s 95ms/step - loss: 1.3994 - accuracy: 0.5056


Epoch 104/200
6/6 [==============================] - 1s 95ms/step - loss: 1.4188 - accuracy: 0.4719


Epoch 105/200
6/6 [==============================] - 1s 99ms/step - loss: 1.4012 - accuracy: 0.4382


Epoch 106/200
6/6 [==============================] - 1s 94ms/step - loss: 1.4000 - accuracy: 0.4944


Epoch 107/200
6/6 [==============================] - 1s 99ms/step - loss: 1.3691 - accuracy: 0.5112


Epoch 108/200
6/6 [==============================] - 1s 96ms/step - loss: 1.3330 - accuracy: 0.5506


Epoch 109/200
6/6 [==============================] - 1s 100ms/step - loss: 1.3167 - accuracy: 0.5562


Epoch 110/200
6/6 [==============================] - 1s 95ms/step - loss: 1.2954 - accuracy: 0.5674


Epoch 111/200
6/6 [==============================] - 1s 94ms/step - loss: 1.2871 - accuracy: 0.5112


Epoch 112/200
6/6 [==============================] - 1s 98ms/step - loss: 1.3029 - accuracy: 0.5337


Epoch 113/200
6/6 [==============================] - 1s 97ms/step - loss: 1.3247 - accuracy: 0.5225


Epoch 114/200
6/6 [==============================] - 1s 99ms/step - loss: 1.3276 - accuracy: 0.5056


Epoch 115/200
6/6 [==============================] - 1s 95ms/step - loss: 1.3469 - accuracy: 0.4494


Epoch 116/200
6/6 [==============================] - 1s 103ms/step - loss: 1.3426 - accuracy: 0.4719


Epoch 117/200
6/6 [==============================] - 1s 153ms/step - loss: 1.3164 - accuracy: 0.5112


Epoch 118/200
6/6 [==============================] - 1s 153ms/step - loss: 1.3283 - accuracy: 0.4607


Epoch 119/200
6/6 [==============================] - 1s 154ms/step - loss: 1.2929 - accuracy: 0.5337


Epoch 120/200
6/6 [==============================] - 1s 155ms/step - loss: 1.2865 - accuracy: 0.5112


Epoch 121/200
6/6 [==============================] - 1s 158ms/step - loss: 1.3387 - accuracy: 0.4438


Epoch 122/200
6/6 [==============================] - 1s 159ms/step - loss: 1.3154 - accuracy: 0.5169


Epoch 123/200
6/6 [==============================] - 1s 164ms/step - loss: 1.2630 - accuracy: 0.5225


Epoch 124/200
6/6 [==============================] - 1s 100ms/step - loss: 1.2408 - accuracy: 0.5843


Epoch 125/200
6/6 [==============================] - 1s 95ms/step - loss: 1.2203 - accuracy: 0.5787


Epoch 126/200
6/6 [==============================] - 1s 95ms/step - loss: 1.2080 - accuracy: 0.6124


Epoch 127/200
6/6 [==============================] - 1s 97ms/step - loss: 1.1882 - accuracy: 0.6067


Epoch 128/200
6/6 [==============================] - 1s 96ms/step - loss: 1.1752 - accuracy: 0.5730


Epoch 129/200
6/6 [==============================] - 1s 101ms/step - loss: 1.1441 - accuracy: 0.6517


Epoch 130/200
6/6 [==============================] - 1s 94ms/step - loss: 1.1083 - accuracy: 0.6685


Epoch 131/200
6/6 [==============================] - 1s 103ms/step - loss: 1.1449 - accuracy: 0.5899


Epoch 132/200
6/6 [==============================] - 1s 103ms/step - loss: 1.1228 - accuracy: 0.6180


Epoch 133/200
6/6 [==============================] - 1s 96ms/step - loss: 1.1138 - accuracy: 0.6517


Epoch 134/200
6/6 [==============================] - 1s 96ms/step - loss: 1.0955 - accuracy: 0.6292


Epoch 135/200
6/6 [==============================] - 1s 95ms/step - loss: 1.0808 - accuracy: 0.6798


Epoch 136/200
6/6 [==============================] - 1s 98ms/step - loss: 1.0624 - accuracy: 0.6910


Epoch 137/200
6/6 [==============================] - 1s 95ms/step - loss: 1.0769 - accuracy: 0.6742


Epoch 138/200
6/6 [==============================] - 1s 99ms/step - loss: 1.0980 - accuracy: 0.6517


Epoch 139/200
6/6 [==============================] - 1s 98ms/step - loss: 1.0786 - accuracy: 0.6292


Epoch 140/200
6/6 [==============================] - 1s 95ms/step - loss: 1.1146 - accuracy: 0.5730


Epoch 141/200
6/6 [==============================] - 1s 150ms/step - loss: 1.1083 - accuracy: 0.6404


Epoch 142/200
6/6 [==============================] - 1s 150ms/step - loss: 1.1186 - accuracy: 0.6011


Epoch 143/200
6/6 [==============================] - 1s 153ms/step - loss: 1.1886 - accuracy: 0.5393


Epoch 144/200
6/6 [==============================] - 1s 152ms/step - loss: 1.1498 - accuracy: 0.5618


Epoch 145/200
6/6 [==============================] - 1s 163ms/step - loss: 1.1328 - accuracy: 0.5730


Epoch 146/200
6/6 [==============================] - 1s 162ms/step - loss: 1.0761 - accuracy: 0.6292


Epoch 147/200
6/6 [==============================] - 1s 157ms/step - loss: 1.0399 - accuracy: 0.6685


Epoch 148/200
6/6 [==============================] - 1s 123ms/step - loss: 1.0482 - accuracy: 0.6404


Epoch 149/200
6/6 [==============================] - 1s 98ms/step - loss: 1.0935 - accuracy: 0.5899


Epoch 150/200
6/6 [==============================] - 1s 96ms/step - loss: 1.0836 - accuracy: 0.5787


Epoch 151/200
6/6 [==============================] - 1s 97ms/step - loss: 1.0584 - accuracy: 0.6573


Epoch 152/200
6/6 [==============================] - 1s 93ms/step - loss: 1.0787 - accuracy: 0.6067


Epoch 153/200
6/6 [==============================] - 1s 97ms/step - loss: 1.0784 - accuracy: 0.6067


Epoch 154/200
6/6 [==============================] - 1s 96ms/step - loss: 1.1129 - accuracy: 0.5393


Epoch 155/200
6/6 [==============================] - 1s 97ms/step - loss: 1.0884 - accuracy: 0.6124


Epoch 156/200
6/6 [==============================] - 1s 98ms/step - loss: 1.0724 - accuracy: 0.5955


Epoch 157/200
6/6 [==============================] - 1s 96ms/step - loss: 1.0388 - accuracy: 0.6404


Epoch 158/200
6/6 [==============================] - 1s 102ms/step - loss: 0.9992 - accuracy: 0.7135


Epoch 159/200
6/6 [==============================] - 1s 95ms/step - loss: 0.9498 - accuracy: 0.7528


Epoch 160/200
6/6 [==============================] - 1s 97ms/step - loss: 0.9396 - accuracy: 0.7584


Epoch 161/200
6/6 [==============================] - 1s 94ms/step - loss: 0.9428 - accuracy: 0.7135


Epoch 162/200
6/6 [==============================] - 1s 97ms/step - loss: 0.9430 - accuracy: 0.6348


Epoch 163/200
6/6 [==============================] - 1s 97ms/step - loss: 0.8967 - accuracy: 0.7697


Epoch 164/200
6/6 [==============================] - 1s 130ms/step - loss: 0.8656 - accuracy: 0.8090


Epoch 165/200
6/6 [==============================] - 1s 247ms/step - loss: 0.8884 - accuracy: 0.7809


Epoch 166/200
6/6 [==============================] - 1s 155ms/step - loss: 1.6586 - accuracy: 0.4607


Epoch 167/200
6/6 [==============================] - 1s 153ms/step - loss: 1.5373 - accuracy: 0.4270


Epoch 168/200
6/6 [==============================] - 1s 154ms/step - loss: 1.3898 - accuracy: 0.4438


Epoch 169/200
6/6 [==============================] - 1s 159ms/step - loss: 1.3184 - accuracy: 0.4551


Epoch 170/200
6/6 [==============================] - 1s 162ms/step - loss: 1.2078 - accuracy: 0.5169


Epoch 171/200
6/6 [==============================] - 1s 161ms/step - loss: 1.1528 - accuracy: 0.5787


Epoch 172/200
6/6 [==============================] - 1s 98ms/step - loss: 1.1330 - accuracy: 0.5112


Epoch 173/200
6/6 [==============================] - 1s 96ms/step - loss: 1.0633 - accuracy: 0.6180


Epoch 174/200
6/6 [==============================] - 1s 97ms/step - loss: 1.0203 - accuracy: 0.6404


Epoch 175/200
6/6 [==============================] - 1s 94ms/step - loss: 1.0061 - accuracy: 0.6742


Epoch 176/200
6/6 [==============================] - 1s 99ms/step - loss: 0.9665 - accuracy: 0.7360


Epoch 177/200
6/6 [==============================] - 1s 98ms/step - loss: 1.0031 - accuracy: 0.6966


Epoch 178/200
6/6 [==============================] - 1s 94ms/step - loss: 0.9758 - accuracy: 0.6910




Epoch 179/200
6/6 [==============================] - 1s 98ms/step - loss: 0.9628 - accuracy: 0.7135


Epoch 180/200
6/6 [==============================] - 1s 95ms/step - loss: 1.0082 - accuracy: 0.6629


Epoch 181/200
6/6 [==============================] - 1s 97ms/step - loss: 0.9403 - accuracy: 0.6854


Epoch 182/200
6/6 [==============================] - 1s 99ms/step - loss: 0.9263 - accuracy: 0.6966


Epoch 183/200
6/6 [==============================] - 1s 93ms/step - loss: 0.8792 - accuracy: 0.7472


Epoch 184/200
6/6 [==============================] - 1s 98ms/step - loss: 0.8727 - accuracy: 0.7472



Epoch 185/200
6/6 [==============================] - 1s 93ms/step - loss: 0.8397 - accuracy: 0.7809


Epoch 186/200
6/6 [==============================] - 1s 99ms/step - loss: 0.8179 - accuracy: 0.7753


Epoch 187/200
6/6 [==============================] - 1s 97ms/step - loss: 0.8242 - accuracy: 0.7865


Epoch 188/200
6/6 [==============================] - 1s 100ms/step - loss: 0.8288 - accuracy: 0.7640


Epoch 189/200
6/6 [==============================] - 1s 156ms/step - loss: 0.7935 - accuracy: 0.8146


Epoch 190/200
6/6 [==============================] - 1s 152ms/step - loss: 0.8026 - accuracy: 0.7247


Epoch 191/200
6/6 [==============================] - 1s 157ms/step - loss: 0.7873 - accuracy: 0.7753


Epoch 192/200
6/6 [==============================] - 1s 152ms/step - loss: 0.7984 - accuracy: 0.7640


Epoch 193/200
6/6 [==============================] - 1s 161ms/step - loss: 0.7664 - accuracy: 0.7921


Epoch 194/200
6/6 [==============================] - 1s 155ms/step - loss: 0.7572 - accuracy: 0.7809


Epoch 195/200
6/6 [==============================] - 1s 160ms/step - loss: 0.7338 - accuracy: 0.8371


Epoch 196/200
6/6 [==============================] - 1s 126ms/step - loss: 0.7560 - accuracy: 0.8090


Epoch 197/200
6/6 [==============================] - 1s 95ms/step - loss: 0.7382 - accuracy: 0.7753


Epoch 198/200
6/6 [==============================] - 1s 96ms/step - loss: 0.7119 - accuracy: 0.8371


Epoch 199/200
6/6 [==============================] - 1s 94ms/step - loss: 0.7229 - accuracy: 0.8371


Epoch 200/200
6/6 [==============================] - 1s 95ms/step - loss: 0.6854 - accuracy: 0.8483
<keras.callbacks.History at 0x7a8418452f50>
```

#### Seed Text of 50 words to predict next 50 words using LSTM technique
```
woods these are i think i know his house is in the village though he will not see me stopping here to watch his woods fill up with snow my little horse must think it queer to stop without a farmhouse near between the woods and frozen lake the darkest evening
```

## Text Generation of Next 50 words
```
Generated Text:
of the year he gives his harness bells a shake to ask there is some some mistake only other other sounds the sweep of easy wind and downy flake the woods are lovely dark and deep but i have promises to keep and miles to go before i go go go i i i i sleep admiring light on a sunny day erika fitzpatrick what light this is i may it know its beams barred by finite time though he should not mind me pausing now to admire this light it it go my mind considers considers how there is

```
