
import os
import time
import pandas as pd

from multiprocessing import Pool
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')
options.add_experimental_option('prefs', {
        "download.prompt_for_download": False,
        "download.default_directory" : r"C:\Users\CESAR\Desktop\Github",
        "savefile.default_directory": r"C:\Users\CESAR\Desktop\Github"})
chromedriver =  r'C:\Program Files\Chromedriver\chromedriver.exe'
os.environ["webdriver.chrome.driver"] = chromedriver

driver = webdriver.Chrome(chromedriver, chrome_options=options)

#Pagina web
driver.get('https://www.senamhi.gob.pe/?&p=estaciones')

driver.switch_to.frame(0)

#Seleccion de estaciones. Seleccion de estacion en tiempo real:
#Tiempo real
#driver.find_element('xpath','/html/body/div/div[2]/div[1]/div[2]/section/div[3]/label[1]/div/input').click()
#Tiempo diferido
driver.find_element('xpath','/html/body/div/div[2]/div[1]/div[2]/section/div[3]/label[2]/div/input').click()
#Automatico
driver.find_element('xpath','/html/body/div/div[2]/div[1]/div[2]/section/div[3]/label[3]/div/input').click()

time.sleep(2)
driver.switch_to.parent_frame()
#Es necesario desplazar el visor hacia abajo para habilitar los botones
driver.execute_script("scrollBy(0,+400)")
time.sleep(2)
driver.switch_to.frame(0)

lista1 = []
lista2 = []
lista3 = []

#Conteo de imagenes
mapa_imagenes = driver.find_element('xpath','/html/body/div/div[1]/div[4]')
imagenes = mapa_imagenes.find_elements(By.TAG_NAME,'img')
for img in range(1,len(imagenes)+1):
	nombre = driver.find_element('xpath','/html/body/div/div[1]/div[4]/img[' + str(img) + ']')
	titulo = nombre.get_attribute("title")
	print("Estacion:",titulo)
	lista1.append([titulo])

print("------------------------------------------------------")
print("Finalizó la descarga de los nombres de las estaciones.")
print("------------------------------------------------------")

for est in range(len(lista1)+1):
	estacion = lista1[est]
	estacion = str(estacion).replace("['","").replace("']","")
	print("Información de la estacion:",estacion)

	#Buscar
	driver.find_element('xpath','/html/body/div/div[2]/div[1]/div[3]/a[2]').click()
	driver.find_element('xpath','/html/body/div/div[2]/div[1]/div[3]/input').send_keys(estacion)
	time.sleep(1)
	driver.find_element('xpath','/html/body/div/div[2]/div[1]/div[3]/ul/li').click()
	time.sleep(4)

	#Tabla
	frame2 = driver.find_element('xpath','//*[@id="mapid"]/div[1]/div[6]/div/div[1]/div/div/iframe')
	driver.switch_to.frame(frame2)
	driver.find_element('xpath','/html/body/div/div/main/div[1]/div/div[2]/a').click()

	#Descargar - Cabecera
	n_dpto = driver.find_element('xpath','/html/body/div/div/main/div[3]/form/table[1]/tbody/tr[3]/td[2]').text
	n_prov = driver.find_element('xpath','/html/body/div/div/main/div[3]/form/table[1]/tbody/tr[3]/td[4]').text
	n_dist = driver.find_element('xpath','/html/body/div/div/main/div[3]/form/table[1]/tbody/tr[3]/td[6]').text
	n_lat = driver.find_element('xpath','/html/body/div/div/main/div[3]/form/table[1]/tbody/tr[4]/td[2]').text
	n_lon = driver.find_element('xpath','/html/body/div/div/main/div[3]/form/table[1]/tbody/tr[4]/td[4]').text
	n_alt = driver.find_element('xpath','/html/body/div/div/main/div[3]/form/table[1]/tbody/tr[4]/td[6]').text
	n_est_tip = driver.find_element('xpath','/html/body/div/div/main/div[3]/form/table[1]/tbody/tr[5]/td[2]').text
	n_est_cod = driver.find_element('xpath','/html/body/div/div/main/div[3]/form/table[1]/tbody/tr[5]/td[4]').text
	time.sleep(1)

	if n_est_tip=='Convencional - Hidrológica':
		#Seleccionar fecha
		conteo_fechas = driver.find_element('xpath','/html/body/div/div/main/div[3]/form/table[1]/tbody/tr[3]/td[7]/div/select')
		fechas = conteo_fechas.find_elements(By.TAG_NAME,'option')
		seleccionar = Select(driver.find_element('id','CBOFiltro'))
		for mes in range(len(fechas)):
			seleccionar.select_by_index(mes)
			time.sleep(3)
			#Descargar - Cuerpo
			nuevo_mes = mes + 1
			n_mes = driver.find_element('xpath','/html/body/div/div/main/div[3]/form/table[1]/tbody/tr[3]/td[7]/div/select/option[' + str(nuevo_mes) + ']')

			#Nuevo frame
			frame3_h = driver.find_element('xpath','//*[@id="interior"]')
			driver.switch_to.frame(frame3_h)
			conteo_dias = driver.find_element('xpath','/html/body/table')
			dias = conteo_dias.find_elements(By.TAG_NAME,'tr')
			for obs in range(3,len(dias)):
				n_dia = driver.find_element('xpath','/html/body/table/tbody/tr[' + str(obs) + ']/td[1]/div').text
				n_06 = driver.find_element('xpath','/html/body/table/tbody/tr[' + str(obs) + ']/td[2]/div').text
				n_10 = driver.find_element('xpath','/html/body/table/tbody/tr[' + str(obs) + ']/td[3]/div').text
				n_14 = driver.find_element('xpath','/html/body/table/tbody/tr[' + str(obs) + ']/td[4]/div').text
				n_18 = driver.find_element('xpath','/html/body/table/tbody/tr[' + str(obs) + ']/td[5]/div').text
				time.sleep(1)
				lista2.append([estacion,n_dpto,n_prov,n_dist,n_lat,n_lon,n_alt,n_est_tip,n_est_cod,n_dia,n_06,n_10,n_14,n_18])
				base_dato = pd.DataFrame(lista2,columns=['estacion','n_dpto','n_prov','n_dist','n_lat','n_lon','n_alt','n_est_tip','n_est_cod','n_dia','n_06','n_10','n_14','n_18'])
				base_dato.to_csv('Senamhi_Estacion_Real_Hidrologica.csv',encoding='utf-8-sig',index=False)
			driver.switch_to.parent_frame()

	else:
		#Seleccionar fecha
		conteo_fechas = driver.find_element('xpath','/html/body/div/div/main/div[3]/form/table[1]/tbody/tr[3]/td[7]/div/select')
		fechas = conteo_fechas.find_elements(By.TAG_NAME,'option')
		seleccionar = Select(driver.find_element('id','CBOFiltro'))
		for mes in range(len(fechas)):
			seleccionar.select_by_index(mes)
			time.sleep(1)
			#Descargar - Cuerpo
			nuevo_mes = mes + 1
			n_mes = driver.find_element('xpath','/html/body/div/div/main/div[3]/form/table[1]/tbody/tr[3]/td[7]/div/select/option[' + str(nuevo_mes) + ']')

			#Nuevo frame
			frame3_m = driver.find_element('xpath','//*[@id="interior"]')
			driver.switch_to.frame(frame3_m)
			conteo_dias = driver.find_element('xpath','/html/body/table')
			dias = conteo_dias.find_elements(By.TAG_NAME,'tr')
			for obs in range(3,len(dias)):
				n_dia = driver.find_element('xpath','/html/body/table/tbody/tr[' + str(obs) + ']/td[1]/div').text
				n_tmax = driver.find_element('xpath','/html/body/table/tbody/tr[' + str(obs) + ']/td[2]/div').text
				n_tmin = driver.find_element('xpath','/html/body/table/tbody/tr[' + str(obs) + ']/td[3]/div').text
				n_hum = driver.find_element('xpath','/html/body/table/tbody/tr[' + str(obs) + ']/td[4]/div').text
				n_pre = driver.find_element('xpath','/html/body/table/tbody/tr[' + str(obs) + ']/td[5]/div').text
				time.sleep(1)
				lista3.append([estacion,n_dpto,n_prov,n_dist,n_lat,n_lon,n_alt,n_est_tip,n_est_cod,n_dia,n_tmax,n_tmin,n_hum,n_pre])
				base_dato = pd.DataFrame(lista3,columns=['estacion','n_dpto','n_prov','n_dist','n_lat','n_lon','n_alt','n_est_tip','n_est_cod','n_dia','n_tmax','n_tmin','n_hum','n_pre'])
				base_dato.to_csv('Senamhi_Estacion_Real_Meteorologica.csv',encoding='utf-8-sig',index=False)
			driver.switch_to.parent_frame()

		driver.switch_to.parent_frame()
	driver.switch_to.parent_frame()

	#Preparacion para la siguiente estacion
	time.sleep(4)
	driver.find_element('xpath','/html/body/div/div[2]/div[1]/div[3]/input').clear()
	time.sleep(2)
	driver.find_element('xpath','/html/body/div/div[2]/div[1]/div[3]/a[2]').click()

