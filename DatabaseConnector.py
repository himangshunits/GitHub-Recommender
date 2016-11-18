import json
import requests
import psycopg2
import sys



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



    # STATIC CLASS TO GET THE RANDOM COMMIT LOGS
    def get_commit_logs_for_test(self, limit):
        query = "select message from commit_events where message <> '' limit " + str(limit)
        self.cur.execute(query)
        rows = self.cur.fetchall()
        result = list()
        for item in rows:
            result.append(item[0])
        return result



