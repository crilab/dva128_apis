from flask import Flask, render_template, request
import json

import ai

app = Flask(__name__)


def response(obj, code=200):
    return json.dumps(obj, indent=2), code, {'content-type': 'application/json'}


def error(msg):
    return response({'error': msg}, 400)


@app.route('/')
def root():
    f = '?filter='

    if request.args.get('filter') == 'false':
        f += 'false'
    else:
        f += 'true'

    return render_template('./index.html', f=f)


@app.route('/classify', methods=['GET'])
def classify_get():
    return error('unsupported method (GET)')


@app.route('/classify', methods=['POST'])
def classify_post():
    if not request.files:
        return error('no file attached')

    if 'image' not in request.files:
        return error('missing image identifier')

    image = request.files['image'].read()

    predictions = ai.classify(image)

    if request.args.get('filter') != 'false':
        predictions = predictions[:5]

    return response(predictions)

