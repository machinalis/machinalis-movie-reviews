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
    2. Import it using: ```$ flask import_movie_dataset movie_metadata.csv```

Running the server
------------------

Use any of the following:
* ```$ flask run```
* ```$ python run.py```
