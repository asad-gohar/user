from flask import Flask, request, render_template, url_for, json
import requests
from json import JSONDecodeError

app = Flask(__name__)
API_KEY = "3870e490-0705-11eb-ab4c-65e0e07acc88"

headers = {'apikey': API_KEY}


def search(terms, country):
    results = []
    for term in terms:
        if "poland" in country:
            params = (
                ("q", term),
                ("device", "desktop"),
                ("gl", "PL"),
                ("hl", "pl"),
                ("search_engine", "google.pl"),
                ("location", "Poland"),
                ("lr", "lang_pl")
            )
        else:
            params = (
                ("q", term),
                ("device", "desktop"),
                ("gl", "RO"),
                ("hl", "ro"),
                ("search_engine", "google.ro"),
                ("location", "Romania"),
                ("lr", "lang_ro")
            )

        response = requests.get('https://app.zenserp.com/api/v2/search', headers=headers, params=params)
        try:
            my_json = response.content.decode('utf8')
            data = json.loads(my_json)
        except:
            pass
        results.append(data['number_of_results'])
    return results


@app.route('/')
def index():
    return render_template('form.html')


@app.route('/submit', methods=['POST'])
def submit():
    keys = format(request.form['text']).split("\n")
    results = search(keys, request.form['country'])
    new_results = []
    for result in results:
        if result is None:
            new_results.append(0)
        else:
            new_results.append(result)
    results_to_pass = [keys, new_results]
    return render_template('data.html', enumerate=len(results), posts=results_to_pass)


if __name__ == "__main__":
    app.run()
