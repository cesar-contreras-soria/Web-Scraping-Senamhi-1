# Web-Scraping-Senamhi
Web Scraping del Servicio Nacional de Meteorología e Hidrología del Perú
El objetivo del documento es descargar información sobre variables climáticas de las Estaciones Convencionales con recepción de datos en tiempo real del Senamhi.
El mismo código puede ser utilizado para obtener información de las "Estaciones Convencionales con recepción de datos en tiempo diferido" y "Estaciones automáticas".
Antes de descargar la información, se recomienda tener en cuenta los siguientes comentarios:
1) La información disponible en la página web a ser scrapeada pertenece a lugares específicos en el Perú. Es necesario aplicar técnicas de interpolación para 
obtener información de todo el Perú.
2) En caso no se dificulte obtener la información mediante el inciso (1), se recomienda utilizar datos procesados del Senamhi como, por ejemplo, la base de datos PISCO
o datos procesados de instituciones internacionales como, por ejemplo, ERA5 (https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-land-monthly-means?tab=form).
