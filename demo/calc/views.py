from django.shortcuts import render
from django.http import HttpResponse 
from bs4 import BeautifulSoup
import requests
from PIL import Image
# Create your views here.
def home(request):
    URL="https://www.worldometers.info/coronavirus/#countries"
    r=requests.get(URL)
    data=BeautifulSoup(r.content,'html.parser')
    table = data.find('div', attrs = {'class':'main_table_countries_div'})
    data1 = []
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data1.append([ele for ele in cols if ele])
    heading=[]
    rows = table.find('thead')
    onlyheading=rows.findAll('th')
    countrieslist=[]
    for i in range(8,len(data1)-8):
        countrieslist.append(data1[i][1])
    country={}
    count=0
    country[0]=data1[7][0]
    for i in data1[8:]:
        count+=1
        if i[1].isalpha():
            country[count]=i[1]
    countries=[]
    for i in country.values():
        countries.append(i)
    data1.remove([])
    attributes=['Total_Cases ','New_cases ','Total_Deaths ','New_Deaths ','Total_Recovered ','Active_cases ','Critical_cases ','Population ','Total_tests']
    coun="world"
    for i in data1:
        l2=[]
        if coun.lower()=='world':
            l2.append(data1[7][1])
            l2.append(data1[7][2])
            l2.append(data1[7][3])
            l2.append(data1[7][4])
            l2.append(data1[7][5])
            l2.append(data1[7][7])
            l2.append(data1[7][8])
            l2.append("7,790,863,980")
            l2.append("")
            info=dict(zip(attributes,l2))
            break
    return render(request,'index.html',{'listitems':countrieslist,'Total_Cases':data1[7][1],'New_cases':data1[7][2],'Total_Deaths':data1[7][3],'New_Deaths':data1[7][4],'Total_Recovered':data1[7][5],'Active_cases':data1[7][7],'Critical_cases':data1[7][8],'Population':"7,790,863,980+",'Total_tests':"",'image':'earth.gif'})
def search(request):
    URL="https://www.worldometers.info/coronavirus/#countries"
    r=requests.get(URL)
    data=BeautifulSoup(r.content,'html.parser')
    table = data.find('div', attrs = {'class':'main_table_countries_div'})
    data1 = []
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data1.append([ele for ele in cols]) 
    heading=[]
    rows = table.find('thead')
    onlyheading=rows.findAll('th')
    countrieslist=[]
    for i in range(8,len(data1)-8):
        countrieslist.append(data1[i][1])
    country={}
    count=0
    country[0]=data1[7][0]
    for i in data1[8:]:
        count+=1
        if i[1].isalpha():
            country[count]=i[1]
    countries=[]
    for i in country.values():
        countries.append(i)
    data1.remove([])
    attributes=['Total_Cases','New_cases','Total_Deaths','New_Deaths','Total_Recovered','Active_cases','Critical_cases','Total_tests','Population']
    coun=request.GET['search']
    if len(coun)==2 or len(coun)==3:
        coun=coun.upper()
    else:
        coun=coun.title()
    for i in data1:
        l2=[]
        if i[1].lower()==coun.lower():
            l2.append(i[2])
            l2.append(i[3])
            l2.append(i[4])
            l2.append(i[5])
            l2.append(i[6])
            l2.append(i[8])
            l2.append(i[9])
            l2.append(i[12])
            l2.append(i[14])
            if i[1]=='usa' or i[1]=='USA':
                countryflag='united-states'
            else:
                countryflag=i[1]
            info=dict(zip(attributes,l2))
            URL1="https://www.countryflags.com/en/"+countryflag+"-flag-image.html"
            r1=requests.get(URL1)
            flag=BeautifulSoup(r1.content,'html.parser')
            flag1 = flag.findAll('img', attrs = {'class':'img-responsive'})
            link='https:'+flag1[2]['src']
            '''page=requests.get(link,stream=True)
            if page.status_code==200:
                img_path='..\static\assets\img\{}.jpg'.format(countryflag)
                fp=open(img_path,'wb')
                for chunk in page:
                    fp.write(chunk)
                fp.close()
            image=countryflag+".jpg"'''
    return render(request,'results.html',{'listitems':countrieslist[1:],'Total_Cases':info.get('Total_Cases'),'New_cases':info['New_cases'],'Total_Deaths':info['Total_Deaths'],'New_Deaths':info['New_Deaths'],'Total_Recovered':info['Total_Recovered'],'Active_cases':info['Active_cases'],'Critical_cases':info['Critical_cases'],'Population':info['Population'],'Total_tests':info['Total_tests'],'image':link})
