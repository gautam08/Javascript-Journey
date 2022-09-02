from oauth2client.service_account import ServiceAccountCredentials
import httplib2
import json

import pandas as pd

# https://developers.google.com/search/apis/indexing-api/v3/prereqs#header_2
JSON_KEY_FILE = "1.json"
SCOPES = ["https://www.googleapis.com/auth/indexing"]

credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY_FILE, scopes=SCOPES)
http = credentials.authorize(httplib2.Http())

def indexURL(urls, http):
    # print(type(url)); print("URL: {}".format(url));return;

    ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
    
    alpha=0
    for u in urls:
        # print("U: {} type: {}".format(u, type(u)))
    
        content = {}
        content['url'] = u.strip()
        content['type'] = "URL_UPDATED"
        json_ctn = json.dumps(content)    
        # print(json_ctn);return
    
        response, content = http.request(ENDPOINT, method="POST", body=json_ctn)

        result = json.loads(content.decode())

        # For debug purpose only
        if("error" in result):
            print("Error({} - {}): {}".format(result["error"]["code"], result["error"]["status"], result["error"]["message"]))
        else:
            print("urlNotificationMetadata.url: {}".format(result["urlNotificationMetadata"]["url"]))
            print("urlNotificationMetadata.latestUpdate.url: {}".format(result["urlNotificationMetadata"]["latestUpdate"]["url"]))
            print("urlNotificationMetadata.latestUpdate.type: {}".format(result["urlNotificationMetadata"]["latestUpdate"]["type"]))
            print("urlNotificationMetadata.latestUpdate.notifyTime: {}".format(result["urlNotificationMetadata"]["latestUpdate"]["notifyTime"]))
            
        # for printing date and Time in the excel sheet
        csv.loc[alpha, 'Date'] = result['urlNotificationMetadata']['latestUpdate']['notifyTime'][0:10]
        csv.loc[alpha, 'Time'] = result['urlNotificationMetadata']['latestUpdate']['notifyTime'][11:19]
        csv.loc[alpha, 'Status'] = result["urlNotificationMetadata"]["latestUpdate"]["type"]
        alpha = alpha +1
        csv.to_csv("data.csv", index=False)

"""
data.csv has 2 columns: URL and date.
I just need the URL column.
"""
csv = pd.read_csv("data.csv")
csv[["URL"]].apply(lambda x: indexURL(x, http))