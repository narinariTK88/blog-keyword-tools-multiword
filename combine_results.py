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
        
        try:
            df = pd.read_csv(f)
            # ラベル名をセンス良く修正
            # ファイル名に TREASURE が入っていれば「インテント修飾語」、それ以外は「サジェストオリジナル」
            source_type = "インテント修飾語" if "TREASURE" in os.path.basename(f) else "サジェストオリジナル"
            
            df['データ種別'] = source_type
            combined_list.append(df)
        except Exception as e:
            print(f"ファイル読み込みエラー ({f}): {e}")

    if combined_list:
        combined_df = pd.concat(combined_list, ignore_index=True)
        
        # 重複削除のルール：
        # 「インテント修飾語」を優先して残す（「イ」は「サ」より五十音順で先に来るため昇順ソートでOK）
        combined_df = combined_df.sort_values('データ種別', ascending=True)
        combined_df = combined_df.drop_duplicates(subset=['サジェスト'], keep='first')

        # 保存先
        os.makedirs("summary", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        output_file = f"summary/ALL_COMBINED_{timestamp}.csv"
        
        # 列の順番を整理
        cols = ['元ワード', '入力文字', 'サジェスト', 'データ種別']
        combined_df = combined_df[cols]
        
        combined_df.to_csv(output_file, index=False, encoding="utf-8-sig")
        print(f"全件統合完了: {output_file}")

if __name__ == "__main__":
    combine()
