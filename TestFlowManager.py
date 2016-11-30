from BiographyAnalyzer import BiographyAnalyzer
from CommitLogAnalyzer import CommitLogAnalyzer
import pandas as pd
import ConfigurationManager as cfg
import datetime
import LoggingManager as log_mgr
from CustomExceptions import UnknownUserException, UserIdAbsetInNewDataError
import graphlab as gl
from NewUserDataSynthesizer import NewUserDataSynthesizer
import dateparser





OldMax = 0
OldMin = 0
NewMax = 10
NewMin = 1

def rescale(OldValue):
	OldRange = (OldMax - OldMin)
	if OldRange == 0:
		NewValue = NewMin
	else:
		NewRange = (NewMax - NewMin)
		NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
	return NewValue





class TestFlowManager:

    def __init__(self, train_flow_manager):
        # Take the ownerships of the predictor models and the data.
        self.train_flow_manager = train_flow_manager
        self.bio_analyzer = BiographyAnalyzer(cfg.interests_tolerance, cfg.tech_tolerance, cfg.languages_tolerance,
                                              cfg.position_tolerance, cfg.student_status_tolerance)
        self.commit_log_analyzer = CommitLogAnalyzer()







    def __none_checker_int(self, input):
        return input if input is not None else 0

    def __none_checker_string(self, input):
        return input if input is not None else ""

    def __get_date_diff(self, input_date):
        curr_date = datetime.datetime.today()
        if input_date is None:
            return curr_date
        #print "The input type of the date is =" + str(type(input_date))
        parsed_date = dateparser.parse(str(input_date))
        #parsed_date = input_date.to_pydatetime()
        diff_in_days = (curr_date - parsed_date).days
        return diff_in_days


    def create_user_data_test(self, user_orig_data_test):
        for index, row in user_orig_data_test.iterrows():
            print row['user_id'], row['name']
            self.user_data_test.set_value(index, 'user_id', row['user_id'])
            self.user_data_test.set_value(index, 'location', self.__none_checker_string(row['location']))
            self.user_data_test.set_value(index, 'repo_count', self.__none_checker_int(row['repo_count']))
            self.user_data_test.set_value(index, 'followers_count', self.__none_checker_int(row['followers_count']))
            self.user_data_test.set_value(index, 'folowee_count', self.__none_checker_int(row['followees_count']))

            # take care of dates here
            self.user_data_test.set_value(index, 'days_from_creation', self.__get_date_diff(row['created_at']))
            self.user_data_test.set_value(index, 'days_from_update', self.__get_date_diff(row['updated_at']))

            # Synthesize the info from bio. Not very Accurate.
            '''"user_id", "location", "repo_count", "followers_count", "folowee_count",  "days_from_creation", "days_from_update",
                                                           "interest_q", "tech_q", "languages_q", "positions_q", "status_q"'''

            curr_bio_text = row['bio']
            if curr_bio_text is None or curr_bio_text == "":
                curr_bio_text = cfg.default_bio_text
            [interest_q, tech_q, languages_q, positions_q, status_q] = self.bio_analyzer.process_bio(curr_bio_text)

            # Add the data to userr data.
            self.user_data_test.set_value(index, 'interest_q', interest_q)
            self.user_data_test.set_value(index, 'tech_q', tech_q)
            self.user_data_test.set_value(index, 'languages_q', languages_q)
            self.user_data_test.set_value(index, 'positions_q', positions_q)
            self.user_data_test.set_value(index, 'status_q', status_q)




    def create_repo_data_test(self, repo_orig_data_test):
        '''["repo_id", "owner_id", "is_private", "is_forked", "cont_count", "language", "days_from_creation",
                                                   "days_from_updation", "days_from_push", "size", "watcher_count", "stargazer_count", "has_wiki", "fork_count", "open_issues",
                                                   "sub_count",  "readme", "description"]'''

        for index, row in repo_orig_data_test.iterrows():
            print row['repo_id'], row['repo_name']
            self.repo_data_test.set_value(index, 'repo_id', row['repo_id'])
            self.repo_data_test.set_value(index, 'owner_id', row['owner_id'])
            self.repo_data_test.set_value(index, 'is_private', row['is_private'])
            self.repo_data_test.set_value(index, 'is_forked', row['is_forked'])

            self.repo_data_test.set_value(index, 'cont_count', self.__none_checker_int(row['contributor_count']))
            self.repo_data_test.set_value(index, 'language', self.__none_checker_string(row['language']))
            # Dates
            self.repo_data_test.set_value(index, 'days_from_creation', self.__get_date_diff(row['created_at']))
            self.repo_data_test.set_value(index, 'days_from_updation', self.__get_date_diff(row['updated_at']))
            self.repo_data_test.set_value(index, 'days_from_push', self.__get_date_diff(row['pushed_at']))


            self.repo_data_test.set_value(index, 'size', self.__none_checker_int(row['size']))
            self.repo_data_test.set_value(index, 'watcher_count', self.__none_checker_int(row['watcher_count']))
            self.repo_data_test.set_value(index, 'stargazer_count', self.__none_checker_int(row['stargazer_count']))

            self.repo_data_test.set_value(index, 'has_wiki', row['has_wiki'])

            forks_count_total = self.__none_checker_int(row['forks_count']) + self.__none_checker_int(row['forks'])
            open_issues_count_total = self.__none_checker_int(row['open_issues_count']) + self.__none_checker_int(row['open_issues'])


            self.repo_data_test.set_value(index, 'fork_count', forks_count_total)
            self.repo_data_test.set_value(index, 'open_issues', open_issues_count_total)
            self.repo_data_test.set_value(index, 'sub_count', self.__none_checker_int(row['subscribers_count']))

            # Capture the description and readme for the repo.  "readme", "description"
            self.repo_data_test.set_value(index, 'readme', self.__none_checker_string(row['readme']))
            self.repo_data_test.set_value(index, 'description', self.__none_checker_string(row['readme']))
            # TODO : Enable the below line
            #self.repo_data.set_value(index, 'description', self.__none_checker_string(row['description']))
        #print self.repo_data.dtypes



    def __map_bool_to_int(self, input_bool):
        return 1 if input_bool == True else 0


    def synthesize_user_repo_association_test(self, user_orig_data_test, repo_orig_data_test, commits_orig_data_test):
        print "Synthesizing User Repo Association."
        # This API will find out the repositories importance and the user's association with them to finally allocate one rating for every repository
        # There are lot of things on which the Rating of this sentiment depends.
        # Rating Synthesizing weights for the different things.
        # Sentiments :: length, structural_integrity_score, topic_relevance_score, positivity_score, spelling_integrity_score
        # "is_forked", "cont_count", "days_from_push", "size", "watcher_count", "stargazer_count", "has_wiki", "fork_count", "open_issues", "sub_count", no_of_commits.
        # Total 16 this on which we are dependent.
        # We use a linear combination of different factors as distributed by the weights set in the configuration manager.
        # We have to divide the weights by 100 for normalisation.
        for index, row in self.repo_data_test.iterrows():
            try:
                '''user_id", "repo_id", "rating'''
                print "Synthesizing info for repo = " + str(row['repo_id']) + " and owner = " + str(row['owner_id'])
                curr_user_id = row['owner_id']
                curr_repo_id = row['repo_id']
                self.user_repo_association_test.set_value(index, 'user_id', curr_user_id)
                self.user_repo_association_test.set_value(index, 'repo_id', curr_repo_id)
                # Synthesize the Rating using the linear combination of the values depending on whether it's directly or inversely proportional.
                # First collect all the commit logs for this repo/repo user combination.
                curr_commits = []

                # TODO : Assuming here the commits are clean for only one user!

                commit_data_for_this_repo = commits_orig_data_test[commits_orig_data_test['repo_id'] == curr_repo_id]
                for index_inner, row_inner in commit_data_for_this_repo.iterrows():
                    curr_commits.append(row_inner['message_text'])

                # Capture the best description text.

                if row['readme'] != "":
                    best_description = row['readme']
                elif row['description'] != "":
                    best_description = row['description']
                else:
                    best_description = cfg.default_description

                [length, structural_integrity_score, topic_relevance_score, positivity_score, spelling_integrity_score] \
                    = self.commit_log_analyzer.process_batch_logs(curr_commits, best_description)

                no_of_commits = len(curr_commits)

                # Sentiments :: length, structural_integrity_score, topic_relevance_score, positivity_score, spelling_integrity_score
                # "is_forked", "cont_count", "days_from_push", "size", "watcher_count", "stargazer_count", "has_wiki", "fork_count", "open_issues", "sub_count", no_of_commits.

                a1 = length * float(cfg.average_commit_length_weight)/100
                a2 = structural_integrity_score * float(cfg.structural_integrity_score_weight)/100
                a3 = topic_relevance_score * float(cfg.topic_relevance_score_weight)/100
                a4 = positivity_score * float(cfg.topic_relevance_score_weight)/100
                a5 = spelling_integrity_score * float(cfg.spelling_integrity_score_weight)/100
                a6 = no_of_commits * float(cfg.no_of_commits_weight)/100
                a7 = float(cfg.is_forked_weight)/(100 * (1 + self.__map_bool_to_int(row['is_forked'])))
                a8 = row['cont_count'] * float(cfg.cont_count_weight)/100
                a9 = float(cfg.days_from_push_weight)/(100 * (1 + row['days_from_push']))
                a10 = row['size'] * float(cfg.repo_size_weight)/100
                a11 = row['watcher_count'] * float(cfg.watcher_count_weight) / 100
                a12 = row['stargazer_count'] * float(cfg.stargazer_count_weight) / 100
                a13 = self.__map_bool_to_int(row['has_wiki']) * float(cfg.has_wiki_weight) / 100
                a14 = row['fork_count'] * float(cfg.fork_count_weight) / 100
                a15 = row['open_issues'] * float(cfg.open_issues_weight) / 100
                a16 = row['sub_count'] * float(cfg.sub_count_weight) / 100

                cumulative_score =  a1 + a2 + a3 + a4 + a5 + a6 + a7 + a8 + a9 + a10 + a11 + a12 + a13 + a14 + a15 + a16
                # Insert the cumulative score to the 3rd column
                self.user_repo_association_test.set_value(index, 'rating', cumulative_score)
            except Exception as e:
                error = "Error in synthesizing association data. The error is = " + str(e) + "Other info :: Row Data = " + str(row)
                print error
                log_mgr.add_log_to_file(error)







    def get_repo_recommendation_from_username_new(self, username, method):
        self.user_data_test = pd.DataFrame(
            columns=["user_id", "location", "repo_count", "followers_count", "folowee_count", "days_from_creation",
                     "days_from_update",
                     "interest_q", "tech_q", "languages_q", "positions_q", "status_q"])
        self.repo_data_test = pd.DataFrame(
            columns=["repo_id", "owner_id", "is_private", "is_forked", "cont_count", "language", "days_from_creation",
                     "days_from_updation", "days_from_push", "size", "watcher_count", "stargazer_count", "has_wiki",
                     "fork_count", "open_issues",
                     "sub_count", "readme", "description"])
        # TODO : Could We keep the description also for matching?
        self.user_repo_association_test = pd.DataFrame(columns=["user_id", "repo_id", "rating"])


        # Get the Data using Murli's script.
        [user_orig_data_test, repo_orig_data_test, commit_orig_data_test] = NewUserDataSynthesizer.get_unknown_data(username)



        self.create_user_data_test(user_orig_data_test)# TODO : may Disable it if want speed! Not being used now anyway.
        self.create_repo_data_test(repo_orig_data_test)
        self.synthesize_user_repo_association_test(user_orig_data_test, repo_orig_data_test, commit_orig_data_test)
        self.user_repo_association_test['rating'] = self.user_repo_association_test['rating'].apply(rescale)

        try:
            test_user = user_orig_data_test[user_orig_data_test['user_login'] == username]
            user_id = test_user['user_id'].iloc[0]
        except:
            raise UserIdAbsetInNewDataError

        test_association_data = gl.SFrame(self.user_repo_association_test)

        '''sliced_columns = ["owner_id", "is_private", "is_forked", "cont_count", "language",
                          "days_from_creation",
                          "days_from_updation", "days_from_push", "size", "watcher_count",
                          "stargazer_count", "has_wiki", "fork_count", "open_issues",
                          "sub_count"]'''

        sliced_columns = ["owner_id", "is_forked", "cont_count", "language", "size", "has_wiki"]
        sliced_repo_data = self.repo_data_test[sliced_columns]
        sliced_repo_data.rename(index=str, columns={"owner_id": "user_id"}, inplace=True)
        # TODO: Rename owner_id to user_id
        # print sliced_repo_data.dtypes
        # print sliced_repo_data.isnull()
        test_repo_data = gl.SFrame(sliced_repo_data)



        if method == "USER_ITEM":
            item_sim_recommendation = self.train_flow_manager.item_sim_model.recommend(users=[user_id], new_observation_data=test_association_data, k=cfg.k_for_repositories)
        elif method == "ITEM_CONTENT":
            # TODO : Implement this.
            try:
                item_sim_recommendation = self.train_flow_manager.item_content_model.recommend(users=[user_id], new_item_data=test_repo_data, new_observation_data=test_association_data,
                                                                                       k=cfg.k_for_repositories)
            except Exception as e :
                error_string = "Error = " + str(e)
                print error_string
        else:
            print "Unknown prediction method! Never Never Get here = " + method
            item_sim_recommendation = None

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








    def get_repo_recommendation_from_username_in_database(self, username, method):
        #  The train has :: self.user_orig_data, self.repo_orig_data, self.user_data, self.repo_data
        # Slice out the test_user
        #print self.train_flow_manager.user_orig_data.head(n=30)
        try:
            test_user = self.train_flow_manager.user_orig_data[self.train_flow_manager.user_orig_data['user_login'] == username]
            user_id = test_user['user_id'].iloc[0]
        except:
            raise UnknownUserException

        if method == "USER_ITEM":
            item_sim_recommendation = self.train_flow_manager.item_sim_model.recommend(users=[user_id], k=cfg.k_for_repositories)
            #print self.train_flow_manager.item_sim_model.recommend()
        elif method == "ITEM_CONTENT":
            # TODO : Implement this.
            item_sim_recommendation = self.train_flow_manager.item_content_model.recommend(users=[user_id],
                                                                                       k=cfg.k_for_repositories)
        else:
            print "Unknown prediction method! Never Never Get here = " + method
            item_sim_recommendation = None

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
        raise NotImplementedError

