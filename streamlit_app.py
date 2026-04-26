import streamlit as st
from PIL import Image
import io

# 設定頁面標題與圖示
st.set_page_config(page_title="極簡圖片切割工具", page_icon="✂️")

st.title("✂️ 極簡圖片切割工具")
st.markdown("上傳圖片，設定行列，一鍵完成切割並下載。")

# --- 第一階段：上傳與參數設定 ---
st.divider()
st.subheader("1. 上傳與參數設定")

# 使用兩欄式佈局來放置上傳與設定
col_upload, col_settings = st.columns([1, 1])

with col_upload:
    uploaded_file = st.file_uploader("選擇一張圖片", type=["png", "jpg", "jpeg", "webp"])

with col_settings:
    # 使用 columns 讓參數並排，更省空間
    c1, c2 = st.columns(2)
    with c1:
        rows = st.number_input("列數 (Rows)", min_value=2, value=2, step=1)
    with c2:
        cols = st.number_input("欄數 (Cols)", min_value=2, value=2, step=1)

# --- 第二階段：預覽與即時處理 ---
if uploaded_file is not None:
    # 讀取圖片
    from PIL import Image
    image = Image.open(uploaded_file)
    
    st.divider()
    
    # 建立顯示區域
    display_col, info_col = st.columns([3, 1])
    
    with info_col:
        st.metric("原始尺寸", f"{image.width} x {image.height} px")
        st.write(f"分割目標: {rows} x {cols} = {rows * cols} 片")

    with display_col:
        # --- 預覽功能：繪製藍色分割線 ---
        # 為了不破壞原圖，我們建立一個副本來做預覽
        preview_img = image.copy().convert("RGB")
        from PIL import ImageDraw
        draw = ImageDraw.Draw(preview_img)
        
        # 定義天空藍顏色 (Sky Blue)
        sky_blue = (0, 191, 255) 
        
        # 計算分割線位置
        width, height = preview_img.size
        
        # 繪製橫線 (Rows)
        if rows > 1:
            for i in range(1, rows):
                y = i * (height / rows)
                draw.line([(0, y), (width, y)], fill=sky_blue, width=3)
                
        # 繪製直線 (Cols)
        if cols > 1:
            for j in range(1, cols):
                x = j * (width / cols)
                draw.line([(x, 0), (x, height)], fill=sky_blue, width=3)
        
        # 顯示預覽圖
        st.image(preview_img, caption="分割預覽 (藍色線條為切割邊界)", use_container_width=True)

    # --- 第三階段：執行切割與下載 ---
    st.divider()
    st.subheader("3. 執行切割與下載")
    
    if st.button("🚀 開始切割圖片", type="primary"):
        st.info(f"正在將圖片切割為 {rows * cols} 個區塊...")
        
        # 建立一個容器來存放生成的圖片
        output_cols = st.columns(3) # 每列顯示 3 張圖
        
        count = 0
        for r in range(rows):
            for c in range(cols):
                # 計算切割邊界
                left = c * (img_width / cols)
                top = r * (img_height / rows)
                right = (c + 1) * (img_width / cols)
                bottom = (r + 1) * (img_height / rows)
                
                # 切割
                cropped_img = img.crop((left, top, right, bottom))
                
                # 準備下載
                buf = io.BytesIO()
                cropped_img.save(buf, format="PNG")
                byte_im = buf.getvalue()
                
                # 顯示在對應的欄位中
                with output_cols[count % 3]:
                    st.image(cropped_img, caption=f"區塊 ({r},{c})", use_container_width=True)
                    st.download_button(
                        label="📥 下載此格",
                        data=byte_im,
                        file_name=f"crop_{r}_{c}.png",
                        mime="image/png",
                        key=f"btn_{r}_{c}"
                    )
                
                count += 1
                if count % 3 == 0: # 換行
                    st.divider()
        
        st.success("✅ 切割完成！")
    else:
        st.write("請點擊上方按鈕執行切割。")

else:
    st.info("👈 請先在上方上傳圖片以開始。")

# 頁尾
st.caption("✂️ 極簡圖片切割工具 | 快速、簡單、隱私（圖片處理皆在您的瀏覽器/伺服器端完成）")
