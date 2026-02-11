import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Calculadora de Permissões Linux/windows",
    page_icon="🛡️",
    layout="centered"
)

# Inicializar Session State se não existir
if 'octal_input' not in st.session_state:
    st.session_state['octal_input'] = "755"

def update_from_octal():
    """Função callback para atualizar tudo quando o user digita o número"""
    octal = st.session_state.octal_input
    if len(octal) == 3 and octal.isdigit():
        # Lógica para converter string "7" em boleanos
        u = int(octal[0])
        g = int(octal[1])
        o = int(octal[2])
        # Atualizar session state das checkboxes (Bitwise logic)
        st.session_state.ur = bool(u & 4)
        st.session_state.uw = bool(u & 2)
        st.session_state.ux = bool(u & 1)
        st.session_state.gr = bool(g & 4)
        st.session_state.gw = bool(g & 2)
        st.session_state.gx = bool(g & 1)
        st.session_state.or_ = bool(o & 4) # or_ porque 'or' é palavra reservada
        st.session_state.ow = bool(o & 2)
        st.session_state.ox = bool(o & 1)

def update_from_checkboxes():
    """Função para recalcular o octal quando clicamos nas caixas"""
    u = (4 if st.session_state.ur else 0) + (2 if st.session_state.uw else 0) + (1 if st.session_state.ux else 0)
    g = (4 if st.session_state.gr else 0) + (2 if st.session_state.gw else 0) + (1 if st.session_state.gx else 0)
    o = (4 if st.session_state.or_ else 0) + (2 if st.session_state.ow else 0) + (1 if st.session_state.ox else 0)
    st.session_state.octal_input = f"{u}{g}{o}"

st.title("🛡️ Calculadora de Permissões Linux/windows")
st.markdown("Converte e gere comandos entre Linux e Windows.")

# --- Área de Input Rápido (Bidirecional) ---
st.write("### ⚡ Input Rápido")
col_in1, col_in2 = st.columns([1, 3])
with col_in1:
    st.text_input("Código Octal:", key="octal_input", max_chars=3, on_change=update_from_octal, help="Digite ex: 777 ou 644")

# --- Matriz Visual (Checkboxes) ---
st.write("### 🎛️ Matriz Visual")
c1, c2, c3 = st.columns(3)

with c1:
    st.info("👤 Dono (User)")
    st.checkbox("Ler (r)", key="ur", on_change=update_from_checkboxes)
    st.checkbox("Escrever (w)", key="uw", on_change=update_from_checkboxes)
    st.checkbox("Executar (x)", key="ux", on_change=update_from_checkboxes)

with c2:
    st.warning("👥 Grupo (Group)")
    st.checkbox("Ler (r)", key="gr", on_change=update_from_checkboxes)
    st.checkbox("Escrever (w)", key="gw", on_change=update_from_checkboxes)
    st.checkbox("Executar (x)", key="gx", on_change=update_from_checkboxes)

with c3:
    st.success("🌍 Outros (Others)")
    st.checkbox("Ler (r)", key="or_", on_change=update_from_checkboxes)
    st.checkbox("Escrever (w)", key="ow", on_change=update_from_checkboxes)
    st.checkbox("Executar (x)", key="ox", on_change=update_from_checkboxes)

# --- Cálculos Finais ---
octal_final = st.session_state.octal_input

# Simbólico (ex: -rwxr-xr-x)
def get_rwx(val):
    val = int(val)
    return f"{'r' if val & 4 else '-'}{'w' if val & 2 else '-'}{'x' if val & 1 else '-'}"

try:
    if len(octal_final) == 3:
        u_sym = get_rwx(octal_final[0])
        g_sym = get_rwx(octal_final[1])
        o_sym = get_rwx(octal_final[2])
        symbolic = f"-{u_sym}{g_sym}{o_sym}"
    else:
        symbolic = "Inválido"
except:
    symbolic = "Erro"

st.divider()

# --- Resultados e Auditoria ---
r1, r2 = st.columns(2)

with r1:
    st.subheader("🐧 Linux Output")
    st.code(f"chmod {octal_final} arquivo.txt", language="bash")
    st.caption(f"Simbólico: `{symbolic}`")

with r2:
    st.subheader("🪟 Windows (ICACLS)")
    # Tradução aproximada para Windows
    win_perm = "F" if octal_final == "777" else "M" if "7" in octal_final else "R"
    st.code(f"icacls arquivo.txt /grant Todos:({win_perm})", language="powershell")
    st.caption("F=Full, M=Modify, R=Read (Aproximação)")

# --- Auditoria de Segurança ---
st.subheader("🚨 Auditoria de Segurança")

if octal_final == "777":
    st.error("⚠️ PERIGO CRÍTICO: Permissão 777 dá acesso total a qualquer pessoa. Nunca use em produção!")
elif octal_final[2] in ['7', '6', '3', '2']:
    st.warning("⚠️ CUIDADO: Os 'Outros' (mundo) têm permissão de escrita. Isto pode permitir injeção de código.")
elif octal_final == "400" or octal_final == "600":
    st.success("✅ SEGURO: Apenas o dono tem acesso. Ideal para chaves SSH (.pem).")
else:
    st.info("ℹ️ Permissão padrão/aceitável para a maioria dos casos.")
