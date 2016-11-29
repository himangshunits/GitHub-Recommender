# coding=utf-8
# --- Import Libraries --- #
from TrainFlowManager import TrainFlowManager
from TestFlowManager import TestFlowManager
import ConfigurationManager as cfg
import flask

# This is the entry point and the instance must be owned by the calling program.

class Driver:
    no_instances = 0

    def __init__(self):
        self.train_flow_manager = TrainFlowManager()
        if not cfg.load_data_from_file:
            # Write to pickle
            self.train_flow_manager.user_data.to_pickle(cfg.user_data_filename_pkl)
            self.train_flow_manager.user_orig_data.to_pickle(cfg.user_orig_data_filename_pkl)
            self.train_flow_manager.repo_data.to_pickle(cfg.repo_data_filename_pkl)
            self.train_flow_manager.repo_orig_data.to_pickle(cfg.repo_orig_data_filename_pkl)
            self.train_flow_manager.user_repo_association.to_pickle(cfg.user_repo_association_filename_pkl)
            # Write to CSV
            self.train_flow_manager.user_data.to_csv(cfg.user_data_filename, sep=',', encoding='utf-8')
            self.train_flow_manager.user_orig_data.to_csv(cfg.user_orig_data_filename, sep=',', encoding='utf-8')
            self.train_flow_manager.repo_data.to_csv(cfg.repo_data_filename, sep=',', encoding='utf-8')
            self.train_flow_manager.repo_orig_data.to_csv(cfg.repo_orig_data_filename, sep=',', encoding='utf-8')
            self.train_flow_manager.user_repo_association.to_csv(cfg.user_repo_association_filename, sep=',', encoding='utf-8')

        self.train_flow_manager.train_for_user_item_association()
        self.train_flow_manager.train_for_item_content_similarity()
        self.test_flow_manager = TestFlowManager(self.train_flow_manager)
        Driver.no_instances += 1
        print "No of instances of Driver is = " + str(Driver.no_instances)





    def get_recommendations_for_username(self, username, method="USER_ITEM"):
        try:
            res_item = self.test_flow_manager.get_repo_recommendation_from_username(username, method)
            return res_item.to_json(orient='records')
        except Exception as e:
            result_message = "Error Occurred. Please Enter Valid User ID ! Error Message = " + str(e)
            res_json = flask.jsonify({"error": result_message})
            return res_json
