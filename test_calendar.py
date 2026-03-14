import os.path
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# カレンダーの読み書き権限を指定
SCOPES = ['https://www.googleapis.com/auth/calendar']

def main():
    creds = None
    # 過去に認証した情報があれば読み込む
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # 認証情報がない、または有効でない場合はログインを行う
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        # 次回のために認証情報を保存
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    # テスト予定の作成
    event = {
        'summary': '🛡️ 生活防衛ナビ：接続テスト成功！',
        'location': 'じゅんさんのMac mini',
        'description': 'この予定が見えていれば、Google Calendar APIとの連携は完璧です。',
        'start': {
            'dateTime': datetime.datetime.now().isoformat(),
            'timeZone': 'Asia/Tokyo',
        },
        'end': {
            'dateTime': (datetime.datetime.now() + datetime.timedelta(hours=1)).isoformat(),
            'timeZone': 'Asia/Tokyo',
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f'予定を作成しました: {event.get("htmlLink")}')

if __name__ == '__main__':
    main()