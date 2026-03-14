import streamlit as st
import pandas as pd
import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# --- 設定 ---
v = "v2.2.2"

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

# --- 2. Google Calendar API 認証関数 ---
def get_calendar_service():
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                return None
            try:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=8080)
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())
            except:
                return None
    return build('calendar', 'v3', credentials=creds)

def main():
    st.set_page_config(page_title=f"生活防衛ナビ {v}", layout="wide", page_icon="🛡️")

    st.title(f"🛡️ 交通事故被害者のための生活防衛ナビ {v}")
    st.subheader("「黙っていたら損をする。被害者の体と生活を守るため、正当な権利の防衛をしましょう。」")
    
    st.info("""
    **【重要】交通事故も、行政と同じく「申請主義」です。** 補償は自ら理論武装して勝ち取るものです。
    
    このアプリでは、作者が実際に事故に遭った**「2024年9月」の失敗と、その教訓を活かした「2026年1月」の対応**を元に、被害者が正当な権利を守るために有効なステップを示します。
    """)

    tabs = st.tabs(["⚡ 初動", "🔍 検査", "🩹 治療", "⚖️ 補償・交渉", "📅 カレンダー同期"])

    # ステップ1〜4はそのまま維持
    with tabs[0]:
        st.header("ステップ1：事故直後のアクション")
        col1, col2 = st.columns(2)
        with col1:
            st.error("⚠️ **言われるがまま（2024年）**")
            st.write("- 相手の「物損で」という空気に流される。\n- 軽い痛みだったので「大丈夫です」と遠慮してしまう。")
        with col2:
            st.success("🔥 **理論武装（2026年）**")
            st.write("- **警察に連絡し、現場検証。事故後なるべく早く医師に診断書を書いてもらい警察に提出。人身事故として処理。**\n- **自分の保険（自転車保険・生命保険等）の通院特約・弁護士費用特約を即確認。**")

    with tabs[1]:
        st.header("ステップ2：医療機関での検査")
        st.info("💡 事故から2週間経っても痛みが引かなければ、それは『別の原因』を疑うべきサインです。")
        col1, col2 = st.columns(2)
        with col1:
            st.error("⚠️ **2024年の失敗**")
            st.write("- レントゲンで「異常なし」と言われ、違和感を伏せてしまった。")
        with col2:
            st.success("🔥 **2026年の戦略**")
            st.write("- 「痛みが引かないのはおかしい」と客観的事実を伝え、CT・MRI検査を要求。\n- **追加したCT検査により右肋骨骨折を、エコー検査により右肩に水が溜まっていることが判明。**\n- **さらにMRI検査により右腱板損傷が見つかり、適切なリハビリ治療を開始。**")

    with tabs[2]:
        st.header("ステップ3：通院とリハビリ")
        comparison_data = {
            "項目": ["通院日数", "休業損害（内金等）", "自身の保険からの補償", "慰謝料", "最終的な納得感"],
            "2024年の失敗": ["2日", "12,200円", "0円（未申請）", "17,200円", "金額にがっかり"],
            "2026年の戦略": ["26日以上（リハビリを追加し治療継続中）", "158,600円（1/23〜2/28分を3/10に獲得）", "上限まで申請中", "交渉準備中", "内金獲得により安心して治療に専念中"]
        }
        st.table(pd.DataFrame(comparison_data))

    with tabs[3]:
        st.header("ステップ4：示談交渉")
        st.success("💡 **「アコギ」ではなく「ロジカルな防衛」**")
        st.write("- **弁護士に相談：** 自己負担ゼロでプロを味方につける。\n- **書面のエビデンス：** 判例に基づいた正当な増額を要求する。")

    # --- ステップ5: カレンダー同期 (デフォルト日付を今日に変更) ---
    with tabs[4]:
        st.header("📅 生活防衛スケジュールの同期")
        st.write("事故日を入力してください。重要なマイルストーンをご自身のカレンダーに取り込めます。")
        
        # デフォルト値を「今日」に変更
        incident_date = st.date_input("事故発生日を選択してください", value=datetime.date.today())

        milestones = [
            {"days": 7, "title": "⚖️ 弁護士への初期相談", "desc": "特約の確認と無料相談の活用。"},
            {"days": 14, "title": "🩺 追加検査の提案", "desc": "痛みが引かない場合のMRI/CT交渉。"},
            {"days": 30, "title": "🩹 リハビリ定着・休業補償交渉", "desc": "内払いの交渉開始。"},
            {"days": 90, "title": "📢 治療打ち切りへの警戒", "desc": "継続意志の明確な伝達。"},
            {"days": 150, "title": "🛡️ リハビリ期限（150日）", "desc": "今後の治療方針の再確認。"},
            {"days": 180, "title": "🩺 症状固定・後遺障害相談", "desc": "同級生の教術：半年目の重要相談。"}
        ]

        st.subheader("📋 予定リストのプレビュー")
        st.table(pd.DataFrame([{"予定日": incident_date + datetime.timedelta(days=m["days"]), "項目": m["title"]} for m in milestones]))

        col_direct, col_ics = st.columns(2)
        
        with col_direct:
            st.write("--- じゅんさん専用 (Mac) ---")
            if st.button("🚀 Googleカレンダーに直接同期"):
                with st.spinner("通信中..."):
                    service = get_calendar_service()
                    if service:
                        try:
                            for m in milestones:
                                target_date = incident_date + datetime.timedelta(days=m["days"])
                                event = {
                                    'summary': f"🛡️ {m['title']}",
                                    'description': m["desc"],
                                    'start': {'date': target_date.isoformat(), 'timeZone': 'Asia/Tokyo'},
                                    'end': {'date': (target_date + datetime.timedelta(days=1)).isoformat(), 'timeZone': 'Asia/Tokyo'},
                                }
                                service.events().insert(calendarId='primary', body=event).execute()
                            st.success("🎉 直接登録が完了しました！")
                            st.balloons()
                        except Exception as e:
                            st.error(f"❌ エラー: {e}")
                    else:
                        st.warning("⚠️ 認証トークンが必要です。Macのローカル環境から実行してください。")

        with col_ics:
            st.write("--- ユーザー様・仲間用 ---")
            ics_content = create_ics_content(incident_date, milestones)
            st.download_button(
                label="📥 カレンダー用ファイルをダウンロード (.ics)",
                data=ics_content,
                file_name="accident_defense_schedule.ics",
                mime="text/calendar",
            )
            st.warning("☝️ **書き出したファイルをご自身が使用しているカレンダーアプリで読み込んで、登録してください。**")
            st.info("※ダウンロードしたファイルを開くだけで、自動的にカレンダーへの追加画面が立ち上がります。")

if __name__ == "__main__":
    main()