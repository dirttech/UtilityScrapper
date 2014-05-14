__author__ = 'inderpal'

from flask import Flask, request
from Scrapper import ScrapHaryanaBijliVitranNigam, ScrapBSESDelhi, ScrapSpancoNagpur, ScrapMahaVitran, ScrapBestMumbai, ScrapWBSEDCL, ScrapTANGEDCO

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

@app.route('/SpancoNagpur', methods=['GET','POST'])
def SpancoDelhi():
    cust_no=request.args.get('cust_no', None)
    return ScrapSpancoNagpur(cust_no)

@app.route('/BestMumbai', methods=['GET','POST'])
def BestMumbai():
    cust_no=request.args.get('cust_no', None)
    return ScrapBestMumbai(cust_no)

@app.route('/MahaVitran', methods=['GET','POST'])
def MahaVitran():
    cust_no=request.args.get('cust_no', None)
    locality=request.args.get('locality', None)
    return ScrapMahaVitran(cust_no, locality)

@app.route('/WBSEDCL', methods=['GET','POST'])
def WBSEDCL():
    cust_no=request.args.get('cust_no', None)
    return ScrapWBSEDCL(cust_no)

@app.route('/TANGEDCO', methods=['GET','POST'])
def TANGEDCO():
    cust_no=request.args.get('cust_no', None)
    locality=request.args.get('locality', None)
    return ScrapTANGEDCO(cust_no, locality)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

