
# 필요한 라이브러리를 가져옵니다.
import requests  # HTTP 요청을 보내기 위한 라이브러리
from bs4 import BeautifulSoup  # HTML을 파싱하기 위한 라이브러리
import pandas as pd  # 데이터 조작 및 CSV 파일 저장을 위한 라이브러리
from loguru import logger  # 로깅을 위한 라이브러리

def main():
    """
    Yes24의 도서 정보를 스크래핑하여 CSV 파일로 저장하는 메인 함수입니다.
    """
    # --- 스크래핑 설정 ---
    # 데이터를 가져올 기본 URL
    base_url = "https://www.yes24.com/product/category/CategoryProductContents"
    # 카테고리 번호 (예: '001001003032'는 'IT > 프로그래밍/언어')
    disp_no = "001001003032"
    # 스크래핑할 페이지 번호
    page = 1
    # 한 페이지에 보여줄 상품 수
    size = 24

    # --- HTTP 요청 헤더 ---
    # 웹서버에 요청을 보낼 때 실제 브라우저처럼 보이게 하기 위한 정보
    headers = {
        "host": "www.yes24.com",
        "referer": f"https://www.yes24.com/product/category/display/{disp_no}",
        "sec-ch-ua": '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
        "viewport-width": "1055",
        "x-requested-with": "XMLHttpRequest",
    }

    # --- HTTP 요청 파라미터 ---
    # URL에 추가될 쿼리 파라미터들
    params = {
        "dispNo": disp_no,
        "order": "SINDEX_ONLY",  # 판매지수순으로 정렬
        "addOptionTp": "0",
        "page": page,
        "size": size,
        "statGbYn": "N",
        "viewMode": "",
        "_options": "",
        "directDelvYn": "",
        "usedTp": "0",
        "elemNo": "0",
        "elemSeq": "0",
        "seriesNumber": "0",
    }

    try:
        # --- 데이터 요청 및 파싱 ---
        logger.info(f"스크래핑 시작: {base_url} (카테고리: {disp_no}, 페이지: {page})")
        # 설정된 URL, 헤더, 파라미터를 사용하여 GET 요청을 보냅니다.
        response = requests.get(base_url, headers=headers, params=params)
        # HTTP 요청이 실패하면 예외를 발생시킵니다.
        response.raise_for_status()

        # BeautifulSoup을 사용하여 응답받은 HTML 텍스트를 파싱합니다.
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 'itemUnit' 클래스를 가진 모든 'div' 요소를 찾아 리스트로 만듭니다. (개별 도서 정보)
        book_items = soup.find_all("div", class_="itemUnit")
        logger.info(f"{len(book_items)}개의 도서 정보를 찾았습니다.")

        # --- 데이터 추출 ---
        # 추출한 데이터를 저장할 리스트를 초기화합니다.
        books_data = []
        # 각 도서 아이템을 순회하며 정보를 추출합니다.
        for item in book_items:
            # 책 제목 추출
            title_tag = item.find("a", class_="gd_name")
            title = title_tag.text if title_tag else "N/A"

            # 저자 추출
            author_tag = item.find("span", class_="authPub info_auth")
            # 저자 정보가 있는 경우, 양쪽 공백을 제거하고 텍스트만 가져옵니다.
            author = author_tag.text.strip() if author_tag else "N/A"

            # 출판사 추출
            publisher_tag = item.find("span", class_="authPub info_pub")
            publisher = publisher_tag.text.strip() if publisher_tag else "N/A"
            
            # 출판일 추출
            date_tag = item.find("span", class_="authPub info_date")
            publication_date = date_tag.text.strip() if date_tag else "N/A"

            # 가격 추출
            price_tag = item.find("em", class_="yes_b")
            # 가격 정보가 있는 경우, 쉼표(,)를 제거하고 텍스트만 가져옵니다.
            price = price_tag.text.replace(",", "") if price_tag else "0"

            # 추출된 정보를 딕셔너리 형태로 리스트에 추가합니다.
            books_data.append({
                "title": title,
                "author": author,
                "publisher": publisher,
                "publication_date": publication_date,
                "price": int(price),  # 가격은 정수형으로 변환
            })

        # --- 데이터 저장 ---
        # 추출한 데이터를 바탕으로 pandas DataFrame을 생성합니다.
        df = pd.DataFrame(books_data)
        # 저장할 파일 경로를 지정합니다.
        output_path = f"yes24/data/yes24_books_{disp_no}_p{page}.csv"
        # DataFrame을 CSV 파일로 저장합니다. (인코딩: utf-8-sig로 한글 깨짐 방지)
        df.to_csv(output_path, index=False, encoding="utf-8-sig")
        logger.info(f"데이터 저장 완료: {output_path}")

    # --- 예외 처리 ---
    except requests.exceptions.RequestException as e:
        # HTTP 요청 관련 오류 발생 시 로그를 남깁니다.
        logger.error(f"HTTP 요청 오류: {e}")
    except Exception as e:
        # 그 외 모든 오류 발생 시 로그를 남깁니다.
        logger.error(f"오류 발생: {e}")

# 이 스크립트가 직접 실행될 때만 아래 코드를 실행합니다.
if __name__ == "__main__":
    # 로그 파일 설정을 추가합니다. 500MB마다 새 파일이 생성됩니다.
    logger.add("yes24/data/scraping_{time}.log", rotation="500 MB")
    # main 함수를 호출하여 스크래핑을 시작합니다.
    main()
