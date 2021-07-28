import json
import warnings
import ckpe

#init
ckpe_obj = ckpe.ckpe()

warnings.filterwarnings("ignore",category=FutureWarning)

import sys
try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass


with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=DeprecationWarning)

import flask

# The flask app for serving predictions
app = flask.Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    """Determine if the container is working and healthy. In this sample container, we declare
    it healthy if we can load the model successfully."""
    # health = ScoringService.get_model() is not None  # You can insert a health check here
    health = 1

    status = 200 if health else 404
    print("===================== PING ===================")
    return flask.Response(response="{'status': 'Healthy'}\n", status=status, mimetype='application/json')

@app.route('/invocations', methods=['POST'])
def invocations():
    """Do an inference on a single batch of data. In this sample server, we take data as CSV, convert
    it to a pandas data frame for internal use and then convert the predictions back to CSV (which really
    just means one prediction per line, since there's a single column.
    """
    data = None
    print("================ INVOCATIONS =================")
    data = flask.request.data.decode('utf-8')
    print ("<<<<<input data: ", data)
    print ("<<<<<input content type: ", flask.request.content_type)

    # Convert from CSV to pandas
    #if flask.request.content_type == 'application/json':
    data = flask.request.data.decode('utf-8')
    print ("<<<<<input data: ", data)
    data = json.loads(data)
    data_input = data['data']

    print('Invoked with {} records'.format(data.keys()))

    # Do the prediction
    key_phrases = ckpe_obj.extract_keyphrase(data_input)
    print(key_phrases)
    result = {"关键词列表":key_phrases}
    print ("<<<result: ", result)
    x = {"res":result}
    response=json.dumps(x,ensure_ascii=False)

    return flask.Response(response=response, status=200, mimetype='application/json')