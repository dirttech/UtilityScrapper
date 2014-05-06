__author__ = 'inderpal'

from flask import Flask, request
from Scrapper import ScrapHaryanaBijliVitranNigam, ScrapBSESDelhi

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World'


@app.route('/HaryanaBijliVitranNigam', methods=['GET', 'POST'])
def HaryanaBijliVitranNigam():
    cust_no=request.args.get('cust_no', None)
    return ScrapHaryanaBijliVitranNigam(cust_no)


@app.route('/BSESDelhi', methods=['GET', 'POST'])
def BSESDelhi():
    cust_no=request.args.get('cust_no', None)
    return ScrapBSESDelhi(cust_no)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

