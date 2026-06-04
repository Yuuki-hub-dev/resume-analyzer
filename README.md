# 智能简历分析助手系统

基于大语言模型（DeepSeek）的简历与岗位匹配分析工具，帮助求职者快速优化简历、预测面试问题。

## 功能特点

- 支持上传 PDF / Word 格式简历  
- 输入岗位描述（JD）后自动分析  
- 输出匹配度分数、匹配/缺失技能列表  
- 生成具体优化建议和面试问题  

## 技术栈

- Python 3.9  
- Streamlit（前端界面）  
- DeepSeek API（大模型推理）  
- PyPDF2 / python-docx（文档解析）  

## 快速开始

1. 克隆本仓库  
2. 安装依赖：`pip install streamlit PyPDF2 python-docx openai`  
3. 运行：`streamlit run app.py`  
4. 运行时输入你的 DeepSeek API Key（需提前注册获取）

## 注意事项

- 本系统不会存储你的 API Key，每次运行需要手动输入。  
- 生成的优化建议仅供参考，请结合实际情况修改简历。
