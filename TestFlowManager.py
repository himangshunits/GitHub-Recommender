import graphlab as gl
import ConfigurationManager as cfg
import pandas as pd



class TestFlowManager:

    def __init__(self, train_flow_manager):
        # Take the ownerships of the predictor models and the data.
        self.train_flow_manager = train_flow_manager


    def get_repo_recommendation_from_username(self, username, method):
        #  The train has :: self.user_orig_data, self.repo_orig_data, self.user_data, self.repo_data
        # Slice out the test_user
        #print self.train_flow_manager.user_orig_data.head(n=30)
        test_user = self.train_flow_manager.user_orig_data[self.train_flow_manager.user_orig_data['user_login'] == username]
        user_id = test_user['user_id'].iloc[0]

        if method == "USER_ITEM":
            item_sim_recommendation = self.train_flow_manager.item_sim_model.recommend(users=[user_id], k=cfg.k_for_repositories)
            #print self.train_flow_manager.item_sim_model.recommend()
        elif method == "ITEM_CONTENT":
            # TODO : Implement this.
            item_sim_recommendation = self.train_flow_manager.item_content_model.recommend(users=[user_id],
                                                                                       k=cfg.k_for_repositories)
        else:
            print "Unknown prediction method! Never Never Get here = " + method

        pandas_frame_recommendations = item_sim_recommendation.to_dataframe()
        results = pd.DataFrame(columns=['html_url', 'repo_name', 'description', 'score', 'rank'])
        for index, row in pandas_frame_recommendations.iterrows():
            curr_repo_id = row['repo_id']
            curr_score = row['score']
            curr_rank = row['rank']
            # Get the other repo info from the repo_id
            repo_orig_row = self.train_flow_manager.repo_orig_data[self.train_flow_manager.repo_orig_data['repo_id'] == curr_repo_id]
            curr_repo_name = repo_orig_row['repo_name'].iloc[0]
            curr_repo_description = repo_orig_row['description'].iloc[0]
            curr_repo_html_url = repo_orig_row['html_url'].iloc[0]
            # Insert the data to the results row
            results.set_value(index, 'html_url', curr_repo_html_url)
            results.set_value(index, 'repo_name', curr_repo_name)
            results.set_value(index, 'description', curr_repo_description)
            results.set_value(index, 'score', curr_score)
            results.set_value(index, 'rank', curr_rank)
        return results



    def get_user_recommendation_from_username(self, username, method):
        pass

