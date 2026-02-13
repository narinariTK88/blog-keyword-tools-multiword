import pandas as pd
import glob
import os
import shutil
from datetime import datetime

def combine():
    # 1. 素材ファイルの取得（dataフォルダのみ対象）
    all_files = glob.glob("data/**/*.csv", recursive=True)
    
    if not all_files:
        print("処理対象のCSVファイル（dataフォルダ内）が見つかりませんでした。")
        return

    combined_list = []
    for f in all_files:
        try:
            df = pd.read_csv(f)
            # ラベル付け
            source_type = "インテント修飾語" if "TREASURE" in os.path.basename(f) else "サジェストオリジナル"
            df['データ種別'] = source_type
            combined_list.append(df)
        except Exception as e:
            print(f"読み込み失敗 ({f}): {e}")

    # 2. 統合処理
    if combined_list:
        combined_df = pd.concat(combined_list, ignore_index=True)
        # インテント修飾語ラベルの方を優先して重複削除
        combined_df = combined_df.sort_values('データ種別', ascending=True)
        combined_df = combined_df.drop_duplicates(subset=['サジェスト'], keep='first')

        # summaryフォルダの整理（古いまとめを削除）
        os.makedirs("summary", exist_ok=True)
        for s_item in os.listdir("summary"):
            s_path = os.path.join("summary", s_item)
            if os.path.isfile(s_path): os.remove(s_path)

        # 最新まとめの保存
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        output_file = f"summary/ALL_COMBINED_{timestamp}.csv"
        
        cols = ['元ワード', '入力文字', 'サジェスト', 'データ種別']
        combined_df = combined_df[cols]
        combined_df.to_csv(output_file, index=False, encoding="utf-8-sig")
        print(f"✅ 全データを統合しました: {output_file}")

        # 3. dataフォルダのお掃除（全削除）
        for item in os.listdir("data"):
            item_path = os.path.join("data", item)
            try:
                if os.path.isdir(item_path): shutil.rmtree(item_path)
                else: os.remove(item_path)
            except Exception as e:
                print(f"削除エラー: {e}")
        
        print("🗑️ dataフォルダ内を空にしました。")

if __name__ == "__main__":
    combine()
