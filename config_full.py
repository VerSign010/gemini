import google.generativeai as genai
import os


try:
    genai.configure(api_key=os.environ["AIzaSyDl1YHnyuf3CWLE-sYNo0T7cPHmLQ9whEw"])
except KeyError:
    print("错误：请设置名为 GOOGLE_API_KEY 的环境变量。")
    print("您可以从 Google AI Studio 获取您的API密钥: https://aistudio.google.com/app/api_keys")
    exit()

# --- 2. 定义模型运行参数 (我们共同确立的最佳设置) ---
generation_config = {
  "temperature": 0.2,      # 低温以确保结果的准确性和一致性
  "top_p": 0.95,           # 采用Top-P采样，保留高质量的词汇选择范围
  "top_k": 0,              # 设置为0，表示不使用Top-K采样，让Top-P主导
  "max_output_tokens": 8192, # 设置足够高的输出长度，防止详细分析被截断
}

# --- 3. 定义安全设置 ---
# 通常使用默认设置即可。这里明确列出以供参考。
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]


# --- 6. 开始一个审校会话 ---
# 现在，你可以像在UI中一样，直接发送需要审校的内容
print("德语翻译审校机器人已准备就绪。请输入您的第一段审校内容。")
print("-" * 50)

# 这是一个示例，您可以将其替换为您自己的内容
# 为了方便，这里将原文和译文放在一个字符串中
review_content = """
【中文原文】
揣摩着神的话，反省自己信神多年外表撇家舍业地尽本分，其实心并没有给神，还一直把撒但的生存法则“爬得高，摔得惨”“高处不胜寒”当成至理名言，一直凭着撒但的生存法则活着，不相信神的公义性情。

【英文译文】
As I pondered God's words and reflected on myself, I realized that although I had believed in God for many years, outwardly forsaking my family and career to do my duty, I had never actually given my heart to God. I had always clung to Satan's rules for survival, like "The bigger they are, the harder they fall" and "It's lonely at the top," treating them as maxims and wise words. I had been living according to Satan's rules of survival, not believing in God's righteous disposition.

【德语译文】
Beim Nachdenken über Gottes Worte und über mich selbst, wurde mir eines klar: Ich glaubte zwar schon viele Jahre an Gott und hatte sogar meine Familie und meine Karriere aufgegeben, um meine Pflicht zu tun, aber mein Herz hatte ich Gott niemals wirklich gegeben. Ich hatte mich immer an Satans überlebensregeln geklammert. Sprüche wie ?Wer hoch steigt, f?llt tief“ oder ?An der Spitze ist man einsam“ behandelte ich wie weise Lehren. Ich hatte nach Satans überlebensregeln gelebt und nicht an Gottes gerechte Disposition geglaubt.
"""

# 启动一个聊天会话
chat = model.start_chat()

# 发送审校内容给模型
response = chat.send_message(review_content)

# 打印模型的专业审校报告
print(response.text)
