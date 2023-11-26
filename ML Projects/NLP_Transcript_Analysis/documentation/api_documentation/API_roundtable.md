## API Documentation
### Keyword\_Hashtag Endpoint :  `/prediction`
#### Type : `POST`


| Input Parameter | Type | Constraints           |
|-----------------|------|-----------------------|
| Title           | str  | No                    |
| Transcript      | str  | Minimum 30 characters |
| Summary         | str  | Minimum 30 characters |
| Model           | str  | No                    |

![](Aspose.Words.e4867d9b-4a9a-4681-99bd-0bc5ba2859b3.001.png)

#### Curl

![](Aspose.Words.e4867d9b-4a9a-4681-99bd-0bc5ba2859b3.002.png)	

#### Return
Returns output (NER , Noun, Overall keywords and hashtag) in JSON format with timestamp

![img_7.png](img_7.png)

#### Error Codes

* **500 - Prediction Module Error :** Occurs when a module fails to execute successfully. Look the list of possible modules

  - PRELIMINARY INITIALIZATION ERROR
  - MODEL INITIALIZATION ERROR
  - SENTENCE TOKENIZING ERROR
  - KEYWORD EXTRACTION ERROR
  - ERROR IN SCORING KEYWORDS
  - TRANSCRIPT CLEANING ERROR
  - ERROR IN DIVIDE\_CHUNKS MODULE
  - ERROR IN CHUNK\_KEYWORDS MODULE
  - ERROR IN OVER\_ALL\_KEYWORDS MODULE
  - ERROR IN TRANSCRIPT\_KEYWORDS MODULE
  - ERROR IN FINAL\_PROCESSING MODULE
  - ERROR IN RETURNING THE OUTPUT

    ![](Aspose.Words.e4867d9b-4a9a-4681-99bd-0bc5ba2859b3.004.png)

    ![](Aspose.Words.e4867d9b-4a9a-4681-99bd-0bc5ba2859b3.005.png)

* **422 - Invalid Input Format :** When the input constraint is not followed

* **401 - Invalid model name**

    ![](Aspose.Words.e4867d9b-4a9a-4681-99bd-0bc5ba2859b3.006.png)

### Topic Endpoint :  `/prediction` 

#### Type : `POST`

| Input Parameter | Type | Constraints           |
|-----------------|------|-----------------------|
| Title           | str  | No                    |
| Summary         | str  | Minimum 30 characters |
| Model           | str  | No                    |

![](Aspose.Words.e4867d9b-4a9a-4681-99bd-0bc5ba2859b3.007.png)

#### Curl

![](Aspose.Words.e4867d9b-4a9a-4681-99bd-0bc5ba2859b3.008.png)

#### Return 

Returns output in JSON format with timestamp

![](Aspose.Words.e4867d9b-4a9a-4681-99bd-0bc5ba2859b3.009.png)

#### Error Codes

* **500 - Prediction Module Error :** Occurs when a module fails to execute successfully. Look the list of possible modules

  - PRELIMINARY INITIALIZATION 
  - MODEL INITIALIZATION
  - TOPIC EMBEDDING
  - SUMMARY EMBEDDING 
  - ERROR IN RETURNING THE OUTPUT
  - RESULT SCORING FAILED
  - COSINE SIMILARITY CALCULATION

     ![](Aspose.Words.e4867d9b-4a9a-4681-99bd-0bc5ba2859b3.010.png)
    
    ![](Aspose.Words.e4867d9b-4a9a-4681-99bd-0bc5ba2859b3.011.png)



* **422 - Invalid Input Format :** When the input constraint is not followed

* **401 - Invalid model name**

  ![](Aspose.Words.e4867d9b-4a9a-4681-99bd-0bc5ba2859b3.006.png)

### Topic_Zeroshot Endpoint :  `/prediction` 

#### Type : `POST`

| Input Parameter   | Type | Constraints           |
|-------------------|------|-----------------------|
| Title             | str  | No                    |
| Summary           | str  | Minimum 30 characters |
| Labels (Optional) | list | Min 2 - Max 20 items  |
| Model             | str  | No                    |

![img_9.png](img_9.png)

#### Curl

![img_1.png](img_1.png)

#### Return 

Returns output in JSON format with timestamp

Custom labels

![img_8.png](img_8.png)

Default labels

![img_10.png](img_10.png)

#### Error Codes

* **500 - Prediction Module Error :** Occurs when a module fails to execute successfully. Look the list of possible modules

  - PRELIMINARY INITIALIZATION 
  - MODEL INITIALIZATION
  - ERROR IN RETURNING THE OUTPUT
  - ERROR IN ZEROSHOT MODULE

    ![](Aspose.Words.e4867d9b-4a9a-4681-99bd-0bc5ba2859b3.011.png)

* **422 - Invalid Input Format :** When the input constraint is not followed

* **401 - Invalid model name**

  ![img_6.png](img_6.png)


### Summary Endpoint : `/prediction`

#### Type : `POST`

| Input Parameter | Type | Constraints           |
|-----------------|------|-----------------------|
| Title           | str  | No                    |
| Transcript      | str  | Minimum 30 characters |
| Model           | str  | No                    |


![](Aspose.Words.e4867d9b-4a9a-4681-99bd-0bc5ba2859b3.012.png)

#### Curl 	

![](Aspose.Words.e4867d9b-4a9a-4681-99bd-0bc5ba2859b3.013.png)

#### Return 

Returns output in JSON format with timestamp	

![](Aspose.Words.e4867d9b-4a9a-4681-99bd-0bc5ba2859b3.014.png)

#### Error Codes

* **500 - Prediction Module Error :** when error occurs inside the keyword module

  - ERROR IN EXTRACTING SUMMARY MODULE
  - MODEL INITIALIZATION FAILED
  - PRELIMINARY INITIALIZATION FAILED
  - ERROR IN DISPLAYING THE OUTPUT
  - TRANSCRIPT CLEANING ERROR
  - PREPROCESSING ERROR
  - DIVIDING CHUNKS ERROR

    ![](Aspose.Words.e4867d9b-4a9a-4681-99bd-0bc5ba2859b3.015.png)

    ![](Aspose.Words.e4867d9b-4a9a-4681-99bd-0bc5ba2859b3.016.png)

* **422 - Invalid Input Format :** When the input constraint is not followed

* **401 - Invalid model name**

    ![](Aspose.Words.e4867d9b-4a9a-4681-99bd-0bc5ba2859b3.017.png)


**END**
