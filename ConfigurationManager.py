# This file keeps all the global Configurations of the system.

# Declare the file paths
interests_file = 'bio_corpuses/interests'
tech_file = 'bio_corpuses/technologies'
language_file = 'bio_corpuses/languages'
position_file = 'bio_corpuses/positions'
student_status_file = 'bio_corpuses/student_statuses'


## Filenames to store the calculated tables.
user_data_filename = "calculated_data/user_data.csv"
user_orig_data_filename = "calculated_data/user_orig_data.csv"
repo_data_filename = "calculated_data/repo_data.csv"
repo_orig_data_filename = "calculated_data/repo_orig_data.csv"
user_repo_association_filename = "calculated_data/user_repo_association.csv"


user_data_filename_pkl = "calculated_data/user_data.pkl"
user_orig_data_filename_pkl = "calculated_data/user_orig_data.pkl"
repo_data_filename_pkl = "calculated_data/repo_data.pkl"
repo_orig_data_filename_pkl = "calculated_data/repo_orig_data.pkl"
user_repo_association_filename_pkl = "calculated_data/user_repo_association.pkl"





# Log File path
log_file_path = "logging_events.txt"





# Declare the matching thresholds for fuzzy string matchings!
# interests_tolerance, tech_tolerance, languages_tolerance, position_tolerance, student_status_tolerance
interests_tolerance = 80
tech_tolerance = 80
languages_tolerance = 80
position_tolerance = 80
student_status_tolerance = 80


# Limits on Data Pulling, normally keep it high.
train_users_limit = 100000
train_repos_limit = 100000
# Change this value to control how big the association matrix should be computed.
association_processing_limit = 10000

# Default Biography
default_bio_text = "Interested in Software Development."
default_commit_text = "Fixed the latest issues and implemented new features for better performance."
default_description = "This is a GitHub Repository."


# Rating Synthesizing weights for the different things.
# Sentiments :: length, structural_integrity_score, topic_relevance_score, positivity_score, spelling_integrity_score
# "is_forked", "cont_count", "days_from_push", "size", "watcher_count", "stargazer_count", "has_wiki", "fork_count", "open_issues", "sub_count", no_of_commits.
# Total 16 this on which we are dependent.
# These are percentages. Must add up-to 100%
average_commit_length_weight = 10
structural_integrity_score_weight = 8
topic_relevance_score_weight = 2
positivity_score_weight = 2
spelling_integrity_score_weight = 5
is_forked_weight = 5
cont_count_weight = 10
days_from_push_weight = 10
repo_size_weight = 10
watcher_count_weight = 2
stargazer_count_weight = 2
has_wiki_weight = 5
fork_count_weight = 8
open_issues_weight = 8
sub_count_weight = 5
no_of_commits_weight = 8


# Whether we have to take only the repo logs or the logs for the user and teh repo
is_commits_from_repo_only = True


# How many recommendations?
k_for_repositories = 10
k_for_users = 10


# Doe we load the models from local file or compute?
load_data_from_file = True



# Rating outliers removal, 80 is a good number from where it becomes a normal.
rating_matrix_removal_limit = 70




# Set the limit on repo for new user
new_user_repo_limit = 10
new_user_commit_limit = 10
