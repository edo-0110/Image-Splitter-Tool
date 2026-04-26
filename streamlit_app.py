import streamlit as st
from PIL import Image
import io

def split_image(image, direction):
    """
    根據方向切割圖片
    direction: "vertical" (左右分) 或 "horizontal" (上下分)
    """
    width, height = image.size
    parts = []

    if direction == "vertical":
        # 左右切割
        mid = width // 2
        part1 = image.crop((0, 0, mid, height))
        part2 = image.crop((mid, 0, width, height))
        parts = [part1, part2]
    else:
        # 上下切割
        mid = height // 2
        part1 = image.crop((0, 0, width, mid))
        part2 = image.crop((0, mid, width, height))
        parts = [part1, part2]
    
    return parts

def main():
    st.set_📸_page_config(page_title="全能圖片切割器", layout="wide")
    st.title("✂️ 全能圖片切割器")
    st.write("你可以選擇將圖片『左右分開』或『上下分開』")

    # 1. 側邊欄：設定功能
    st.sidebar.header("⚙️ 切割設定")
    direction_option = st.sidebar.radio(
        "選擇切割方向：",
        ("垂直切割 (左右分)", "水平切割 (上下分)")
    )
    
    # 將使用者的文字轉換為程式邏輯文字
    split_mode = "vertical" if "垂直" in direction_option else "horizontal"

    # 2. 檔案上傳
    uploaded_file = st.file_io_uploader("請上傳一張圖片", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        # 開啟圖片
        image = Image.open(uploaded_file)
        
        # 顯示原圖
        st.subheader("🖼️ 原圖預覽")
        st.image(image, use_container_width=True)
        
        st.divider()

        # 3. 執行切割邏ient
        st.subheader(f"🚀 執行任務：{direction_option}")
        parts = split_image(image, split_mode)

        # 4. 顯示結果與下載按鈕
        if split_mode == "vertical":
            # 左右佈局
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("👈 左半部分")
                st.image(parts[0], use_container_width=True)
                # 下載按鈕
                buf = io.BytesIO()
                parts[0].save(buf, format="PNG")
                st.download_button("下載左半部", buf.getvalue(), "left_part.png", "image/png")

            with col2:
                st.write("👉 右半部分")
                st.image(parts[1], use_container_width=True)
                # 下載按鈕
                buf = io.BytesIO()
                parts[1].save(buf, format="PNG")
                st.download_button("下載右半部", buf.getvalue(), "image/png", "image/png")
        
        else:
            # 上下佈局
            col_top, col_bottom = st.columns(1)
            
            with col_top:
                st.write("👆 上半部分")
                st.image(parts[0], use_container_width=True)
                buf = io.BytesIO()
                parts[0].save(buf, format="PNG")
                st.download_button("下載上半部", buf.getvalue(), "top_part.png", "image/png")
            
            st.write("---") # 分隔線
            
            with col_bottom:
                st.write("👇 下半部分")
                st.image(parts[1], use_container_width=True)
                buf = io.BytesIO()
                parts[1].save(buf, format="PNG")
                st.download_button("下載下半部", buf.getvalue(), "bottom_part.png", "image/png")

    else:
        st.info("👈 請從上方上傳圖片開始使用")

if __name__
