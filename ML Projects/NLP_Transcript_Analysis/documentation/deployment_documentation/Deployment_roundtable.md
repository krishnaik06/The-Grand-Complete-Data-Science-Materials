

## Deployment Documentation

### GitHub
   * #### Clone Repository

      `sudo apt update`

      `sudo apt install git`

      `sudo apt install git-lfs`  _To clone large files_

      `git clone <repo link>`

      ![](Aspose.Words.91c4ee3f-692b-4196-9295-542bcb88b350.001.png)

   * #### SSH Key Generation
      Add ssh access in a new server to clone private repo


      `ssh-keygen -t ed25519 -C "example@gmail.com"`

      `eval "$(ssh-agent -s)"`

      `ssh-add ~/.ssh/id\_ed25519`

      `cat ~/.ssh/id\_ed25519.pub`

      Copy this public key and paste it in **SSH and GPG keys**  section in your Github profile

      ![](Aspose.Words.91c4ee3f-692b-4196-9295-542bcb88b350.002.png)

### Install Dependencies

   * #### Normal Instance
      `sudo apt update`

      `sudo apt install python3-pip`

      `sudo apt install uvicorn`

      `pip3  install -r requirements.txt`

   * #### GPU Instance
      Additional packages for NVIDIA GPU instances

      * NVIDIA driver

         `sudo apt install nvidia-driver-525 nvidia-dkms-525`

         `sudo apt install nvidia-kernel-common-525`

      * NVIDIA Toolkit 

         `curl https://get.docker.com | sh \
      && sudo systemctl --now enable docker`

         `sudo apt-get install -y nvidia-container-toolkit`

         `sudo nvidia-ctk runtime configure --runtime=docker`

         `sudo systemctl restart docker`

### Execution
* #### Download files from huggingface
  * #### Summary Module

     Go to roundtable\_dockerize -> api_modules -> summary -> prediction -> files

     Then open terminal and clone the repo from huggingface - including the large files

      `git clone https://huggingface.co/facebook/bart-large-cnn`
        
  * #### Topic, Keyword-Hashtag Module

     Go to roundtable\_dockerize -> api_modules -> topic/keyword_hashtag -> prediction -> files

     Then open terminal and clone the repo from huggingface -  including the large files

     `git clone https://huggingface.co/sentence-transformers/all-mpnet-base-v2`

  * #### Topic_zeroshot Module

       Go to roundtable\_dockerize -> api_modules -> topic_zeroshot -> prediction -> files

       Then open terminal and clone the repo from huggingface -  including the large files

       `git clone https://huggingface.co/facebook/bart-large-mnli`

* #### Download from Google Drive (Preferred Method)
   * #### Sumamry Module

      Go to roundtable\_dockerize -> api_modules -> summary -> prediction -> files

      Download the files and paste in the folder

      [GOOGLE DRIVE LINK](https://drive.google.com/drive/folders/1MjOHVo-QH8ngSPML7z8vEpjNP5_mV8xN?usp=sharing)
           
   * #### Topic, Keyword-Hashtag Module

      Go to roundtable\_dockerize -> api_modules -> topic/keyword_hashtag -> prediction -> files

      Download the files and paste in the folder

      [GOOGLE DRIVE LINK](https://drive.google.com/drive/folders/11_gJBIOJoI-Sf-LNi2JLRTMiDDLnixCx?usp=sharing)

   * #### Topic_zeroshot Module

      Go to roundtable\_dockerize -> api_modules -> topic_zeroshot -> prediction -> files

      Download the files and paste in the folder

      [GOOGLE DRIVE LINK](https://drive.google.com/drive/folders/19maVgmkCr5_jgaQ1FTS8bNehMg05L5FQ?usp=share_link)

    **NOTE - You can download these and put it in your Network storage and then attach it as a volume in your docker. These will be required during run time.
     We strongly recommend to keep a copy of it with you.**
* #### Configuration file

   Each module has its own **config\_xxx.ini** file to store parameter values. Changing the values will reflect in module execution.
   
* #### Server startup

   Run **xxxxx\_fastapi**.py to start the prediction module and use [http://127.0.0.1:8001/](http://127.0.0.1:8000/)<endpoint>  to access the endpoint

   `uvicorn <prediction filename_without_py_extension>:app --port 8001 --host 0.0.0.0 --reload`

   **Note : port should be the same as mentioned or else the client script will fail to communicate**

* #### Client Script

   You can also access the endpoints using the client script. Run **client\_xxx** prefix file to automate the endpoint access. You can do prediction by feeding the .txt file to the client script.

   `python3 client_topic.py`

   * #### Summary Module

      Place text file named **sample\_transcript.txt** under **roundtable\_dockerize/sample_data** folder - file should have the transcript data.

   * #### Keyword_Hashtag Module

      Place text file named **sample\_transcript.txt** in **roundtable\_dockerize/sample_data** folder - file should have the transcript data.

      Place text file named **sample\_summary.txt** in **roundtable\_dockerize/sample_data** folder - file should have the summary data.

   * #### Topic Module

      Place text file named **sample\_transcript.txt** in **roundtable\_dockerize/sample_data** folder - file should have the transcript data.
   * #### Topic_zeroshot Module
    
        Place text file named **sample\_transcript.txt** in **roundtable\_dockerize/sample_data** folder - file should have the transcript data. Labels input is optional - if given, model will predict based on new labels or else it will use the predefined labels.
       
            egs: Input without custom labels
            {'title' : 'test title', 'model': 'bart-large-mnli','summary': summary_data}
        
            egs: Input with custom labels
            {'title' : 'test title', 'model': 'bart-large-mnli','summary': summary_data, 'labels' : ['sports','music']}
        
        **Note**: In the server side basic transcript cleaning is performed like removing timestamp, backslash and newline character.
        If the transcript contains noisy text other than this, prediction quality will be degraded.
        

### Docker
   * #### Installation

      Dockerizing the application can help to run it in different environments irrespective of operating system, versions of packages installed. Install the docker using the following commands in linux operating system

      `sudo apt update -qq`

      `sudo apt install apt-transport-https ca-certificates curl software-properties-common -qq`

      `curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -`

      `sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"`

      `sudo apt update -qq`

      `sudo apt install docker-ce`

   * #### Dockerfile

      File specifies how the image has to be created and run on execution.

      **FROM** - base image to run our module

      **COPY** - working  directory source path in local system

      **RUN** - run requirements.txt file to install all dependent packages

      **EXPOSE** - port for app to run

      **WORDIR** - working directory path inside docker image

      **CMD** - command to run the application after starting the container

   * #### Docker Image
      Build the docker images as specified in Dockerfile

      `sudo docker build -t <image_name>:<version_tag> <source_directory>`

      `sudo docker build -t hash:1.0 .`

   * #### Docker Container

      Run both containers in different ports.

      `sudo docker run -p <port>:<port> -d <img_name>:<version_tag>`
   * 
      `sudo docker run -p 8000:8000 -d hashtag:1.0`

      GPU enabled container

      `sudo docker run --rm -p 8001:8001 --gpus all -d summary:1.0`

### AWS Deployment

   * #### Instance
      Choose the apt configuration available in EC2 instances depending on the module requirement

      ![](Aspose.Words.91c4ee3f-692b-4196-9295-542bcb88b350.003.png)

   * #### File Transfer
      
      You can either transfer model files or clone directly from huggingface site and build the docker image. 

      To transfer files from local system to AWS instance using SCP

      `scp -i <private key.pem> <localpath_tocopy> username@ec2address:<destination_path>`

      `scp -i ./home/token.pem /home/test.txt <ubuntu@ec2-xx-xx-xx-xx.ap-south-1.compute.amazonaws.com>:~/home/files`

      ![](Aspose.Words.91c4ee3f-692b-4196-9295-542bcb88b350.004.png)

   * #### Open Additional Ports
      We need to open a custom TCP port 8000 and 8001 in security settings to allow access through that channel. After enabling, type the following command in case you face any issue in accessing the ports. 

      `sudo ufw allow 8000/tcp`

      `sudo ufw allow 8001/tcp`
      
      In security groups open port 8000 and 8001 under CUSTOM TCP 

      ![](Aspose.Words.91c4ee3f-692b-4196-9295-542bcb88b350.005.png)

      Once the port is enabled, run the docker and access the endpoints 

         http://<EC2_instance_public_ip>:8001/v1.0/<endpoints>
         http://<EC2_instance_public_ip>:8000/v1.0/<endpoints>
   
      




