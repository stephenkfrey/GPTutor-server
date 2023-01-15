print ("Starting server.py")

print ('Importing libraries')
from flask import Flask, render_template, request
import os
import gunicorn

import csv

print ('importing from py script ')
try: 
    from transcribe_youtube import get_transcription_from_youtube_url
except Exception as e:
    print (f"ERROR: {e}")

# Flask 
app = Flask(__name__)
print('Flask app created')


# def save to ccsv (title url content )


############################
# return the stored CSV 
############################
@app.route("/getCSV", methods=["GET"])
def getLocalCSV(): 
    print("Received request to get local CSV")

    # extract the request from the json 

    # request = request.args.get('request') # TODO 

    try: 
        request_content = request.get_json(silent=True)
        request = request_content['mock']
    except Exception as e:
        request = ''
        print ("ERROR: no request in request_content")

    try: 
        ############################
        # MOCK DATA
        if request == "mock": 
                # load the local CSV 
            with open('mockBrowsingData.csv', 'r') as f:
                reader = csv.reader(f)
                data = list(reader)

            print ("Successfully loaded mock CSV\n")

            return data 

        ############################
        # REAL DATA
        else:
            # load the local CSV 
            with open('allBrowsingData.csv', 'r') as f:
                reader = csv.reader(f)
                data = list(reader)

            print ("Successfully loaded local CSV\n")

            return data 
    except Exception as e: 
        print (f"ERROR: {e}")
        return "ERROR"

############################
# send articles  {title, url, content}
############################
@app.route("/article", methods=["POST"])
def article():
    print ('Received article Request')

    request_content = request.get_json(silent=True)

    try: 
        title = request_content.get('title', "")
        url = request_content['url']
        content = request_content['content']

        print ('article request url:', url)

        # add a new row to the local CSV with url and content 
        with open('allBrowsingData.csv', 'a') as f:
            print (f"about to log new data to CSV. \nurl: {url}\ncontent[:200[]: {content[:200]}")

            writer = csv.writer(f)
            writer.writerow([title, url, content])

            print ("Article - Successfully wrote new data to CSV\n")

            return "OK"

    except Exception as e:
        print (f"ERROR in ARTICLE request: {e}")
        return "ERROR"


############################
# send youtube video URLs 
############################
@app.route("/youtube", methods=["POST"])
def youtube():
    print ('Received youtube Request')

    request_content = request.get_json(silent=True)
    url = request_content['url']

    print ('youtube request url:', url)

    # check URL is a youtube URL 

    try: 
        title, url, content = get_transcription_from_youtube_url(url)

        # add a new row to the local CSV with url and content
        with open('allBrowsingData.csv', 'a') as f:
            print (f"about to log new data to CSV. \nurl: {url}\ncontent[:200[]: {content[:200]}")

            writer = csv.writer(f)
            writer.writerow([title, url, content])

            print ("Youtube - Successfully wrote new data to CSV\n")
            return "OK"

    except Exception as e:
        print (f"ERROR in ARTICLE request: {e}")
        
        return "ERROR"
 

############################
# test
############################
@app.route("/test", methods=["GET","POST"])
def test():
    return "HI YOU FOUND ME" 

############################
print ("server.py has loaded")

if __name__ == '__main__':
    print ("ran __main__")
    app.run()