from flask import Flask, request
import json

app = Flask(__name__)

messages = []


def response(obj, code=200):
    return json.dumps(obj, indent=2), code, {'content-type': 'application/json'}


def error(msg):
    return response({'error': msg}, 400)


@app.route('/')
def root():
    return response(messages)


@app.route('/send')
def send():
    message = request.args.get('message')

    if not message:
        return error('missing query string parameter (message)')

    messages.append(message)

    return response({
        'success': f'message ({message}) sent'
    })


@app.route('/delete')
def delete():
    message_id = request.args.get('id')

    if not message_id:
        return error('missing query string parameter (id)')

    try:
        message_id = int(message_id)
    except ValueError:
        return error(f'not a valid id ({message_id})')

    try:
        message = messages.pop(message_id)
    except IndexError:
        return error(f'id ({message_id}) not found')

    return response({
        'success': f'message ({message}) deleted'
    })

