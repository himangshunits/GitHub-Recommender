import requests
res = requests.post('http://localhost:5000/api/get_repo_recommendation/petroav', json={"mytext":"lalala"})
if res.ok:
    print res.json()