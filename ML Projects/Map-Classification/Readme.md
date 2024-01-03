## The Author 
- Linkedin: https://www.linkedin.com/in/vibudh/
- Github: https://github.com/iVibudh
- Medium: https://medium.com/@ivibudh

## Task 
In this project, we want to develop a Machine Learning Algorithm to differentiate the pages which are maps (aka alignment sheets) from pages which are not maps.

*Note*: For this project, we will not be using computer vision. Instead we intend to use basic feacture extraction from a pdf page to extract the relevant features.

#### Sample Maps:
<img src="https://github.com/iVibudh/CER-classify-maps/blob/main/images/map_1.PNG" alt="map_1.png" width="150" height = "200" />   <img src="https://github.com/iVibudh/CER-classify-maps/blob/main/images/map_2.PNG" alt="map_2.png" width="200" height = "150" />   <img src="https://github.com/iVibudh/CER-classify-maps/blob/main/images/map_3.PNG" alt="map_3.png" width="200" height = "150" />

#### Sample Non-Maps:
<img src="https://github.com/iVibudh/CER-classify-maps/blob/main/images/page_1.PNG" alt="page_1.png" width="150" height = "200" />   <img src="https://github.com/iVibudh/CER-classify-maps/blob/main/images/page_2.PNG" alt="page_2.png" width="150" height = "200" />   <img src="https://github.com/iVibudh/CER-classify-maps/blob/main/images/page_3.PNG" alt="page_3.png" width="150" height = "200" />


## Approach 

For the problem stated above we will be using classification algorithms and we will be using features such as area of images in a page, number of images in a page, count of words, we will also be checking if the page has certain words such as the word "North" or "N", "Figure", "Map", "Alignment Sheet" or "Sheet", "Legend", "scale", and "kilometers" or "km".  

Once we have the features extracted we will be training Classification models such as, XG Boost Classifier, Support Vector Classifier, Decision Treen Classifier,  Random Forest Classifier, Random Forest Regressor and XG Boost Regressor. We will be comparing the accuracy and performance of the confusion matrix for these models on Test Set and Training Set. Then we will save the best performing model for future use.

Note: The results from the regressor models are converted into binary output, hence, we will be referring these regression models classification models. 

## Code Files
- **code/feature_extraction.py**: This file contains the funtions which are used to extract the features in a PDF page. These features will be used to do classification.
- **code/training.ipynb**: This notebook is used to train multiple classification algorithm and then compares the results on the test data. Further the best model is chosen for inference.
In this file first we read the PDF files in the Training Set fonder. We treat each page as a unique entity and then we use functions from feature_extraction.py to extract feaures for all the pages. Then all these pages with their features are split in to Training set and Test Set. Then we train the classification models and evaluate the model performances. Further we exctract the features for the PDF in the Validation Set folder in the same way. Then we evaluate the models and pick the best model.
- **code/inference.ipynb**: This file is used to run inference for new documents.

