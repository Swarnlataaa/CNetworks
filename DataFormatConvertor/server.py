from flask import Flask, render_template, request, jsonify
import json
import xmltodict

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    data = request.form['data']
    input_format = request.form['input_format']
    output_format = request.form['output_format']

    try:
        if input_format == 'json' and output_format == 'xml':
            xml_data = json_to_xml(data)
            return render_template('index.html', result=xml_data, original_data=data)

        elif input_format == 'xml' and output_format == 'json':
            json_data = xml_to_json(data)
            return render_template('index.html', result=json_data, original_data=data)

        else:
            return render_template('index.html', error="Invalid conversion: Unsupported formats")

    except Exception as e:
        return render_template('index.html', error=f"Error during conversion: {str(e)}")

def json_to_xml(json_data):
    return xmltodict.unparse(json.loads(json_data), pretty=True)

def xml_to_json(xml_data):
    return json.dumps(xmltodict.parse(xml_data), indent=2)

if __name__ == '__main__':
    app.run(debug=True)
