import streamlit as st
from prep import preprocesar
import matplotlib.pyplot as plt 
import plotly.express as px
import pandas as pd
from sklearn.cluster import KMeans
import seaborn as sns

st.title("Optimizacion de estrategias de forex")

def optimizar():

	file = st.file_uploader("Selecciona el reporte de optimizacion de metatrader")

	if not file:
		st.warning("Por favor carga el reporte de optimizacion")
		return

	df = preprocesar(file)
	st.dataframe(df.head(10))

	cols = st.multiselect("Selecciona las columnas a optimizar", df.columns)
	if len(cols)<3:
		return st.warning("Selecciona al menos 3 columnas")

	s = px.scatter_3d(data_frame=df, x=cols[0], y=cols[1], z=cols[2], color=cols[2], opacity=1, size_max=0.1)
	st.write(s)

	st.header("Seleccionar cantidad de clusters 'k'")

	inertias = []
	for k in range(2,10):
		clusters = KMeans(k)
		clusters.fit(df[cols])
		inertias.append(clusters.inertia_)
    
	ax = px.line(x=range(2,10), y=inertias)
	st.write(ax)

	k= st.slider("K= ", 2, 20, 4)

	clusters = KMeans(k)
	clusters.fit(df[cols])

	centros = clusters.cluster_centers_

	labels = clusters.labels_.reshape(-1,1)
	cols.append("labels")
	df["labels"] = labels
	s = px.scatter_3d(data_frame=df, x=cols[0], y=cols[1], z=cols[2], color=df.labels, opacity=1, size_max=0.1)
	st.write(s)

	st.header("Resultados")
	d = {}
	for i, col in enumerate(cols[:-1]):
		d[col] = centros[:,i]

	st.table(d)

optimizar()