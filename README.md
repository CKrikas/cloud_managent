How to run (bash specific instructions):


1) Create a new venv with "python3 -m venv /path/to/new/virtual/environment"
2) Activate it with "source <venv>/bin/activate"
3) Install the required packages with "pip install -r requirements.txt"
4) Run "sudo docker compose up -d" and give it some seconds before doing anything else
5) Open up a browser and search for "http://localhost:8081" and "http://localhost:9000" for an overview of the mongodb database and kafka cluster respectively
6) Execute the mainfile.py file with "python3 mainfile.py" which activates the kafka producer and consumer
7) Execute the app.py file with "python3 app.py" which activates the flask application
