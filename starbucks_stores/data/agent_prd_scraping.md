## 스타벅스 매장정보 수집
https://www.starbucks.co.kr/store/store_map.do

## 네트워크 메뉴를 통해 실제 데이터를 가져오는 URL

Request URL
https://www.starbucks.co.kr/store/getStore.do?r=S9WAEUEA84
Request Method
POST




## 해당 Request에 대한 Header 정보
host
www.starbucks.co.kr
origin
https://www.starbucks.co.kr
referer
https://www.starbucks.co.kr/store/store_map.do
sec-ch-ua
"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"
sec-ch-ua-mobile
?0
sec-ch-ua-platform
"Windows"
sec-fetch-dest
empty
sec-fetch-mode
cors
sec-fetch-site
same-origin
user-agent
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36
x-requested-with
XMLHttpRequest


## Payload

in_biz_cds=0&in_scodes=0&ins_lat=35.30964382125532&ins_lng=128.73521467010917&search_text=&p_sido_cd=01&p_gugun_cd=&isError=true&in_distance=0&in_biz_cd=&iend=1000&searchType=C&set_date=&rndCod=PQVECKB5P2&todayPop=0&all_store=0&T03=0&T01=0&T27=0&T12=0&T09=0&T30=0&T05=0&T22=0&T21=0&T36=0&T43=0&Z9999=0&T64=0&T66=0&P02=0&P10=0&P50=0&P20=0&P60=0&P30=0&P70=0&P40=0&P80=0&whcroad_yn=0&P90=0&P01=0&new_bool=0




## 응답 예시 (JSON 의 일부 정보)
{
    "list": [
        {

"list"하위의 모든 정보 수집하기

## 수집 내역
p_sido_cd=01 부터 17까지 전국 스타벅스 매장 정보를 수집하는 파이썬 코드를 starbucks_stores/starbucks_scraper.py작성할 것 
중간에 수집되는 내역을 확인할 수 있게 로그를 남길 것
수집한 내용을 현재 폴더 하위에 있는 data에 저장하고 파일명은 starbucks_stores/data/starbucks_ai.csv로 저장할 것 
