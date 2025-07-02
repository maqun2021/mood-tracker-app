import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os

# 页面配置
st.set_page_config(
    page_title="情绪追踪 - here with you",
    page_icon="😊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #5B8FF9, #FF85C0);
        min-height: 100vh;
    }
    .stApp {
        background: linear-gradient(135deg, #5B8FF9, #FF85C0);
    }
    .mood-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        backdrop-filter: blur(10px);
    }
    .mood-icon {
        display: inline-block;
        margin: 5px;
        padding: 10px;
        border-radius: 50%;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .mood-icon:hover {
        transform: scale(1.1);
    }
    .mood-icon.selected {
        border: 3px solid #5B8FF9;
        transform: scale(1.1);
    }
    .header-text {
        color: white;
        font-family: 'Pacifico', cursive;
        font-size: 2rem;
        text-align: center;
        margin-bottom: 20px;
    }
    .time-display {
        color: white;
        text-align: right;
        font-size: 1.2rem;
    }
</style>
""", unsafe_allow_html=True)

# 初始化session state
if 'mood_data' not in st.session_state:
    st.session_state.mood_data = []
if 'selected_mood' not in st.session_state:
    st.session_state.selected_mood = None

# 情绪选项
moods = {
    'happy': {'emoji': '😊', 'name': '开心', 'color': '#FEF3C7'},
    'calm': {'emoji': '😌', 'name': '平静', 'color': '#DBEAFE'},
    'excited': {'emoji': '🤩', 'name': '兴奋', 'color': '#F3E8FF'},
    'sad': {'emoji': '😢', 'name': '难过', 'color': '#BFDBFE'},
    'tired': {'emoji': '😴', 'name': '疲惫', 'color': '#E5E7EB'},
    'anxious': {'emoji': '😰', 'name': '焦虑', 'color': '#FEF3C7'},
    'angry': {'emoji': '😠', 'name': '愤怒', 'color': '#FEE2E2'},
    'loved': {'emoji': '🥰', 'name': '被爱', 'color': '#FCE7F3'},
    'other': {'emoji': '🤔', 'name': '其他', 'color': '#F3F4F6'}
}

def save_mood_entry(mood, intensity, thoughts, image=None):
    """保存情绪记录"""
    entry = {
        'timestamp': datetime.now().isoformat(),
        'mood': mood,
        'intensity': intensity,
        'thoughts': thoughts,
        'image': image
    }
    st.session_state.mood_data.append(entry)
    
    # 保存到本地文件
    with open('mood_data.json', 'w', encoding='utf-8') as f:
        json.dump(st.session_state.mood_data, f, ensure_ascii=False, indent=2)

def load_mood_data():
    """加载情绪数据"""
    if os.path.exists('mood_data.json'):
        with open('mood_data.json', 'r', encoding='utf-8') as f:
            st.session_state.mood_data = json.load(f)

def create_mood_chart():
    """创建情绪图表"""
    if not st.session_state.mood_data:
        return None
    
    # 准备数据
    df = pd.DataFrame(st.session_state.mood_data)
    df['date'] = pd.to_datetime(df['timestamp']).dt.date
    df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
    
    # 情绪分布饼图
    mood_counts = df['mood'].value_counts()
    fig_pie = px.pie(
        values=mood_counts.values,
        names=[moods[mood]['name'] for mood in mood_counts.index],
        title="情绪分布",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    # 情绪强度时间线
    fig_line = px.line(
        df, 
        x='timestamp', 
        y='intensity',
        title="情绪强度变化",
        labels={'intensity': '强度', 'timestamp': '时间'}
    )
    
    return fig_pie, fig_line

# 主应用
def main():
    # 加载数据
    load_mood_data()
    
    # 头部
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.markdown('<div class="header-text">here with you</div>', unsafe_allow_html=True)
    
    with col3:
        current_time = datetime.now().strftime("%Y年%m月%d日 %H:%M")
        st.markdown(f'<div class="time-display">{current_time}</div>', unsafe_allow_html=True)
    
    # 主要内容区域
    st.markdown('<div class="mood-card">', unsafe_allow_html=True)
    st.subheader("今天感觉怎么样？")
    
    # 情绪选择
    st.write("选择你的情绪：")
    cols = st.columns(3)
    
    for i, (mood_key, mood_info) in enumerate(moods.items()):
        with cols[i % 3]:
            if st.button(
                f"{mood_info['emoji']} {mood_info['name']}", 
                key=f"mood_{mood_key}",
                help=f"选择{mood_info['name']}情绪"
            ):
                st.session_state.selected_mood = mood_key
                st.success(f"已选择：{mood_info['name']}")
    
    # 情绪强度
    st.write("---")
    intensity = st.slider("情绪强度", 1, 10, 5, help="1=轻微，10=强烈")
    
    # 文字记录
    thoughts = st.text_area("有什么想法？", placeholder="写下你的想法...", height=100)
    
    # 图片上传
    uploaded_file = st.file_uploader("添加照片", type=['png', 'jpg', 'jpeg'])
    
    # 保存按钮
    if st.button("保存记录", type="primary"):
        if st.session_state.selected_mood:
            save_mood_entry(
                mood=st.session_state.selected_mood,
                intensity=intensity,
                thoughts=thoughts,
                image=uploaded_file.name if uploaded_file else None
            )
            st.success("情绪记录已保存！")
            st.session_state.selected_mood = None
        else:
            st.error("请先选择一个情绪！")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 显示历史记录
    if st.session_state.mood_data:
        st.markdown('<div class="mood-card">', unsafe_allow_html=True)
        st.subheader("最近的情绪记录")
        
        # 显示最近5条记录
        recent_data = st.session_state.mood_data[-5:][::-1]
        for entry in recent_data:
            mood_info = moods[entry['mood']]
            timestamp = datetime.fromisoformat(entry['timestamp']).strftime("%m月%d日 %H:%M")
            
            col1, col2 = st.columns([1, 3])
            with col1:
                st.markdown(f"### {mood_info['emoji']}")
            with col2:
                st.write(f"**{mood_info['name']}** - 强度: {entry['intensity']}/10")
                st.write(f"*{timestamp}*")
                if entry['thoughts']:
                    st.write(entry['thoughts'])
            st.divider()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 显示图表
        st.markdown('<div class="mood-card">', unsafe_allow_html=True)
        st.subheader("情绪分析")
        
        fig_pie, fig_line = create_mood_chart()
        if fig_pie and fig_line:
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(fig_pie, use_container_width=True)
            with col2:
                st.plotly_chart(fig_line, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main() 