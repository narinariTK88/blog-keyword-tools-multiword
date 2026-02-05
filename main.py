import requests
import time
import pandas as pd
import os
from datetime import datetime

def get_google_suggestions(keyword):
    url = "http://www.google.com/complete/search"
    params = {"client": "firefox", "hl": "ja", "q": keyword}
    try:
        response = requests.get(url, params=params, timeout=10)
        return response.json()[1]
    except Exception as e:
        print(f"Error fetching {keyword}: {e}")
        return []

def run():
    input_file = "keywords.txt"
    if not os.path.exists(input_file): return

    with open(input_file, "r", encoding="utf-8") as f:
        base_keywords = [line.strip() for line in f if line.strip()]

    chars = [chr(i) for i in range(ord('ぁ'), ord('ん')+1)] + \
            [chr(i) for i in range(ord('a'), ord('z')+1)] + \
            [str(i) for i in range(10)]

    # フィルタリングしたいインテント修飾語
    treasure_words = [
        "おすすめ", "比較", "やり方", "始め方", "初心者", "レビュー", 
        "とは", "理由", "仕組み", "作り方", "最安値", "ランキング", "選び方", "違い"
    ]

    for base in base_keywords:
        print(f"--- 調査中: {base} ---")
        results = []
        seen = set()
        
        for char in chars:
            query = f"{base} {char}"
            suggestions = get_google_suggestions(query)
            for s in suggestions:
                if s not in seen:
                    results.append({"元ワード": base, "入力文字": char, "サジェスト": s})
                    seen.add(s)
            time.sleep(0.4)

        if results:
            now = datetime.now()
            dir_path = f"data/{now.strftime('%Y-%m')}"
            os.makedirs(dir_path, exist_ok=True)
            timestamp = now.strftime("%Y%m%d_%H%M")
            
            df = pd.DataFrame(results)
            
            # 1. 全件保存
            filename_all = f"{dir_path}/KW_{base}_{timestamp}.csv"
            df.to_csv(filename_all, index=False, encoding="utf-8-sig")

            # 2. お宝（インテント）抽出保存
            df_treasure = df[df['サジェスト'].str.contains('|'.join(treasure_words))]
            if not df_treasure.empty:
                filename_t = f"{dir_path}/TREASURE_{base}_{timestamp}.csv"
                df_treasure.to_csv(filename_t, index=False, encoding="utf-8-sig")
            
            print(f"保存完了: {base}")

if __name__ == "__main__":
    run()
