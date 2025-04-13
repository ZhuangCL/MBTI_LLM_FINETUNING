import os

# 定義資料夾與檔案結構
project_structure = {
    "LLM_Project": [
        "data",
        "data/raw",
        "models",
        "scripts",
        "logs"
    ]
}

files = [
    "data/raw/raw_data.json",
    "scripts/preprocess.py",
    "scripts/fine_tune.py",
    "models/fine_tuned_model.json",
    "logs/fine_tuning_log.txt",
    "logs/test_log.txt",
    "main.py",
    "requirements.txt",
    "README.md"
]

# 建立資料夾
for folder, subfolders in project_structure.items():
    os.makedirs(folder, exist_ok=True)
    for subfolder in subfolders:
        os.makedirs(os.path.join(folder, subfolder), exist_ok=True)

# 建立檔案
for file in files:
    file_path = os.path.join("LLM_Project", file)
    with open(file_path, "w") as f:
        pass  # 建立空檔案

print("✅ 專案檔案結構已建立完成！")