# Automated SEO Reporting
*Python, Web Scraping*
<p align="justify"> 
El objetivo de este proyecto es la creación de una herramienta para analizar las menciones de una empresa en el motor de búsqueda Google. A través de ella se pretende automatizar la creación de informes sobre posicionamiento SEO, de manera que, al introducir palabras clave en el buscador, el programa analiza todos los resultados, así como las búsquedas relacionadas sugeridas por el navegador, e identifica en cuantas de ellas aparece la empresa y por qué conceptos. La solución consiste en realizar un web scraping seguido del procesamiento de los datos, la generación de gráficos y, asimismo, la creación de un documento html con la información obtenida para análisis posteriores.
</p>

## Objetivos 
- Rastrear las menciones de la empresa en relación a ciertas búsquedas
- Analizar las menciones de la empresa para las búsquedas similares sugeridas por Google
- Automatizar la creación de KPIs y gráficos predefinidos para agilizar el análisis SEO de la empresa

## Proyecto

### Web Scraping
<p align="justify"> 
La creación del proceso de web scraping es el primer paso para el desarrollo de la aplicación. Para hacerlo se ha creado una clase con varias funciones que permite automatizar la búsqueda de palabras clave y de las búsquedas relacionadas sugeridas por Google. Asimismo, esta también permite hacer el parsing de los resultados. Otra de las funciones permite especificar las SERP (Search Engine Result Pages) que desean consultarse, para acotar el análisis a los parámetros que se deseen y filtrar aquellos resultados de mayor calidad (teniendo en cuenta que motores de búsqueda como Google proporcionan un CTR muy bajo a partir de la tercera SERP).

Los datos extraídos serán los headers y el texto asociado (etiquetado como "Results" en los gráficos) a cada resultado en el buscador. Una vez ejecutada la búsqueda es necesario procesar los datos pasa su posterior visualización. Este paso incluye ordenar los resultados según su posicionamiento en el motor de búsqueda, analizar si contienen la palabra clave (que será el nombre de la empresa en cuestión; en este caso, La Vanguardia) y recopilar el número de menciones totales en las SERP por esta búsqueda y las relacionadas que se detecten como óptimas.
</p>

### Menciones Totales
<p align="justify"> 
Una de las métricas principales para el análisis SEO es el total de menciones contabilizadas. En este caso al analizar los resultados de la query "Noticias Barcelona", así como los de las búsquedas relacionadas, podemos observar siete menciones en los headers y trece en los resultados.
</p>

<p align="center">
<img src="Images/Graph_1" width="500">
</p>

### Porcentaje de Menciones en los Resultados
<p align="justify"> 
Aunque puede resultar muy útil conocer el total de menciones, saber el porcentaje que estas representan respecto al resto de resultados enriquece el análisis sobre la presencia online de la empresa.

Como puede observarse La Vanguardia esta en un 8,33% de los headers y en un 15,5% de los resultados para el conjunto de la búsqueda.
</p>

<p align="center">
<img src="Images/Graph_2" width="500">
</p>

### Ranking por Búsqueda
<p align="justify"> 
Otro indicador importante es saber cómo se distribuyen las menciones entre las distintas búsquedas tanto para los headers como para los resultados.

En este gráfico podemos cuáles han sido las búsquedas relacionadas sugeridas por Google así como el ranking de La Vanguardia en los distintos casos. De aquí podemos obtener dos conclusiones interesantes, la primera es que una de la búsquedas sugeridas ha sido la propia empresa, un muy buen indicador. La segunda es que La Vanguardia tiende a no incluir el nombre de la empresa en los headers.
</p>

<p align="center">
<img src="Images/Graph_3" width="500">
</p>

### Número de Menciones por Ranking
<p align="justify"> 
Finalmente, un buen medidor global del posicionamiento online de la empresa es el recuento de menciones en el entre el top tres de los resultados en Google.

En este caso el resultado es de una mención en el top uno tanto para headers como para resultados, una en el top dos para resultados y una para headers y resultados en el top 3.
</p>

<p align="center">
<img src="Images/Graph_4" width="500">
</p>

### Creación del Documento de Reporting
<p align="justify"> 
Si la aplicación tiene que ser usada por usuarios no técnicos, lo mas conveniente es crear un archivo ejecutable o un .bat a partir del script que genere un archivo con los gráficos presentados anteriormente. En este caso las visualizaciones se han realizado con la librería plotly, una de las ventajas de la cual es que cuenta con una función para extraer los gráficos en formato html e incrustarlos en un archivo.

<p align="center">
<img src="Images/HTML" width="500">
</p>
