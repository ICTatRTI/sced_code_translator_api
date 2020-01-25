from pathlib import Path
import json
from flask import Flask, jsonify, request, abort, redirect, render_template
from helpers import response_description, is_valid_sced_request, get_sced_v7_equivalent_codes
from time import time
from flask_cors import cross_origin

# Load crosswalk into memory
crosswalk_path = Path('./crosswalks/')
with open(crosswalk_path / 'sced_v7_crosswalk.json', 'r') as f:
    crosswalk = json.load(f)

class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        variable_start_string='%%',  # Default is '{{', I'm changing this because Vue.js uses '{{' / '}}'
        variable_end_string='%%',
    ))


app = CustomFlask(__name__)


@app.route('/')
def index():
    return redirect('/interface/')


@app.route('/interface/')
@cross_origin(allow_headers=['*'])
def interface():
    return render_template('interface.html')


@app.route('/api/')
def api():
    return render_template('api.html')


@app.route('/sced-v7-translate/', methods=['POST'])
@cross_origin(allow_headers=['*'])
def translate_to_sced_v7():
    start_time = time()
    if request.is_json is True:
        request_type = "json"
        request_data = request.get_json()
    else:
        request_type = "form"
        request_data = request.form

    # Check required field (sced_code)
    if not request_data or 'sced_code' not in request_data:
        bad_request_response = {'error' : 'Data missing sced_code variable',
                                'request_type': request_type}
        return jsonify(bad_request_response)

    # Return text a little differently for web format
    web_fmt = "web_fmt" in request_data

    # Get SCED code input and check format
    sced_code = request_data["sced_code"]
    err, msg = is_valid_sced_request(sced_code, crosswalk)
    if err:
        bad_request_response = {'error': msg, 'request_type': request_type}
        return jsonify(bad_request_response)

    # We now know input SCED code actually exists in crosswalk
    v7_codes = get_sced_v7_equivalent_codes(sced_code, crosswalk)

    warning = None
    if not v7_codes:
        warning = "Archived SCED code exists but cannot be crosswalked to SCED v7"

    time_elapsed = time() - start_time
    submitted_data = {'sced_code': sced_code}
    info = {'time_elapsed': str(round(time_elapsed, 2)) + ' s',
            'warning': warning}

    response = {
        'description': response_description,
        'submitted_data': submitted_data,
        'info': info,
        'translated_codes': v7_codes
    }

    # Format request differently for webform reponse
    if web_fmt:
        # Unpack archived versions into a single string of archived SCED codes
        for v7_code in v7_codes:
            archived_codes = ["{0}: {1}".format(archived_code["sced_code"],
                                                archived_code["course_title"])
                              for archived_code in v7_code["archived_versions"]]
            archived_codes = "\n".join(archived_codes)
            v7_code["archived_versions"] = archived_codes if archived_codes else "None"

    return jsonify(response)
