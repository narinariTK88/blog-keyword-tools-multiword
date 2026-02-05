import pandas as pd
import glob
import os
from datetime import datetime

def combine():
    # dataフォルダ内の全CSVファイルを取得
    all_files = glob.glob("data/**/*.csv", recursive=True)
    
    if not all_files:
        print("CSVファイルが見つかりません。")
        return

    combined_list = []
    for f in all_files:
        # すでに「まとめファイル」として作ったものは除外する
        if "ALL_COMBINED" in f:
            continue
        df = pd.read_csv(f)
        combined_list.append(df)

    if combined_list:
        combined_df = pd.concat(combined_list, ignore_index=True)
        # 重複を削除（別キーワードで同じサジェストが出た場合など）
        combined_df = combined_df.drop_duplicates(subset=['サジェスト'])

        # 保存先
        os.makedirs("summary", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        output_file = f"summary/ALL_COMBINED_{timestamp}.csv"
        
        combined_df.to_csv(output_file, index=False, encoding="utf-8-sig")
        print(f"全件統合完了: {output_file}")

if __name__ == "__main__":
    combine()
