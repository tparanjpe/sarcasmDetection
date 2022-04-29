'''
This script pulls data from the Twitter API and writes it into a JSON file
Dataset of Twitter IDs should be provided in a tsv file in data/raw
'''
#from dotenv import load_dotenv
from pathlib import Path
from tqdm.auto import tqdm
import tweepy
import os
import json
import csv
import pandas as pd

# Dataset of ~15,000 English COVID-19 Tweets from 3-4PM on January 6th, Wednesday, 2021

DSET = "iSarcasm-master\isarcasm_train.csv"
#DSET = "isarcasm_trainSHORT.csv"
#isarcasm_trainSHORT.csv
myDF = pd.read_csv(DSET)
# Path to root directory of project
ROOT = Path(__file__).parent.parent

if __name__ == '__main__':

    consumer_key = ""
    consumer_secret = ""
    access_token = ""
    access_token_secret = ""

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    api.verify_credentials()

    rate_lim_mins = len(myDF.index) // 900 * 15
    print(f"Pulling all {len(myDF.index)} tweets will result in rate limits of {rate_lim_mins % 60} minutes.")

    colNames = ["tweet_data", "sarcasm_label", "tweet_id"]
    results = pd.DataFrame(columns=colNames)
    broken = 0
    res_index = 0

    for index, row in myDF.iterrows():
        status_id = row['tweet_id']
        sarc_label = row['sarcasm_label']
        try:
            if res_index %100 == 0:
                print("hit multiple of 100")
            response = api.get_status(status_id, tweet_mode="extended")
            fullText = response._json["full_text"]
            new_row = {'tweet_data': fullText, 'sarcasm_label': sarc_label, 'tweet_id': status_id}
            results = results.append(new_row, ignore_index=True)
            res_index+=1
            broken = 0
        except KeyboardInterrupt:
            break
        except:
            broken += 1

            if broken > 20:
                print("May be an issue!")
            else:
                continue

    results.to_csv("training.csv")
