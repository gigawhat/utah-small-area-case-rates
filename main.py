#!/usr/bin/env python3

from flask import Flask, jsonify
import json
import os
import re
import requests

app = Flask(__name__)


def get_cases():
    data = []
    url = "https://coronavirus-dashboard.utah.gov"
    r = requests.get(url)
    for line in r.text.splitlines():
        if 'data-for="htmlwidget-6bc80ecf58dffc13636e"' in line:
            foo = line.replace('<script type="application/json" data-for="htmlwidget-6bc80ecf58dffc13636e">', '')
            foo = foo.replace('</script>', '')
            foo = json.loads(foo)['x']['calls'][1]['args'][4]
            for i in foo:
                i = i.replace('<strong>Name: </strong>', '')
                i = i.replace('<br><b>Case Count:</b> ', ',')
                i = i.replace('<br><b>Case Rate / 100,000:</b> ', ',')
                bar = re.sub(r"^\d.*-\d*\.\d |^\d.*-\d* ", "", i)
                bar = bar.split(',')
                baz = {
                  'area': bar[0],
                  'case_count': bar[1],
                  'case_rate': bar[2]
                }
                data.append(baz)
    return data


@app.route("/")
def main():
    return(jsonify(get_cases()))


if __name__ == "__main__":
    port = int(os.getenv('PORT', "5000"))
    app.run(debug=True, host='0.0.0.0', port=port)
