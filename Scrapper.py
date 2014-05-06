__author__ = 'inderpal'

import urllib2
from bs4 import BeautifulSoup
import mechanize
import cookielib
import json
import sys


Name = ""
City = ""
LoadSanctioned = ""
LoadType = ""
PlaceType = ""
LoadConnected = ""
Address=""
District=""
Circle=""
BillCategory=""

def initBrowser():
    br=mechanize.Browser()
    cj=cookielib.LWPCookieJar()

    br.set_handle_robots(False)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_equiv(True)
    br.set_cookiejar(cj)
    return br

def ScrapBSESDelhi(customerNo):
    try:
        br = initBrowser()
        br.open('http://www.bsesdelhi.com/bsesdelhi/caVerification4Pay.do')
        br.select_form(name='askForNumberBean')
        br['txtCA_Number'] = customerNo

        resp=br.submit()

        soup = BeautifulSoup(br.response().read())
        Name = soup.find("div", {"class": "txtCen"}).next.next.string
        Address = soup.find("div", {"class": "tc2 fleft"}).next.next.next.next.next.string
        elements = soup.find_all("div", {"class": "tc4 fleft"})

        LoadSanctioned = elements[3].string
        District = elements[13].string
        PlaceType = elements[15].string
        Circle = elements[9].string

        td = soup.find_all("td")
        BillReadings=[[0,0]]
        BillReadings[0][0] = td[19].string
        BillReadings[0][1] = float(td[28].string.replace(',', ''))

        br.open('http://www.bsesdelhi.com/bsesdelhi/billHistory.do?caNumber=000'+customerNo)
        soup=BeautifulSoup(br.response().read())
        td=soup.find_all("td")
        for i in range(2, 7, 1):
            temp = td[7*i].string
            val = float(td[7*i+3].string.replace(',', ''))
            BillReadings.append([temp,val])

        obj = {u"BillReadings": BillReadings, u"Name": Name[2:], u"Address": Address[2:], u"Sanctioned Load": LoadSanctioned, u"District": District, u"Circle": Circle, u"Place Type": PlaceType}
        json_obj=json.dumps(obj)
        br.close()
        return json_obj
    except Exception as e:
        return "error"
        pass

def ScrapHaryanaBijliVitranNigam(customerNo):
    try:
        br = initBrowser()
        br.open('http://202.56.120.172/elpsoftmis/WebPages/ConsumerInfoStart.aspx')
        br.select_form(name='form1')
        br['txtKNo'] = customerNo

        resp=br.submit()

        br.open('http://202.56.120.172/elpsoftmis/WebPages/ViewConsumerInfo.aspx')
        soup = BeautifulSoup(br.response().read())

        Name = soup.find("span", {"id": "lblName"}).string
        City = soup.find("span", {"id": "lblCity"}).string
        LoadSanctioned = soup.find("span", {"id": "lblLoadSanctioned"}).string
        LoadType = soup.find("span", {"id": "lblLoadtype"}).string
        PlaceType = soup.find("span", {"id": "lblBusinessName"}).string
        LoadConnected = soup.find("span", {"id": "lblLoadConnected"}).string
        BillCategory = soup.find("span", {"id": "lblCategory"}).string

        br.open('http://202.56.120.172/elpsoftmis/WebPages/ConsumerDetails.aspx?value=3')
        br.open('http://202.56.120.172/elpsoftmis/WebPages/BillingInformation.aspx')

        soup = BeautifulSoup(br.response().read())

        table = soup.find("table", {"style": "border-width:0px;width:749px;border-collapse:collapse;"})
        tr = table.find_all("tr")
        ct=0
        EnergyReadings = [[0,0]]
        for rows in tr:
            td = rows.find_all("td")
            if(ct == 9):
                EnergyReadings[0][0] = td[0].text+" "+td[3].text
                EnergyReadings[0][1] = float(td[21].text.replace(',', ''))

            if(ct > 1):
                try:
                    val = float(td[24].text.replace(',', ''))
                    EnergyReadings.append([td[3].text+" "+td[6].text, val])
                except:
                    pass
            ct = ct + 1

        br.open('http://202.56.120.172/elpsoftmis/WebPages/ConsumerDetails.aspx?value=4')
        br.open('http://202.56.120.172/elpsoftmis/WebPages/BillingInformation.aspx')

        soup = BeautifulSoup(br.response().read())

        table = soup.find("table", {"style": "border-width:0px;width:749px;border-collapse:collapse;"})
        tr = table.find_all("tr")
        ct=0
        BillReadings = [[0,0]]
        for rows in tr:
            td = rows.find_all("td")
            if(ct == 7):
                try:
                    BillReadings[0][0] = td[6].text
                    BillReadings[0][1] = float(td[12].text)
                except:
                    pass

            if(ct > 7):
                try:
                    BillReadings.append([td[6].text, float(td[12].text)])
                except:
                    pass
            ct = ct + 1

        obj = {u"EnergyReadings": EnergyReadings, u"BillReadings": BillReadings, u"Name": Name, u"Load Sanctioned": LoadSanctioned, u"Load Type": LoadType, u"BillCategory": BillCategory, u"PlaceType": PlaceType, u"City": City, u"Load Connected": LoadConnected}
        json_obj = json.dumps(obj)
        br.close()
        return json_obj
    except Exception as e:
        return "error"
        pass
