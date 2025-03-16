import tweepy
from datetime import datetime
from datetime import timedelta
import math
import os 
from util import fileupdate

access_token = ""
access_token_secret = ""
bearer_token = ""
api = ""
api_secret = ""

client = tweepy.Client(bearer_token,api, api_secret, access_token, access_token_secret)
auth = tweepy.OAuth1UserHandler(api, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)

start_date = datetime(2023, 11, 12)
target_date = datetime(2024, 11, 9)

today = datetime.today().replace(hour=0,minute=0,second=0,microsecond=0)

          
def write_log(text, progress_percentage_yesterday, progress_percentage_today):
     f = open("/home/pi/code/progress/" + os.path.splitext(os.path.basename(__file__))[0] + ".log", "a", encoding="utf-8")
     f.write(datetime.now().strftime("%d.%m.%Y %H:%M:%S") + " | " + today.strftime("%d.%m.%Y") + "\t" + text + "\t yesterday: " + str(round(progress_percentage_yesterday,2)) + "%  today: " + str(round(progress_percentage_today,2)) + "% \t \n")
     f.close()


def check_percentage(start_date, target_date):
    total_days = (target_date - start_date).days

    yesterday = today - timedelta(days = 1)

    remaining_days_today = (target_date - today).days
    remaining_days_yesterday = (target_date - yesterday).days

    progress_percentage_today = 100 - (remaining_days_today / total_days) * 100
    progress_percentage_yesterday = 100 - (remaining_days_yesterday / total_days) * 100

    if remaining_days_today < 0:
        return write_log("done", progress_percentage_yesterday, progress_percentage_today)

    cut_percentage_today = math.trunc(progress_percentage_today)    
    cut_percentage_yesterday = math.trunc(progress_percentage_yesterday)

    if progress_percentage_today == 0:
        write_log("post", progress_percentage_yesterday, progress_percentage_today)
        print(generate_progress_bar(total_days, remaining_days_today))
        client.create_tweet(text=generate_progress_bar(total_days, remaining_days_today) + " #Arcane #ArcaneSeason2")
        fileupdate.plus_one()

    if cut_percentage_yesterday < cut_percentage_today:
        write_log("post", progress_percentage_yesterday, progress_percentage_today)
        print(generate_progress_bar(total_days, remaining_days_today))
        client.create_tweet(text=generate_progress_bar(total_days, remaining_days_today) + " #Arcane #ArcaneSeason2")
        fileupdate.plus_one()

    else:
        write_log("skip", progress_percentage_yesterday, progress_percentage_today)

    print(progress_percentage_yesterday, progress_percentage_today)
    print(cut_percentage_yesterday, cut_percentage_today)

def generate_progress_bar(total_days, remaining_days): 

    progress_percentage = 100 - (remaining_days / total_days) * 100
    progress_bar_length = 20
    completed_length = int(progress_percentage / 100 * progress_bar_length)
    remaining_length = progress_bar_length - completed_length

    progress_bar = 'â' * completed_length + 'â' * remaining_length
    return f"{progress_bar} {math.trunc(progress_percentage)}%"


def main():
    check_percentage(start_date, target_date)


if __name__ == "__main__":
    main()
