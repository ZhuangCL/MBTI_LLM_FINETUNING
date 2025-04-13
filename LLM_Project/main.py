import os
from langchain_openai import ChatOpenAI
# from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.agents import initialize_agent, Tool, AgentType
from dotenv import dotenv_values

# _______________________________________________________________________
config = dotenv_values(".env")
os.environ["OPENAI_API_KEY"] = config["API_KEY"]
llm = ChatOpenAI(model_name = "ft:gpt-3.5-turbo-0125:personal::BAAVeRzD", temperature = 0.5)

# _________________________________________________________________________
mbti_prompt = PromptTemplate(
    imput_variables = ["text"],
    # 第一次描述
    template="請根據以下內容判斷使用者的MBTI類型，並且分析是A和T哪種子型人格，並且簡單分析一下為什麼，以下為內容:\n{text}",
    max_tokens = 100
)

mbti_chain = LLMChain(prompt=mbti_prompt, llm=llm)
# mbti_chain = mbti_prompt | llm

# __________________________________________________________________________
# 設定工具並初始化 Agent
tools = [
    Tool(
        name = "MBTI分析",
        func = mbti_chain.run,
        # 第二次具體描述
        description = "根據用戶輸入的文字分析 MBTI 類型，並分析是A和T哪種子型人格，簡短說明為什麼，使用繁體中文回答，不要使用其他語言"
    )
]

# 初始化 AgentExecutor
agent = initialize_agent(
    tools,
    llm,
    agent_type = AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors = True
)

# 紀錄_____________________________________________________________________________
import datetime

test_log_file = "logs/test_log.txt"

def log_test_result(user_input, model_output):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(test_log_file, "a", encoding="utf-8") as f:
        f.write(f"[timestamp] 📝 使用者輸入: {user_input}\n")
        f.write(f"[{timestamp}] 🤖 模型回應: {model_output}\n\n")

# _____________________________________________________________________________
# 客戶與 Agent 的對話，這裡用戶可以自定義輸入
def start_conversation():
    print("🎉 歡迎來到 MBTI 類型分析！請隨意輸入你的性格或介紹自己(以下為範例:我最近在學習新技術，覺得探索新知識的過程很有趣。我通常會先了解基本概念，然後自己嘗試應用，這樣比較能掌握核心原理。我比較少依賴既有的範例，而是喜歡自己摸索新的方法，雖然有時候會多花點時間，但這樣學得比較扎實。)(若要結束請輸入 'exit', 'quit', 'bye')：")
    while True:
        user_input = input("您：")  # 客戶輸入

        # 檢查亂輸入（例如數字、空白等）
        if user_input.strip().isdigit() or not user_input.strip():
            print("⚠️ 無效輸入！請輸入有效的文字來描述您的特徵，若要結束請輸入 'bye'")
            continue

        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("🎉 感謝您的使用，再見！")
            break
        agent_response = agent.run(user_input)
        print("🤖 Agent 回應：", agent_response)
        log_test_result(user_input, agent_response)
        break
start_conversation()

# 舊版______________________________________________________________________
# def analyze_mbti_from_text(user_text):
#     return mbti_chain.invoke(user_text)
# user_post = """
# 我最近在學習新技術，覺得探索新知識的過程很有趣。我通常會先了解基本概念，
# 然後自己嘗試應用，這樣比較能掌握核心原理。我比較少依賴既有的範例，而是
# 喜歡自己摸索新的方法，雖然有時候會多花點時間，但這樣學得比較扎實。
# """
# mbti_from_post = analyze_mbti_from_text(user_post)
# print("\n🔹 **MBTI 分析結果：**\n")
# print(mbti_from_post.content)
# print("\n🔹 **API 回應元數據（Metadata）：**\n")
# print(mbti_from_post.response_metadata)