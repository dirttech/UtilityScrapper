__author__ = 'inderpal'

from bs4 import BeautifulSoup
import mechanize
import cookielib
import csv
import requests
import json

kNo=0
named = ""
address = ""
consumed = 0
billed = 0

def initBrowser():
    br=mechanize.Browser()
    cj=cookielib.LWPCookieJar()

    br.set_handle_robots(False)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_equiv(True)
    br.set_cookiejar(cj)
    return br

def ScrapHaryanaBijliVitranNigam():
    try:
        f = open("C:\Users\inderpal\Desktop\utility list\hbvn_data_csv_old.csv","r")
        reader = csv.reader(f)
        ct = 0
        for row in reader:
            kNo = row[0]
            named = row[1]
            named = named.replace(',', '')
            address = row[2]
            address = address.replace(',', '')
            rower = str(kNo)+","+named+","+address
            ct = ct + 1
            print "Printing: "+str(ct)+" Sequence "+rower
            try:
                r = requests.get('http://localhost:5000/HaryanaBijliVitranNigam?cust_no='+kNo)
                obj = r.json()
                billReadings = obj['BillReadings']
                energyReadings = obj['EnergyReadings']
                biller = billReadings[len(billReadings)-1][1]
                billmonth = billReadings[len(billReadings)-1][0]
                consumer = energyReadings[0][1]
                consumemonth = energyReadings[0][0]
                rower = rower+","+billmonth+","+str(biller)+","+consumemonth+","+str(consumer)+"\n"
                print rower
            except Exception as exp:
                print exp.__str__()
                rower = rower +","+exp.__str__()+"\n"
                pass

            ft = open("C:\Users\inderpal\Desktop\utility list\hbvn_data_csv_new.csv","a")
            ft.write(rower)
            ft.close()

        f.close()

    except Exception as e:
        print e.__str__()
        pass

if __name__ == '__main__':
    ScrapHaryanaBijliVitranNigam()