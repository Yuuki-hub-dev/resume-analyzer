import os
import json
import re
from openai import OpenAI

# 首先尝试从环境变量获取（如果有的话）
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# 如果环境变量中没有，则询问用户输入
if not DEEPSEEK_API_KEY:
    DEEPSEEK_API_KEY = input("请输入你的 DeepSeek API Key（输入后按回车）: ").strip()
    if not DEEPSEEK_API_KEY:
        raise ValueError("API Key 不能为空")

DEEPSEEK_BASE_URL = "https://api.deepseek.com"

def analyze_resume_job_match(resume_text, job_description):
    system_prompt = """
你是一位专业的HR简历分析师。请根据简历和岗位描述，进行人岗匹配分析。
严格按照以下JSON格式输出，不要输出其他内容：
{
    "match_score": 85,
    "matched_skills": ["Python", "SQL"],
    "missing_skills": ["Docker"],
    "suggestions": "1. 建议补充Docker技能...\\n2. 量化项目经历...",
    "interview_questions": ["1. 请介绍一下你的Python项目经验", "2. 如何处理数据库性能问题"]
}
"""
    user_prompt = f"""
【岗位描述】：
{job_description}

【简历内容】：
{resume_text}

请分析并输出JSON格式结果。
"""
    client = OpenAI(
        api_key=DEEPSEEK_API_KEY,
        base_url=DEEPSEEK_BASE_URL
    )
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7
    )
    result_text = response.choices[0].message.content
    try:
        result = json.loads(result_text)
    except:
        json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
        else:
            result = {
                "match_score": 0,
                "matched_skills": [],
                "missing_skills": [],
                "suggestions": "分析失败，请重试",
                "interview_questions": []
            }
    return result