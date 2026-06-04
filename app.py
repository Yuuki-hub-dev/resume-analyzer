import streamlit as st
import tempfile
import os
from resume_parser import parse_resume
from llm_analyzer import analyze_resume_job_match

st.set_page_config(page_title="智能简历分析助手", page_icon="📄", layout="wide")

st.title("📄 智能简历分析助手系统")
st.markdown("---")

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📁 上传简历")
    uploaded_file = st.file_uploader("选择简历文件", type=["pdf", "docx"])
    if uploaded_file is not None:
        st.success(f"已上传：{uploaded_file.name}")
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name
        file_ext = uploaded_file.name.split('.')[-1].lower()
        with st.spinner("正在解析简历..."):
            resume_text = parse_resume(tmp_path, file_ext)
        os.unlink(tmp_path)
        st.session_state['resume_text'] = resume_text
        st.session_state['resume_filename'] = uploaded_file.name
        if "错误" not in resume_text and len(resume_text) > 100:
            st.success(f"✅ 解析成功，提取 {len(resume_text)} 字符")
        else:
            st.error(f"❌ 解析失败：{resume_text}")
    else:
        st.session_state['resume_text'] = ""

with col_right:
    st.subheader("💼 岗位描述")
    job_description = st.text_area("请输入目标岗位描述（JD）", height=300,
        placeholder="例如：\n\n岗位名称：Python开发工程师\n\n岗位职责：\n1. 负责后端服务开发\n2. 参与系统架构设计\n\n任职要求：\n1. 熟练掌握Python\n2. 熟悉SQL数据库\n3. 了解Docker容器技术")
    st.session_state['job_description'] = job_description

st.markdown("---")

if st.button("🔍 开始分析"):
    if not st.session_state.get('resume_text'):
        st.error("请先上传简历文件")
    elif not job_description:
        st.error("请输入岗位描述")
    else:
        with st.spinner("AI 正在分析中，请稍候..."):
            result = analyze_resume_job_match(st.session_state['resume_text'], job_description)
        st.subheader("📊 分析结果")
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.metric("匹配度", f"{result.get('match_score', 0)} 分")
            st.markdown("**✅ 匹配的技能**")
            for skill in result.get('matched_skills', []):
                st.markdown(f"- {skill}")
            st.markdown("**❌ 缺失的技能**")
            for skill in result.get('missing_skills', []):
                st.markdown(f"- {skill}")
        with col_res2:
            st.markdown("**💡 优化建议**")
            st.write(result.get('suggestions', '无'))
            st.markdown("**🎯 面试问题预测**")
            for q in result.get('interview_questions', []):
                st.markdown(f"- {q}")

st.markdown("---")
st.caption("提示：系统将根据简历与岗位描述的匹配度，生成优化建议和面试问题")