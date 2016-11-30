import requests
import pandas as pd
import ConfigurationManager as cfg



class NewUserDataSynthesizer:


    def __init__(self):
        pass



    @staticmethod
    def get_unknown_data(user_name):
        unknown_user_data = pd.DataFrame(
            columns=["user_id", "user_login", "html_url", "name", "company", "location", "email", "bio", "repo_count",
                     "followers_count", "followees_count", "created_at", "updated_at", "blog_url"])
        unknown_repos_data = pd.DataFrame(
            columns=["repo_id", "repo_name", "owner_id", "is_private", "html_url", "is_forked", "contributor_count",
                     "language", "created_at", "updated_at", "pushed_at", "size", "watcher_count", "stargazer_count",
                     "has_wiki", "forks_count", "open_issues_count", "forks", "open_issues", "subscribers_count",
                     "readme", "description"])
        unknown_commits_data = pd.DataFrame(columns=["sha", "repo_id", "committer_id", "message_text"])

        unknown_user = requests.get(
            "https://api.github.com/users/" + user_name + "?client_id=1095193b20259f256419&client_secret=8bcf2cddc7a4d597cdcbe1446e0c2b9d750605be")
        unknown_user_json = unknown_user.json()

        unknown_user_data.set_value(0, 'user_id', unknown_user_json["id"])
        unknown_user_data.set_value(0, 'user_login', unknown_user_json["login"])
        unknown_user_data.set_value(0, 'html_url', unknown_user_json["html_url"])
        unknown_user_data.set_value(0, 'name', unknown_user_json["name"])
        unknown_user_data.set_value(0, 'company', unknown_user_json["company"])
        unknown_user_data.set_value(0, 'location', unknown_user_json["location"])
        unknown_user_data.set_value(0, 'email', unknown_user_json["email"])
        unknown_user_data.set_value(0, 'bio', unknown_user_json["bio"])
        unknown_user_data.set_value(0, 'repo_count', unknown_user_json["public_repos"])
        unknown_user_data.set_value(0, 'followers_count', unknown_user_json["followers"])
        unknown_user_data.set_value(0, 'followees_count', unknown_user_json["following"])
        unknown_user_data.set_value(0, 'created_at', unknown_user_json["created_at"])
        unknown_user_data.set_value(0, 'updated_at', unknown_user_json["updated_at"])
        unknown_user_data.set_value(0, 'blog_url', unknown_user_json["blog"])

        unknown_repo = requests.get(unknown_user_json["repos_url"] + "?client_id=1095193b20259f256419&client_secret=8bcf2cddc7a4d597cdcbe1446e0c2b9d750605be")
        unknown_repo_json = unknown_repo.json()

        i = 0
        j = 0

        for unknown_single_repo_json in unknown_repo_json:
            try:
                print "Synthesizing Repositories for new User, Left to process = " + str(cfg.new_user_repo_limit - i)
                if i >= cfg.new_user_repo_limit:
                    break
                unknown_repos_data.set_value(i, 'repo_id', unknown_single_repo_json["id"])
                unknown_repos_data.set_value(i, 'repo_name', unknown_single_repo_json["name"])
                unknown_repos_data.set_value(i, 'owner_id', unknown_single_repo_json["owner"]["id"])
                unknown_repos_data.set_value(i, 'is_private', unknown_single_repo_json["private"])
                unknown_repos_data.set_value(i, 'html_url', unknown_single_repo_json["html_url"])
                unknown_repos_data.set_value(i, 'is_forked', unknown_single_repo_json["fork"])
                contributor_data = requests.get(unknown_single_repo_json[
                                                    "contributors_url"] + "?client_id=1095193b20259f256419&client_secret=8bcf2cddc7a4d597cdcbe1446e0c2b9d750605be")
                contributor_data_json = contributor_data.json()
                unknown_repos_data.set_value(i, 'contributor_count', len(contributor_data_json))
                unknown_repos_data.set_value(i, 'language', unknown_single_repo_json["language"])
                unknown_repos_data.set_value(i, 'created_at', unknown_single_repo_json["created_at"])
                unknown_repos_data.set_value(i, 'updated_at', unknown_single_repo_json["updated_at"])
                unknown_repos_data.set_value(i, 'pushed_at', unknown_single_repo_json["pushed_at"])
                unknown_repos_data.set_value(i, 'size', unknown_single_repo_json["size"])
                unknown_repos_data.set_value(i, 'watcher_count', unknown_single_repo_json["watchers_count"])
                unknown_repos_data.set_value(i, 'stargazer_count', unknown_single_repo_json["stargazers_count"])
                unknown_repos_data.set_value(i, 'has_wiki', unknown_single_repo_json["has_wiki"])
                unknown_repos_data.set_value(i, 'forks_count', unknown_single_repo_json["forks_count"])
                unknown_repos_data.set_value(i, 'open_issues_count', unknown_single_repo_json["open_issues_count"])
                unknown_repos_data.set_value(i, 'forks', unknown_single_repo_json["forks"])
                unknown_repos_data.set_value(i, 'open_issues', unknown_single_repo_json["open_issues"])
                subscribers = requests.get(unknown_single_repo_json["subscribers_url"] + "?client_id=1095193b20259f256419&client_secret=8bcf2cddc7a4d597cdcbe1446e0c2b9d750605be")
                subscribers_json = subscribers.json()
                unknown_repos_data.set_value(i, 'subscribers_count', len(subscribers_json))
                readme_data = requests.get(unknown_single_repo_json["html_url"] + "/raw/master/README.md")
                if readme_data.status_code is 200:
                    unknown_repos_data.set_value(i, 'readme', readme_data.text)
                else:
                    unknown_repos_data.set_value(i, 'readme', "no readme")
                unknown_repos_data.set_value(i, 'description', unknown_single_repo_json["description"])

                unknown_single_repo_branches = requests.get(unknown_single_repo_json[
                                                                "url"] + "/branches" + "?client_id=1095193b20259f256419&client_secret=8bcf2cddc7a4d597cdcbe1446e0c2b9d750605be")
                unknown_single_repo_branches_json = unknown_single_repo_branches.json()
                unknown_single_repo_master_json = unknown_single_repo_branches_json[-1]
                unknown_single_repo_master_commits = requests.get(unknown_single_repo_json[
                                                                      "url"] + "/commits" + "?client_id=1095193b20259f256419&client_secret=8bcf2cddc7a4d597cdcbe1446e0c2b9d750605be&per_page=100&sha=" +
                                                                  unknown_single_repo_master_json["commit"]["sha"])
                unknown_single_repo_master_commits_json = unknown_single_repo_master_commits.json()

                inner_j = 0
                for commit in unknown_single_repo_master_commits_json:
                    try:
                        if inner_j >= cfg.new_user_commit_limit:
                            break
                        unknown_commits_data.set_value(j, 'sha', commit["sha"])
                        unknown_commits_data.set_value(j, 'repo_id', unknown_single_repo_json["id"])
                        unknown_commits_data.set_value(j, 'committer_id', commit["committer"]["id"])
                        unknown_commits_data.set_value(j, 'message_text', commit["commit"]["message"])
                        j = j + 1
                        inner_j += 1
                    except:
                        pass

                i = i + 1
            except Exception as e:
                error_text = "Repo was not processed well, Error Message = " + str(e)
                print error_text
        return unknown_user_data, unknown_repos_data, unknown_commits_data