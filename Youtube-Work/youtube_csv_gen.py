# Author:  Allen Best

#  youtube.py searches YouTube for videos matching a search term and max results

# To run from terminal window:   python3 youtube.py 

from googleapiclient.discovery import build      # use build function to create a service object
import os, csv
from datetime import datetime, timedelta

# put your API key into the API_KEY field below, in quotes
API_KEY = os.environ.get("GOOGLE_API_KEY")

API_NAME = "youtube"
API_VERSION = "v3"       # this should be the latest version

youtube = build(API_NAME, API_VERSION, developerKey=API_KEY)

#  retrieve the YouTube records matching search term and max
search_term = str(input("Please enter the term you would like to search: "))
search_max = int(input("Please enter the max length of values you would like to recieve back: "))

print(f"Your search term: {search_term} \nYour search max: {search_max}")

search_data = youtube.search().list(q=search_term, part="id,snippet", maxResults=search_max).execute()
search_results = []
    
# search for videos matching search term;   
for search_instance in search_data.get("items", []):
    if search_instance["id"]["kind"] == "youtube#video":
        videoId = search_instance["id"]["videoId"]  
        title = search_instance["snippet"]["title"]
                      
                  
        video_data = youtube.videos().list(id=videoId,part="statistics,contentDetails").execute()
        for video_instance in video_data.get("items",[]):
            viewCount = video_instance["statistics"]["viewCount"]

            totalDuration = datetime.strptime(video_instance["contentDetails"]["duration"],"PT%MM%SS").time()
            likeCount = 0 if 'likeCount' not in video_instance["statistics"] else video_instance["statistics"]["likeCount"]
            dislikeCount = 0 if 'dislikeCount' not in video_instance["statistics"] else video_instance["statistics"]["dislikeCount"]

        search_results.append({'Video ID': videoId, 'View Count': viewCount, 'Like Count': likeCount, 'Dislike Count': dislikeCount, 'Duration': totalDuration, 'Title': title})

def sortPercentage(val): 
    return(int(val['Like Count'])/int(val['View Count']))

def printColSpace(str, space):
    return('|' + str + ' '*(space-len(str)))

search_results.sort(key=sortPercentage, reverse=True)

print("")
print('\t\t\t\t Top 5 Highest Percentage')
print('-------------------------------------------------------------------------------------------------------')
print("%-15s %-10s %-10s %-10s %-15s %-40s" % ('Video ID', 'Views', 'Likes', 'Dislikes',  'Duration', 'Title') ) 
if len(search_results) <= 5:
    [print("%-15s %-10s %-10s %-10s %-15s %-40s" % (val['Video ID'], val['View Count'], val['Like Count'], val['Dislike Count'], val['Duration'], val['Title'][:40])) for val in search_results] 
else:
    [print("%-15s %-10s %-10s %-10s %-15s %-40s" % (val['Video ID'], val['View Count'], val['Like Count'], val['Dislike Count'], val['Duration'], val['Title'][:40])) for val in search_results[:5]]

with open('youtube_output.csv', mode='w') as csv_file:
    fieldnames = ['Video ID', 'View Count', 'Like Count', 'Dislike Count',  'Duration', 'Title']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    
    writer.writeheader()
    writer.writerows(search_results)