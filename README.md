# 情绪追踪应用 (Mood Tracker)

这是一个情绪追踪应用，提供HTML版本和Streamlit版本两种实现。

## 项目结构

```
my_first_app/
├── app.py              # Streamlit应用（推荐）
├── emotional_company.py # 原始HTML文件
├── requirements.txt    # Python依赖库
├── run_app.py         # 启动脚本
└── README.md          # 项目说明
```

## 本地调试方法

### 🚀 推荐：Streamlit版本（支持部署）

#### 方法1：使用启动脚本（最简单）
```bash
python run_app.py
```

#### 方法2：手动启动
```bash
# 安装依赖
pip install -r requirements.txt

# 启动应用
streamlit run app.py
```

应用将在浏览器中自动打开：`http://localhost:8501`

### 📱 HTML版本（仅本地使用）

#### 方法1：直接打开HTML文件
1. 将 `emotional_company.py` 重命名为 `index.html`
2. 双击文件，用浏览器打开

#### 方法2：使用Python内置服务器
```bash
python -m http.server 8000
```
访问：`http://localhost:8000`

#### 方法3：使用Live Server（VS Code扩展）
1. 安装Live Server扩展
2. 右键HTML文件，选择"Open with Live Server"

## 🚀 Streamlit部署

### 本地部署
```bash
streamlit run app.py
```

### 云端部署（Streamlit Cloud）
1. 将代码推送到GitHub
2. 访问 [share.streamlit.io](https://share.streamlit.io)
3. 连接GitHub仓库
4. 设置主文件为 `app.py`
5. 点击部署

### 其他平台部署
- **Heroku**: 支持Streamlit部署
- **Railway**: 简单易用的部署平台
- **Vercel**: 需要额外配置

## 当前应用功能

- ✅ 情绪选择（9种情绪）
- ✅ 情绪强度滑块
- ✅ 文字记录
- ✅ 图片上传
- ✅ 时间轴显示
- ✅ 情绪统计图表
- ✅ 响应式设计

## 技术栈

### Streamlit版本
- **后端框架**：Streamlit
- **数据处理**：Pandas
- **图表库**：Plotly
- **数据存储**：JSON文件

### HTML版本
- **前端框架**：纯HTML/CSS/JavaScript
- **样式框架**：Tailwind CSS
- **图标库**：Remix Icons
- **图表库**：ECharts
- **字体**：Google Fonts (Pacifico)

## 下一步开发建议

1. **添加后端功能**：使用Python Flask或FastAPI
2. **数据库集成**：SQLite或PostgreSQL
3. **用户认证**：登录注册功能
4. **数据持久化**：保存用户情绪记录
5. **移动端优化**：PWA支持 