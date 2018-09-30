from watson_developer_cloud import ToneAnalyzerV3
from watson_developer_cloud import WatsonApiException
from flask import Flask,request,jsonify
from tweepy import OAuthHandler
from tweepy import API
from tweepy import TweepError
import random
import ast
number_of_tweets=5

# Twitter authentication
auth= OAuthHandler('9ZPpI5c3yLi8ZtSrzHAcIsppc'
,'W81EmOuPneZh39dwbK1nq0cjnc9iqpzKQqy4tu2pW8ruinsNbg')
auth.set_access_token('1044242601480675335-91v8RfyCaOJjjybdjGFYy3AhOe07Gk','DK9KGTSbvXj31DksRv3G8W09SA3eznwoYw7QJ5D1rKZge')
auth_api=API(auth)

# Watson authentication
tone_analyzer = ToneAnalyzerV3(
    version='2017-09-21',
    username='0c748a69-8ed7-48a7-b28e-50a20497caa1',
    password='6HjQgyIEcnVP',
    url='https://gateway.watsonplatform.net/tone-analyzer/api'
)

#flask app
app=Flask(__name__)
# @app.route('/',methods=['GET'])
# def check():
#     return 'Ok'
@app.route('/',methods=['POST'])
def Sentimize():
    target=request.get_json('userhandle')['userhandle']
    print("Getting data for " + target)
    emotions=['anger','joy','fear','sadness']
    emotion_value=0
    emotion_name='joy'
    try:
        user=auth_api.get_user(target)
    except TweepError as e:
        return jsonify({'message':"Not valid"})
    tweet_data=auth_api.user_timeline(screen_name=target,count=number_of_tweets)
    analyzer_input=""
    for i in tweet_data:
        analyzer_input+=i.text
    try:    
        tone_analysis = tone_analyzer.tone(
        {'text': analyzer_input},
        'application/json').get_result()
        cadidate_sentiments=tone_analysis['document_tone']['tones']
        # print(cadidate_sentiments)
        for sentiment in cadidate_sentiments:
            if(sentiment['score']>emotion_value and (sentiment['tone_id'] in emotions)):
                emotion_name=sentiment['tone_id']
                emotion_value=sentiment['score']
        # print(emotion_name+" "+str(emotion_value))
        with open(emotion_name+'.txt', 'r') as f:
             songlist = ast.literal_eval(f.read())
        return jsonify({'message':random.choice(songlist)})
        # print(json.dumps(tone_analysis, indent=2))

    except WatsonApiException as ex:
        print ("Method failed with status code " + str(ex.code) + ": " + ex.message)

if __name__=='__main__':
    app.run()
