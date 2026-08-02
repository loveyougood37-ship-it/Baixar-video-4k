import streamlit as st
import requests

st.set_page_config(page_title="Baixador Privado 4K", page_icon="🎬", layout="centered")

# --- OCULTAR TUDO NO STREAMLIT (CSS GLOBAL) ---
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden !important;}
            footer {visibility: hidden !important; display: none !important;}
            header {visibility: hidden !important; display: none !important;}
            .stAppHeader {display: none !important;}
            [data-testid="stStatusWidget"] {display: none !important;}
            [data-testid="stDecoration"] {display: none !important;}
            [data-testid="stToolbar"] {display: none !important;}
            .viewerBadge_container__1A54N,
            .viewerBadge_link__1S137,
            div[class*="viewerBadge"],
            div[class*="styles_viewerBadge"],
            div[class*="stActionButton"],
            iframe[title*="streamlit"] {
                display: none !important;
                visibility: hidden !important;
            }
            .block-container {
                padding-top: 1.5rem !important;
                padding-bottom: 0rem !important;
            }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --- SEGURANÇA E SENHA ---
SENHA_CORRETA = "suasenha123"

if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    st.title("🎬 Baixador Privado de Vídeos 4K")
    senha = st.text_input("🔑 Digite a Senha de Acesso:", type="password")
    if st.button("Entrar no Sistema"):
        if senha == SENHA_CORRETA:
            st.session_state["autenticado"] = True
            st.rerun()
        else:
            st.error("Senha incorreta!")
    st.stop()

# --- INTERFACE PRINCIPAL ---
st.title("🎬 Baixador Privado de Vídeos 4K")
st.caption("Acesso Exclusivo — Alta Qualidade sem Limites")

raw_url = st.text_input("🔗 Cole a URL do Vídeo do YouTube:")

qualidade = st.selectbox(
    "📺 Selecione a Resolução / Formato:",
    ["4K Ultra HD (2160p)", "1080p Full HD", "720p HD", "Apenas Áudio (MP3)"]
)

if st.button("🚀 Processar Vídeo"):
    if not raw_url:
        st.warning("Por favor, cole um link válido.")
    elif "playlist" in raw_url.lower():
        st.error("Links de playlist não são suportados. Cole o link de um vídeo individual!")
    else:
        with st.spinner("⚡ Gerando link de download direto em alta velocidade..."):
            clean_url = raw_url.strip()
            is_audio = "Apenas Áudio" in qualidade
            
            if "4K" in qualidade:
                res_val = "2160"
            elif "1080p" in qualidade:
                res_val = "1080"
            elif "720p" in qualidade:
                res_val = "720"
            else:
                res_val = "1080"

            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }

            payload = {
                "url": clean_url,
                "videoQuality": res_val,
                "downloadMode": "audio" if is_audio else "auto",
                "youtubeVideoCodec": "vp9"
            }

            # Instâncias da API de alta velocidade
            instancias_api = [
                "https://api.cobalt.tools/",
                "https://cobalt-api.kwiatekmonster.com/",
                "https://co.wuk.sh/"
            ]

            download_url = None

            for api_base in instancias_api:
                try:
                    response = requests.post(api_base, headers=headers, json=payload, timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        status = data.get("status")
                        if status in ["stream", "redirect", "tunnel"]:
                            download_url = data.get("url")
                            break
                        elif status == "picker":
                            picker_items = data.get("picker", [])
                            if picker_items:
                                download_url = picker_items[0].get("url")
                                break
                except:
                    continue

            if download_url:
                st.success("✅ Link gerado na máxima resolução nativa!")
                st.markdown(
                    f'''
                    <a href="{download_url}" target="_blank" style="text-decoration: none;">
                        <div style="
                            background-color: #28a745;
                            color: white;
                            padding: 15px;
                            text-align: center;
                            border-radius: 8px;
                            font-weight: bold;
                            font-size: 18px;
                            margin-top: 10px;
                        ">
                            📥 CLIQUE AQUI PARA BAIXAR O VÍDEO
                        </div>
                    </a>
                    ''',
                    unsafe_allow_html=True
                )
            else:
                st.error("Não foi possível processar este vídeo no momento. Verifique a URL.")
