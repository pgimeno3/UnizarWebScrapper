# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 23:36:40 2019

@author: Pablo Gimeno Jordan @pablogj
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np

# Get current size
fig_size = plt.rcParams["figure.figsize"]
# Set figure width
fig_size[0] = 16
fig_size[1] = 12
plt.rcParams["figure.figsize"] = fig_size

def parse_table_html(table):
    n_columns = 0
    n_rows = 0
    column_names = []

    for row in table.find_all('tr'):

        td_tags = row.find_all('td')
        if len(td_tags) > 0:
            n_rows += 1
            if n_columns == 0:
                n_columns = len(td_tags)

        th_tags = row.find_all('th')
        if len(th_tags) > 0 and len(column_names) == 0:
            for th in th_tags:
                column_names.append(th.get_text())

    if len(column_names) > 0 and len(column_names) != n_columns:
        raise Exception("columns titles dont match the number of columns")

    columns = column_names if len(column_names) > 0 else range(0,n_columns)
    df = pd.DataFrame(columns = columns, index = range(0,n_rows))

    row_marker = 0
    for row in table.find_all('tr'):
        column_marker = 0
        columns = row.find_all('td')
        for column in columns:
            df.iat[row_marker,column_marker] = column.get_text()
            column_marker += 1
        if len(columns) > 0:
            row_marker += 1

    return df

#20180682 es Master Ingenieria Telecomunicacion
url = 'https://estudios.unizar.es/informe/globales?estudio_id=20180682'
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

#Obtiene el nombre de la titulacion
h1 = soup.find('h1')
str_comp= u'\u2014' #Guion usado para separar ambas cadenas

titulacion = h1.text.split(str_comp)[1].strip()
#print(titulacion.encode('utf-8'))

#Parsea todos los elementos tabla en el html
list_parsed = []
table_list = soup.findAll('table')
for table in table_list:
   table_parsed = parse_table_html(table)
   list_parsed.append(table_parsed)

iterate_list = iter(list_parsed)


#Primera lista contiene info sobre matricula e ingreso
table_parsed = next(iterate_list)

labels =  table_parsed.loc[:,0].values
ofertadas = np.array(table_parsed.loc[1:,1].values, dtype = np.int)
nuevo_ingreso = np.array(table_parsed.loc[1:,2].values, dtype = np.int)
matriculados =  np.array(table_parsed.loc[1:,3].values, dtype = np.int)

indx = np.arange(len(ofertadas))
width=0.2
plt.figure()
plt.bar(indx - width,ofertadas, width = width)
plt.bar(indx,matriculados, width = width)
plt.bar(indx + width,nuevo_ingreso, width = width)

for i in range(len(ofertadas)):
    plt.text(indx[i] - width - 0.04, ofertadas[i] + 0.3, str(ofertadas[i]))
    plt.text(indx[i] + width - 0.04, nuevo_ingreso[i] + 0.3, str(nuevo_ingreso[i]))
    plt.text(indx[i] - 0.04, matriculados[i] + 0.3 , str(matriculados[i]))

plt.gca().set_xticklabels(labels)
plt.title(titulacion)
plt.xlabel("Curso academico")
plt.legend(['Plazas ofertadas','Alumnos nuevo ingreso','Matriculados'])

plt.savefig("figures_examples/fig_matricula.png")

#Esta tabla contiene informacion sobre el numero de creditos
#TODO
table_parsed = next(iterate_list)

#Esta tabla contiene informacion de los cursos de adaptacion
table_parsed = next(iterate_list)

#Esta lista contiene duracion media graduados
table_parsed = next(iterate_list).replace("","0")
labels =  table_parsed.loc[1:,0].values
duracion_media = np.array(table_parsed.loc[1:,1].values, dtype = np.float)

indx = np.arange(len(duracion_media))

width=0.4
plt.figure()
plt.bar(indx,duracion_media, width = width)

for i in range(len(duracion_media)):
    plt.text(indx[i] - 0.05, duracion_media[i] + 0.02, str(duracion_media[i]), size = 12)

plt.xticks(indx)
plt.gca().set_xticklabels(labels)
plt.title(titulacion)
plt.xlabel("Curso academico")
plt.ylabel("Años")
plt.legend(["Duración media graduados"])

plt.savefig("figures_examples/fig_duracion_graduados.png")


#Esta tabla contiene tasa de exito, rendimiento y eficiencia
table_parsed = next(iterate_list).replace("","0")

labels =  table_parsed.loc[1:,0].values
exito = np.array(table_parsed.loc[1:,1].values, dtype = np.float)
rendimiento = np.array(table_parsed.loc[1:,2].values, dtype = np.float)
eficiencia = np.array(table_parsed.loc[1:,3].values, dtype = np.float)

indx = np.arange(len(exito))
width=0.2
plt.figure()
plt.bar(indx - width,exito, width = width)
plt.bar(indx,rendimiento, width = width)
plt.bar(indx + width,eficiencia, width = width)

for i in range(len(exito)):
    plt.text(indx[i] - width - 0.08, exito[i] + 0.4, str(exito[i]) + "%", size=9)
    plt.text(indx[i] - 0.08 , rendimiento[i] + 0.4, str(rendimiento[i]) + "%", size=9)
    plt.text(indx[i] + width - 0.08 , eficiencia[i] + 0.4, str(eficiencia[i]) + "%", size=9)

plt.xticks(indx)
plt.gca().set_xticklabels(labels)
plt.title(titulacion)
plt.xlabel("Curso academico")
plt.ylabel("Porcentaje (%)")
plt.legend(["Exito","Rendimiento","Eficiencia"], loc = 'lower right')

plt.savefig("figures_examples/fig_tasas.png")
