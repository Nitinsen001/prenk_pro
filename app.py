import streamlit as st
import qrcode
import socket
import os
from io import BytesIO

# Agar offline test karna ho toh local IP chahiye
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

if hasattr(st, "query_params"):
    params = st.query_params
else:
    params = st.experimental_get_query_params()

# ==========================================
# 1. PHONE WALA VIEW (Jaise hi scan hoga ye khulega)
# ==========================================
if "prank" in params:
    prank_id = params["prank"]
    if isinstance(prank_id, list):
        prank_id = prank_id[0]
        
    # Yahan 4-5 options ki images set ki hain
    if prank_id == "1":
        image_path = 'Gemini_Generated_Image_30lvh230lvh230lv.png' # 1G Wi-Fi Prank Image
    elif prank_id == "2":
        image_path = 'image2.png' # 2G Wi-Fi Prank Image (Aap apna naam dal lena)
    elif prank_id == "3":
        image_path = 'image3.png' # 3G Wi-Fi Prank Image
    elif prank_id == "4":
        image_path = 'image4.png' # 4G Wi-Fi Prank Image

    else:
        image_path = None
        
    if image_path and os.path.exists(image_path):
        st.image(image_path, use_container_width=True)
    else:
        st.error(f"Image '{image_path}' nahi mili! Dhyan rakhein file ka naam code me same ho.")

# ==========================================
# 2. TUMHARA DASHBOARD VIEW (Laptop par)
# ==========================================
else:
    st.markdown("<h3 style='text-align: center; color: #ff4b4b; background-color: #ffe6e6; padding: 10px; border-radius: 10px;'>✨ Developed by Nitin ✨</h3>", unsafe_allow_html=True)
    st.title("Free Wi-Fi for all jitians by QR Generator 📶")
    st.write("Apne doston ko 'Free Wi-Fi' ka maja uthane do!")
    
    # Selectbox me options
    options_mapping = {
        "1G Wi-Fi Setup (Very Slow)": "1",
        "2G Wi-Fi Setup (Normal Speed)": "2",
        "3G Wi-Fi Setup (High Speed)": "3",
        "4G Wi-Fi Setup (Ultra Fast!)": "4",
       
    }
    
    selected_text = st.selectbox("Select Wi-Fi Option to Show:", list(options_mapping.keys()))
    selected_option = options_mapping[selected_text] # Ye "1", "2", "3" me convert kar dega
    
    st.write("---")
    
    # HOSTING YA OFFLINE KA SETTING
    hosting_mode = st.radio("Abhi tum code kahan chala rahe ho?", ["Offline (Local Laptop par)", "Online (GitHub/Streamlit par Host ho chuka hai)"])
    
    if hosting_mode == "Offline (Local Laptop par)":
        ip_address = get_local_ip()
        base_url = f"http://{ip_address}:8501"
    else:
        # Jab tum host kar doge, tab apna website ka link yahan daal sakte ho
        base_url = st.text_input("Apni hosted website ka link daalo:", value="https://tumhara-prank-project.streamlit.app")
        # Ya fir baad me code me fix kar dena: base_url = "https://tumhara-prank-project.streamlit.app"
    
    # Final URL banana
    url = f"{base_url.rstrip('/')}/?prank={selected_option}"
    
    # Generate QR Code
    qr = qrcode.make(url)
    buf = BytesIO()
    qr.save(buf)
    buf.seek(0)
    
    st.image(buf, caption=f"Scan for: {selected_text}", width=400)
    
    # with st.expander("Dekho background URL kaisa ban raha hai:"):
    #     st.code(url)




