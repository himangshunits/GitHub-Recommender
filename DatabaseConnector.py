import json
import requests
import psycopg2
import sys
import pandas as pd



class DatabaseConnector:
    'Class that maintain all the database connectivity'
    instance_counter = 0

    def __init__(self):
        # Connect to the Database
        try:
            print "Connecting to database..."
            self.conn = psycopg2.connect("dbname='team5' user='team5' host='127.0.0.1' password='eThiPh3n' port ='8000'")
            self.cur = self.conn.cursor()
            DatabaseConnector.instance_counter += 1
            print "Connected! Instance Counter = " + str(DatabaseConnector.instance_counter)
        except:
            print "Connection to Database Failed! Current instance counter value = " + str(DatabaseConnector.instance_counter)
            sys.exit(0)
        self.users_org_data = pd.DataFrame()
        self.repo_org_data = pd.DataFrame()



    # STATIC CLASS TO GET THE RANDOM COMMIT LOGS :: Used for testing purposes only.
    def get_commit_logs_for_test(self, limit):
        query = "select message from commit_events where message <> '' limit " + str(limit)
        self.cur.execute(query)
        rows = self.cur.fetchall()
        result = list()
        for item in rows:
            result.append(item[0])
        return result


    # Get the commit logs for one user repo combination.
    def get_commits_for_user_repo(self, user_id, repo_id):
        query = "select message_text from commit_events_new where repo_id = " + str(repo_id) + " and committer_id = " + str(user_id)
        self.cur.execute(query)
        rows = self.cur.fetchall()
        result = list()
        for item in rows:
            result.append(item[0])
        return result

    def get_commits_for_repo(self, repo_id):
        query = "select message_text from commit_events_new where repo_id = " + str(repo_id)
        self.cur.execute(query)
        rows = self.cur.fetchall()
        result = list()
        for item in rows:
            result.append(item[0])
        return result



    def get_user_data(self, limit = 1000):
        '''"user_id", "user_login", "html_url", "name", "company", "location", "email",
                     "bio", "repo_count", "followers_count", "followee_count", "days_from_creation",
                     "days_from_update"'''
        query = "select * from users_new limit " + str(limit)
        self.cur.execute(query)
        rows = self.cur.fetchall()
        col_names = []
        for elt in self.cur.description:
            col_names.append(elt[0])

        self.users_org_data = pd.DataFrame(rows, columns=col_names)

        return self.users_org_data


    def get_repo_data(self, limit = 1000):
        query = "select * from repositories_new limit " + str(limit)
        self.cur.execute(query)
        rows = self.cur.fetchall()
        col_names = []
        for elt in self.cur.description:
            col_names.append(elt[0])

        self.repo_org_data = pd.DataFrame(rows, columns=col_names)

        return self.repo_org_data






