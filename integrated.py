from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import pandas as pd
import json
import os
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

CLIENT_SECRETS_FILE = "client_secret.json"

DEVELOPER_KEY = "AIzaSyB3OjFaaHL7yjV8B_SySi9wEYjR_513icQ"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

query = input("Enter the search query : ")
print("Please wait while we retrieve the videos from the server ...")

argparser.add_argument("--q", help="Search here", default=query)
argparser.add_argument("--max-results", help="Max results", default=25)
args = argparser.parse_args()
options = args

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

search_result = youtube.search().list(
    q=options.q,
    type="video",
    part="id,snippet",
    maxResults=options.max_results
).execute()

videos = {}

for search_result in search_result.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
        videos[search_result["id"]["videoId"]] = search_result["snippet"]["title"]

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

print('The list of videos has been retrieved ...')
print('\nGive us a momment while we validate the JSON data ...')
# Validating the JSON data
result = str(res)
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
result = result.replace("*#", "'");

print('JSON data validated...')
# Adding the comments to the videos

print('\nStarting Retrieval of comments...')
root = json.loads(result)

outputRoot = []
commentData = ""
def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials=credentials)


def print_response(response):
    response = str(response)
    response = response.replace("\"", "'");
    response = response.replace("True", "\"True\"");
    response = response.replace("''", "\" ");
    response = response.replace("{'", "{\"");
    response = response.replace(" '", " \"");
    response = response.replace("':", "\":");
    response = response.replace(":'", ":\"");
    response = response.replace("',", "\",");
    response = response.replace("'}", "\"}");
    commentData = response
    # print(response)

def build_resource(properties):
    resource = {}
    for p in properties:
        # Given a key like "snippet.title", split into "snippet" and "title", where
        # "snippet" will be an object and "title" will be a property in that object.
        prop_array = p.split('.')
        ref = resource
        for pa in range(0, len(prop_array)):
            is_array = False
            key = prop_array[pa]

            # For properties that have array values, convert a name like
            # "snippet.tags[]" to snippet.tags, and set a flag to handle
            # the value as an array.
            if key[-2:] == '[]':
                key = key[0:len(key) - 2:]
                is_array = True

            if pa == (len(prop_array) - 1):
                # Leave properties without values out of inserted resource.
                if properties[p]:
                    if is_array:
                        ref[key] = properties[p].split(',')
                    else:
                        ref[key] = properties[p]
            elif key not in ref:
                # For example, the property is "snippet.title", but the resource does
                # not yet have a "snippet" object. Create the snippet object here.
                # Setting "ref = ref[key]" means that in the next time through the
                # "for pa in range ..." loop, we will be setting a property in the
                # resource's "snippet" object.
                ref[key] = {}
                ref = ref[key]
            else:
                # For example, the property is "snippet.description", and the resource
                # already has a "snippet" object.
                ref = ref[key]
    return resource


# Remove keyword arguments that are not set
def remove_empty_kwargs(**kwargs):
    good_kwargs = {}
    if kwargs is not None:
        for key, value in kwargs.iteritems():
            if value:
                good_kwargs[key] = value
    return good_kwargs


def comment_threads_list_by_video_id(client, **kwargs):
    # See full sample for function
    # kwargs = remove_empty_kwargs(**kwargs)

    response = client.commentThreads().list(**kwargs).execute()

    return print_response(response)


for video in root:
    outputVideo = {}
    outputVideo["videoId"] = video['v_id']
    outputVideo["videoTitle"] = video['v_title']

    # Retrieving the comments

    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    client = get_authenticated_service()
    print("Retriieving comments for : " + outputVideo['videoId'] + " => " + outputVideo['videoTitle'] + "...")
    comment_threads_list_by_video_id(client, part='snippet,replies', videoId=outputVideo['videoId'])

    outputVideo["comments"] = commentData
    outputRoot.append(outputVideo)

try:
    f = open("./finalData.json", "w", encoding='utf8')
    f.write(str(outputRoot))
    f.close()
except FileNotFoundError as error:
    print("There was an error writing to the file" + error)
else:
    print("The list of comments was successffully written to the file 'finalData.json'")
