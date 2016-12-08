# GitHub-Recommender
---
This Project was developed for Recommending Repositories for Users in the GitHub Network. 

The Code has mainly 4 modules,

1. The Core Recommendation Engine
2. WebApp Simulating the UI
3. Data Collection Scripts
4. SQL Scripts for RDBMS Creation


The Code uses the following Libraries for operation, so please go ahead and install them in your system before starting to use it.


1. fuzzywuzzy
2. itertools
3. unicodedata
4. graphlab(This is a Licensed library, you will need to create one student license for that.)
5. grammar_check
6. pyenchant
7. psycopg2
8. pandas
9. flask
10. sklearn
11. nltk
12. nltk.corpus(Not sure if this comes with the NLTK library itself.)
13. nltk.stem.snowball(Not sure if this comes with the NLTK library itself.)
14. nltk.stem.wordnet(Not sure if this comes with the NLTK library itself.)
15. requests
16. datetime
17. Dateparser
18. Flask-OAuthlib


Also the code uses the connectivity with our Private Postgres DB for the Data Extraction, so please change it in code if needed to connect to a different server. The core engine has the following classes,

1. Driver.py : This is the Main Class which will be owned by the Web App server to run all the flows.
2. TrainFlowManager.py : Manages the training phase, owned by Driver class.
3. TestFlowManager.py : Manages the Test Flow, the real time recommendations. Owned by the Driver class.
4. DatabaseConnector.py : Manages all the DB Connectivity. Separately owned by everyone.
5. CommitLogAnalyzer.py : Synthesizes the matrices for the Commit Logs, owned by Train Flow Manager.
6. BiographyAnalyzer.py : Analyses the Bio fields of Users.
7. LoggingManager.py : Manages the Logging of during the Data Synthesization part.
8. PreprocessManager.py : Class with static methods for preprocessing text data, uses many of the NLP Techniques for this.
9. ConfigurationManager.py : Config file for all custom parameters.
10. MainDriver.py : Used for testing the core flows without the server presence.
11. CustomExceptions.py: Houses many of the custom excpetions used for handling.
12. NewUserDataSynthesizer.py : One of the most importantclasses, used for the generation of vector data for the unseen test users.
13. Run.py : Entry point for the server serving the user requests.
14. index.html : The html content and the bootstrap logic for application flow, which contains the home screen, the Github OAuth and login details.
15. Repos.html : This page has html content to display the repositories of a particular user.
16. Error.html : Handles the error occurring in the application whenever the information of a particular user is not found by the model.
17. 404.html : Handles the 404, file not found exception in the application and displays the error message.


Instructions To Run:

1. Clone the repository to your machine.
2. Run the file, run.py as “python run.py”. , it will take up some time for training the models.
3. Voila! Navigate to address : http://127.0.0.1:5000/
4. If entering new id for recommendation, it will take up some time to synthesize the new user data, the process can be tracked using the terminal logs.
