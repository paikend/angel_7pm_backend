# 제 3회 엔젤톤 해커톤 - 오후 7시 팀

7Hacks - 누구나 쉽게 즐길 수 있는 해커톤 플랫폼! 

***

> ## API 문서
- http://127.0.0.1:8000/redocs/
- http://127.0.0.1:8000/swagger/
> ## 개발 환경
- python 3.6.8 (https://www.python.org/downloads/release/python-368/)
- Redis server 5.0.5     


> ## 가상환경 생성
    $ python3.6 -m venv venv  

> ## 가상환경 활성화
 ### Linux & MAC
    $ source venv/bin/activate  
 ### Windows
    $ source venv\Scripts\activate.bat  

> ## packages 설치
    (venv) $ pip install -r requirements.txt  


> ## 데이터 베이스 migration 
    (venv) $ python manage.py migrate  


> ## Django(WAS) 실행  
    (venv) $ python manage.py runserver  


> ## Celery 실행
    (venv) $ celery worker -A config -P --loglevel=INFO  


> ## Celery beat 실행 
    (venv) $ celery beat -A config  --loglevel=INFO  

