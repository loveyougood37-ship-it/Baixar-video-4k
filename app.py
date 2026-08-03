import streamlit as st
import yt_dlp
import os

# Configuração da página
st.set_page_config(page_title="Baixador Privado 4K", page_icon="🎬", layout="centered")

# --- SISTEMA DE SENHA ---
SENHA_CORRETA = "suasenha123"  # 👈 TROQUE AQUI PELA SUA SENHA DESEJADA!

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🔒 Acesso Restrito")
    senha_digitada = st.text_input("Digite a senha para acessar:", type="password")
    
    if st.button("Entrar"):
        if senha_digitada == SENHA_CORRETA:
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("Senha incorreta!")
    st.stop()  # Trava o app aqui até acertar a senha

# --- CONTEÚDO DO APP ---
st.title("🎬 Baixador Privado 4K")
st.caption("Baixe vídeos do YouTube na máxima resolução e sem limitações.")

# Entrada da URL
url = st.text_input("🔗 Cole a URL do Vídeo do YouTube:")

# Seleção de Qualidade
qualidade = st.selectbox(
    "📺 Selecione a Resolução Desejada:",
    ["4K (2160p)", "1080p Full HD", "720p HD", "Apenas Áudio (MP3)"]
)

# Botão de Ação
if st.button("🚀 Processar Vídeo"):
    if not url:
        st.warning("Por favor, cole um link válido antes de continuar.")
    else:
        with st.spinner("⚡ Baixando e unindo áudio e vídeo em alta resolução... Aguarde um instante."):
            try:
                out_dir = "downloads"
                os.makedirs(out_dir, exist_ok=True)
                
                # Resoluções nativas do yt-dlp
                if "4K" in qualidade:
                    fmt = "bestvideo[height<=2160]+bestaudio/best[height<=2160]/best"
                elif "1080p" in qualidade:
                    fmt = "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best"
                elif "720p" in qualidade:
                    fmt = "bestvideo[height<=720]+bestaudio/best[height<=720]/best"
                else:
                    fmt = "bestaudio/best"

                ydl_opts = {
                    'format': fmt,
                    'outtmpl': f'{out_dir}/%(title)s.%(ext)s',
                    'merge_output_format': 'mp4',
                    'quiet': True,
                    'no_warnings': True,
                    # CABEÇALHOS PARA EVITAR O ERRO 403 (DISFARCE DE NAVEGADOR)
                    'http_headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Language': 'en-us,en;q=0.5',
                    }
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                    
                    if not os.path.exists(filename):
                        base, _ = os.path.splitext(filename)
                        filename = f"{base}.mp4"

                st.success("✅ Vídeo processado com sucesso!")
                
                with open(filename, "rb") as file:
                    st.download_button(
                        label="📥 CLIQUE AQUI PARA SALVAR O VÍDEO",
                        data=file,
                        file_name=os.path.basename(filename),
                        mime="video/mp4"
                    )
            except Exception as e:
                st.error(f"Erro ao processar o vídeo: {e}")
