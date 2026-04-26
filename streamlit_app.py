import streamlit as st
import io
from PIL import Image

# 設定頁面標題與圖示
st.set_page_config(page_title="圖片切分工具", page_icon="✂️")

st.title("✂️ 圖片切分工具")
st.markdown("上傳一張圖片，設定切分份數，快速完成圖片分割！")

# 讀取檔案
uploaded_file = st.file_uploader("請上傳圖片 (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:  # <--- 這裡已經修正為正確的語法 is not None
    # 讀取圖片
    image = Image.open(uploaded_file)
    img_width, img_height = image.size

    # 顯示原圖
    st.subheader("🖼️ 原圖預覽")
    st.image(image, use_container_width=True)
    st.info(f"圖片解析度: {img_width} x {img_height} px")

    st.divider()

    # --- 切分參數設定 ---
    col1, col2 = st.columns(2)
    
    with col1:
        rows = st.number_input("垂直切分份數 (列)", min_value=1, value=1, step=1)
    with col2:
        cols = st.number_input("水平切分份數 (欄)", min_value=1, value=1, step=1)

    if st.button("🚀 開始切分圖片"):
        st.subheader("✂️ 切分結果")
        
        # 計算每個區塊的大小
        piece_width = img_width // cols
        piece_height = img_height // rows
        
        # 用來存放切分後的圖片
        pieces = []

        # 執行切分邏輯
        for r in range(rows):
            for c in range(cols):
                # 計算左、上、右、下的座標
                left = c * piece_width
                top = r * piece_height
                # 最後一列/欄要補足剩餘像素，避免因為整除不盡導致邊緣留白
                right = (c + 1) * piece_width if c < cols - 1 else img_width
                bottom = (r + 1) * piece_height if r < rows - 1 else img_height
                
                # 裁切圖片
                piece = image.crop((left, top, right, bottom))
                pieces.append(piece)

        # --- 顯示結果與下載 ---
        # 使用 Grid 佈局顯示切分後的圖
        display_cols = st.columns(2) # 每列顯示 2 張圖
        
        for idx, p in enumerate(pieces):
            with display_cols[idx % 2]:
                st.image(p, caption=f"區塊 {idx+1}", use_container_width=True)
                
                # 準備下載按鈕
                buf = io.BytesIO()
                p.save(buf, format="PNG")
                byte_im = buf.getvalue()
                
                st.download_button(
                    label=f"下載區塊 {idx+1}",
                    data=byte_im,
                    file_name=f"piece_{idx+1}.png",
                    mime="image/png",
                    key=f"btn_{idx}"
                )
        
        st.success(f"✅ 完成！共切分成 {len(pieces)} 個區塊。")

else:
    st.info("👋 尚未上傳圖片，請點擊上方按鈕上傳圖片以開始。")

# --- 頁尾 ---
st.divider()
st.caption("由 Streamlit 驅動的自動化圖像處理工具")
