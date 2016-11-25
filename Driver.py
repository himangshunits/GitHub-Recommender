# coding=utf-8
# --- Import Libraries --- #
import pandas as pd
import graphlab as gl
from DatabaseConnector import DatabaseConnector
from PreprocessManager import PreprocessManager
from BiographyAnalyzer import BiographyAnalyzer
from CommitLogAnalyzer import CommitLogAnalyzer
from TrainFlowManager import TrainFlowManager
from TestFlowManager import TestFlowManager
from flask import Flask, request, jsonify
import sys
import copy
import ConfigurationManager as cfg


# The Server!
app_flask = Flask(__name__)

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
    item_sim_recomm = item_sim_model.recommend(users=[2], k=5)
    item_sim_recomm.print_rows(num_rows=25)

    return item_sim_model, test_data



def main():
    tr = TrainFlowManager()

    if not cfg.load_data_from_file:
        # Write to pickle
        tr.user_data.to_pickle(cfg.user_data_filename_pkl)
        tr.user_orig_data.to_pickle(cfg.user_orig_data_filename_pkl)
        tr.repo_data.to_pickle(cfg.repo_data_filename_pkl)
        tr.repo_orig_data.to_pickle(cfg.repo_orig_data_filename_pkl)
        tr.user_repo_association.to_pickle(cfg.user_repo_association_filename_pkl)
        # Write to CSV
        tr.user_data.to_csv(cfg.user_data_filename, sep=',', encoding='utf-8')
        tr.user_orig_data.to_csv(cfg.user_orig_data_filename, sep=',', encoding='utf-8')
        tr.repo_data.to_csv(cfg.repo_data_filename, sep=',', encoding='utf-8')
        tr.repo_orig_data.to_csv(cfg.repo_orig_data_filename, sep=',', encoding='utf-8')
        tr.user_repo_association.to_csv(cfg.user_repo_association_filename, sep=',', encoding='utf-8')

    tr.train_for_user_item_association()
    tr.train_for_item_content_similarity()
    tf = TestFlowManager(tr)
    res = tf.get_repo_recommendation_from_username("izuzero", "USER_ITEM")
    print "test Flow Manager updated! Going to start server."
    print "Recommendations for user =" + str(res)

    #app_flask.run(host='0.0.0.0', debug=True)


    # TODO :: Save the models here once everything is final.
    # Pass these models to the test flow manager.
    exit(0)


    '''[pop_model, test_data] = test_popularity_model()

    [item_sim_model, test_data1] = test_collaborative_filtering_model()

    model_performance = gl.compare(test_data, [pop_model, item_sim_model])
    gl.show_comparison(model_performance, [pop_model, item_sim_model])'''

    item_data = gl.SFrame({"my_item_id": range(4),
                           "data_1": ["North Carolina", "South Carolina", "Washington", "New Orleans"],
                           "data_2": [100, 150, 500, 50]})

    obs_data = gl.SFrame({"user_id": [0, 0, 0, 1, 1, 1, 2, 2],
                          "my_item_id": [0, 1, 2, 0, 1, 2, 1, 2],
                          "rating": [2, 3, 4, 1, 3, 4, 5, 0]})

    test_data = gl.SArray(["North Carolina", 120])

    m1 = gl.recommender.item_content_recommender.create(item_data=item_data, item_id='my_item_id',
                                                        observation_data=obs_data,
                                                        user_id='user_id', target='rating')

    print m1.recommend_from_interactions([0, 1])
    print m1.recommend(new_observation_data=test_data)


    exit(0)


def get_json_data_from_results(result):
    # Results in Pandas Frame of signature 'html_url', 'repo_name', 'description', 'score', 'rank'
    # TODO implement this
    return jsonify({'repo_name':"awesome repo"})


'''@app_flask.route('/api/get_repo_recommendation/<uuid>', methods=['GET', 'POST'])
def add_message(uuid):
    print "Request Received = " + str(uuid)
    #res = test_flow_manager_global.get_repo_recommendation_from_username(str(uuid), "USER_ITEM")
    json_data_to_send = get_json_data_from_results(res)
    return json_data_to_send'''


if __name__ == '__main__':
    main()


