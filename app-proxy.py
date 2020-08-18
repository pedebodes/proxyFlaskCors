import requests
import json
from flask import Flask, request, jsonify, redirect
app = Flask(__name__)
from flask_cors import CORS, cross_origin
CORS(app)

TOKEN = None

def obter_token():
    # data = {
    #     'username':'andre.saraujo',
    #     'password': 'Gilberto1'
    # }

    data = {
        'username': 'goliveira',
        'password': 'hhv2573@2'
    }

    # data = {
    #     'username': 'bernardo.abreu',
    #     'password': 'Brasil123.'
    # }
    # data = {
    #     'username': 'bernardo.abreu',
    #     'password': 'Gerais123.'
    # }

    # data = {
    #     'username': 'keller.simone',
    #     'password': 'KELLER03!'
    # }
    # data = {
    #     'username': 'TMARCOLINO',
    #     'password': 'TAVARES13'
    # }
    #data = {
    #    'username': 'MINASFER',
    #    'password': 'MFL18533-@'
    #}

    #data = {
    #    'username': 'MARCELOVASCONCELOS',
    #    'password': 'RA102030'
    #}
    #data = {
    #     'username':'bernardo.abreu',
    #     'password': 'Minas123.'
    #}


    # data = {
    #     'username':'centralcomprassuperbuy',
    #     'password': 'SUPERBUY2017'
    # }

    r = requests.post("http://localhost:5000/mobile/api/login", data=json.dumps(data))
    # import pdb; pdb.set_trace()
    global TOKEN
    if r.status_code == 200:
        TOKEN = r.json()['token']
        print(TOKEN)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET'])
def catch_all(path):
    url = request.url.replace("5001", "5000").replace("172.16.0.24", "127.0.0.1")
    if TOKEN:
        headers = {'Authorization': "Bearer " + TOKEN}
    else:
        headers = {}

    keywords = ['favicon', 'static', 'robots']
    if any([ key in url for key in keywords] ):
        return redirect(url.replace('sstatic', 'static'), code=301)
    else:
        response = requests.get(url, headers=headers)
        try:
            resp = jsonify(response.json())

            resp.status_code = response.status_code
            return resp
        except ValueError:
            return response.content, response.status_code

@app.route('/', defaults={'path': ''}, methods=['POST'])
@app.route('/<path:path>', methods=['POST'])
def catch_all_post(path):
    url = request.url.replace("5001", "5000")

    data = json.dumps(json.loads(request.data or '{}'))
    global Token

    if TOKEN:
        headers = {'Authorization': "Bearer " + TOKEN}
    else:
        headers = {}

    if request.files and data == '{}':
        data = {}
        for k, v in request.form.items():
            data[k] = v

    response = requests.post(url, data=data, files=request.files, headers=headers)

    try:
        resp = jsonify(response.json())

        resp.status_code = response.status_code
        return resp
    except ValueError:
        return response.content, response.status_code

if __name__ == '__main__':
    obter_token()
    app.run(host='0.0.0.0', debug=True, port=5001, threaded=True)
