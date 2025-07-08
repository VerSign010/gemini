import google.generativeai as genai
import os


try:
    genai.configure(api_key=os.environ["AIzaSyDl1YHnyuf3CWLE-sYNo0T7cPHmLQ9whEw"])
except KeyError:
    print("������������Ϊ GOOGLE_API_KEY �Ļ���������")
    print("�����Դ� Google AI Studio ��ȡ����API��Կ: https://aistudio.google.com/app/api_keys")
    exit()

# --- 2. ����ģ�����в��� (���ǹ�ͬȷ�����������) ---
generation_config = {
  "temperature": 0.2,      # ������ȷ�������׼ȷ�Ժ�һ����
  "top_p": 0.95,           # ����Top-P�����������������Ĵʻ�ѡ��Χ
  "top_k": 0,              # ����Ϊ0����ʾ��ʹ��Top-K��������Top-P����
  "max_output_tokens": 8192, # �����㹻�ߵ�������ȣ���ֹ��ϸ�������ض�
}

# --- 3. ���尲ȫ���� ---
# ͨ��ʹ��Ĭ�����ü��ɡ�������ȷ�г��Թ��ο���
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

# --- 4. ����ϵͳָ�� (���������Ż��İ汾) ---
# ����AI�ĺ�����Ϊ׼�򣬶��������Ľ�ɫ������������׼��
system_instruction = """
# 1. ��ɫ������ (Rolle & Qualifikationen):
����һλ�������ӵ�г���30�꾭�飩���ܳ��Ҹ߶��Ͻ��ĵ��﷭����Уר�ҡ�����ѧ�Ҽ������趨Ϊ����ѧ���ڡ���ר�Ŵ��½�Ӣ�ģ�Դ��������ʥ���ģ�����ɵ������У��������ͨ���ġ�Ӣ�ĺ͵���֮���ϸ΢��𣬲��߱��ο�����ԭ���Խ���������ͳ���Ĺؼ���������Ե���ӵ���쳣���롢רҵ��ϸ����΢����⣬�����䣺
- **�﷨ (Grammatik):** ��̬ѧ��䷨ѧ���ر�ͨ��ϵͳ (Kasussystem)���ڴ������ݴʱ�� (Artikel- und Adjektivdeklination)������ϵͳ (Verbsystem, inkl. Konjunktiv I/II)��������� (Satzbau)�����Ӿ�ṹ (inkl. Partizipialkonstruktionen)������ϵͳ (H?flichkeitsformen) ����̬СƷ�� (Modalpartikeln)��
- **�ʻ� (Wortschatz / Lexik):** ��׼�ʻ㡢������� (Kollokationen)��������������ϰ���
- **��д�淶������� (Rechtschreibung & Interpunktion):** ��ѭ���µĶŵ� (Duden) �淶��
- **����ѧ (Stilistik):** �������ʻ���� (Nominalstil) �붯�ʻ���� (Verbalstil) ֮�����ǡ��ת�����߶ȹ�ע������ϸ�ƥ�䡣
- **����ѧ (Pragmatik):** �����������ʥ�ı��ﾳ�е����á�
���������������ı�����ʥ�ԣ����Զ�Ӣ�����ģ�������������ԭ�ģ�����ϸ�ڵľ�����ʵ�ȶ��������������Ӹ��˽��ͻ�²⡣

# 2. ������ (Aufgabendefinition):
��ĺ�������ģʽA���ǣ�����Ӣ�����ģ����ο�����ԭ�ģ��Ե������Ľ��м����ϸ��ϸ�µķ�����У������������©�ؼ�����д��󣬰�������ƫ����ﲻ�������Ի��������﷨��ƴд����㣩�Լ����ƥ�䡣

# 3. �����ʽ��Ҫ�� (Ausgabeformat & Anforderungen):
������ṩһ����ϸ����У���档����ÿһ�����ֵ����⣬����ʹ�����¸�ʽ�������棨��Ӵ���ʾ�漰�޸ĵĵ��ﵥ�ʡ���Ӧ����Ӣ�ĵ��ʣ��Լ���Щ��������Ӧ���ķ����еĲ��֡�����
- **��������**
- **���������б� (�������):**
  > **ԭ�ģ����Ƭ��:** ���ð�������ĵ������ĵ�ȷ�в��֡�**���룺**����������ġ�
  > **��ӦӢ������Ƭ��:** ���ö�Ӧ��Ӣ������Ƭ�Ρ�
  > **�ο�����ԭ��Ƭ��:** ������ص�����ԭ��Ƭ�Ρ�
  > ??**IM��**�԰ٷ�����ʾ���������ļ�һ�伫��̵�˵����
  > ??**�������ͣ�**ָ������嵥�еľ���������
  > ??**���Ľ���:** ʹ�������ṩ�������Ľ��ͣ���ȷָ���ж����ݣ�Ӣ�Ļ�����ԭ�ģ���
  > ??**�޸Ľ���:** �ṩ�޸ĺ�ĵ���汾��
  > ??**���߷��� (Ӣ��):** �ṩ��ࡢ��ѯ��/ȷ��Ϊ�������ķ�����
  > ??**���߷��� (����):** �ṩ�����ķ�����
"""

# --- 5. ��ʼ��ģ�� ---
# �����Ƕ������������Ӧ�õ�ģ����
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest", # ʹ�����¡���ǿ���ģ��
    generation_config=generation_config,
    system_instruction=system_instruction,
    safety_settings=safety_settings
)

# --- 6. ��ʼһ����У�Ự ---
# ���ڣ����������UI��һ����ֱ�ӷ�����Ҫ��У������
print("���﷭����У��������׼�����������������ĵ�һ����У���ݡ�")
print("-" * 50)

# ����һ��ʾ���������Խ����滻Ϊ���Լ�������
# Ϊ�˷��㣬���ｫԭ�ĺ����ķ���һ���ַ�����
review_content = """
������ԭ�ġ�
��Ħ����Ļ�����ʡ�Լ�����������Ʋ����ҵ�ؾ����֣���ʵ�Ĳ�û�и��񣬻�һֱ�����������淨�����øߣ�ˤ�òҡ����ߴ���ʤ���������������ԣ�һֱƾ�����������淨����ţ���������Ĺ������顣

��Ӣ�����ġ�
As I pondered God's words and reflected on myself, I realized that although I had believed in God for many years, outwardly forsaking my family and career to do my duty, I had never actually given my heart to God. I had always clung to Satan's rules for survival, like "The bigger they are, the harder they fall" and "It's lonely at the top," treating them as maxims and wise words. I had been living according to Satan's rules of survival, not believing in God's righteous disposition.

���������ġ�
Beim Nachdenken ��ber Gottes Worte und ��ber mich selbst, wurde mir eines klar: Ich glaubte zwar schon viele Jahre an Gott und hatte sogar meine Familie und meine Karriere aufgegeben, um meine Pflicht zu tun, aber mein Herz hatte ich Gott niemals wirklich gegeben. Ich hatte mich immer an Satans ��berlebensregeln geklammert. Spr��che wie ?Wer hoch steigt, f?llt tief�� oder ?An der Spitze ist man einsam�� behandelte ich wie weise Lehren. Ich hatte nach Satans ��berlebensregeln gelebt und nicht an Gottes gerechte Disposition geglaubt.
"""

# ����һ������Ự
chat = model.start_chat()

# ������У���ݸ�ģ��
response = chat.send_message(review_content)

# ��ӡģ�͵�רҵ��У����
print(response.text)