import streamlit as st
import requests

# Configuração da página
st.set_page_config(page_title="ZPL Converter | Empresa", page_icon="🏷️", layout="wide")

# --- BARRA LATERAL (CONFIGURAÇÕES) ---
with st.sidebar:
    st.image("logo.png") # Ícone ilustrativo
    st.title("Configurações")
    st.markdown("---")
    
    dpmm = st.selectbox(
        "Resolução da Impressora:",
        options=[8, 12, 24],
        format_func=lambda x: f"{x} dpmm ({x*25} dpi)",
        help="A maioria das Zebras usam 8 dpmm (203 dpi)."
    )
    
    tamanho = st.selectbox(
        "Tamanho da Etiqueta:",
        options=["4x6", "4x4", "4x2", "2x1"],
        help="Largura x Altura em polegadas."
    )
    
    st.info("💡 Dica: Verifique se o código ZPL termina com ^XZ para cada etiqueta.")

# --- ÁREA PRINCIPAL ---
st.header("🚀 Conversor Interno de Etiquetas ZPL")

# Criamos duas colunas: uma para o código e outra para o resultado/instruções
col_cod, col_res = st.columns([1.2, 0.8])

with col_cod:
    st.subheader("Entrada de Dados")
    zpl_input = st.text_area(
        "Cole seu código ZPL aqui:",
        height=400,
        placeholder="^XA\n^FO50,50^A0N,50,50^FDEXEMPLO^FS\n^XZ"
    )

with col_res:
    st.subheader("Ações")
    if st.button("🛠️ Processar e Gerar PDF", use_container_width=True):
        if zpl_input:
            url = f'http://api.labelary.com/v1/printers/{dpmm}dpmm/labels/{tamanho}/'
            headers = {'Accept': 'application/pdf'}
            
            with st.spinner('Gerando lote de etiquetas...'):
                try:
                    res = requests.post(url, data=zpl_input.encode('utf-8'), headers=headers)
                    if res.status_code == 200:
                        st.success("✅ Tudo pronto!")
                        st.download_button(
                            label="📥 BAIXAR PDF AGORA",
                            data=res.content,
                            file_name="etiquetas_producao.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                        st.balloons() # Um charminho visual para o usuário
                    else:
                        st.error(f"Erro na API: {res.text}")
                except Exception as e:
                    st.error(f"Falha na conexão: {e}")
        else:
            st.warning("⚠️ Insira um código ZPL antes de converter.")