import spacy
from flask import Flask, request, redirect, jsonify, Response
import json
import en_core_web_sm as en
"""
	Service receive a list of text and return a list of vector of appropriate text
"""

nlp = en.load()
app = Flask(__name__)

@app.route('/', methods=["POST", "GET"])

def sen2vec():
	res = {'vector' : []}
	if request.method == 'POST':
		payload = json.loads((request.data).decode('utf-8'))
		txts = payload['text']
		for txt in txts:
			res['vector'].append(nlp(txt).vector.tolist())
	return jsonify(res)

if __name__ == '__main__':
	app.run(port=5000)