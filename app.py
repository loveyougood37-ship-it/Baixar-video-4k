import streamlit as st
import yt_dlp
import os

# Configuração da página
st.set_page_config(page_title="Baixador Privado 4K", page_icon="🎬", layout="centered")

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
                # Pasta de saída temporária
                out_dir = "downloads"
                os.makedirs(out_dir, exist_ok=True)
                
                # Definindo formatos nativos do yt-dlp
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
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                    
                    # Trata a extensão caso o yt-dlp altere ao juntar MP4
                    if not os.path.exists(filename):
                        base, _ = os.path.splitext(filename)
                        filename = f"{base}.mp4"

                st.success("✅ Vídeo processado com sucesso!")
                
                # Botão verde para salvar no celular/PC
                with open(filename, "rb") as file:
                    st.download_button(
                        label="📥 CLIQUE AQUI PARA SALVAR O VÍDEO",
                        data=file,
                        file_name=os.path.basename(filename),
                        mime="video/mp4"
                    )
            except Exception as e:
                st.error(f"Erro ao processar o vídeo: {e}")
