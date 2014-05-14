__author__ = 'inderpal'

import urllib2
from bs4 import BeautifulSoup
import mechanize
import cookielib
import json
import datetime
import requests
import sys

now = datetime.datetime.now()
day = now.day
month = now.month
year = now.year

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

def ScrapSpancoNagpur(customerNo):
    try:
        br = initBrowser()

        br.open('http://customercare.sndl.in/view_bill.aspx')
        br.select_form(name='aspnetForm')
        br['ctl00$cph$txtServiceNo'] = customerNo

        resp=br.submit()

        soup = BeautifulSoup(br.response().read())

        tab = soup.find("table", {"id": "ctl00_cph_grdv_Bill_history"})
        tr = tab.find_all("tr")
        #print tr
        EnergyReadings=[[0,0]]
        ct=0
        for rows in tr:
            #print rows
            td = rows.find_all("td")
            if(ct == 1):
                try:
                    EnergyReadings[0][0] = td[0].text
                    EnergyReadings[0][1] = float(td[1].text)
                except:
                    pass

            if(ct > 1):
                try:
                    EnergyReadings.append([td[0].text, float(td[1].text)])
                except:
                    pass
            ct = ct + 1

        br.open("http://customercare.sndl.in/frm_bill_print.aspx?serv_no="+customerNo+"&billmonth=Apr-2014")
        soup = BeautifulSoup(br.response().read())
        #print soup

        Name = soup.find("span", {"id": "lbl_name"}).string
        Address = soup.find("span", {"id": "lbl_address"}).string
        LoadSanctioned = soup.find("span", {"id": "lbl_sancLoad"}).string
        PlaceType = soup.find("span", {"id": "lbl_category"}).string

        obj = {u"BillReadings": EnergyReadings, u"Name": Name, u"Address": Address, u"Sanctioned Load": LoadSanctioned, u"Place Type": PlaceType}
        json_obj=json.dumps(obj)
        br.close()
        return json_obj
    except Exception as e:
        return "error"
        pass

def ScrapBestMumbai(customerNo):
    try:
        br = initBrowser()

        br.open('https://www.bestundertaking.net/CUSTOMERBillInfo.aspx')
        br.select_form(name='aspnetForm')
        br['ctl00$Contentplaceholder2$ctl02$txtAccno'] = customerNo

        resp = br.submit()

        print br.response().read()
        br.open('https://www.bestundertaking.net/CUSTOMERPaymentInfo.aspx')

        soup = BeautifulSoup(br.response().read())

        tab = soup.find("table", {"id": "ctl00_Contentplaceholder2_gvPaymentDetails"})
        tr = tab.find_all("tr")
        #print tr
        BillReadings=[[0,0]]
        ct=0
        for rows in tr:
            #print rows
            td = rows.find_all("td")
            if(ct == 1):
                try:
                    BillReadings[0][0] = td[0].text
                    BillReadings[0][1] = float(td[1].text)
                except:
                    pass

            if(ct > 1):
                try:
                    BillReadings.append([td[0].text, float(td[1].text)])
                except:
                    pass
            ct = ct + 1

        #br.open("http://customercare.sndl.in/frm_bill_print.aspx?serv_no="+customerNo+"&billmonth=Apr-2014")
        #soup = BeautifulSoup(br.response().read())
        #print soup

        #Name = soup.find("span", {"id": "lbl_name"}).string
        #Address = soup.find("span", {"id": "lbl_address"}).string
        #LoadSanctioned = soup.find("span", {"id": "lbl_sancLoad"}).string
        #PlaceType = soup.find("span", {"id": "lbl_category"}).string

        obj = {u"BillReadings": BillReadings, u"Name": Name, u"Address": Address, u"Sanctioned Load": LoadSanctioned, u"Place Type": PlaceType}
        json_obj=json.dumps(obj)
        br.close()
        return json_obj
    except Exception as e:
        print e.__str__()
        return "error"
        pass

def ScrapMahaVitran(customerNo, locality):
    try:
        br = initBrowser()

        br.open('http://wss.mahadiscom.in/wss/wss?uiActionName=getViewPayBill')

        br.select_form(name='viewPayBillForm')
        payload = {'ConsumerNo': customerNo, 'BuNumber': locality}

        r = requests.post('http://wss.mahadiscom.in/wss/wss?uiActionName=postViewPayBill&IsAjax=true', payload)
        print r.text

        soup = BeautifulSoup(br.response().read())
        print br.response().read()
        tab = soup.find("table", {"id": "ctl00_cph_grdv_Bill_history"})
        tr = tab.find_all("tr")
        #print tr
        BillReadings=[[0,0]]
        ct=0
        for rows in tr:
            #print rows
            td = rows.find_all("td")
            if(ct == 1):
                try:
                    BillReadings[0][0] = td[0].text
                    BillReadings[0][1] = float(td[1].text)
                except:
                    pass

            if(ct > 1):
                try:
                    BillReadings.append([td[0].text, float(td[1].text)])
                except:
                    pass
            ct = ct + 1

        br.open("http://customercare.sndl.in/frm_bill_print.aspx?serv_no="+customerNo+"&billmonth=Apr-2014")
        soup = BeautifulSoup(br.response().read())
        #print soup

        Name = soup.find("span", {"id": "lbl_name"}).string
        Address = soup.find("span", {"id": "lbl_address"}).string
        LoadSanctioned = soup.find("span", {"id": "lbl_sancLoad"}).string
        PlaceType = soup.find("span", {"id": "lbl_category"}).string

        obj = {u"BillReadings": BillReadings, u"Name": Name, u"Address": Address, u"Sanctioned Load": LoadSanctioned, u"Place Type": PlaceType}
        json_obj=json.dumps(obj)
        br.close()
        return json_obj
    except Exception as e:
        print e.__str__()
        return "error"
        pass

def ScrapWBSEDCL(customerNo):
    try:
        br = initBrowser()
        br.open('http://www.wbsedcl.in/webdynpro/dispatcher/local/LmvBilling_ZCC/LmvBillingApp')
        print br.response().read()
        br.select_form(nr=0)
        br['MDAA.LmvBillingView.consumerIdInputField'] = customerNo

        resp=br.submit()
        print br.response().read()
        soup = BeautifulSoup(br.response().read())
        Name = soup.find("span", {"id": "MDAA.LmvBillingView.consumerName"}).string
        Address = soup.find("span", {"id": "MDAA.LmvBillingView.consumerAddress"}).string


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
        print e.__str__()
        return "error"
        pass

def ScrapTANGEDCO(customerNo, locality):
    try:
        br = initBrowser()
        br.open('https://www.tnebnet.org/awp/account?execution=e1s1')
        br.select_form(name='form')
        br['form:consumerNo'] = customerNo
        control = br.form.find_control("form:firstName")
        for item in control.items:
            if item.name == locality:
                item.selected = True

        resp=br.submit()

        soup = BeautifulSoup(br.response().read())
        tab = soup.find("table", {"class": "billtable"})
        tr = tab.find_all("tr")
        td0 = tr[0].find_all("td")
        Name = td0[1].text

        td2 = tr[2].find_all("td")
        Circle = td2[1].text

        td6 = tr[6].find_all("td")
        Address = td6[1].text

        divv = soup.find("div", {"id": "j_idt31:j_idt233"})
        grid = divv.find("table", {"role": "grid"})
        tds = grid.find_all("td", {"role": "gridcell"})

        BillReadings=[[0,0]]
        BillReadings[0][0] = tds[0].next.next.string
        BillReadings[0][1] = float(tds[8].next.next.string)

        for i in range(1, 6, 1):
            temp = tds[14*i].next.next.string
            val = float(tds[14*i+8].next.next.string)
            BillReadings.append([temp,val])

        obj = {u"BillReadings": BillReadings, u"Name": Name[2:], u"Address": Address[2:], u"Circle": Circle}
        json_obj=json.dumps(obj)
        br.close()
        return json_obj
    except Exception as e:
        print e.__str__()
        return "error"
        pass