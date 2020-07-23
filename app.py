#!/usr/bin/env python3

from flask import Flask, jsonify
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
import json
import os
import re
import requests

DATA_URL = os.getenv('DATA_URL', 'https://coronavirus-dashboard.utah.gov')

app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True


def get_cases():
    data = []
    try:
        r = requests.get(DATA_URL)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, 'html.parser')
        draper = soup.find(string=re.compile("Draper"))
        rates = json.loads(draper)['x']['calls'][1]['args'][4]
        for i in rates:
            i = i.replace('<strong>Name: </strong>', '')
            i = i.replace('<br><b>Case Count:</b> ', ',')
            i = i.replace('<br><b>Case Rate / 100,000:</b> ', ',')
            area_id = re.search(r"^\d.*-\d*\.\d|^\d.*-\d*", i)[0]
            i = re.sub(r"^\d.*-\d*\.\d |^\d.*-\d* ", "", i)
            i = i.split(',')

            if 'Data Note' in i[2]:
                note = i[2].split('<br>')[1]
                note = re.sub(r"<b>Data Note:</b> ", "", note)
                case_rate = float(re.sub(r"<br><b>Data Note:</b>.*", "", i[2]))
            else:
                case_rate = float(i[2])
                note = ""

            rate = {
                'area': i[0],
                'area_id': area_id,
                'case_count': int(i[1]),
                'case_rate': case_rate,
                'case_note': note
            }

            data.append(rate)
        return True, data
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        return False, http_err
    except Exception as err:
        print(f'Other error occurred: {err}')
        return False, err


@app.route("/")
def main():
    err, results = get_cases()
    if err is not False:
        return jsonify(results)
    else:
        return str(results), 500


if __name__ == "__main__":
    port = int(os.getenv('PORT', "5000"))
    app.run(debug=True, host='0.0.0.0', port=port)
