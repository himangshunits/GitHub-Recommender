# coding=utf-8
# --- Import Libraries --- #
import pandas as pd
import graphlab as gl
from DatabaseConnector import DatabaseConnector
from PreprocessManager import PreprocessManager
from BiographyAnalyzer import BiographyAnalyzer
from CommitLogAnalyzer import CommitLogAnalyzer
from TrainFlowManager import TrainFlowManager
import sys
import ConfigurationManager as cfg

def test_popularity_model():
    print("Inside the Main Method")
    # pass in column names for each CSV and read them using pandas.
    # Column names available in the readme file

    # Reading users file:
    u_cols = ['user_id', 'age', 'sex', 'occupation', 'zip_code']
    users = pd.read_csv('ml-100k/u.user', sep='|', names=u_cols,
                        encoding='latin-1')

    # Reading ratings file:
    r_cols = ['user_id', 'movie_id', 'rating', 'unix_timestamp']
    ratings = pd.read_csv('ml-100k/u.data', sep='\t', names=r_cols,
                          encoding='latin-1')

    # Reading items file:
    i_cols = ['movie id', 'movie title', 'release date', 'video release date', 'IMDb URL', 'unknown', 'Action',
              'Adventure',
              'Animation', 'Children\'s', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
              'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
    items = pd.read_csv('ml-100k/u.item', sep='|', names=i_cols,
                        encoding='latin-1')

    print(users.shape)
    print(users.head())

    print(ratings.shape)
    print(ratings.head())

    print(items.shape)
    print(items.head())

    r_cols = ['user_id', 'movie_id', 'rating', 'unix_timestamp']
    ratings_base = pd.read_csv('ml-100k/ua.base', sep='\t', names=r_cols, encoding='latin-1')
    ratings_test = pd.read_csv('ml-100k/ua.test', sep='\t', names=r_cols, encoding='latin-1')
    print(ratings_base.shape, ratings_test.shape)

    train_data = gl.SFrame(ratings_base)
    test_data = gl.SFrame(ratings_test)

    popularity_model = gl.popularity_recommender.create(train_data, user_id='user_id', item_id='movie_id',
                                                        target='rating')

    # Get recommendations for first 5 users and print them
    # users = range(1,6) specifies user ID of first 5 users
    # k=5 specifies top 5 recommendations to be given
    popularity_recomm = popularity_model.recommend(users=range(1, 6), k=5)
    popularity_recomm.print_rows(num_rows=25)

    print(ratings_base.groupby(by='movie_id')['rating'].mean().sort_values(ascending=False).head(20))

    return popularity_model, test_data


def test_collaborative_filtering_model():
    r_cols = ['user_id', 'movie_id', 'rating', 'unix_timestamp']
    ratings_base = pd.read_csv('ml-100k/ua.base', sep='\t', names=r_cols, encoding='latin-1')



    ratings_test = pd.read_csv('ml-100k/ua.test', sep='\t', names=r_cols, encoding='latin-1')
    print(ratings_base.shape, ratings_test.shape)

    train_data = gl.SFrame(ratings_base)
    test_data = gl.SFrame(ratings_test)


    # Train Model
    item_sim_model = gl.item_similarity_recommender.create(train_data, user_id='user_id', item_id='movie_id',
                                                                 target='rating', similarity_type='pearson')




    # Make Recommendations:
    item_sim_recomm = item_sim_model.recommend(users=1, k=5)
    item_sim_recomm.print_rows(num_rows=25)

    return item_sim_model, test_data



def main():
    #docs = gl.SArray('https://static.turi.com/datasets/nytimes')
    #exit(0)

    tr = TrainFlowManager()
    user_item_model = tr.train_for_user_item_association()
    item_content_model = tr.train_for_item_content_similarity()
    # Pass these models to the test flow manager.
    exit(0)

    item_data = gl.SFrame({"my_item_id": range(4),
                           "data_1": ["North Carolina","South Carolina","Washington","New Orleans"],
                           "data_2": [100,150,500,50]})


    test_data = gl.SArray(["North Carolina", 120])

    m = gl.recommender.item_content_recommender.create(item_data, "my_item_id")
    print m.recommend_from_interactions([0, 1])
    print m.recommend(new_observation_data = test_data)



    exit(0)
    '''[pop_model, test_data] = test_popularity_model()

    [item_sim_model, test_data1] = test_collaborative_filtering_model()

    model_performance = gl.compare(test_data, [pop_model, item_sim_model])
    gl.show_comparison(model_performance, [pop_model, item_sim_model])'''






if __name__ == '__main__':
        main()

