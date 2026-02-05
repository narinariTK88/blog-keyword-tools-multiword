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
    if not os.path.exists(input_file):
        print(f"Error: {input_file} が見つかりません。")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        base_keywords = [line.strip() for line in f if line.strip()]

    # 日本語、英語、数字のサジェスト用文字リスト
    chars = [chr(i) for i in range(ord('ぁ'), ord('ん')+1)] + \
            [chr(i) for i in range(ord('a'), ord('z')+1)] + \
            [str(i) for i in range(10)]

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
            time.sleep(0.4) # 少し慎重に設定

        if results:
            # フォルダ作成（例: data/2026-02/）
            now = datetime.now()
            dir_path = f"data/{now.strftime('%Y-%m')}"
            os.makedirs(dir_path, exist_ok=True)
            
            # ファイル名生成（例: KW_ブログ運営_20260205_1530.csv）
            timestamp = now.strftime("%Y%m%d_%H%M")
            filename = f"{dir_path}/KW_{base}_{timestamp}.csv"
            
            df = pd.DataFrame(results)
            df.to_csv(filename, index=False, encoding="utf-8-sig")
            print(f"保存完了: {filename}")

if __name__ == "__main__":
    run()
