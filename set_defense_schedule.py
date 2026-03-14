import os.path
import datetime
import sys
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# カレンダーの読み書き権限
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_accident_date():
    """ユーザーから事故日を入力してもらう関数"""
    while True:
        date_str = input("📅 交通事故にあった日を教えてください (例: 2026/01/23): ")
        try:
            # スラッシュ区切りでパース
            return datetime.datetime.strptime(date_str, "%Y/%m/%d").date()
        except ValueError:
            print("❌ 入力形式が違います。 2026/01/23 の形式で入力してください。")

def add_event(service, summary, description, date):
    """Googleカレンダーに予定を1件登録する関数"""
    event = {
        'summary': summary,
        'description': description,
        'start': {'date': date.isoformat(), 'timeZone': 'Asia/Tokyo'},
        'end': {'date': (date + datetime.timedelta(days=1)).isoformat(), 'timeZone': 'Asia/Tokyo'},
    }
    try:
        service.events().insert(calendarId='primary', body=event).execute()
        print(f'✅ 登録完了: {summary} ({date})')
    except Exception as e:
        print(f'❌ 登録失敗: {summary} - {e}')

def main():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    # --- ユーザーに事故日を入力してもらう ---
    accident_date = get_accident_date()

    # --- 戦略的マイルストーン ---
    milestones = [
        {"days": 7, "title": "⚖️ 弁護士への初期相談（特約確認）", "desc": "保険会社へ弁護士費用特約の有無を確認。なければ無料相談へ。"},
        {"days": 14, "title": "🩺 追加検査の提案（異常なしの場合）", "desc": "痛みが引かないならMRIやCT等の追加検査を医師に強く提案。"},
        {"days": 30, "title": "🩹 リハビリ定着確認・休業補償交渉", "desc": "リハビリ継続。並行して保険会社に休業補償の内払いを交渉。"},
        {"days": 90, "title": "📢 治療打ち切り打診への警戒（3ヶ月）", "desc": "保険会社からの治療終了打診に注意。継続の意志を伝える。"},
        {"days": 150, "title": "🛡️ リハビリ期限（150日ルール）", "desc": "健康保険リハビリの目安。今後の方向性を医師と再確認。"},
        {"days": 180, "title": "🩺 症状固定・後遺障害の相談（6ヶ月）", "desc": "同級生の教訓：医師に後遺症を相談。弁護士と示談交渉の対策を練る。"},
    ]

    print(f"\n🚀 {accident_date} を起点に、一件ずつ確認しながら登録します...")
    print("--------------------------------------------------")

    for ms in milestones:
        target_date = accident_date + datetime.timedelta(days=ms['days'])
        
        print(f"\n📍 予定案: {ms['title']}")
        print(f"   予定日: {target_date}")
        print(f"   内容  : {ms['desc']}")
        
        answer = input("👉 登録しますか？ (y / n): ").lower()
        if answer == 'y':
            add_event(service, ms['title'], ms['desc'], target_date)
        else:
            print(f"⏭️ スキップしました")

    print("\n--------------------------------------------------")
    print("✨ すべての工程が完了しました！リハビリ、いってらっしゃい！")

if __name__ == '__main__':
    main()