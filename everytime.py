from selenium import webdriver
import time
import pandas as pd
import sys

data=pd.DataFrame()
r= 5
driver=webdriver.Chrome('./chromedriver.exe')#path설정
driver.maximize_window()
time.sleep(r)

year=2022 #년도
hacgi=1 #학기
id='아이디'
psw='비밀번호'
#로그인
driver.get('https://everytime.kr/timetable/{year}/{hacgi}'.format(year=year,hacgi=hacgi))
driver.find_element_by_name('userid').send_keys(id)
driver.find_element_by_name('password').send_keys(psw)
driver.find_element_by_xpath('//*[@class="submit"]/input').click()
time.sleep(r)




driver.find_element_by_xpath('//*[@id="container"]/ul/li[1]').click() #시간표
time.sleep(r)

#학기 선택

#스크롤 끝까지 내리기
while True:
    before_e = driver.find_elements_by_css_selector('table > tbody > tr')[-1]
    driver.execute_script("arguments[0].scrollIntoView(true);", before_e)
    time.sleep(4)
    after_e =driver.find_elements_by_css_selector('table > tbody > tr')[-1]
    if before_e==after_e:
        break

num=len(driver.find_elements_by_css_selector('table > tbody > tr')) #강의수(반복수)
time.sleep(r)
for n in range(1,num+1):
    lecture_code=driver.find_element_by_xpath('//*[@id="subjects"]/div[2]/table/tbody/tr[{n}]/td[2]'.format(n=n)).text #과목코드
    classification=driver.find_element_by_xpath('//*[@id="subjects"]/div[2]/table/tbody/tr[{n}]/td[1]'.format(n=n)).text #구분(교필)
    lecture_name=driver.find_element_by_xpath('//*[@id="subjects"]/div[2]/table/tbody/tr[{n}]/td[3]'.format(n=n)).text #과목이름
    professor_name=driver.find_element_by_xpath('//*[@id="subjects"]/div[2]/table/tbody/tr[{n}]/td[4]'.format(n=n)).text #교수이름
    credit=driver.find_element_by_xpath('//*[@id="subjects"]/div[2]/table/tbody/tr[{n}]/td[5]'.format(n=n)).text #학점
    avg_score=driver.find_element_by_xpath('//*[@id="subjects"]/div[2]/table/tbody/tr[{n}]/td[7]/a'.format(n=n)).get_attribute('title') #평점
    print(lecture_code,classification,lecture_name,professor_name,credit,avg_score)

    url=driver.find_element_by_xpath('//*[@id="subjects"]/div[2]/table/tbody/tr[{n}]/td[7]/a'.format(n=n)).get_attribute('href') #tr[i]
    driver.get(str(url))
    time.sleep(r)


    #driver.switch_to.window(driver.window_handles[1])
    #time.sleep(8)

    lecture_review=driver.find_elements_by_css_selector('div.articles > article > p.text') #강의평
    semester=driver.find_elements_by_css_selector('div.articles > article > p.info > span.semester') #강의평 작성 학기
    score=driver.find_elements_by_css_selector('p.rate > span.star > span.on') #별점

    #추천수 속도 너무 느림
    # recommands=[]
    # for r in range(1,len(lecture_review)+1):
    #     try:
    #         recommand=driver.find_element_by_xpath('//*[@id="container"]/div[4]/div[2]/article[{n}]/p[2]/span[2]'.format(n=r)).text
    #         recommands.append(int(recommand))
    #     except:
    #         recommands.append(0)

    print(len(lecture_review),len(semester),len(score))


    time.sleep(r)
    lecture_reviews=[]
    semesters=[]
    scores=[]
    for i in lecture_review:
        lecture_reviews.append(i.text)
    for j in semester:
        semesters.append(j.text.replace(' 수강자',''))
    for k in score:
        x=float(k.get_attribute('style').replace('width: ','').replace('%;',''))/20
        scores.append(x)

    #print(lecture_reviews)
    #print(semesters)

    dic={}
    dic['lecture_code']=[lecture_code]*len(lecture_review)
    dic['classification']=[classification]*len(lecture_review)
    dic['lecture_name']=[lecture_name]*len(lecture_review)
    dic['professor_name']=[professor_name]*len(lecture_review)
    dic['credit']=[int(credit)]*len(lecture_review)
    dic['score']=scores
    dic['avg_score']=[float(avg_score)]*len(lecture_review)
    dic['semester']=semesters
    dic['lecture_review']=lecture_reviews
    data=data.append(pd.DataFrame(data=dic), ignore_index=True)

    time.sleep(r)
    #driver.close()
    #driver.switch_to.window(driver.window_handles[0])
    driver.back()
    time.sleep(r)

data.to_csv('{year}-{hacgi}.csv'.format(year=year,hacgi=hacgi),encoding='utf-8-sig',index=False)
driver.quit()