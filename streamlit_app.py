import streamlit as st
from PIL import Image, ImageDraw
import io

# 設定頁面標題
st.set_page_config(page_title="極速圖片切割器", layout="wide")

# --- 1. 快取機制：避免重複讀取大圖 ---
@st.cache_data
def load_image_from_bytes(file_bytes):
    """將 bytes 轉換為 PIL Image 物件，並快取結果"""
    return Image.open(io_bytes_to_image(file_bytes))

def io_bytes_to_image(file_bytes):
    return io.BytesIO(file_bytes)

# --- 2. 核心優化：生成輕量化的預覽圖 ---
def create_preview_image(original_img, rows, cols):
    """
    製作一張極小的預覽圖，用來顯示線條。
    這樣無論原圖多大，預覽時傳輸的數據量都極小。
    """
    # 建立一個縮圖，長邊限制在 800px，這樣顯示速度會非常快
    preview_img = original_img.copy()
    preview_img.thumbnail((800, 800))
    
    draw = ImageDraw.Draw(preview_img)
    width, height = preview_img.size
    
    # 計算線條位置
    # 橫線
    if rows > 1:
        for i in range(1, rows):
            y = (height / rows) * i
            draw.line([(0, y), (width, y)], fill="red", width=2)
    
    # 縱線
    if cols > 1:
        for i in range(1, cols):
            x = (width / cols) * i
            draw.line([(x, 0), (x, height)], fill="red", width=2)
            
    return preview_img

# --- UI 介面 ---
st.title("🚀 極速圖片切割器 (Optimized)")
st.markdown("使用縮圖預覽技術，即使原圖很大，調整參數也能瞬間反應。")

uploaded_file = st.file_uploader("請上傳圖片", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # 將上傳的檔案讀取為 bytes (為了快取)
    file_bytes = uploaded_file.getvalue()
    
    # 使用快取讀取原圖
    try:
        original_img = load_image_from_bytes(file_bytes)
        
        # Sidebar 控制參數
        st.sidebar.header("切割參數設定")
        rows = st.sidebar.number_input("橫向切割數量 (Rows)", min_value=1, value=1, step=1)
        cols = st.sidebar.number_input("縱向切割數量 (Cols)", min_value=1, value=1, step=1)
        
        # 建立左右佈局
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔍 預覽模式 (Thumbnail Preview)")
            # 重點：我們只在預覽圖上畫線，且圖片經過縮小
            preview_img = create_preview_image(original_img, rows, cols)
            st.image(preview_img, use_container_width=True)
            st.caption("此預覽圖為縮圖，僅用於快速查看切割範圍。")

        with col2:
            st.subheader("🖼️ 原始影像資訊")
            st.write(f"**尺寸:** {original_img.size[0]} x {original_img.size[1]} px")
            st.write(f"**格式:** {original_img.format}")
            st.info("調整左側參數時，預覽圖會瞬間更新，因為我們傳輸的是輕量化縮圖。")

        # --- 3. 實際執行切割 (只有按下按鈕時才執行大圖處理) ---
        st.divider()
        if st.button("⚡ 開始執行高畫質切割", type="primary"):
            with st.spinner("正在處理高解析度影像，請稍候..."):
                # 這裡才進行真正的原圖切割
                width, height = original_img.size
                part_w = width / cols
                part_h = height / rows
                
                output_images = []
                
                for r in range(rows):
                    for c in range(cols):
                        left = c * part_w
                        top = r * part_h
                        right = (c + 1) * part_w
                        bottom = (r + 1) * part_h
                        
                        # 切割原圖
                        crop_img = original_img.crop((left, top, right, bottom))
                        
                        # 儲存到記憶體
                        buf = io.BytesIO()
                        crop_img.save(buf, format="PNG")
                        output_images.append(buf.getvalue())
                
                st.success(f"✅ 完成！成功切割出 {len(output_images)} 張圖片。")
                
                # 提供下載
                for i, img_data in enumerate(output_images):
                    st.download_button(
                        label=f"下載切割片 #{i+1}",
                        data=img_data,
                        file_name=f"crop_{i+1}.png",
                        mime="image/png",
                        key=f"btn_{i}"
                    )

    except Exception as e:
        st.error(f"處理圖片時發生錯誤: {e}")

else:
    st.info("請先上傳圖片開始使用。")
