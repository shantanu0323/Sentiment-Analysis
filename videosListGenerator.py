import json

f = open("./videosList.json", encoding='utf8')
s= f.read()

root = json.loads(s)

for item in root :
    videoId = item['v_id']
    print(videoId)

