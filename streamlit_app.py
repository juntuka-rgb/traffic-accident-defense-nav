import streamlit as st
import pandas as pd
import datetime
import os.path

# --- 設定 ---
v = "v2.2.6" 

# --- 1. iCal形式のテキストを生成する関数 ---
def create_ics_content(incident_date, milestones):
    ics_text = "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Life Defense Nav//JP\nCALSCALE:GREGORIAN\nMETHOD:PUBLISH\n"
    for m in milestones:
        target_date = incident_date + datetime.timedelta(days=m["days"])
        date_str = target_date.strftime("%Y%m%d")
        ics_text += "BEGIN:VEVENT\n"
        ics_text += f"SUMMARY:🛡️ {m['title']}\n"
        ics_text += f"DESCRIPTION:{m['desc']}\n"
        ics_text += f"DTSTART;VALUE=DATE:{date_str}\n"
        ics_text += f"DTEND;VALUE=DATE:{date_str}\n"
        ics_text += "STATUS:CONFIRMED\n"
        ics_text += "SEQUENCE:0\n"
        ics_text += "TRANSP:TRANSPARENT\n"
        ics_text += "END:VEVENT\n"
    ics_text += "END:VCALENDAR"
    return ics_text

def main():
    st.set_page_config(page_title=f"生活防衛ナビ {v}", layout="wide", page_icon="🛡️")

    st.title(f"🛡️ 交通事故被害者のための生活防衛ナビ {v}")
    st.subheader("「黙っていたら損をする。被害者の体と生活を守るため、正当な権利の防衛をしましょう。」")
    
    st.info("""
    **【重要】交通事故も、行政と同じく「申請主義」です。** 補償は自ら理論武装して勝ち取るものです。
    
    このアプリでは、作者が実際に事故に遭った**「2024年9月」の失敗と、その教訓を活かした「2026年1月」の対応**を元に、被害者が正当な権利を守るために有効なステップを示します。
    """)

    tabs = st.tabs(["⚡ 初動", "🔍 検査", "🩹 治療", "⚖️ 補償・交渉", "📅 カレンダー同期"])

    # --- タブ1: 初動 (最新フィードバックを反映) ---
    with tabs[0]:
        st.header("ステップ1：事故直後のアクション")
        col1, col2 = st.columns(2)
        with col1:
            st.error("⚠️ **言われるがまま（2024年）**")
            st.write("- 相手の「物損で」という空気に流される。\n- 軽い痛みだったので「大丈夫です」と遠慮してしまう。")
        with col2:
            st.success("🔥 **理論武装（2026年）**")
            st.write("- **警察に連絡し人身事故として処理。**\n- **事故後数日中に、自分の保険（自転車保険・生命保険等）の特約を確認。**")
            st.info("""
            💡 **体験談：** 最初は「相手から治療費が出るなら自分の保険は関係ない」と思っていましたが、通院特約を並行して受け取れることがわかり、連絡し、必要書類を送ってもらいました。
            """)

    # --- タブ2: 検査 ---
    with tabs[1]:
        st.header("ステップ2：医療機関での検査")
        st.info("💡 事故から2週間経っても痛みが引かなければ、それは『別の原因』を疑うべきサインです。")
        col1, col2 = st.columns(2)
        with col1:
            st.error("⚠️ **2024年の失敗**")
            st.write("- レントゲンで「異常なし」と言われ、違和感を伏せてしまった。")
        with col2:
            st.success("🔥 **2026年の戦略**")
            st.write("- 「痛みが引かないのはおかしい」と客観的事実を伝え、CT・MRI検査を要求。\n- **精密検査により肋骨骨折、腱板損傷、肩の関節水腫が判明。適切な治療計画に繋げた。**")

    # --- タブ3: 治療 (最新フィードバックを反映) ---
    with tabs[2]:
        st.header("ステップ3：通院とリハビリ")
        st.success("🎉 **実証された「備え」の重要性（2026年3月更新）**")
        
        comparison_data = {
            "項目": ["通院日数", "休業損害（内金等）", "自身の保険からの補償", "慰謝料", "最終的な納得感"],
            "2024年の失敗": ["2日", "12,200円", "0円（未申請）", "17,200円", "金額にがっかり"],
            "2026年の戦略": [
                "**30日達成（3/6時点）** ※現在も治療継続中", 
                "158,600円（1/23〜2/28分を3/10に獲得）", 
                "**通院補償（1000円/回・上限30回分）として30,000円を受領（3/16）**", 
                "交渉準備中", 
                "休業損害を交渉し、2月末までを内金として振り込まれたため不安なく治療に専念中" 
            ]
        }
        st.table(pd.DataFrame(comparison_data))
        st.info("💡 **自身の自転車保険の通院特約により、1/23の事故当日からの治療による通院回数の規定の上限まで正当な補償を受けました。**")

    # --- タブ4: 補償・交渉 ---
    with tabs[3]:
        st.header("ステップ4：示談交渉")
        st.success("💡 **「アコギ」ではなく「ロジカルな防衛」**")
        st.write("- **弁護士に相談：** 自己負担ゼロでプロを味方につける。\n- **書面のエビデンス：** 判例に基づいた正当な増額を要求する。")

    # --- タブ5: カレンダー同期 ---
    with tabs[4]:
        st.header("📅 生活防衛スケジュールの同期")
        st.write("事故日を入力してください。重要なマイルストーンをご自身のカレンダーに取り込めます。")
        
        incident_date = st.date_input("事故発生日を選択してください", value=datetime.date.today())

        milestones = [
            {"days": 7, "title": "⚖️ 弁護士への初期相談", "desc": "特約の確認と無料相談の活用。"},
            {"days": 14, "title": "🩺 追加検査の提案", "desc": "痛みが引かない場合のMRI/CT交渉。"},
            {"days": 30, "title": "🩹 自身の保険会社へ中間報告", "desc": "通院日数の進捗確認と書類の準備。"}, 
            {"days": 90, "title": "📢 治療打ち切りへの警戒", "desc": "継続意志の明確な伝達。"},
            {"days": 150, "title": "🛡️ リハビリ期限（150日）", "desc": "今後の治療方針の再確認。"},
            {"days": 180, "title": "🩺 症状固定・後遺障害相談", "desc": "半年目の重要相談。"}
        ]

        st.subheader("📋 予定リストのプレビュー")
        st.table(pd.DataFrame([{"予定日": incident_date + datetime.timedelta(days=m["days"]), "項目": m["title"]} for m in milestones]))

        ics_content = create_ics_content(incident_date, milestones)
        st.download_button(
            label="📥 カレンダー用ファイルをダウンロード (.ics)",
            data=ics_content,
            file_name="accident_defense_schedule.ics",
            mime="text/calendar",
            use_container_width=True
        )
        st.info("※ダウンロードしたファイルをご自身が使用しているカレンダーアプリで読み込んでください。")

if __name__ == "__main__":
    main()
