import streamlit as st
import pandas as pd
import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# --- 設定 ---
v = "v2.2.1"
SCOPES = ['https://www.googleapis.com/auth/calendar']

def google_calendar_auth():
    """Googleカレンダー認証"""
    creds = None
    # token.jsonがあるか確認（.gitignoreでGitHubからは保護）
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # サーバー上では認証画面が出せないため、ローカルで作成したtoken.jsonを使用する前提
            st.error("認証トークン(token.json)が見つかりません。Mac miniで一度実行して作成してください。")
            return None
    try:
        return build('calendar', 'v3', credentials=creds)
    except Exception as e:
        st.error(f"Google API接続エラー: {e}")
        return None

def add_to_calendar(service, summary, description, date):
    """Googleカレンダーに予定登録"""
    event = {
        'summary': summary,
        'description': description,
        'start': {'date': date.isoformat(), 'timeZone': 'Asia/Tokyo'},
        'end': {'date': (date + datetime.timedelta(days=1)).isoformat(), 'timeZone': 'Asia/Tokyo'},
    }
    try:
        service.events().insert(calendarId='primary', body=event).execute()
        return True
    except:
        return False

def main():
    # アプリ設定
    st.set_page_config(page_title=f"生活防衛ナビ {v}", layout="wide", page_icon="🛡️")

    # --- ヘッダー ---
    st.title(f"🛡️ 交通事故被害者のための生活防衛ナビ {v}")
    st.subheader("「黙っていたら損をする。被害者の体と生活を守る『攻め』の手順書」")
    
    st.info("""
    **【重要】交通事故も、行政と同じく「申請主義」です。** 補償は与えられるものではなく、自ら理論武装して勝ち取るものです。
    加害者側の保険会社は、必ずしも被害者の生活を第一に考えてはくれません。
    
    このアプリでは、作者が実際に事故に遭った**「2024年9月」**の失敗と、その教訓を活かした**「2026年1月」の対応**を比較し、被害者が正当な権利を守るためのステップを示します。
    """)

    # --- メインメニュー（タブ形式） ---
    tabs = st.tabs(["⚡ 初動", "🔍 検査", "🩹 治療", "⚖️ 補償・交渉", "🗓️ カレンダー連携"])

    # --- 1. 初動 ---
    with tabs[0]:
        st.header("ステップ1：事故直後のアクション")
        col1, col2 = st.columns(2)
        with col1:
            st.error("⚠️ **言われるがまま（2024年）**")
            st.write("""
            - 相手の「物損で」という空気に流される。
            - 軽い痛みだったので「大丈夫です」と遠慮してしまう。
            - **結果：** 警察への届け出が軽く扱われ、権利主張の土台が弱くなる。
            """)
        with col2:
            st.success("🔥 **理論武装（2026年）**")
            st.write("""
            - **即座に110番。人身事故として処理。**
            - 加害者の過失をその場で確定させる。
            - **自分の保険（自転車保険・生命保険等）の担当者に即連絡し、通院特約の有無を確認。**
            - **結果：** 警察に「人身」として記録され、正当な補償を受ける権利を確保。
            """)

    # --- 2. 検査 ---
    with tabs[1]:
        st.header("ステップ2：医療機関での検査と費用交渉")
        st.info("💡 事故から2週間経っても痛みが引かなければ、それは『別の原因』を疑うべきサインです。")
        col1, col2 = st.columns(2)
        with col1:
            st.error("⚠️ **言われるがまま（2024年）**")
            st.write("""
            - 事故当日のレントゲン検査のみ。
            - 医師の「異常なし（打撲・捻挫）」を鵜呑みにし、違和感を伏せてしまう。
            - **結果：** 原因不明の痛みを抱えたまま、早期に治療が終了。
            """)
        with col2:
            st.success("🔥 **理論武装（2026年）**")
            st.write("""
            - **「事故から一ヶ月経過してるのに痛みが引かない。レントゲンで異常なしなのはおかしい」と客観的事実を伝える。**
            - **費用交渉：** 保険会社に先に連絡し「痛みが引かないので精密検査を受けたい。医療費の直接支払いを病院へ連絡してほしい」と了承を得る。
            - 2/19にCT検査を受け、**右肋骨骨折**が判明。
            - エコー・MRI検査を経て、**右腱板損傷**が発覚。
            """)

    # --- 3. 治療 ---
    with tabs[2]:
        st.header("ステップ3：通院と休業損害")
        comparison_data = {
            "項目": ["通院日数", "休業損害（内金等）", "自身の保険からの補償", "慰謝料", "最終的な納得感"],
            "2024年の失敗": ["2日", "12,200円", "0円（未申請）", "17,200円", "金額にがっかり"],
            "2026年の戦略": ["26日以上（リハビリ開始）", "158,600円（内金獲得）", "通院補償30回分を申請", "交渉準備中", "安心して治療に専念"]
        }
        st.table(pd.DataFrame(comparison_data))
        st.write("""
        - **「通院実績＝休業損害の根拠」** と理解し、治療のための通院時間はしっかりと確保。
        - 自分の保険（自転車保険等）の「通院補償」も上限まで活用。
        """)

    # --- 4. 補償・交渉 ---
    with tabs[3]:
        st.header("ステップ4：示談交渉と専門家への相談")
        col1, col2 = st.columns(2)
        with col1:
            st.error("⚠️ **言われるがまま（2024年）**")
            st.write("- 知識がないため、増額交渉の余地や、自分の自転車保険からも補償を受けられることを知らない。")
        with col2:
            st.success("🔥 **理論武装（2026年）**")
            st.write("- **無料相談を活用し、プロのアドバイスを受ける。** 「休業損害の交渉は正当な権利」という裏付けを得て交渉。")

    # --- 5. カレンダー連携（v2.2.1 新機能） ---
    with tabs[4]:
        st.header("🗓️ Googleカレンダー戦略連携")
        st.write("事故日を入力すると、教訓に基づいた戦略的マイルストーンをカレンダーに登録できます。")
        
        accident_date = st.date_input("事故発生日を選択してください", datetime.date.today())
        
        # 戦略的マイルストーンの定義
        milestones = [
            {"days": 0, "title": "🚨 事故発生・初動対応", "desc": "警察・保険会社への連絡、人身切り替え。"},
            {"days": 7, "title": "⚖️ 弁護士への初期相談", "desc": "保険会社へ特約確認。なければ無料相談へ。"},
            {"days": 14, "title": "🩺 追加検査の提案", "desc": "痛みが引かないならMRI等を医師に強く提案。"},
            {"days": 30, "title": "🩹 休業補償・内払いの交渉", "desc": "リハビリ継続。生活費確保のため内払いを交渉。"},
            {"days": 90, "title": "📢 治療打ち切り打診への警戒", "desc": "保険会社からの終了打診に注意。継続の意志。"},
            {"days": 180, "title": "🩺 症状固定・後遺障害の相談", "desc": "医師に後遺症を相談。弁護士と示談対策。"},
        ]

        st.table(pd.DataFrame([{
            "予定日": (accident_date + datetime.timedelta(days=m['days'])).strftime("%Y/%m/%d"),
            "項目": m['title'],
            "内容": m['desc']
        } for m in milestones]))

        if st.button("🚀 このスケジュールをGoogleカレンダーに一括登録する"):
            service = google_calendar_auth()
            if service:
                with st.spinner("カレンダーに登録中..."):
                    count = 0
                    for ms in milestones:
                        target_date = accident_date + datetime.timedelta(days=ms['days'])
                        if add_to_calendar(service, ms['title'], ms['desc'], target_date):
                            count += 1
                    if count > 0:
                        st.success(f"✅ {count}件の予定をGoogleカレンダーに登録しました！")
                    else:
                        st.warning("登録に失敗しました。認証を確認してください。")

    st.divider()
    st.write("© 2026 Jun Tsukada - ロジカルな防衛で、正当な権利を。")

if __name__ == "__main__":
    main()