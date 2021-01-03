from urllib.request import urlopen
from urllib.request import urlretrieve
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import numpy as np
import cv2

def folder(folder):
    try:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print('폴더를 생성하였습니다. '+folder)
    except OSError:
        print('이미 있는 같은 이름의 폴더가 존재합니다.' + folder)
#다운받을 이미지를 저장할 폴더를 생성

search = input('검색하고 싶은것을 입력하세요 ')
file_name = input("저장할 파일의 이름을 영어로 입력해주세요 ")
folder('image/data/'+file_name)
url = 'https://www.google.com/search?q=' + quote_plus(search) + '&source=lnms&tbm=isch'
driver = webdriver.Chrome("chromedriver.exe")
#검색어를 입력받고 chrome드라이버에 연결

driver.get(url)
#chrome드라이버로 url을 연결하여 오픈함

for i in range(500):
    driver.execute_script("window.scrollBy(0,10000)")
# 자동으로 스크롤을 내리면서 이미지를 계속 가져옴

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
img = soup.select('.rg_i.Q4LuWd')
# .rg_i.Q4LuWd은 구글 이미지검색에서 이미지만 해당하는 코드
n = 1
imgurl = []

for i in img:
    try:
        imgurl.append(i.attrs["src"])
    except KeyError:
        imgurl.append(i.attrs["data-src"])
# imgurl이라는 list에 이미지 주소를 저장

for i in imgurl:
        urlretrieve(i, "image/data/" + file_name + "/" + file_name + str(n) + ".jpg")
        print('downloading.........',n)
        n += 1
print(n)
driver.close()
#이미지를 다운받는것을 보여주기위한 for문과 이미지 다운로드가 완료되면 검색창을 닫음

for i in range(1,n):
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    main_img = cv2.imread("image/"+file_name + "/" + file_name + str(i) +".jpg")
    gray = cv2.cvtColor(main_img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.05, 5)
    for (x,y,row,col) in faces:
        img = cv2.rectangle(main_img,(x,y),(x+row,y+col),(255,0,0),2)
        roi_gray = gray[y:y+col, x:x+row]
        roi_color = img[y:y+col, x:x+row]
        face_img = img[y:y+col, x:x+row]
        cv2.imwrite("image/" + file_name + "/" + file_name + str(i) + '!' +".jpg" ,face_img)
#다운받은 이미지를 opencv에서 제공하는 haarcascade_frontalface라는 파일로 얼굴만을 추출하여 저장

cv2.waitKey(0)
cv2.destroyAllWindows()