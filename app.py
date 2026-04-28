import streamlit as st
import pandas as pd
import os
from datetime import datetime
import json

st.set_page_config(page_title="Teacher App MVP", layout="centered")

# -------------------------
# Load students
# -------------------------
with open("students/grupos.json", "r") as f:
    grupos = json.load(f)

# -------------------------
# Load or create data
# -------------------------
DATA_PATH = "data/registros.csv"

if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)
else:
    df = pd.DataFrame(columns=["fecha", "grupo", "alumno", "accion"])

# -------------------------
# UI
# -------------------------
st.title("📚 Teacher App MVP")

grupo = st.selectbox("Selecciona grupo", list(grupos.keys()))
alumno = st.selectbox("Selecciona alumno", grupos[grupo])

col1, col2 = st.columns(2)

# -------------------------
# Register actions
# -------------------------
if col1.button("➕ Positivo"):
    nuevo = {
        "fecha": datetime.now(),
        "grupo": grupo,
        "alumno": alumno,
        "accion": "positivo"
    }
    df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
    df.to_csv(DATA_PATH, index=False)
    st.success("Registrado positivo")

if col2.button("➖ Negativo"):
    nuevo = {
        "fecha": datetime.now(),
        "grupo": grupo,
        "alumno": alumno,
        "accion": "negativo"
    }
    df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
    df.to_csv(DATA_PATH, index=False)
    st.warning("Registrado negativo")

# -------------------------
# Filters
# -------------------------
st.subheader("🔍 Historial")

filtro_alumno = st.selectbox("Filtrar por alumno", ["Todos"] + list(df["alumno"].unique()))

df_filtrado = df.copy()

if filtro_alumno != "Todos":
    df_filtrado = df_filtrado[df_filtrado["alumno"] == filtro_alumno]

st.dataframe(df_filtrado.sort_values(by="fecha", ascending=False))

# -------------------------
# Summary
# -------------------------
st.subheader("📊 Resumen")

resumen = df.groupby("alumno")["accion"].value_counts().unstack().fillna(0)
st.dataframe(resumen)
