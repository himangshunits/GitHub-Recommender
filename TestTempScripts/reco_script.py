import graphlab as gl
import pandas as pd

repo_data = pd.read_csv("repo_data.csv", sep=',')


repo_data.drop(repo_data.columns[[0]], axis=1, inplace=True)
            # Replace NaNs
repo_data['language'].fillna(' ', inplace=True)
repo_data['readme'].fillna(' ', inplace=True)
repo_data['description'].fillna(' ', inplace=True)




user_repo_association = pd.read_csv("user_repo_association.csv", sep=',', encoding='utf-8')
user_repo_association.drop(user_repo_association.columns[[0]], axis=1, inplace=True)
       






sliced_columns = ["repo_id", "is_private", "is_forked", "cont_count", "language", "days_from_creation",
                          "days_from_updation", "days_from_push", "size", "watcher_count",
                          "stargazer_count", "has_wiki", "fork_count", "open_issues",
                          "sub_count", "owner_id"]
sliced_repo_data = repo_data[sliced_columns]

sliced_repo_data.rename(index=str, columns={"owner_id": "user_id"}, inplace = True)
train_data = gl.SFrame(sliced_repo_data)

train_obs_data = gl.SFrame(user_repo_association)

print train_data


train_obs, test_obs = gl.recommender.util.random_split_by_user(train_obs_data, item_id="repo_id")
sf_train, sf_test = train_data.random_split(.7, seed=123)
print "Train Test Splitted!"

#item_sim_model = gl.item_similarity_recommender.create(train, user_id='user_id', item_id='repo_id',
 #                                                              target='rating', similarity_type='pearson', verbose=True)
item_content_model = gl.recommender.item_content_recommender.create(item_data=sf_train, item_id='repo_id', user_id= 'user_id',observation_data=train_obs, target="rating", verbose=True)
        
print "Model Built !"

eval_model = item_content_model.evaluate(sf_test, new_observation_data=test_obs, target="rating")
#pre_recall = item_content_model.evaluate_precision_recall(sf_test)
#rmse = item_content_model.evaluate_rmse(sf_test, target='rating')

print eval_model
#print pre_recall
#print rmse
