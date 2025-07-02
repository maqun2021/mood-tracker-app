import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import json
import os
import base64
from PIL import Image
import io

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
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .comment-card {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #5B8FF9;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .header-text {
        color: white;
        font-family: 'Pacifico', cursive;
        font-size: 2.5rem;
        text-align: center;
        margin-bottom: 20px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    .time-display {
        color: white;
        text-align: right;
        font-size: 1.1rem;
        font-weight: 500;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
    }
    .image-preview {
        border-radius: 8px;
        max-width: 100%;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .mood-button {
        background: linear-gradient(135deg, #5B8FF9, #FF85C0);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 20px;
        margin: 5px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 500;
    }
    .mood-button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .mood-entry {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #5B8FF9;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .mood-emoji {
        font-size: 2rem;
        margin-right: 10px;
    }
    .mood-info {
        font-weight: 600;
        color: #333;
    }
    .mood-time {
        color: #666;
        font-size: 0.9rem;
        font-style: italic;
    }
    .mood-thoughts {
        margin-top: 10px;
        padding: 10px;
        background: rgba(91, 143, 249, 0.1);
        border-radius: 6px;
        border-left: 3px solid #5B8FF9;
    }
</style>
""", unsafe_allow_html=True)

# 初始化session state
if 'mood_data' not in st.session_state:
    st.session_state.mood_data = []
if 'selected_mood' not in st.session_state:
    st.session_state.selected_mood = None
if 'comments' not in st.session_state:
    st.session_state.comments = []

# 情绪选项
moods = {
    'happy': {'emoji': '😊', 'name': '开心'},
    'calm': {'emoji': '😌', 'name': '平静'},
    'excited': {'emoji': '🤩', 'name': '兴奋'},
    'sad': {'emoji': '😢', 'name': '难过'},
    'tired': {'emoji': '😴', 'name': '疲惫'},
    'anxious': {'emoji': '😰', 'name': '焦虑'},
    'angry': {'emoji': '😠', 'name': '愤怒'},
    'loved': {'emoji': '🥰', 'name': '被爱'},
    'other': {'emoji': '🤔', 'name': '其他'}
}

def image_to_base64(image):
    """将图片转换为base64编码"""
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"

def save_mood_entry(mood, intensity, thoughts, image=None):
    """保存情绪记录"""
    entry = {
        'id': len(st.session_state.mood_data) + 1,
        'timestamp': datetime.now().isoformat(),
        'mood': mood,
        'intensity': intensity,
        'thoughts': thoughts,
        'image': image,
        'comments': []
    }
    st.session_state.mood_data.append(entry)
    
    # 保存到本地文件
    save_data_to_file()

def save_comment(mood_entry_id, commenter_name, comment_text):
    """保存评论"""
    comment = {
        'id': len(st.session_state.comments) + 1,
        'mood_entry_id': mood_entry_id,
        'commenter_name': commenter_name,
        'comment_text': comment_text,
        'timestamp': datetime.now().isoformat()
    }
    st.session_state.comments.append(comment)
    
    # 更新情绪记录的评论
    for entry in st.session_state.mood_data:
        if entry['id'] == mood_entry_id:
            entry['comments'].append(comment)
            break
    
    save_data_to_file()

def save_data_to_file():
    """保存所有数据到文件"""
    data = {
        'mood_data': st.session_state.mood_data,
        'comments': st.session_state.comments
    }
    with open('mood_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_mood_data():
    """加载情绪数据"""
    if os.path.exists('mood_data.json'):
        with open('mood_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            st.session_state.mood_data = data.get('mood_data', [])
            st.session_state.comments = data.get('comments', [])

def create_mood_chart():
    """创建情绪图表"""
    if not st.session_state.mood_data:
        return None
    
    # 准备数据
    df = pd.DataFrame(st.session_state.mood_data)
    df['date'] = pd.to_datetime(df['timestamp']).dt.date
    
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

def display_mood_entry(entry, show_comments=True):
    """显示单个情绪记录"""
    mood_info = moods[entry['mood']]
    timestamp = datetime.fromisoformat(entry['timestamp']).strftime("%m月%d日 %H:%M")
    
    # 创建卡片
    with st.container():
        st.markdown(f"""
        <div class="mood-entry">
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                <span class="mood-emoji">{mood_info['emoji']}</span>
                <div>
                    <div class="mood-info">{mood_info['name']} - 强度: {entry['intensity']}/10</div>
                    <div class="mood-time">{timestamp}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if entry['thoughts']:
            st.markdown(f"""
            <div class="mood-thoughts">
                {entry['thoughts']}
            </div>
            """, unsafe_allow_html=True)
        
        # 显示图片
        if entry.get('image'):
            try:
                # 如果是base64图片
                if entry['image'].startswith('data:image'):
                    st.markdown(f"""
                    <img src="{entry['image']}" class="image-preview" alt="情绪图片">
                    """, unsafe_allow_html=True)
                else:
                    st.write(f"📷 图片: {entry['image']}")
            except:
                st.write(f"📷 图片: {entry['image']}")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 显示评论
        if show_comments and entry.get('comments'):
            st.write("💬 评论:")
            for comment in entry['comments']:
                comment_time = datetime.fromisoformat(comment['timestamp']).strftime("%m月%d日 %H:%M")
                st.markdown(f"""
                <div class="comment-card">
                    <strong>{comment['commenter_name']}</strong> - <em>{comment_time}</em><br>
                    {comment['comment_text']}
                </div>
                """, unsafe_allow_html=True)
        
        # 添加评论功能
        if show_comments:
            with st.expander(f"💬 为这条记录添加评论"):
                commenter_name = st.text_input("你的名字", key=f"name_{entry['id']}")
                comment_text = st.text_area("评论内容", key=f"comment_{entry['id']}")
                
                if st.button("发表评论", key=f"submit_{entry['id']}"):
                    if commenter_name and comment_text:
                        save_comment(entry['id'], commenter_name, comment_text)
                        st.success("评论已发表！")
                        st.rerun()
                    else:
                        st.error("请填写名字和评论内容")
        
        st.divider()

def main():
    # 加载数据
    load_mood_data()
    
    # 头部
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.markdown('<div class="header-text">here with you</div>', unsafe_allow_html=True)
    
    with col3:
        # 实时更新时间
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
    
    # 图片上传（增强版）
    st.write("📷 添加照片（可选）")
    uploaded_file = st.file_uploader("选择图片", type=['png', 'jpg', 'jpeg'], key="mood_image")
    
    # 图片预览
    image_data = None
    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption="图片预览", use_column_width=True)
            
            # 转换为base64存储
            image_data = image_to_base64(image)
        except Exception as e:
            st.error(f"图片处理失败: {e}")
    
    # 保存按钮
    if st.button("保存记录", type="primary"):
        if st.session_state.selected_mood:
            save_mood_entry(
                mood=st.session_state.selected_mood,
                intensity=intensity,
                thoughts=thoughts,
                image=image_data
            )
            st.success("情绪记录已保存！")
            st.session_state.selected_mood = None
            st.rerun()
        else:
            st.error("请先选择一个情绪！")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 显示历史记录
    if st.session_state.mood_data:
        st.markdown('<div class="mood-card">', unsafe_allow_html=True)
        st.subheader("最近的情绪记录")
        
        # 显示最近10条记录
        recent_data = st.session_state.mood_data[-10:][::-1]
        for entry in recent_data:
            display_mood_entry(entry)
        
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
    
    # 评论统计
    if st.session_state.comments:
        st.markdown('<div class="mood-card">', unsafe_allow_html=True)
        st.subheader("💬 评论统计")
        st.write(f"总共有 {len(st.session_state.comments)} 条评论")
        
        # 显示最新评论
        recent_comments = st.session_state.comments[-5:][::-1]
        st.write("最新评论:")
        for comment in recent_comments:
            comment_time = datetime.fromisoformat(comment['timestamp']).strftime("%m月%d日 %H:%M")
            st.markdown(f"""
            <div class="comment-card">
                <strong>{comment['commenter_name']}</strong> - <em>{comment_time}</em><br>
                {comment['comment_text']}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main() 

