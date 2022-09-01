import io,json
from flask import Flask, request, jsonify, render_template
from get_drug_details import get_all_drugs,get_selected_drug_data
from get_prediction import get_predicted_data

app = Flask(__name__)


@app.route('/test')
def test_app():
    return "<h1>welcome to Optimization of Drug Inventory</h1>"

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/get_all_drugs', methods=['GET'])
def get_all_drug_data():
    resp = jsonify({'output': get_all_drugs()})
    resp.status_code = 200
    return resp

@app.route('/get_drug_data', methods=['POST'])
def get_drug_data():
    data = request.get_json()
    drug_id = int(data["drug_id"])
    resp = jsonify({'output': get_selected_drug_data(drug_id)})
    resp.status_code = 200
    return resp

@app.route('/get_drug_prediction', methods=['POST'])
def get_drug_predicted_data():
    data = request.get_json()
    drug_id = data.get("drug_id",'0')
    avail_stock = data.get("avail_stock",'00')
    resp = jsonify({'output': get_predicted_data(int(drug_id),int(avail_stock))})
    resp.status_code = 200
    return resp
