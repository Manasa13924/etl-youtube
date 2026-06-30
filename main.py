import os
import streamlit as st
import pandas as pd
import sqlite3
import json
import time
import subprocess
import joblib
from googleapiclient.discovery import build
import google.generativeai as genai
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="ViralVision AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. PROFESSIONAL CUSTOM CSS
if 'theme' not in st.session_state:
    st.session_state.theme = "Dark"

if st.session_state.theme == "Dark":
    primary = "#2563eb"
    primary_hover = "#1d4ed8"
    app_bg = "#0f172a"
    sidebar_bg = "#0b0f19"
    card_bg = "#1e293b"
    text_color = "#f8fafc"
    text_muted = "#94a3b8"
    border_color = "#334155"
    plotly_template = "plotly_dark"
    wc_bg = "#111827"
    wc_colormap = "viridis"
else:
    primary = "#2563eb"
    primary_hover = "#1d4ed8"
    app_bg = "#f8fafc"
    sidebar_bg = "#f1f5f9"
    card_bg = "#ffffff"
    text_color = "#0f172a"
    text_muted = "#475569"
    border_color = "#e2e8f0"
    plotly_template = "plotly_white"
    wc_bg = "#ffffff"
    wc_colormap = "plasma"

st.markdown(f'''    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    :root {{
        --primary-blue: {primary};
        --card-bg: {card_bg};
        --border-color: {border_color};
        --text-color: {text_color};
        --text-muted: {text_muted};
        --bg-color: {app_bg};
    }}

    /* ── Global background ── */
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"],
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"],
    section.main > div {{
        background-color: var(--bg-color) !important;
    }}

    /* ── All readable text ── */
    h1, h2, h3, h4, h5, h6 {{
        color: var(--text-color) !important;
    }}
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stMarkdownContainer"] strong,
    [data-testid="stMarkdownContainer"] em,
    [data-testid="stMarkdownContainer"] code {{
        color: var(--text-color) !important;
    }}
    [data-testid="stText"] {{
        color: var(--text-color) !important;
    }}
    [data-testid="stCaptionContainer"] p {{
        color: var(--text-muted) !important;
    }}

    /* ── Subheader ── */
    [data-testid="stHeadingWithActionElements"] *,
    .stSubheader, .stSubheader * {{
        color: var(--text-color) !important;
    }}

    /* ── Metric cards ── */
    [data-testid="stMetric"] {{
        background: var(--card-bg) !important;
        border: 1px solid var(--border-color) !important;
        padding: 20px !important;
        border-radius: 12px !important;
    }}
    [data-testid="stMetricValue"],
    [data-testid="stMetricLabel"],
    [data-testid="stMetricDelta"] {{
        color: var(--text-color) !important;
    }}

    /* ── Alert / info / warning / success boxes ── */
    [data-testid="stAlert"] p,
    [data-testid="stAlert"] li,
    div[data-testid="stInfo"] p,
    div[data-testid="stWarning"] p,
    div[data-testid="stSuccess"] p,
    div[data-testid="stError"] p {{
        color: var(--text-color) !important;
    }}

    /* ── Labels and radio buttons ── */
    label, .stRadio label, .stCheckbox label, .stSelectbox label {{
        color: var(--text-color) !important;
    }}

    /* ── Form inputs ── */
    .stTextInput input,
    .stTextArea textarea,
    .stNumberInput input,
    .stSelectbox div[data-baseweb="select"] {{
        background-color: var(--card-bg) !important;
        color: var(--text-color) !important;
        border: 1px solid var(--border-color) !important;
    }}
    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder {{
        color: var(--text-muted) !important;
        opacity: 1 !important;
    }}
    .stTextInput input:focus,
    .stTextArea textarea:focus,
    .stNumberInput input:focus {{
        border-color: var(--primary-blue) !important;
        box-shadow: 0 0 0 1px var(--primary-blue) !important;
    }}

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {{
        background-color: {sidebar_bg} !important;
        border-right: 1px solid var(--border-color);
    }}
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] small,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{
        color: var(--text-color) !important;
    }}

    /* ── Buttons ── */
    div.stButton > button,
    div.stFormSubmitButton > button,
    div.stDownloadButton > button,
    button[data-testid="baseButton-secondary"],
    button[data-testid="baseButton-primary"] {{
        border-radius: 8px !important;
        background-color: var(--primary-blue) !important;
        color: white !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        border: 1px solid var(--primary-blue) !important;
        width: 100% !important;
        padding: 8px 16px !important;
    }}
    div.stButton > button:hover,
    div.stFormSubmitButton > button:hover,
    div.stDownloadButton > button:hover,
    button[data-testid="baseButton-secondary"]:hover,
    button[data-testid="baseButton-primary"]:hover {{
        background-color: {primary_hover} !important;
        color: white !important;
        border-color: {primary_hover} !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(37,99,235,0.35) !important;
    }}
    div.stButton > button:active,
    div.stFormSubmitButton > button:active,
    div.stDownloadButton > button:active {{
        background-color: #1e40af !important;
        border-color: #1e40af !important;
        color: white !important;
        transform: translateY(0px) !important;
    }}
    div.stButton > button:focus,
    div.stFormSubmitButton > button:focus,
    div.stDownloadButton > button:focus {{
        outline: none !important;
        box-shadow: 0 0 0 2px rgba(37,99,235,0.4) !important;
        color: white !important;
    }}

    /* ── Video card ── */
    .video-card {{
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        padding: 20px;
        border-radius: 16px;
        margin-bottom: 20px;
    }}
    .video-card h3, .video-card p {{
        color: var(--text-color) !important;
    }}

    /* ── Tabs ── */
    [data-baseweb="tab-list"] {{
        background-color: var(--bg-color) !important;
        border-bottom: 1px solid var(--border-color) !important;
    }}
    [data-baseweb="tab"] {{
        color: var(--text-muted) !important;
        font-weight: 600 !important;
        background-color: transparent !important;
    }}
    [data-baseweb="tab"][aria-selected="true"] {{
        color: var(--text-color) !important;
        border-bottom: 2px solid var(--primary-blue) !important;
    }}

    /* ── Chat messages ── */
    [data-testid="stChatMessage"] p {{
        color: var(--text-color) !important;
    }}

    .js-plotly-plot .plotly .main-svg {{
        border-radius: 12px;
    }}
    </style>''', unsafe_allow_html=True)


# 3. SESSION STATE INITIALIZATION
if 'theme' not in st.session_state:
    st.session_state.theme = "Dark"  # Default theme

# Theme selector in sidebar
with st.sidebar:
    st.markdown("## 🎨 Theme")
    selected_theme = st.radio("Select Theme", ["Dark", "Light"], index=0 if st.session_state.theme == "Dark" else 1)
    if selected_theme != st.session_state.theme:
        st.session_state.theme = selected_theme
        try:
            st.rerun()
        except AttributeError:
            st.experimental_rerun()

if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'market_summary' not in st.session_state:
    st.session_state.market_summary = ""
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# --- Tab 4: Channel & Competitor persistence ---
if 'single_channel_data' not in st.session_state:
    st.session_state.single_channel_data = None
if 'single_channel_query' not in st.session_state:
    st.session_state.single_channel_query = ""
if 'competitor_data_a' not in st.session_state:
    st.session_state.competitor_data_a = None
if 'competitor_data_b' not in st.session_state:
    st.session_state.competitor_data_b = None
if 'competitor_ai_analysis' not in st.session_state:
    st.session_state.competitor_ai_analysis = ""
if 'competitor_query_a' not in st.session_state:
    st.session_state.competitor_query_a = ""
if 'competitor_query_b' not in st.session_state:
    st.session_state.competitor_query_b = ""

# --- Tab 5: Title Generator & Script Outline persistence ---
if 'viral_metadata_result' not in st.session_state:
    st.session_state.viral_metadata_result = ""
if 'viral_metadata_concept' not in st.session_state:
    st.session_state.viral_metadata_concept = ""
if 'script_outline_result' not in st.session_state:
    st.session_state.script_outline_result = ""
if 'script_outline_concept' not in st.session_state:
    st.session_state.script_outline_concept = ""

# 4. SIDEBAR - PLATFORM CONTROLS
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    st.markdown("Configure your access credentials to enable live data fetching and AI analysis.")

    with st.container(border=True):
        st.markdown("**🔑 API Keys**")
        youtube_key = st.text_input("YouTube Data v3 API", type="password", help="Required for live search results.")
        gemini_key = st.text_input("Google Gemini API", type="password", help="Required for deep market analysis and the chatbot.")

        if not youtube_key or not gemini_key:
            st.warning("⚠️ Both API keys are required.")
        else:
            st.success("✅ APIs Configured")

    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.caption("AI Video Intelligence Platform v2.5")
    st.caption("© 2026 Professional Grade Analytics")

# 5. DATA & MODEL LOADING FUNCTIONS
@st.cache_data
def load_db_data(query):
    try:
        if not os.path.exists("data/trends.db"): return pd.DataFrame()
        conn = sqlite3.connect("data/trends.db")
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        return pd.DataFrame()

@st.cache_resource
def load_prediction_model():
    model_path = "scripts/saved_models/view_count_rf_model.joblib"
    if os.path.exists(model_path):
        return joblib.load(model_path)
    return None

def fetch_youtube_data(query, api_key, max_results=5):
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        search_response = youtube.search().list(q=query, part='id,snippet', maxResults=max_results, type='video', order='relevance').execute()
        video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]
        if not video_ids: return []
        videos_response = youtube.videos().list(id=','.join(video_ids), part='snippet,statistics,contentDetails').execute()
        data = []
        for v in videos_response.get('items', []):
            data.append({
                "id": v['id'], "title": v['snippet']['title'], "channel": v['snippet']['channelTitle'],
                "description": v['snippet']['description'][:300], "views": int(v['statistics'].get('viewCount', 0)),
                "likes": int(v['statistics'].get('likeCount', 0)), "publishedAt": v['snippet']['publishedAt'],
                "thumbnail": v['snippet']['thumbnails']['high']['url']
            })
        return data
    except Exception as e:
        st.error(f"YouTube Error: {str(e)}")
        return []

def analyze_with_gemini(video_data, api_key):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"Analyze these videos for market relevance. Return ONLY JSON list with keys: id, score, reasoning, engagement_potential_label. Videos: {json.dumps([{k: v[k] for k in ('id', 'title', 'channel', 'description')} for v in video_data])}"
        response = model.generate_content(prompt)
        raw_text = response.text.strip().replace('```json', '').replace('```', '')
        return json.loads(raw_text)
    except Exception as e:
        st.error(f"Gemini Error: {str(e)}")
        return []

def get_market_summary(video_data, api_key):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"Summarize market trends for these videos in 2 sentences: {[v['title'] for v in video_data]}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except: return "Market trend analysis currently unavailable."

def fetch_channel_data(channel_name, api_key):
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        search_resp = youtube.search().list(q=channel_name, type='channel', part='id', maxResults=1).execute()
        if not search_resp.get('items'): return None
        channel_id = search_resp['items'][0]['id']['channelId']
        
        channel_resp = youtube.channels().list(id=channel_id, part='statistics,snippet').execute()
        info = channel_resp['items'][0]
        
        vid_resp = youtube.search().list(channelId=channel_id, type='video', order='viewCount', part='id', maxResults=5).execute()
        video_ids = [item['id']['videoId'] for item in vid_resp.get('items', [])]
        
        top_videos = []
        if video_ids:
            vid_details = youtube.videos().list(id=','.join(video_ids), part='snippet,statistics').execute()
            for v in vid_details.get('items', []):
                top_videos.append({
                    "title": v['snippet']['title'],
                    "views": int(v['statistics'].get('viewCount', 0)),
                    "likes": int(v['statistics'].get('likeCount', 0))
                })
                
        return {
            "title": info['snippet']['title'],
            "description": info['snippet']['description'],
            "thumbnail": info['snippet']['thumbnails']['high']['url'],
            "subscribers": int(info['statistics'].get('subscriberCount', 0)),
            "views": int(info['statistics'].get('viewCount', 0)),
            "video_count": int(info['statistics'].get('videoCount', 0)),
            "top_videos": top_videos
        }
    except Exception as e:
        st.error(f"Error fetching channel: {e}")
        return None

def extract_video_id(url):
    import re
    for pat in [r'(?:v=|/)([0-9A-Za-z_-]{11})', r'youtu\.be/([0-9A-Za-z_-]{11})']:
        m = re.search(pat, url)
        if m: return m.group(1)
    return None

def fetch_single_video(video_id, api_key):
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        resp = youtube.videos().list(id=video_id, part='snippet,statistics,contentDetails').execute()
        if not resp.get('items'): return None
        v = resp['items'][0]
        return {
            "id": v['id'], "title": v['snippet']['title'], "channel": v['snippet']['channelTitle'],
            "description": v['snippet']['description'][:500], "tags": v['snippet'].get('tags', [])[:10],
            "views": int(v['statistics'].get('viewCount', 0)), "likes": int(v['statistics'].get('likeCount', 0)),
            "comments": int(v['statistics'].get('commentCount', 0)), "thumbnail": v['snippet']['thumbnails']['high']['url'],
            "publishedAt": v['snippet']['publishedAt']
        }
    except Exception as e:
        st.error(f"Error fetching video: {e}")
        return None

def audit_video_with_gemini(video_data, api_key):
    try:
        genai.configure(api_key=api_key)
        m = genai.GenerativeModel('gemini-2.5-flash')
        eng = round(video_data['likes'] / max(video_data['views'], 1), 4)
        prompt = (
            "Audit this YouTube video. Return ONLY valid JSON with these exact keys: "
            "title_score (int 1-10), title_feedback (str), seo_score (int 1-10), seo_feedback (str), "
            "engagement_score (int 1-10), engagement_feedback (str), overall_score (int 1-10), "
            "strengths (list of 3 strings), improvements (list of 3 strings), verdict (str 2 sentences). "
            f"Video: Title={video_data['title']!r}, Channel={video_data['channel']!r}, "
            f"Views={video_data['views']}, Likes={video_data['likes']}, "
            f"Comments={video_data['comments']}, Engagement={eng}, "
            f"Tags={video_data['tags']}, Description={video_data['description'][:300]!r}"
        )
        response = m.generate_content(prompt)
        raw = response.text.strip().replace('```json', '').replace('```', '')
        return json.loads(raw)
    except Exception as e:
        st.error(f"Audit Error: {e}")
        return None

# 6. MAIN DASHBOARD UI
st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>ViralVision AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>Professional Grade Video Analytics & Market Research</p>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Trending Insights", "Market Intelligence", "Performance Predictor", "Channels & Competitors", "Viral Title Generator", "Video Score Card"])

# --- TAB 2: MARKET INTELLIGENCE ---
with tab2:
    st.subheader("Deep Market Analysis")
    col1, col2 = st.columns([3, 1])
    with col1:
        search_topic = st.text_input("Enter Search Topic", placeholder="e.g. Future of Generative AI 2026")
    with col2:
        max_res = st.slider("Samples", 3, 10, 5)
    
    if st.button("Run Analysis"):
        if not youtube_key or not gemini_key:
            st.error("Please provide both API keys in the sidebar.")
        elif not search_topic:
            st.warning("Please enter a search topic.")
        else:
            with st.spinner("Analyzing samples..."):
                raw_vids = fetch_youtube_data(search_topic, youtube_key, max_res)
                if raw_vids:
                    evals = analyze_with_gemini(raw_vids, gemini_key)
                    if evals:
                        st.session_state.analysis_results = pd.merge(pd.DataFrame(raw_vids), pd.DataFrame(evals), on="id").sort_values(by="score", ascending=False)
                        st.session_state.market_summary = get_market_summary(raw_vids, gemini_key)
    
    if st.session_state.analysis_results is not None:
        df = st.session_state.analysis_results
        st.info(f"**Market Insight:** {st.session_state.market_summary}")
        
        report_text = f"Market Insight:\n{st.session_state.market_summary}\n\nTop Videos:\n"
        for _, r in df.iterrows():
            report_text += f"- {r['title']} ({r['channel']}): Score {r['score']}/10. {r['reasoning']}\n"
        st.download_button("📥 Download Market Summary", data=report_text, file_name=f"market_summary_{search_topic.replace(' ', '_')}.txt", mime="text/plain")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Avg Quality Score", f"{df['score'].mean():.1f}/10")
        m2.metric("Total Views Analyzed", f"{df['views'].sum():,}")
        m3.metric("Top Recommended Channel", df.iloc[0]['channel'])
        
        st.markdown("#### Top Ranked Recommendations")
        for i, row in df.iterrows():
            with st.container():
                st.markdown(f"""
                    <div class="video-card">
                        <h3 style='margin-bottom: 5px; color: {text_color};'>#{i+1}: {row['title']}</h3>
                        <p style='color: #3b82f6; font-weight: 600;'>{row['channel']} | Score: {row['score']}/10</p>
                        <p style='color: {text_muted};'>{row['reasoning']}</p>
                    </div>
                """, unsafe_allow_html=True)
                if i == 0:
                    st.video(f"https://www.youtube.com/watch?v={row['id']}")

    # Chatbot Section
    st.markdown("---")
    st.markdown("### Intelligence Consultant")
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])
    
    if chat_input := st.chat_input("Ask about these results..."):
        st.session_state.chat_history.append({"role": "user", "content": chat_input})
        with st.chat_message("user"): st.markdown(chat_input)
        with st.chat_message("assistant"):
            try:
                genai.configure(api_key=gemini_key)
                model = genai.GenerativeModel('gemini-2.5-flash')
                ctx = f"Context: {st.session_state.analysis_results[['title', 'score']].to_dict() if st.session_state.analysis_results is not None else 'None'}"
                resp = model.generate_content(f"{ctx}\nQuestion: {chat_input}")
                st.markdown(resp.text)
                st.session_state.chat_history.append({"role": "assistant", "content": resp.text})
            except: st.error("Chat error. Check API key.")

# --- TAB 1: TRENDING INSIGHTS ---
with tab1:
    st.subheader("Historical Trends & Sentiment")
    
    df_trends = load_db_data("SELECT * FROM trending_videos")
    df_sent = load_db_data("SELECT * FROM video_sentiments")
    
    if not df_trends.empty:
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.markdown("#### Views per Category")
            cat_views = df_trends.groupby('category_name')['views'].sum().sort_values(ascending=False).head(10)
            fig_cat = px.bar(cat_views, orientation='h', color=cat_views.values, color_continuous_scale='Viridis', labels={'views': 'Total Views', 'category_name': 'Category'})
            fig_cat.update_layout(
                template=plotly_template,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color=text_color),
                xaxis=dict(tickfont=dict(color=text_color), title_font=dict(color=text_color), gridcolor=border_color),
                yaxis=dict(tickfont=dict(color=text_color), title_font=dict(color=text_color), gridcolor=border_color),
                coloraxis_colorbar=dict(tickfont=dict(color=text_color), title_font=dict(color=text_color))
            )
            st.plotly_chart(fig_cat, use_container_width=True)
            
        with col_t2:
            st.markdown("#### Sentiment Distribution")
            if not df_sent.empty:
                sent_counts = df_sent['sentiment_label'].value_counts()
                fig_sent = px.pie(values=sent_counts.values, names=sent_counts.index, hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
                fig_sent.update_layout(
                    template=plotly_template,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color=text_color),
                    legend=dict(font=dict(color=text_color))
                )
                st.plotly_chart(fig_sent, use_container_width=True)
            else: st.warning("Sentiment data not yet available. Train models first.")

        if 'show_advanced' not in st.session_state:
            st.session_state.show_advanced = False
            
        if st.button("Load Advanced Insights (Word Cloud, Heatmap)"):
            st.session_state.show_advanced = not st.session_state.show_advanced
            
        if st.session_state.show_advanced:
            st.markdown("#### Engagement Heatmap (Category vs. Publish Hour)")
            heatmap_data = df_trends.pivot_table(index='category_name', columns='publish_hour', values='engagement_ratio', aggfunc='mean').fillna(0)
            fig_heat = px.imshow(heatmap_data, labels=dict(x="Hour of Day (UTC)", y="Category", color="Avg Engagement"), color_continuous_scale='Plasma')
            fig_heat.update_layout(
                template=plotly_template,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color=text_color),
                xaxis=dict(tickfont=dict(color=text_color), title_font=dict(color=text_color)),
                yaxis=dict(tickfont=dict(color=text_color), title_font=dict(color=text_color)),
                coloraxis_colorbar=dict(tickfont=dict(color=text_color), title_font=dict(color=text_color))
            )
            st.plotly_chart(fig_heat, use_container_width=True)

            st.markdown("#### Most Common Keywords (Word Cloud)")
            all_titles = " ".join(df_trends['title'].dropna())
            wc = WordCloud(width=800, height=400, background_color=wc_bg, colormap=wc_colormap).generate(all_titles)
            fig_wc, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(wc, interpolation='bilinear')
            ax.axis("off")
            fig_wc.patch.set_facecolor(wc_bg)
            st.pyplot(fig_wc)

            st.markdown("#### Top 5 Most Liked Videos")
            top_liked = df_trends.sort_values(by='likes', ascending=False).head(5)
            for i, row in top_liked.iterrows():
                st.markdown(f"**#{i+1}: {row['title']}** — 👍 {row['likes']:,} Likes | 👁️ {row['views']:,} Views")

            st.markdown("#### Best Time to Post")
            if 'publish_hour' in df_trends.columns:
                btp = df_trends.groupby('publish_hour')['views'].mean().reset_index()
                btp.columns = ['Hour (UTC)', 'Avg Views']
                fig_btp = px.bar(btp, x='Hour (UTC)', y='Avg Views', color='Avg Views',
                    color_continuous_scale='Viridis', title="Average Views by Publish Hour (UTC)")
                fig_btp.update_layout(
                    template=plotly_template,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color=text_color),
                    title_font=dict(color=text_color),
                    xaxis=dict(tickfont=dict(color=text_color), title_font=dict(color=text_color), gridcolor=border_color),
                    yaxis=dict(tickfont=dict(color=text_color), title_font=dict(color=text_color), gridcolor=border_color),
                    coloraxis_colorbar=dict(tickfont=dict(color=text_color), title_font=dict(color=text_color))
                )
                st.plotly_chart(fig_btp, use_container_width=True)
                peak = int(btp.loc[btp['Avg Views'].idxmax(), 'Hour (UTC)'])
                st.success(f"📊 **Optimal upload window: {peak:02d}:00–{(peak+1)%24:02d}:00 UTC** — historically yields the highest average views.")
    else: st.info("Database is empty. Run ETL in the next tab.")

# --- TAB 3: PERFORMANCE PREDICTOR ---
with tab3:
    st.subheader("AI View Prediction Tool")
    model = load_prediction_model()
    
    if model:
        st.markdown("Predict potential view count based on engagement and timing.")
        with st.form("pred_form"):
            p_title = st.text_input("Potential Video Title")
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                all_cats = ["Autos & Vehicles", "Comedy", "Education", "Entertainment", "Film & Animation", "Gaming", "Howto & Style", "Music", "News & Politics", "Nonprofits & Activism", "People & Blogs", "Pets & Animals", "Science & Technology", "Shows", "Sports", "Travel & Events"]
                p_cat = st.selectbox("Category", all_cats)
                p_hour = st.slider("Publish Hour (UTC)", 0, 23, 12)
            with col_p2:
                p_eng = st.number_input("Expected Engagement Ratio (Likes/Views)", 0.0, 0.2, 0.05, format="%.3f")
            
            if st.form_submit_button("Predict Performance"):
                p_df = pd.DataFrame([{'category_name': p_cat, 'publish_hour': p_hour, 'engagement_ratio': p_eng}])
                p_res = model.predict(p_df)[0]
                st.success(f"### Predicted View Count: **{int(p_res):,}**")
    else: st.warning("Model not found. Please train models in the ETL tab.")

# --- TAB 4: CHANNELS & COMPETITORS ---
with tab4:
    st.subheader("YouTube Channel & Competitor Analysis")
    mode = st.radio("Select Mode", ["Single Channel Analyzer", "Competitor Battle"],
                    key="tab4_mode")

    # Helper to render single channel results
    def render_single_channel(c_data):
        st.markdown("---")
        c_img, c_info = st.columns([1, 4])
        with c_img:
            st.image(c_data['thumbnail'], use_column_width=True)
        with c_info:
            st.markdown(f"### {c_data['title']}")
            st.markdown(f"**Subscribers:** {c_data['subscribers']:,} &nbsp;|&nbsp; **Total Views:** {c_data['views']:,} &nbsp;|&nbsp; **Videos:** {c_data['video_count']:,}")
            desc = c_data['description']
            st.caption(desc[:400] + "..." if len(desc) > 400 else desc)
        st.markdown("#### Top 5 Most Viewed Videos")
        for i, v in enumerate(c_data['top_videos']):
            st.markdown(f"**#{i+1}: {v['title']}** — 👁️ {v['views']:,} Views | 👍 {v['likes']:,} Likes")

    # Helper to render competitor battle results
    def render_competitor_battle(data_a, data_b, ai_text):
        st.markdown("---")
        col_a, col_b = st.columns(2)
        with col_a:
            st.image(data_a['thumbnail'], width=80)
            st.markdown(f"### {data_a['title']}")
            st.metric("Subscribers", f"{data_a['subscribers']:,}")
            st.metric("Total Views", f"{data_a['views']:,}")
            st.metric("Video Count", f"{data_a['video_count']:,}")
        with col_b:
            st.image(data_b['thumbnail'], width=80)
            st.markdown(f"### {data_b['title']}")
            st.metric("Subscribers", f"{data_b['subscribers']:,}")
            st.metric("Total Views", f"{data_b['views']:,}")
            st.metric("Video Count", f"{data_b['video_count']:,}")
        if ai_text:
            st.markdown("---")
            st.markdown("#### AI Strategic Content Gap Analysis")
            st.info(ai_text)

    if mode == "Single Channel Analyzer":
        st.markdown("Enter any YouTube channel name to instantly retrieve its core statistics and top-performing videos.")
        col_c1, col_c2 = st.columns([3, 1])
        with col_c1:
            c_query = st.text_input("Enter Channel Name", placeholder="e.g. Marques Brownlee", key="single_q")

        if st.button("Analyze Channel", key="analyze_single_btn"):
            if not youtube_key:
                st.error("Please provide your YouTube API Key in the sidebar.")
            elif c_query:
                with st.spinner(f"Fetching data for '{c_query}'..."):
                    c_data = fetch_channel_data(c_query, youtube_key)
                    if c_data:
                        # Save to session state
                        st.session_state.single_channel_data = c_data
                        st.session_state.single_channel_query = c_query
                    else:
                        st.warning(f"Could not find '{c_query}'.")

        # Always render if data exists in state
        if st.session_state.single_channel_data is not None:
            if st.session_state.single_channel_query:
                st.caption(f"📊 Showing results for: **{st.session_state.single_channel_query}**")
            render_single_channel(st.session_state.single_channel_data)

    else:  # Competitor Battle
        st.markdown("Compare two channels side-by-side to discover content gaps and market positioning.")
        c_a, c_b = st.columns(2)
        with c_a:
            q_a = st.text_input("Channel A", placeholder="e.g. MKBHD", key="comp_a")
        with c_b:
            q_b = st.text_input("Channel B", placeholder="e.g. MrWhosetheboss", key="comp_b")

        if st.button("Start Competitor Battle", key="competitor_btn"):
            if not youtube_key or not gemini_key:
                st.error("Both YouTube and Gemini API keys are required.")
            elif q_a and q_b:
                with st.spinner("Fetching channel data and running AI analysis..."):
                    data_a = fetch_channel_data(q_a, youtube_key)
                    data_b = fetch_channel_data(q_b, youtube_key)
                    if data_a and data_b:
                        ai_text = ""
                        try:
                            genai.configure(api_key=gemini_key)
                            model = genai.GenerativeModel('gemini-2.5-flash')
                            desc_a = data_a.get('description', '') or 'No description available.'
                            desc_b = data_b.get('description', '') or 'No description available.'
                            p = (f"Compare these two YouTube channels based on their descriptions. "
                                 f"Channel A ({data_a['title']}): {desc_a[:500]}. "
                                 f"Channel B ({data_b['title']}): {desc_b[:500]}. "
                                 f"Give a 3 sentence professional analysis of their content gap and differing strategies.")
                            resp = model.generate_content(p)
                            ai_text = resp.text
                        except Exception as e:
                            st.error(f"AI Analysis failed: {str(e)}")
                        # Save everything to session state
                        st.session_state.competitor_data_a = data_a
                        st.session_state.competitor_data_b = data_b
                        st.session_state.competitor_ai_analysis = ai_text
                        st.session_state.competitor_query_a = q_a
                        st.session_state.competitor_query_b = q_b
                    else:
                        st.warning("Could not fetch data for one or both channels.")

        # Always render if data exists in state
        if st.session_state.competitor_data_a and st.session_state.competitor_data_b:
            if st.session_state.competitor_query_a and st.session_state.competitor_query_b:
                st.caption(f"📊 Showing results for: **{st.session_state.competitor_query_a}** vs **{st.session_state.competitor_query_b}**")
            render_competitor_battle(
                st.session_state.competitor_data_a,
                st.session_state.competitor_data_b,
                st.session_state.competitor_ai_analysis
            )

# --- TAB 5: TITLE GENERATOR ---
with tab5:
    st.subheader("Viral Title & SEO Generator")
    st.markdown("Provide a basic video concept, and our AI will generate highly optimized titles and metadata.")

    concept = st.text_area("Video Concept or Working Title",
                           placeholder="e.g. A review of the new iPhone 16 Pro focusing on its camera and battery life.")

    if st.button("Generate Viral Metadata", key="viral_meta_btn"):
        if not gemini_key:
            st.error("Please provide your Gemini API Key in the sidebar.")
        elif concept:
            with st.spinner("Generating psychological triggers and SEO tags..."):
                try:
                    genai.configure(api_key=gemini_key)
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    prompt = (
                        f"You are an expert YouTube SEO strategist. For this video concept: '{concept}'. Provide:\n"
                        "1. 5 highly optimized, click-worthy titles (mix of curiosity and search intent).\n"
                        "2. A list of the top 10 SEO tags (comma separated).\n"
                        "3. A professional, highly searchable 2-paragraph video description."
                    )
                    resp = model.generate_content(prompt)
                    # Persist to session state
                    st.session_state.viral_metadata_result = resp.text
                    st.session_state.viral_metadata_concept = concept
                except Exception as e:
                    st.error(f"Gemini Error: {e}")

    # Always render if result exists
    if st.session_state.viral_metadata_result:
        if st.session_state.viral_metadata_concept:
            st.caption(f"📝 Results for concept: **{st.session_state.viral_metadata_concept[:80]}{'...' if len(st.session_state.viral_metadata_concept) > 80 else ''}**")
        st.success("Generation Complete!")
        st.markdown(st.session_state.viral_metadata_result)

    st.markdown("---")
    st.markdown("### Script Outline Generator")
    st.markdown("Turn any title into a structured, ready-to-film script outline with hooks and timestamps.")
    outline_concept = st.text_input("Video Title for Script",
                                    placeholder="e.g. 5 AI Tools That Will Replace Programmers in 2026",
                                    key="outline_input")

    if st.button("Generate Script Outline", key="outline_btn"):
        if not gemini_key:
            st.error("Please provide your Gemini API Key in the sidebar.")
        elif outline_concept:
            with st.spinner("Crafting your script outline..."):
                try:
                    genai.configure(api_key=gemini_key)
                    mdl = genai.GenerativeModel('gemini-2.5-flash')
                    op = f"""You are a professional YouTube scriptwriter. Create a detailed script outline for: "{outline_concept}".
Format it with these sections:
🎬 HOOK (0:00–0:30): Opening line that instantly grabs attention
📌 INTRO (0:30–1:30): Context + what the viewer will learn
📖 MAIN SECTIONS: 4-5 titled sections with timestamps and 2-3 key talking points each
💡 KEY INSIGHT: The single most memorable takeaway
🚀 CTA (Closing): Subscribe prompt + next video suggestion
⏱ Estimated total runtime
Make it engaging, specific, and formatted clearly."""
                    or_ = mdl.generate_content(op)
                    # Persist to session state
                    st.session_state.script_outline_result = or_.text
                    st.session_state.script_outline_concept = outline_concept
                except Exception as e:
                    st.error(f"Gemini Error: {e}")

    # Always render if result exists
    if st.session_state.script_outline_result:
        if st.session_state.script_outline_concept:
            st.caption(f"📝 Outline for: **{st.session_state.script_outline_concept[:80]}{'...' if len(st.session_state.script_outline_concept) > 80 else ''}**")
        st.success("Script Outline Ready!")
        st.markdown(st.session_state.script_outline_result)
        st.download_button(
            "📥 Download Outline",
            data=st.session_state.script_outline_result,
            file_name=f"outline_{st.session_state.script_outline_concept[:25].replace(' ','_')}.txt",
            mime="text/plain"
        )

# --- TAB 6: VIDEO SCORE CARD ---
with tab6:
    st.subheader("Video Score Card")
    st.markdown("Paste any YouTube URL for a comprehensive AI audit — title quality, SEO, engagement, and actionable improvements.")
    video_url_input = st.text_input("YouTube Video URL", placeholder="https://www.youtube.com/watch?v=...", key="score_url")
    if st.button("Run Full Audit", key="audit_btn"):
        if not youtube_key or not gemini_key:
            st.error("Both API keys are required for this feature.")
        elif video_url_input:
            vid_id = extract_video_id(video_url_input)
            if not vid_id:
                st.error("Invalid YouTube URL. Please check the link and try again.")
            else:
                with st.spinner("Fetching video data and running AI audit..."):
                    v_data = fetch_single_video(vid_id, youtube_key)
                    if v_data:
                        audit = audit_video_with_gemini(v_data, gemini_key)
                        if audit:
                            st.markdown("---")
                            v_img, v_info = st.columns([1, 2])
                            with v_img:
                                st.image(v_data['thumbnail'], use_column_width=True)
                            with v_info:
                                st.markdown(f"### {v_data['title']}")
                                st.caption(f"**Channel:** {v_data['channel']} | **Published:** {v_data['publishedAt'][:10]}")
                                mi1, mi2, mi3 = st.columns(3)
                                mi1.metric("Views", f"{v_data['views']:,}")
                                mi2.metric("Likes", f"{v_data['likes']:,}")
                                mi3.metric("Comments", f"{v_data['comments']:,}")
                            st.markdown("---")
                            st.markdown("#### AI Audit Scores")
                            def score_icon(s):
                                return "🟢" if s >= 8 else ("🟡" if s >= 5 else "🔴")
                            sc1, sc2, sc3, sc4 = st.columns(4)
                            sc1.metric(f"{score_icon(audit.get('title_score',0))} Title", f"{audit.get('title_score','N/A')}/10")
                            sc2.metric(f"{score_icon(audit.get('seo_score',0))} SEO", f"{audit.get('seo_score','N/A')}/10")
                            sc3.metric(f"{score_icon(audit.get('engagement_score',0))} Engagement", f"{audit.get('engagement_score','N/A')}/10")
                            sc4.metric(f"{score_icon(audit.get('overall_score',0))} Overall", f"{audit.get('overall_score','N/A')}/10")
                            st.markdown(f"> 💬 **Verdict:** {audit.get('verdict', '')}")
                            col_s, col_i = st.columns(2)
                            with col_s:
                                st.markdown("**✅ Strengths**")
                                for s in audit.get('strengths', []):
                                    st.markdown(f"- {s}")
                            with col_i:
                                st.markdown("**🔧 Areas to Improve**")
                                for imp in audit.get('improvements', []):
                                    st.markdown(f"- {imp}")
                            st.markdown("**📝 Detailed Feedback**")
                            st.info(f"**Title:** {audit.get('title_feedback','')}  \n**SEO:** {audit.get('seo_feedback','')}  \n**Engagement:** {audit.get('engagement_feedback','')}")
