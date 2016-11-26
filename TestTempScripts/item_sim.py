import graphlab as gl
import pandas as pd

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



#user_repo_association.csv
user_repo_association = pd.read_csv("movie_data.csv", sep=',', encoding='utf-8')
#user_repo_association.drop(user_repo_association.columns[[0]], axis=1, inplace=True)
       

print user_repo_association.shape

# Remove the extremem points to stay away from power law.
#rating <80

user_repo_association = user_repo_association[user_repo_association['rating'] < 90]

OldMax = user_repo_association['rating'].max()
OldMin = user_repo_association['rating'].min()

print user_repo_association.shape
user_repo_association['rating'] = user_repo_association['rating'].apply(rescale)

#print OldMin, OldMax

#print user_repo_association.head(n = 30)

#exit(0)

train_obs_data = gl.SFrame(user_repo_association)
train_obs_data.dropna()
print train_obs_data


#item_similarity_recommender
#factorization_recommender
train_obs, test_obs = gl.recommender.util.random_split_by_user(train_obs_data, item_id="repo_id")
item_sim_model = gl.recommender.factorization_recommender.create(train_obs, item_id='repo_id', user_id= 'user_id', target="rating", verbose=True)
        
print "Model Built !"
#print item_sim_model.evaluate(train_obs_data)

eval_model = item_sim_model.evaluate(test_obs)
#pre_recall = item_sim_model.evaluate_precision_recall(sf_test)
#rmse = item_sim_model.evaluate_rmse(sf_test, target='rating')


print item_sim_model.recommend(users=[8675834])
print item_sim_model.recommend(users=[16546086])
print eval_model
#print pre_recall
#print rmse
