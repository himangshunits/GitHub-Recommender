import graphlab as gl
import pandas as pd

user_repo_association = pd.read_csv("user_repo_association.csv", sep=',', encoding='utf-8')
user_repo_association.drop(user_repo_association.columns[[0]], axis=1, inplace=True)

my_data = gl.SFrame(user_repo_association)

#print my_data[:10]


train, test = gl.recommender.util.random_split_by_user(my_data, item_id='repo_id')

print "Train Test Splitted!"

item_sim_model = gl.item_similarity_recommender.create(train, user_id='user_id', item_id='repo_id',
                                                               target='rating', similarity_type='pearson', verbose=True)

print "Model Built !"

eval_model = item_sim_model.evaluate(test)
pre_recall = item_sim_model.evaluate_precision_recall(test)
rmse = item_sim_model.evaluate_rmse(test, target='rating')

#print eval_model
#print pre_recall
print rmse
