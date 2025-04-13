import json
import os

# 假設你有一個原始的 JSON 資料文件
input_file = os.path.join('..', 'data', 'raw', '16personalities.json')
output_file = os.path.join('..', 'data', 'training_data.jsonl')

# 讀取原始資料
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

cleaned_data = []

# 清洗過程
for item in data:
    messages = item['messages']
    
    # 檢查資料是否完整，移除無效資料
    if len(messages) < 3:
        continue  # 跳過資料不完整的項目

    # 確保資料格式一致，去除多餘的空白符
    for message in messages:
        message['content'] = message['content'].strip()

    # 這裡可以加入更多處理邏輯，比如過濾特殊字符、拼寫檢查等
    # 比如：清理掉特殊字符
    # for message in messages:
    #     message['content'] = ''.join(e for e in message['content'] if e.isalnum() or e.isspace())
    
    # 把清洗過的資料加入結果列表
    cleaned_data.append(item)

# 確保目錄存在
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# 寫入 cleaned_data 為 .jsonl 格式
with open(output_file, 'w', encoding='utf-8') as f:
    for item in cleaned_data:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')

print(f"資料已成功清洗並保存為 .jsonl 格式，儲存路徑:{output_file}")