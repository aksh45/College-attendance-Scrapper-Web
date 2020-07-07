from django.shortcuts import render
from math import ceil
import requests
from bs4 import BeautifulSoup as bs
from django.views.decorators.csrf import csrf_protect
def button(request):
    return render(request,'home.html',{'val':''})
@csrf_protect
def output(request):
    uname =  request.POST['uname']
    password = request.POST['psw']
    with requests.Session() as s:
        r = s.get('https://guru.gndec.ac.in/login/index.php',verify=False)
        soup = bs(r.content,features="html.parser")
        filtered = soup.find_all("input")
        payload = {'logintoken':filtered[2]['value'],'username':uname,'password':password}
        login = s.post('https://guru.gndec.ac.in/login/index.php',data = payload,verify=False)
        disp_page =  bs(login.content,features="html.parser")
        drop_down = disp_page.find("ul", {"id": "dropdownmain-navigation0"})
        subject_selected = s.get(drop_down.find('li').find('a')['href'],verify=False)
        subject_page = bs(subject_selected.content,features="html.parser")
        teacher_select1 = subject_page.find('ul',{"class": "section img-text"})
        teacher_select2 = teacher_select1.find('li',{'class':'activity attendance modtype_attendance'})
        attendance_link = teacher_select2.find('a',{'class':''})['href']
        attendance = s.get(attendance_link,verify=False)
        attendance_content = bs(attendance.content,features="html.parser")
        allcourses_search = attendance_content.find('ul',{"class": "nav nav-tabs mb-3"})
        allcourses_search1 = list(allcourses_search)[1]
        allattendance_link = allcourses_search1.find('a',{"class": "nav-link"})['href']
        attendance_all = s.get(allattendance_link,verify=False)
        display_attendance = bs(attendance_all.content,features="html.parser")
        filtered1 = display_attendance.find_all("tr",class_ = "")
    l = []
    c = 0
    count = 1
    for x in filtered1:
        if c != 0:
            tmp = x.text.splitlines()
            if tmp[4] != '0 / 0':
                percentge = tmp[5][0:len(tmp[5])-1]
                l += [[tmp[1],tmp[2],tmp[4],float(percentge)]]
                count += 1
        c += 1
    l.sort(key = lambda x:x[2],reverse = True)
    l = [['subject name','teacher or batch','Attendance','percentage','lectures need to achieve 75']]+l
    for x in range(1,count):
        given_lectures,total_lectures = map(int,l[x][2].split(" / "))
        percentage = l[x][3]
        if percentage<75:
            bunks = int(ceil((given_lectures-0.75*total_lectures)/0.25))*-1
        else:    
            bunks = int((given_lectures-0.75*total_lectures)//0.75)*-1
        l[x] += [bunks]
    data = l
    return render(request,'display.html',{'data':data})
