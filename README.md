(bash specific instructions)

How to run the 1st assignment:
1) Create a new venv with "python3 -m venv /path/to/new/virtual/environment"
2) Activate it with "source <venv>/bin/activate"
3) Install the required packages with "pip install -r requirements.txt"
4) Create a .env file and enter your newsapi key like this "NEWSAPIKEY = <api key goes here>"
5) Run "sudo docker compose up -d" and give it some seconds before doing anything else
6) Open up a browser and search for "http://localhost:8081" and "http://localhost:9000" for an overview of the mongodb database and kafka cluster respectively
7) Execute the mainfile.py file with "python3 mainfile.py" **while inside the "assignment1" folder** which activates the kafka producer and consumer
8) Execute the app.py file with "python3 app.py" which activates the flask application

How to run the 2nd assignment:
1) Same instructions as 1st assignment up until the 5th step
2) Execute "graph.py" to create a graph that identifies each article's next best recommendation
3) Execute "stackedbar.py" to plot a stacked bar graph of the number of articles per topic over the last five days

How to run the 3rd assignment:
1) Same instructions as 1st assignment up until the 5th step
2) **While inside the "assignment3" folder**, execute "titlesToCsv.py" to generate a csv dataset with all of the articles' titles inside the database. There is already an existing dataset so there is no need to run this command. 
3) **While inside the "assignment3" folder**, execute "lda.py" to train the Latent Dirichlet allocation model on the dataset
4) **While inside the "assignment3" folder**, execute "ldavisualize.py" to get a visualization of the topic model in .html form. Copy the path of the newly created html file and paste it in a browser to get an interactive overview of the topic model.
5) **While inside the "assignment3" folder**, execute "nerSentiment.py" to perform named entity recognition on the article titles dataset and sentiment analysis on the retrieved entities and then plot a a horizontal bar chart that displays the sentiment scores of the top entities
