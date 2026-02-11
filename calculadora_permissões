import streamlit as st

# Configuração da página
st.set_page_config(page_title="Calculadora de Permissões", page_icon="🔐")

st.title("🔐 Calculadora de Permissões (Chmod)")
st.markdown("Selecione as permissões desejadas para gerar o código octal e o comando Linux.")

# Layout em 3 colunas para Dono, Grupo e Outros
col1, col2, col3 = st.columns(3)

def calculate_octal(read, write, execute):
    return (4 if read else 0) + (2 if write else 0) + (1 if execute else 0)

with col1:
    st.subheader("👤 Dono (User)")
    u_r = st.checkbox("Ler (r)", key="ur")
    u_w = st.checkbox("Escrever (w)", key="uw")
    u_x = st.checkbox("Executar (x)", key="ux")
    u_val = calculate_octal(u_r, u_w, u_x)

with col2:
    st.subheader("👥 Grupo (Group)")
    g_r = st.checkbox("Ler (r)", key="gr")
    g_w = st.checkbox("Escrever (w)", key="gw")
    g_x = st.checkbox("Executar (x)", key="gx")
    g_val = calculate_octal(g_r, g_w, g_x)

with col3:
    st.subheader("🌍 Outros (Others)")
    o_r = st.checkbox("Ler (r)", key="or")
    o_w = st.checkbox("Escrever (w)", key="ow")
    o_x = st.checkbox("Executar (x)", key="ox")
    o_val = calculate_octal(o_r, o_w, o_x)

# Resultado final
permissao_final = f"{u_val}{g_val}{o_val}"

st.divider()

st.header(f"Resultado: `{permissao_final}`")

# Exibição do Comando
st.info(f"**Comando Linux:** `chmod {permissao_final} nome_do_arquivo` shadow")

# Explicação técnica
with st.expander("📝 Entender o que isto significa"):
    st.write(f"""
    * **Dono ({u_val}):** Tem permissão de {'leitura, ' if u_r else ''}{'escrita, ' if u_w else ''}{'execução' if u_x else 'nenhuma'}.
    * **Grupo ({g_val}):** Tem permissão de {'leitura, ' if g_r else ''}{'escrita, ' if g_w else ''}{'execução' if g_x else 'nenhuma'}.
    * **Outros ({o_val}):** Tem permissão de {'leitura, ' if o_r else ''}{'escrita, ' if o_w else ''}{'execução' if o_x else 'nenhuma'}.
    """)
    
    st.markdown("""
    ---
    **Tabela de Referência:**
    * `4` = Ler (Read)
    * `2` = Escrever (Write)
    * `1` = Executar (Execute)
    * A soma destes valores define o dígito de cada categoria.
    """)

# Rodapé simples
st.caption("Criado para o curso de Gestão de Redes e Sistemas Informáticos.")
