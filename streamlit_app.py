import streamlit as st
from PIL import Image, ImageDraw
import io

# 設定頁面標題
st.set_page_config(page_title="圖片切分神器", layout="wide")
st.title("✂️ 圖片切分神器 (帶有預覽功能)")
st.markdown("透過預覽線條，確保你的切分位置完全正確！")

# --- 核心功能函數：繪製預覽線條 ---
def create_preview(img, num_parts, mode):
    """
    在圖片上繪製切分線作為預覽
    mode: 'rows' (橫向切分，產生水平線) 或 'columns' (縱向切 欄，產生垂直線)
    """
    preview_img = img.copy()
    draw = ImageDraw.Draw(preview_img)
    width, height = preview_img.size
    
    # 設定線條顏色 (亮青色，確保在各種背景都清晰)
    line_color = (0, 255, 255) 
    line_width = 5
    
    if mode == 'rows':
        # 產生水平線 (把圖片切成橫列)
        for i in range(1, num_parts):
            y = height * (i / num_parts)
            draw.line([(0, y), (width, y)], fill=line_color, width=line_width)
            
    elif mode == 'columns':
        # 產生垂直線 (把圖片切成直欄)
        for i in range(1, num_parts):
            x = width * (i / num_parts)
            draw.line([(x, 0), (x, height)], fill=line_color, width=line_width)
            
    return preview_img

# --- 主程式介面 ---
uploaded_file = st.file_uploader("請上傳一張圖片", type=["jpg", "jpeg", "png"])

if uploaded_file is not_none:
    # 讀取原始圖片
    image = Image.open(uploaded_file)
    
    # 建立側邊欄控制面板
    st.sidebar.header("⚙️ 切分設定")
    
    # 1. 選擇切分模式
    split_mode = st.sidebar.selectbox(
        "切分方向",
        options=['columns', 'rows'],
        format_func=lambda x: "垂直切分 (產生直欄)" if x == 'columns' else "水平切分 (產生橫列)"
    )
    
    # 2. 設定切分數量
    num_parts = st.sidebar.slider(
        "切分數量",
        min_value=2,
        max_value=20,
        value=2
    )

    # 建立預覽圖
    preview_image = create_preview(image, num_parts, split_mode)

    # --- 畫面佈局：左邊原始圖，右邊預覽圖 ---
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🖼️ 原始圖片")
        st.image(image, use_container_width=True)
        
    with col2:
        st.subheader("👀 預覽切分線 (青色線條)")
        st.image(preview_image, use_container_width=True)

    st.divider()

    # --- 執行切分邏輯 ---
    if st.button("🚀 開始執行切分"):
        st.success("切分完成！正在準備下載...")
        
        width, height = image.size
        parts_list = []
        
        # 根據模式進行切分
        if split_mode == 'rows':
            # 水平切分 (產生橫列)
            for i in range(num_parts):
                top = height * (i / num_parts)
                bottom = height * ((i + 1) / num_parts)
                part = image.crop((0, top, width, bottom))
                parts_list.append(part)
                
        else:
            # 垂直切分 (產生直欄)
            for i in range(num_parts):
                left = width * (i / num_parts)
                right = width * ((i + 1) / num_parts)
                part = image.crop((left, 0, right, height))
                parts_list.append(part)

        # 顯示結果並提供下載
        st.subheader("📦 切分結果")
        cols = st.columns(min(len(parts_list), 4)) # 建立列來顯示圖片
        
        for idx, part in enumerate(parts_list):
            with cols[idx % 4]:
                st.image(part, caption=f"Part {idx+1}")
                
                # 準備下載按鈕
                # 將圖片轉為 bytes 供下載使用
                import io
                buf = io.BytesIO()
                part.save(buf, format="PNG")
                byte_im = buf.getvalue()
                
                st.download_button(
                    label=f"下載 Part {idx+1}",
                    data=byte_im,
                    file_name=f"split_part_{idx+1}.png",
                    mime="image/png",
                    key=f"btn_{idx}"
                )
        
        if len(parts_list) > 4:
            st.info("提示：如果切分數量很多，請向上捲動查看完整結果。")

else:
    st.info("👋 請在上方上傳一張圖片開始操作！")
