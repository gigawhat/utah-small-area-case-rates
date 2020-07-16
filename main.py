#!/usr/bin/env python3

from flask import Flask, jsonify
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
import json
import os
import re
import requests

app = Flask(__name__)


def get_cases():
    data = []
    url = "https://coronavirus-dashboard.utah.gov"
    try:
        r = requests.get(url)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, 'html.parser')
        draper = soup.find(string=re.compile("Draper"))
        rates = json.loads(draper)['x']['calls'][1]['args'][4]
        for i in rates:
            i = i.replace('<strong>Name: </strong>', '')
            i = i.replace('<br><b>Case Count:</b> ', ',')
            i = i.replace('<br><b>Case Rate / 100,000:</b> ', ',')
            i = re.sub(r"^\d.*-\d*\.\d |^\d.*-\d* ", "", i)
            i = i.split(',')
            rate = {
                'area': i[0],
                'case_count': i[1],
                'case_rate': i[2]
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
