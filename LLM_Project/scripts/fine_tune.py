import openai
import json 
import time 
import os 
import datetime
from dotenv import dotenv_values
from tqdm import tqdm

# 設定 OpenAI API Key
config = dotenv_values(".env")
os.environ["OPENAI_API_KEY"] = config["API_KEY"]
model_name = "gpt-3.5-turbo"

# 設定檔案路徑
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRAINING_FILE_PATH = os.path.join(BASE_DIR, "data", "training_data.jsonl")
MODEL_INFO_PATH = os.path.join(BASE_DIR, "models", "fine_tuned_model.json")
log_file = os.path.join(BASE_DIR, "logs", "fine_tuning_log.txt")

# 設定記錄檔
def log_fine_tuning(message):
    """記錄 Fine-tuning 過程到 logs/fine_tuning_log.txt"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

# 1️⃣ 讀取訓練數據
def load_training_data(file_path):
    print("📂 檢查訓練資料格式中...")
    with open(file_path, "r", encoding="utf-8") as f:
        for i, line in enumerate(tqdm(f, desc="驗證 JSONL")):
            try:
                json.loads(line)
            except json.JSONDecodeError as e:
                raise ValueError(f"❌ 第 {i+1} 行格式錯誤: {e}")
    print("✅ 訓練資料格式正確！")
    
# 2️⃣ 上傳數據並建立 Fine-tuning 任務
def upload_training_data():
    print("🔄 上傳訓練數據中...")
    log_fine_tuning("🔄 上傳訓練數據中...")
    with open(TRAINING_FILE_PATH, "rb") as f:
        response = openai.files.create(file=f, purpose="fine-tune")
    file_id = response.id
    # response = openai.fine_tuning.jobs.create(
    #     training_file = file_id,
    #     model = model
    # )
    print(f"✅ 訓練數據已上傳，File ID: {file_id}")
    log_fine_tuning(f"✅ 訓練數據已上傳，File ID: {file_id}")
    return file_id

# 3️⃣ 開始 Fine-tuning
def start_fine_tuning(file_id, model = model_name):
    print(f"🚀 啟動 {model} 的 Fine-tuning 訓練...")
    response = openai.fine_tuning.jobs.create(
        training_file = file_id,
        model = model
    )
    job_id = response.id
    print(f"✅ Fine-tuning 任務已啟動，Job ID: {job_id}")
    log_fine_tuning(f"✅ Fine-tuning 任務已啟動，Job ID: {job_id}")
    return job_id

# 4️⃣ 檢查 Fine-tuning 任務狀態
def check_fine_tuning_status(job_id):
    print("🔄 檢查訓練進度中...")
    while True:
        try:
            response = openai.fine_tuning.jobs.retrieve(job_id)
            status = response.status
            print(f"⏳ 訓練進度: {status}")
            log_fine_tuning(f"⏳ 訓練進度: {status}")


            if status == "failed":
                # 查看失敗原因
                error = response.error if hasattr(response, 'error') else "未知錯誤"
                print(f"❌ 訓練失敗，原因: {error}")
                log_fine_tuning(f"❌ 訓練失敗，原因: {error}")
                return response

            if status == "succeeded":
                return response
        
            # 每 60 秒檢查一次
            # time.sleep(60)
            for _ in tqdm(range(60), desc="等待訓練完成"):
                time.sleep(1)

        except Exception as e:
            print(f"⚠️ 發生錯誤: {str(e)}")
            log_fine_tuning(f"⚠️ 發生錯誤: {str(e)}")
            break

# 5️⃣ 儲存 Fine-tuned 模型資訊
def save_model_info(model_info):
    os.makedirs(os.path.dirname(MODEL_INFO_PATH), exist_ok=True)
    print("保存的模型資訊:", model_info)
    with open(MODEL_INFO_PATH, "w", encoding="utf-8") as f:
        json.dump(model_info, f, indent = 4)
    print(f"✅ 模型資訊已儲存至 {MODEL_INFO_PATH}")
    log_fine_tuning(f"✅ 模型資訊已儲存至 {MODEL_INFO_PATH}")

# **執行 Fine-tuning 流程**
if __name__ == "__main__":
    try:
        print("🔵 Fine-tuning 訓練開始...") 
        log_fine_tuning("🔵 Fine-tuning 訓練開始...")   

        load_training_data(TRAINING_FILE_PATH)
        file_id = upload_training_data()
        job_id = start_fine_tuning(file_id)
        result = check_fine_tuning_status(job_id)

        if result.status == "succeeded":
            fine_tuned_model_id = result.fine_tuned_model
            print(f"🎉 訓練完成！Fine-tuned 模型 ID: {fine_tuned_model_id}")
            log_fine_tuning(f"🎉 訓練完成！Fine-tuned 模型 ID: {fine_tuned_model_id}")

            # 儲存 Fine-tuned 模型資訊
            save_model_info({"model_id" : fine_tuned_model_id})

        else:
            print("❌ 訓練失敗，請檢查錯誤資訊")
            log_fine_tuning("❌ 訓練失敗，請檢查錯誤資訊")
    
    except Exception as e:
        print(f"⚠️ 發生錯誤: {str(e)}")
        log_fine_tuning(f"⚠️ 發生錯誤: {str(e)}")
