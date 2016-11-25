from DatabaseConnector import DatabaseConnector
from PreprocessManager import PreprocessManager
from BiographyAnalyzer import BiographyAnalyzer
from CommitLogAnalyzer import CommitLogAnalyzer
import sys
import pandas as pd
import ConfigurationManager as cfg
import datetime
import graphlab as gl
import LoggingManager as log_mgr
#import dateparser



class TrainFlowManager:
    'This class collects the data from database, synthesizes the data in the form the recommendation engines can use and then make the models for reco.'

    def __init__(self):
        self.db_connector = DatabaseConnector()
        if cfg.load_data_from_file:
            '''self.user_data = pd.read_csv(cfg.user_data_filename, sep=',', encoding='utf-8')
            self.user_data.drop(self.user_data.columns[[0]], axis=1, inplace=True)
            self.user_orig_data = pd.read_csv(cfg.user_orig_data_filename, sep=',', encoding='utf-8')
            self.user_orig_data.drop(self.user_orig_data.columns[[0]], axis=1, inplace=True)
            self.repo_data = pd.read_csv(cfg.repo_data_filename, sep=',', encoding='utf-8')
            self.repo_data.drop(self.repo_data.columns[[0]], axis=1, inplace=True)
            self.repo_orig_data = pd.read_csv(cfg.repo_orig_data_filename, sep=',', encoding='utf-8')
            self.repo_orig_data.drop(self.repo_orig_data.columns[[0]], axis=1, inplace=True)
            self.user_repo_association = pd.read_csv(cfg.user_repo_association_filename, sep=',', encoding='utf-8')
            self.user_repo_association.drop(self.user_repo_association.columns[[0]], axis=1, inplace=True)'''
            # Load from Pickle.
            self.user_data = pd.read_pickle(cfg.user_data_filename_pkl)
            self.user_orig_data = pd.read_pickle(cfg.user_orig_data_filename_pkl)
            self.repo_data = pd.read_pickle(cfg.repo_data_filename_pkl)
            self.repo_orig_data = pd.read_pickle(cfg.repo_orig_data_filename_pkl)
            self.user_repo_association = pd.read_pickle(cfg.user_repo_association_filename_pkl)
        else:
            self.user_orig_data = self.db_connector.get_user_data(limit=cfg.train_users_limit)
            self.repo_orig_data = self.db_connector.get_repo_data(limit=cfg.train_repos_limit)
            self.user_data = pd.DataFrame(columns=["user_id", "location", "repo_count", "followers_count", "folowee_count",  "days_from_creation", "days_from_update",
                                                   "interest_q", "tech_q", "languages_q", "positions_q", "status_q"])
            self.repo_data = pd.DataFrame(columns=["repo_id", "owner_id", "is_private", "is_forked", "cont_count", "language", "days_from_creation",
                                                       "days_from_updation", "days_from_push", "size", "watcher_count", "stargazer_count", "has_wiki", "fork_count", "open_issues",
                                                       "sub_count", "readme", "description"])
            # TODO : Could We keep the description also for matching?
            self.user_repo_association = pd.DataFrame(columns=["user_id", "repo_id", "rating"])
            self.bio_analyzer = BiographyAnalyzer(cfg.interests_tolerance, cfg.tech_tolerance, cfg.languages_tolerance,
                                    cfg.position_tolerance, cfg.student_status_tolerance)
            self.commit_log_analyzer = CommitLogAnalyzer()
            self.create_datasets()

    # this API will give the internal stuff of this class
    def get_data_structures(self):
        return self.user_orig_data, self.repo_orig_data, self.user_data, self.repo_data
    # This API will pull the Data and populate the local data structures.
    def create_datasets(self):
        self.create_user_data()
        self.create_repo_data()
        self.synthesize_user_repo_association()
        return

    def __none_checker_int(self, input):
        return input if input is not None else 0

    def __none_checker_string(self, input):
        return input if input is not None else ""

    def __get_date_diff(self, input_date):
        curr_date = datetime.datetime.today()
        if input_date is None:
            return curr_date
        #print "The input type of the date is =" + str(type(input_date))
        #parsed_date = dateparser.parse(str(input_date))
        parsed_date = input_date.to_pydatetime()
        diff_in_days = (curr_date - parsed_date).days
        return diff_in_days


    def create_user_data(self):
        for index, row in self.user_orig_data.iterrows():
            print row['user_id'], row['name']
            self.user_data.set_value(index, 'user_id', row['user_id'])
            self.user_data.set_value(index, 'location', self.__none_checker_string(row['location']))
            self.user_data.set_value(index, 'repo_count', self.__none_checker_int(row['repo_count']))
            self.user_data.set_value(index, 'followers_count', self.__none_checker_int(row['followers_count']))
            self.user_data.set_value(index, 'folowee_count', self.__none_checker_int(row['followees_count']))

            # take care of dates here
            self.user_data.set_value(index, 'days_from_creation', self.__get_date_diff(row['created_at']))
            self.user_data.set_value(index, 'days_from_update', self.__get_date_diff(row['updated_at']))

            # Synthesize the info from bio. Not very Accurate.
            '''"user_id", "location", "repo_count", "followers_count", "folowee_count",  "days_from_creation", "days_from_update",
                                                           "interest_q", "tech_q", "languages_q", "positions_q", "status_q"'''

            curr_bio_text = row['bio']
            if curr_bio_text is None or curr_bio_text == "":
                curr_bio_text = cfg.default_bio_text
            [interest_q, tech_q, languages_q, positions_q, status_q] = self.bio_analyzer.process_bio(curr_bio_text)

            # Add the data to userr data.
            self.user_data.set_value(index, 'interest_q', interest_q)
            self.user_data.set_value(index, 'tech_q', tech_q)
            self.user_data.set_value(index, 'languages_q', languages_q)
            self.user_data.set_value(index, 'positions_q', positions_q)
            self.user_data.set_value(index, 'status_q', status_q)


    # Main public API which will return a graph lab model for user_item_rating model
    def train_for_user_item_association(self):
        train_data = gl.SFrame(self.user_repo_association)

        # Train Model
        self.item_sim_model = gl.item_similarity_recommender.create(train_data, user_id='user_id', item_id='repo_id',
                                                               target='rating', similarity_type='pearson', verbose=True)
        return self.item_sim_model


    # This API will train a model for item similarity.
    def train_for_item_content_similarity(self):
        sliced_columns = ["repo_id", "is_private", "is_forked", "cont_count", "language", "days_from_creation",
                          "days_from_updation", "days_from_push", "size", "watcher_count",
                          "stargazer_count", "has_wiki", "fork_count", "open_issues",
                          "sub_count"]
        sliced_repo_data = self.repo_data[sliced_columns]
        train_data = gl.SFrame(sliced_repo_data)
        train_data_observation = gl.SFrame(self.user_repo_association)
        self.item_content_model = gl.recommender.item_content_recommender.create(item_data=train_data, item_id='repo_id',
                                                                                 observation_data=train_data_observation, user_id='user_id', target='rating', verbose=True)
        return self.item_content_model



    def create_repo_data(self):
        '''["repo_id", "owner_id", "is_private", "is_forked", "cont_count", "language", "days_from_creation",
                                                   "days_from_updation", "days_from_push", "size", "watcher_count", "stargazer_count", "has_wiki", "fork_count", "open_issues",
                                                   "sub_count",  "readme", "description"]'''
        for index, row in self.repo_orig_data.iterrows():
            print row['repo_id'], row['repo_name']
            self.repo_data.set_value(index, 'repo_id', row['repo_id'])
            self.repo_data.set_value(index, 'owner_id', row['owner_id'])
            self.repo_data.set_value(index, 'is_private', row['is_private'])
            self.repo_data.set_value(index, 'is_forked', row['is_forked'])

            self.repo_data.set_value(index, 'cont_count', self.__none_checker_int(row['contributor_count']))
            self.repo_data.set_value(index, 'language', self.__none_checker_string(row['language']))
            # Dates
            self.repo_data.set_value(index, 'days_from_creation', self.__get_date_diff(row['created_at']))
            self.repo_data.set_value(index, 'days_from_updation', self.__get_date_diff(row['updated_at']))
            self.repo_data.set_value(index, 'days_from_push', self.__get_date_diff(row['pushed_at']))


            self.repo_data.set_value(index, 'size', self.__none_checker_int(row['size']))
            self.repo_data.set_value(index, 'watcher_count', self.__none_checker_int(row['watcher_count']))
            self.repo_data.set_value(index, 'stargazer_count', self.__none_checker_int(row['stargazer_count']))

            self.repo_data.set_value(index, 'has_wiki', row['has_wiki'])

            forks_count_total = self.__none_checker_int(row['forks_count']) + self.__none_checker_int(row['forks'])
            open_issues_count_total = self.__none_checker_int(row['open_issues_count']) + self.__none_checker_int(row['open_issues'])


            self.repo_data.set_value(index, 'fork_count', forks_count_total)
            self.repo_data.set_value(index, 'open_issues', open_issues_count_total)
            self.repo_data.set_value(index, 'sub_count', self.__none_checker_int(row['subscribers_count']))

            # Capture the description and readme for the repo.  "readme", "description"
            self.repo_data.set_value(index, 'readme', self.__none_checker_string(row['readme']))
            self.repo_data.set_value(index, 'description', self.__none_checker_string(row['readme']))
            # TODO : Enable the below line
            #self.repo_data.set_value(index, 'description', self.__none_checker_string(row['description']))



    def __map_bool_to_int(self, input_bool):
        return 1 if input_bool == True else 0


    def synthesize_user_repo_association(self):
        print "Synthesizing User Repo Association."
        # This API will find out the repositories importance and the user's association with them to finally allocate one rating for every repository
        # There are lot of things on which the Rating of this sentiment depends.
        # Rating Synthesizing weights for the different things.
        # Sentiments :: length, structural_integrity_score, topic_relevance_score, positivity_score, spelling_integrity_score
        # "is_forked", "cont_count", "days_from_push", "size", "watcher_count", "stargazer_count", "has_wiki", "fork_count", "open_issues", "sub_count", no_of_commits.
        # Total 16 this on which we are dependent.
        # We use a linear combination of different factors as distributed by the weights set in the configuration manager.
        # We have to divide the weights by 100 for normalisation.
        association_processing_limit = cfg.association_processing_limit
        for index, row in self.repo_data.iterrows():
            if association_processing_limit <= 0:
                break
            try:
                '''user_id", "repo_id", "rating'''
                print "Synthesizing info for repo = " + str(row['repo_id']) + " and owner = " + str(row['owner_id'])
                curr_user_id = row['owner_id']
                curr_repo_id = row['repo_id']
                self.user_repo_association.set_value(index, 'user_id', curr_user_id)
                self.user_repo_association.set_value(index, 'repo_id', curr_repo_id)
                # Synthesize the Rating using the linear combination of the values depending on whether it's directly or inversely proportional.
                # First collect all the commit logs for this repo/repo user combination.
                curr_commits = []
                if cfg.is_commits_from_repo_only:
                    curr_commits = self.db_connector.get_commits_for_repo(curr_repo_id)
                else:
                    curr_commits = self.db_connector.get_commits_for_user_repo(curr_user_id, curr_repo_id)

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
                self.user_repo_association.set_value(index, 'rating', cumulative_score)
            except Exception as e:
                error = "Error in synthesizing association data. The error is = " + str(e) + "Other info :: Row Data = " + str(row)
                print error
                log_mgr.add_log_to_file(error)
