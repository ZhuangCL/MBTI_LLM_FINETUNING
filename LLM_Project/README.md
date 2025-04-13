1. 專案介紹
## 📘 MBTI 人格分析系統
本專案使用 LLM 與 LangChain 建構 MBTI 分析機器人，能夠根據使用者輸入的描述，判斷其 MBTI 類型（如 ISTJ）與子型人格（A/T），並給予簡單分析說明。

2. 功能特點
### ✅ 功能特色
- 支援中文輸入並回覆繁體中文
- 使用 LangChain Agent 自動判斷人格類型
- 可識別固執、猶豫等行為關鍵詞
- 使用者可透過輸入多段描述，最終獲得 MBTI 結果


3. 安裝與執行方式
### ⚙️ 安裝與執行
```bash
cd mbti-project
pip install -r requirements.txt
在.env檔案裡輸入你的API_KEY(預設OPENAI)
python main.py

4. 檔案結構（選填）
### 📁 專案結構
- `main.py`：主程式，啟動 MBTI 分析對話
- `scripts/fine_tune.py`：微調模型用的腳本
- `data/`：存放訓練資料

5. 注意事項
### ⚠️ 注意事項
- 請輸入有意義的描述（避免亂碼、數字如 "123"）
- 若要結束對話，請輸入 `bye`

6. 授權與作者
### 👤 作者
ZhuangCL 長霖
