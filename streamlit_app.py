import streamlit as st
from PIL import Image
import io

# 設定頁面標題
st.set_page_config(page_title="萬能圖片切割器", layout="centered")

st.title("✂️ 萬能圖片切割器")
st.write("上傳一張圖片，快速進行水平或垂直切割。")

# 上傳檔案
uploaded_file = st.file_uploader("選擇一張圖片...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 讀取圖片
    image = Image.open(uploaded_file)
    st.image(image, caption='上傳的圖片', use_container_width=True)
    
    st.write("---")
    st.subheader("切割設定")

    # 取得圖片尺寸
    width, height = image.size
    st.info(f"目前圖片尺寸: {width} x {height} px")

    # 切割模式選擇
    mode = st.radio("選擇切割方向", ("水平切割 (Horizontal)", "垂直切割 (Vertical)"))

    if mode == "水平切割 (Horizontal)":
        num_parts = st.slider("要切成幾份？", min_value=2, max_value=10, value=2)
        part_height = height // num_parts
        
        if st.button("執行切割"):
            cols = st.columns(1) # 這裡用單欄顯示結果
            for i in range(num_capture := num_parts):
                top = i * part_height
                # 最後一份要確保包含到底部，避免因整除餘數導致漏掉像素
                bottom = (i + 1) * part_height if i < num_parts - 1 else height
                
                cropped_img = image.crop((0, top, width, bottom))
                
                st.write(f"第 {i+1} 份")
                st.image(cropped_img, use_container_width=True)
                
                # 提供下載按鈕
                buf = io.BytesIO()
                cropped_img.save(buf, format="PNG")
                st.download_button(
                    label=f"下載第 {i+1} 份",
                    data=buf.getvalue(),
                    file_name=f"part_{i+1}.png",
                    mime="image/png"
                )

    else: # 垂直切割
        num_parts = st.slider("要切成幾份？", min_value=2, max_value=10, value=2)
        part_width = width // num_parts
        
        if st.button("執行切割"):
            for i in range(num_parts):
                left = i * part_width
                right = (i + 1) * part_width if i < num_parts - 1 else width
                
                cropped_img = image.crop((left, 0, right, height))
                
                st.write(f"第 {i+1} 份")
                st.image(cropped_img, use_container_width=True)
                
                # 提供下載按鈕
                buf = io.BytesIO()
                cropped_img.save(buf, format="PNG")
                st.download_button(
                    label=f"下載第 {i+1} 份",
                    data=buf.getvalue(),
                    file_name=f"part_{i+1}.png",
                    mime="image/png"
                )

else:
    st.info("請在上方上傳圖片以開始使用。")
