# coding=utf-8
# --- Import Libraries --- #
import pandas as pd
import graphlab as gl
from DatabaseConnector import DatabaseConnector
from PreprocessManager import PreprocessManager
from BiographyAnalyzer import BiographyAnalyzer
from CommitLogAnalyzer import CommitLogAnalyzer
import sys

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

    item_data = gl.SFrame({"my_item_id": range(4),
                           "data_1": ["North Carolina","South Carolina","Washington","New Orleans"],
                           "data_2": [100,150,500,50]})


    test_data = gl.SArray(["North Carolina", 120])

    m = gl.recommender.item_content_recommender.create(item_data, "my_item_id")
    print m.recommend_from_interactions([0, 1])
    print m.recommend(new_observation_data = test_data)



    exit(0)

    database_driver = DatabaseConnector()
    commits = database_driver.get_commit_logs_for_test(100)
    log_analyzer = CommitLogAnalyzer()
    [length, structural_integrity_score, topic_relevance_score, positivity_score, spelling_integrity_score] \
        = log_analyzer.process_batch_logs(commits, "")

    print length, structural_integrity_score, topic_relevance_score, positivity_score, spelling_integrity_score

    exit(0)


    log_analyzer = CommitLogAnalyzer()
    [length, structural_integrity_score, topic_relevance_score, positivity_score, spelling_integrity_score] \
        = log_analyzer.process_one_log("Modification de la méthode CalculerDateFinContratCtrl","")

    print length, structural_integrity_score, topic_relevance_score, positivity_score, spelling_integrity_score

    sys.exit(0)

    bio = BiographyAnalyzer(80, 80, 80, 80, 80)
    bio_p = bio.process_bio("Interested in web and other softwares. Also workign as phd student ")
    print bio_p


    database_driver = DatabaseConnector()
    commits = database_driver.get_commit_logs_for_test(50)
    print commits

    data = "Notice that due to the fact that here you are searching in a set (not in a list) the speed would be theoretically len(stop_words)/2 times faster, which is significant if you need to operate through many documents. For 5000 documents of approximately 300 words each the difference is between 1.8 seconds for my example and 20 seconds for @alvas's. P.S. in most of the cases you need to divide the text into words to perform some other classification tasks for which tf-idf is used. So most probably it would be better to use stemmer as well:"
    freq_count = PreprocessManager.get_unique_words(data)

    print freq_count


    '''[pop_model, test_data] = test_popularity_model()

    [item_sim_model, test_data1] = test_collaborative_filtering_model()

    model_performance = gl.compare(test_data, [pop_model, item_sim_model])
    gl.show_comparison(model_performance, [pop_model, item_sim_model])'''






if __name__ == '__main__':
        main()

