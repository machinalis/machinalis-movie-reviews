Setup
-----

1. Create a new virtualenv
2. Install the dependencies:

    ```$ pip install -r requirements.txt```
3. Export the environment variables of the project:

    ```
    $ export FLASK_APP=movie_recommendations/__init__.py
    $ export FLASK_DEBUG=1
    ```

Generating the Database
-----------------------

1. Initialize the database: ```$ flask init_db```
2. Fill it with mock data: ```$ flask generate_user_network```
3. (optional) Fill it with a dataset info:
    1. Download the dataset from: [https://www.kaggle.com/deepmatrix/imdb-5000-movie-dataset]()
    2. Import it using: ```$ flask import_movie_dataset data/imdb-5000-movie-dataset.zip```

Running the server (development)
--------------------------------

Use any of the following:
* ```(venv)$ flask run```
* ```(venv)$ python run.py```


Running the server (production)
-------------------------------

(venv)$ gunicorn -w 4 -b 127.0.0.1:5000 movie_recommendations:app
