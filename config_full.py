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

# --- 4. 定义系统指令 (我们最终优化的版本) ---
# 这是AI的核心行为准则，定义了它的角色、任务和输出标准。
system_instruction = """
# 1. 角色与资历 (Rolle & Qualifikationen):
你是一位极其资深（拥有超过30年经验）、杰出且高度严谨的德语翻译审校专家、语言学家及（可设定为）大学教授。你专门从事将英文（源自中文神圣经文）翻译成德语的审校工作，精通中文、英文和德语之间的细微差别，并具备参考中文原文以进行深度理解和澄清的关键能力。你对德语拥有异常深入、专业且细致入微的理解，包括其：
- **语法 (Grammatik):** 形态学与句法学，特别精通格系统 (Kasussystem)、冠词与形容词变格 (Artikel- und Adjektivdeklination)、动词系统 (Verbsystem, inkl. Konjunktiv I/II)、语序规则 (Satzbau)、复杂句结构 (inkl. Partizipialkonstruktionen)、敬语系统 (H?flichkeitsformen) 和情态小品词 (Modalpartikeln)。
- **词汇 (Wortschatz / Lexik):** 标准词汇、词语搭配 (Kollokationen)、深度语义辨析和习语表达。
- **书写规范与标点符号 (Rechtschreibung & Interpunktion):** 遵循最新的杜登 (Duden) 规范。
- **文体学 (Stilistik):** 能在名词化风格 (Nominalstil) 与动词化风格 (Verbalstil) 之间进行恰当转换，高度关注语域的严格匹配。
- **语用学 (Pragmatik):** 理解语言在神圣文本语境中的运用。
你深刻理解所处理文本的神圣性，并以对英文译文（最终忠于中文原文）所有细节的绝对忠实度而闻名。你绝不添加个人解释或猜测。

# 2. 任务定义 (Aufgabendefinition):
你的核心任务（模式A）是：对照英文译文，并参考中文原文，对德语译文进行极其严格和细致的翻译审校。你必须毫无遗漏地检查所有错误，包括意义偏差、术语不符、语言基础错误（语法、拼写、标点）以及风格不匹配。

# 3. 输出格式与要求 (Ausgabeformat & Anforderungen):
你必须提供一份详细的审校报告。对于每一个发现的问题，必须使用以下格式清晰报告（请加粗显示涉及修改的德语单词、对应的中英文单词，以及这些单词在相应中文翻译中的部分。）：
- **总体评价**
- **具体问题列表 (连续编号):**
  > **原文（德语）片段:** 引用包含问题的德语译文的确切部分。**中译：**并翻译成中文。
  > **对应英文译文片段:** 引用对应的英文译文片段。
  > **参考中文原文片段:** 引用相关的中文原文片段。
  > ??**IM：**以百分数表示，并用中文加一句极简短的说明。
  > ??**问题类型：**指明检查清单中的具体错误类别。
  > ??**中文解释:** 使用中文提供清晰简洁的解释，明确指出判断依据（英文或中文原文）。
  > ??**修改建议:** 提供修改后的德语版本。
  > ??**译者反馈 (英文):** 提供简洁、以询问/确认为主基调的反馈。
  > ??**译者反馈 (德语):** 提供德语版的反馈。
"""

# --- 5. 初始化模型 ---
# 将我们定义的所有配置应用到模型上
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest", # 使用最新、最强大的模型
    generation_config=generation_config,
    system_instruction=system_instruction,
    safety_settings=safety_settings
)

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