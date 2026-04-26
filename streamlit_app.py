import streamlit as st
from PIL import Image
import io

# --- 頁面設定 ---
st.set_page_config(page_title="圖片左右分割器", page_icon="✂️")

st.title("✂️ 圖片左右分割器")
st.write("上傳一張圖片，我會幫你把它從中間切成左右兩半，並提供下載！")

# --- 處理邏輯函數 ---
def split_image(input_image):
    """將圖片從中間垂直切割成左右兩部分"""
    width, height = input_image.size
    mid_point = width // 2
    
    # 切割左半部 (左, 上, 右, 下)
    left_part = input_image.crop((0, 0, mid_point, height))
    # 切割右半部
    right_part = input_image.crop((mid_point, 0, width, height))
    
    return left_part, right_part

def convert_image_to_bytes(img, format="PNG"):
    """將 PIL Image 物件轉換為可以下載的 Bytes 格式"""
    buf = io.BytesIO()
    img.save(buf, format=format)
    return buf.getvalue()

# --- UI 介面 ---
uploaded_file = st.file_uploader("請上傳圖片 (JPG, PNG, JPEG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 1. 開啟圖片
    image = Image.open(uploaded_file)
    
    # 2. 顯示原始圖片
    st.subheader("🖼️ 原始圖片")
    st.image(image, use_container_width=True)
    
    st.divider()
    
    # 3. 執行切割邏輯
    with st.spinner('正在切割中...'):
        left_img, right_img = split_image(image)
    
    # 4. 顯示結果與下載按鈕
    st.subheader("✂️ 切割結果")
    
    # 使用左右兩欄佈局
    col1, col2 = st.columns(2)
    
    with col1:
        st.image(left_img, caption="左半部", use_container_width=True)
        # 準備左半部下載用的資料
        left_bytes = convert_image_to_bytes(left_img)
        st.download_button(
            label="📥 下載左半部",
            data=left_bytes,
            file_name="left_part.png",
            mime="image/png",
            key="download_left"
        )
        
    with col2:
        st.image(right_img, caption="右半部", use_container_width=True)
        # 準備右半部下載用的資料
        right_bytes = convert_image_to_bytes(right_img)
        st.download_button(
            label="📥 下載右半部",
            data=right_bytes,
            file_name="right_part.png",
            mime="image/png",
            key="download_right"
        )

    st.success("處理完成！請點擊上方按鈕下載圖片。")

else:
    st.info("💡 請在上方的檔案上傳框中選擇一張圖片開始。")
