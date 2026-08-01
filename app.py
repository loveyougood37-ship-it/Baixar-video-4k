import streamlit as st
import yt_dlp
import os
import tempfile

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
    ["4K Ultra HD", "1080p Full HD", "720p HD", "Apenas Áudio (MP3)"]
)

if st.button("🚀 Processar Vídeo"):
    if not raw_url:
        st.warning("Por favor, cole um link válido.")
    elif "playlist" in raw_url.lower():
        st.error("Links de playlist não são suportados. Cole o link de um vídeo individual!")
    else:
        with st.spinner("⏳ Processando vídeo..."):
            clean_url = raw_url.strip()

            if "4K" in qualidade:
                format_opt = "bestvideo[height<=2160]+bestaudio/best"
            elif "1080p" in qualidade:
                format_opt = "bestvideo[height<=1080]+bestaudio/best"
            elif "720p" in qualidade:
                format_opt = "bestvideo[height<=720]+bestaudio/best"
            else:
                format_opt = "bestaudio/best"

            is_audio = "Apenas Áudio" in qualidade
            ext_target = "mp3" if is_audio else "mp4"

            temp_dir = tempfile.gettempdir()
            output_template = os.path.join(temp_dir, 'yt_download_temp.%(ext)s')

            def rodar_download():
                opts = {
                    'outtmpl': output_template,
                    'format': format_opt,
                    'nocheckcertificate': True,
                    'quiet': True,
                    'no_warnings': True,
                }

                # Se o arquivo cookies.txt existir no projeto, usa ele para bypassar a trava
                if os.path.exists("cookies.txt"):
                    opts['cookiefile'] = "cookies.txt"

                if is_audio:
                    opts['postprocessors'] = [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }]
                else:
                    opts['merge_output_format'] = 'mp4'

                with yt_dlp.YoutubeDL(opts) as ydl:
                    info = ydl.extract_info(clean_url, download=True)
                    return info.get('title', 'video') if info else 'video'

            try:
                titulo = rodar_download()
                final_file = os.path.join(temp_dir, f"yt_download_temp.{ext_target}")

                if os.path.exists(final_file):
                    with open(final_file, "rb") as f:
                        file_bytes = f.read()

                    try:
                        os.remove(final_file)
                    except:
                        pass

                    st.success("✅ Vídeo pronto para envio!")
                    st.download_button(
                        label="📥 CLIQUE AQUI PARA BAIXAR NO SEU CELULAR",
                        data=file_bytes,
                        file_name=f"{titulo}.{ext_target}",
                        mime="audio/mp3" if is_audio else "video/mp4",
                        use_container_width=True
                    )
                else:
                    st.error("Não foi possível gerar o arquivo. Tente novamente.")

            except Exception as e:
                st.error(f"Erro ao processar: {e}")
