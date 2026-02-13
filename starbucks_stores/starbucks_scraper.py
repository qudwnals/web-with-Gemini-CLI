
import requests
import pandas as pd
from loguru import logger
import os

# --- 설정 ---
LOG_DIR = "starbucks_stores/log"
DATA_DIR = "starbucks_stores/data"
OUTPUT_CSV_PATH = os.path.join(DATA_DIR, "starbucks_ai.csv")
URL = "https://www.starbucks.co.kr/store/getStore.do"

# --- 디렉토리 생성 ---
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

# --- 로거 설정 ---
logger.add(os.path.join(LOG_DIR, "scraping_{time}.log"), rotation="10 MB")

# --- 스크레이핑 함수 ---
@logger.catch
def scrape_starbucks():
    """전국 스타벅스 매장 정보를 스크레이핑합니다."""
    
    headers = {
        "host": "www.starbucks.co.kr",
        "origin": "https://www.starbucks.co.kr",
        "referer": "https://www.starbucks.co.kr/store/store_map.do",
        "sec-ch-ua": '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
    }

    all_stores = []
    
    # p_sido_cd=01 부터 17까지 반복
    sido_codes = [f"{i:02d}" for i in range(1, 18)]

    logger.info("스타벅스 매장 정보 수집을 시작합니다.")

    for sido_code in sido_codes:
        payload = {
            "in_biz_cds": "0",
            "in_scodes": "0",
            "ins_lat": "37.56682",  # Default latitude (e.g., Seoul)
            "ins_lng": "126.97865",  # Default longitude (e.g., Seoul)
            "search_text": "",
            "p_sido_cd": sido_code,
            "p_gugun_cd": "",
            "isError": "true",
            "in_distance": "0",
            "in_biz_cd": "",
            "iend": "1000",
            "searchType": "C",
            "set_date": "",
            "rndCod": "PQVECKB5P2", # This might need to be dynamic, but let's try with a fixed one first
            "all_store": "0"
        }
        
        try:
            logger.info(f"시/도 코드 '{sido_code}'의 매장 정보를 요청합니다.")
            response = requests.post(URL, headers=headers, data=payload, timeout=30)
            response.raise_for_status()  # HTTP 오류가 발생하면 예외를 발생시킴

            data = response.json()
            stores = data.get("list", [])
            
            if stores:
                logger.success(f"시/도 코드 '{sido_code}': {len(stores)}개 매장 정보를 수집했습니다.")
                all_stores.extend(stores)
            else:
                logger.warning(f"시/도 코드 '{sido_code}': 매장 정보가 없습니다.")

        except requests.exceptions.RequestException as e:
            logger.error(f"시/도 코드 '{sido_code}' 요청 중 오류 발생: {e}")
        except ValueError: # JSONDecodeError is a subclass of ValueError
            logger.error(f"시/ado 코드 '{sido_code}'의 응답을 파싱하는 중 오류 발생 (JSON 형식 오류).")

    if not all_stores:
        logger.error("수집된 매장 정보가 없습니다. 스크레이핑을 종료합니다.")
        return

    # --- 데이터프레임 변환 및 저장 ---
    df = pd.DataFrame(all_stores)
    logger.info(f"총 {len(df)}개의 매장 정보를 데이터프레임으로 변환했습니다.")
    
    try:
        df.to_csv(OUTPUT_CSV_PATH, index=False, encoding='utf-8-sig')
        logger.success(f"데이터를 성공적으로 '{OUTPUT_CSV_PATH}' 파일에 저장했습니다.")
    except IOError as e:
        logger.error(f"파일 저장 중 오류 발생: {e}")

if __name__ == "__main__":
    scrape_starbucks()
