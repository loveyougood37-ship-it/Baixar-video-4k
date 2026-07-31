import streamlit as st
import yt_dlp
import os
import tempfile

st.set_page_config(page_title="Baixador Privado 4K", page_icon="🎬", layout="centered")

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

            # Tenta com o Chrome primeiro; se der erro por estar aberto, usa fallback direto sem travar
            def rodar_download(usar_cookies=True):
                opts = {
                    'outtmpl': output_template,
                    'format': format_opt,
                    'nocheckcertificate': True,
                    'quiet': True,
                    'no_warnings': True,
                    'extractor_args': {
                        'youtube': {
                            'player_client': ['android', 'ios']
                        }
                    }
                }
                if usar_cookies:
                    opts['cookiesfrombrowser'] = ('chrome',)

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
                try:
                    titulo = rodar_download(usar_cookies=True)
                except Exception:
                    # Se o Chrome estiver aberto e bloquear, roda o download seguro via client sem cookies
                    titulo = rodar_download(usar_cookies=False)

                final_file = os.path.join(temp_dir, f"yt_download_temp.{ext_target}")

                if os.path.exists(final_file):
                    with open(final_file, "rb") as f:
                        file_bytes = f.read()

                    # Apaga do PC imediatamente após ler
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