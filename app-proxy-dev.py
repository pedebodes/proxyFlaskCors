import requests
import json
from flask import Flask, request, jsonify, redirect
app = Flask(__name__)
from flask_cors import CORS, cross_origin
CORS(app)

TOKEN = None

def obter_token():
    # data = {
    #     'username':'ACOPAIVAADM',
    #     'password': '8978911'
    # }

    data = {
        'username': 'bernardo.abreu',
        'password': 'Brasil123.'
    }
    data = {
        'username': 'MINASFER',
        'password': 'MFL18533-@'
    }

    # data = {
    #     'username':'bernardo.abreu',
    #     'password': 'Brasil123.'
    # }


    # data = {
    #     'username':'centralcomprassuperbuy',
    #     'password': 'SUPERBUY2017'
    # }

    r = requests.post("http://dev.superbuy.com.br/mobile/api/login", data=json.dumps(data))

    global TOKEN
    if r.status_code == 200:
        TOKEN = r.json()['token']
        print(TOKEN)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET'])
def catch_all(path):
    url = request.url.\
        replace(":5001", "").\
        replace("127.0.0.1", "dev.superbuy.com.br")
    if TOKEN:
        headers = {'Authorization': "Bearer " + TOKEN}
    else:
        headers = {}

    keywords = ['favicon', 'static', 'robots']
    if any([ key in url for key in keywords] ):
        return redirect(url.replace('sstatic', 'static'), code=301)
    else:
        response = requests.get(url, headers=headers)
        resp = jsonify(response.json())

        resp.status_code = response.status_code
        return resp

@app.route('/', defaults={'path': ''}, methods=['POST'])
@app.route('/<path:path>', methods=['POST'])
def catch_all_post(path):
    url = request.url.\
        replace(":5001", "").\
        replace("127.0.0.1", "dev.superbuy.com.br")

    data = json.dumps(json.loads(request.data or '{}'))
    global Token

    if TOKEN:
        headers = {'Authorization': "Bearer " + TOKEN}
    else:
        headers = {}
    response = requests.post(url, data=data, headers=headers)
    resp = jsonify(response.json())

    resp.status_code = response.status_code
    return resp

if __name__ == '__main__':
    obter_token()
    app.run(host='0.0.0.0', debug=True, port=5001)
