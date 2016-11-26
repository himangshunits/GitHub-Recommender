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
#app_flask = Flask(__name__)

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
    res_item = tf.get_repo_recommendation_from_username("tamil1", "USER_ITEM")
    #print "Recommendations for user =" + str(res_item.to_json(orient='records'))
    print "Recommendations for user =" + str(res_item)

    print "###########################################"

    res_item = tf.get_repo_recommendation_from_username("nilegsalcin", "USER_ITEM")
    # print "Recommendations for user =" + str(res_item.to_json(orient='records'))
    print "Recommendations for user =" + str(res_item)

    print "###########################################"


    res_content = tf.get_repo_recommendation_from_username("tamil1", "ITEM_CONTENT")
    #print "Recommendations for user =" + str(res_content.to_json(orient='records'))
    print "Recommendations for user =" + str(res_content)

    res_content = tf.get_repo_recommendation_from_username("nilegsalcin", "ITEM_CONTENT")
    # print "Recommendations for user =" + str(res_content.to_json(orient='records'))
    print "Recommendations for user =" + str(res_content)

    #app_flask.run(host='0.0.0.0', debug=True)


    # TODO :: Send the above JSONs as the result to the WebApp
    # Pass these models to the test flow manager.


if __name__ == '__main__':
    main()