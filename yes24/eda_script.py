
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import koreanize_matplotlib
import re
from loguru import logger

# 로거 설정
logger.add("yes24/log/eda.log", rotation="500 MB")

@logger.catch
def main():
    """
    YES24 AI 도서 데이터 분석 및 시각화
    """
    # 1. 데이터 불러오기
    try:
        df = pd.read_csv("yes24/data/yes24_ai.csv")
        logger.info("데이터 불러오기 성공")
    except FileNotFoundError:
        logger.error("CSV 파일을 찾을 수 없습니다.")
        return

    # 2. 데이터 전처리
    logger.info("데이터 전처리 시작")
    # 'price'를 숫자형으로 변환
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df.dropna(subset=['price'], inplace=True)
    df['price'] = df['price'].astype(int)

    # 'publication_date'에서 '년'과 '월' 분리
    df['year'] = df['publication_date'].apply(lambda x: int(re.search(r'(\d{4})년', str(x)).group(1)) if re.search(r'(\d{4})년', str(x)) else None)
    df['month'] = df['publication_date'].apply(lambda x: int(re.search(r'(\d{1,2})월', str(x)).group(1)) if re.search(r'(\d{1,2})월', str(x)) else None)
    
    # 'author'에서 '저' 제거 및 첫번째 저자만 선택
    df['author_main'] = df['author'].apply(lambda x: str(x).split(',')[0].replace(' 저', '').strip())
    logger.info("데이터 전처리 완료")

    # 3. 데이터 분석 및 시각화
    logger.info("데이터 분석 및 시각화 시작")

    # --- 가격 분포 ---
    plt.figure(figsize=(10, 6))
    sns.histplot(df['price'], kde=True)
    plt.title('가격 분포')
    plt.xlabel('가격')
    plt.ylabel('빈도')
    price_dist_path = 'yes24/data/price_distribution.png'
    plt.savefig(price_dist_path)
    plt.close()
    logger.info(f"가격 분포도 저장 완료: {price_dist_path}")

    # --- 출판사별 출간 도서 수 ---
    plt.figure(figsize=(12, 8))
    publisher_counts = df['publisher'].value_counts().sort_values(ascending=False)
    sns.barplot(x=publisher_counts.values, y=publisher_counts.index, palette='viridis')
    plt.title('출판사별 출간 도서 수')
    plt.xlabel('도서 수')
    plt.ylabel('출판사')
    publisher_books_path = 'yes24/data/publisher_books.png'
    plt.savefig(publisher_books_path, bbox_inches='tight')
    plt.close()
    logger.info(f"출판사별 출간 도서 수 그래프 저장 완료: {publisher_books_path}")
    
    # --- 워드 클라우드 ---
    text = " ".join(title for title in df.title)
    wordcloud = WordCloud(
        font_path='c:/Windows/Fonts/malgun.ttf',
        width=800,
        height=400,
        background_color='white'
    ).generate(text)

    plt.figure(figsize=(15, 7))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    wordcloud_path = 'yes24/data/title_wordcloud.png'
    plt.savefig(wordcloud_path)
    plt.close()
    logger.info(f"워드 클라우드 이미지 저장 완료: {wordcloud_path}")
    
    logger.info("데이터 분석 및 시각화 완료")
    print("데이터 분석 및 시각화가 완료되었습니다. 'yes24/data' 디렉토리에서 생성된 이미지 파일을 확인하세요.")


if __name__ == '__main__':
    main()
