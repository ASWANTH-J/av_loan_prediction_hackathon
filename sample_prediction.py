
import os  
import flask  
import spacy  
from flask import make_response, jsonify  
  
prefix = '/opt/ml/'  
model_path = os.path.join(prefix, 'gembrill_ner')  
  
nlp = spacy.load(model_path)  
  
  
  
  
# The flask app for serving predictions  
app = flask.Flask(__name__)  
  
@app.route('/ping', methods=['GET'])  
def ping():  
    """Determine if the container is working and healthy. In this sample container, we declare  it healthy if we can load the model successfully."""
	health = nlp is not None # You can insert a health check here  
	
	status = 200 if health else 404  
	return flask.Response(response='\n', status=status, mimetype='application/json')  

@app.route('/invocations', methods=['POST'])  
def transformation():
	if flask.request.content_type == 'application/json':  
	    data = flask.request.get_json()  
	    text = data['text']
		doc = nlp(text)
		ents = str([ent.text,ent.label_ for ent in doc.ents])
		result = make_response(  
				jsonify(  
					"ents":ents
				),  
		200,  
		)  
			result.headers["Content-Type"] = "application/json"  
		return result  
	
	else:  
		return flask.Response(response='This predictor json data', status=415, mimetype='text/plain')
