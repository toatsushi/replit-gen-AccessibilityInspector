# WCAG Accessibility Evaluator

このプロジェクトは、Webサイトのアクセシビリティを自動・AIによる手動評価で総合的にチェックし、WCAG（Web Content Accessibility Guidelines）への準拠状況を可視化・レポート化するツールです。

## 主な機能

- **自動テスト**: axe-coreとSeleniumを用いた自動アクセシビリティ検査
- **AI手動評価**: OpenAI（GPT-4o）やAnthropic（Claude）を活用したAIによる手動評価
- **レポート生成**: 詳細なアクセシビリティレポートの生成・ダウンロード
- **StreamlitベースのWeb UI**: 直感的な操作が可能なWebアプリ

## 必要条件

- Python 3.11 以上
- Google Chrome（SeleniumのWebDriver用）

## インストール

1. リポジトリをクローン
    ```bash
    git clone <このリポジトリのURL>
    cd replit-gen-AccessibilityInspector
    ```

2. 依存パッケージのインストール
    ```bash
    pip install -r requirements.txt
    ```

3. 必要に応じてAPIキーを環境変数に設定  
   - OpenAI: `OPENAI_API_KEY`
   - Anthropic: `ANTHROPIC_API_KEY`

## 使い方

1. Streamlitアプリの起動
    ```bash
    streamlit run app.py
    ```

2. ブラウザで表示されるUIから、評価したいWebサイトのURLを入力し、「Analyze Website」ボタンを押してください。

   - 「Testing Options」でどちらも未選択の場合、または「WCAG Compliance Levels」で何も選択していない場合、「Analyze Website」ボタンはグレーアウトされ実行できません。
   - URLは「http://」または「https://」で始まる必要があります。

3. 結果が画面に表示され、レポートのダウンロードも可能です。

## ファイル構成

- `app.py` : Streamlitアプリ本体
- `accessibility_checker.py` : Selenium/axe-coreによる自動検査
- `ai_evaluator.py` : AIによる手動評価
- `report_generator.py` : レポート生成
- `wcag_criteria.py` : WCAG基準データ
- `requirements.txt` : 必要なPythonパッケージ一覧

## 注意事項

- SeleniumのChromeDriverが必要です。自動でインストールされない場合は、[公式サイト](https://chromedriver.chromium.org/downloads)からダウンロードしてください。
- AI評価を利用する場合は、各APIの利用登録・APIキーが必要です。

## ライセンス

このプロジェクトはMITライセンスです。

---

ご不明点があれば、IssueやPull Requestでご連絡ください。 