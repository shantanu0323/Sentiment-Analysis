from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import pandas as pd

DEVELOPER_KEY = "AIzaSyB3OjFaaHL7yjV8B_SySi9wEYjR_513icQ"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

query = input("Enter the search query : ")
argparser.add_argument("--q", help="Search here", default=query)
# change the default to the search term you want to search
argparser.add_argument("--max-results", help="Max results", default=25)
# default number of results which are returned. It can vary from 0 - 100
args = argparser.parse_args()
options = args

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

# Call the search.list method to retrieve results matching the specified
# query term.
search_result = youtube.search().list(
    q=options.q,
    type="video",
    part="id,snippet",
    maxResults=options.max_results
).execute()

videos = {}

# Add each result to the appropriate list, and then display the lists of
# matching videos.
# Filter out channels, and playlists.
for search_result in search_result.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
        # videos.append("%s" % (search_result["id"]["videoId"]))
        videos[search_result["id"]["videoId"]] = search_result["snippet"]["title"]

# print ("Videos:\n", "\n".join(videos), "\n")
s = ','.join(videos.keys())

videos_list_result = youtube.videos().list(
    id=s,
    part='id,statistics'
).execute()

res = []
for i in videos_list_result['items']:
    temp_res = dict(v_id=i['id'], v_title=videos[i['id']])
    temp_res.update(i['statistics'])
    res.append(temp_res)
pd.DataFrame.from_dict(res)

result = str(res)
# print (result)
result = result.replace(":\"", ":'");
result = result.replace(": \"", ": '");

result = result.replace("\",", "',");
result = result.replace("\" ,", "' ,");

result = result.replace("\"", "*#");

result = result.replace("{'", "{\"");
result = result.replace("{ '", "{ \"");

result = result.replace("' :", "\" :");
result = result.replace("':", "\":");

result = result.replace(": '", ": \"");
result = result.replace(":'", ":\"");

result = result.replace("',", "\",");
result = result.replace("' ,", "\" ,");

result = result.replace(", '", ", \"");
result = result.replace(",'", ",\"");

result = result.replace("' }", "\" }");
result = result.replace("'}", "\"}");
result = result.replace("*#","'");

try:
    text_file = open("videosList.json", "w", newline='', encoding='utf8')
    text_file.write(result)
    text_file.close()
except FileNotFoundError as error:
    print("There was an error writing to the file" + error)
else:
    print("The list of comments was successffully written to the file 'videosList.json'")






