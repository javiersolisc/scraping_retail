from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import os
import csv

#Obtener los links por item

def get_links_from_page(url:str) -> list:
    options = Options()
    options.add_argument('--window-size=1920,1200')
    options.add_argument('--headless') 

    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),options=options)

    driver.get(url)
    page = driver.page_source
    driver.quit()

    html_soup = BeautifulSoup(page, 'html.parser')
    
    link_list = html_soup.find_all('a', {'class':'catalog-product-item catalog-product-item__container undefined'})
    
    urls_items = []
    for item in link_list:
            i = item['href']
            urls_items.append(f'https://simple.ripley.com.pe{i}')
    return urls_items


#Obtener los links por paginas

def get_all_links():
    link_all = []
    for i in range(1,14):
        print(f"Processing... Page: {i}")
        sleep(1)
        url_base = f"https://simple.ripley.com.pe/tecnologia/celulares/celulares-y-smartphones?s=mdco&page={i}"
        link_list_page = get_links_from_page(url_base)
        link_all.extend(link_list_page)
    
    return link_all

# normalize 
def normalize(s):
    replacements = (
    ("á", "a"),
    ("é", "e"),
    ("í", "i"),
    ("ó", "o"),
    ("ú", "u"),
    )
    for a, b in replacements:
        s = s.lower().replace(a, b)
    return s

# Obtener informacion por item

def get_info_from_link(url:str) -> dict:
    options = Options()
    options.add_argument('--window-size=1920,1200')
    options.add_argument('--headless') 

    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),options=options)

    driver.get(url)
    page = driver.page_source
    driver.quit()

    html_soup = BeautifulSoup(page, 'html.parser')
    
    #obtener el nombre 
    try:
        product_header = html_soup.find('section',{'class':'product-header hidden-xs'})
        product_name = product_header.h1.text
    except:
        product_name = " "
                
    #obtener precio normal
    try:
        precio_normal = html_soup.find('div',{'class':'product-price-container product-internet-price-not-best'})
        price = precio_normal.dt.text
    except:
        price = " "
        
    #obtener el precio oferta
    try:
        precio_oferta = html_soup.find('div',{'class':'product-price-container product-ripley-price'})
        price_off = precio_oferta.dt.text
    except:
        price_off = " "
        
    #obtener las especificaciones
    rows = html_soup.find_all('tr')
    dic = {}
    for row in rows:
        # find all the columns in each row
        cols = row.find_all('td')
        # extract the text from each column
        cols_text = [col.text for col in cols]
        dic[normalize(cols_text[0])] = cols_text[1]
    
    #Agregando las variables
    
    dic_var = {'nombre': product_name, 'precio normal': price, 'precio oferta': price_off}
    dic_var.update(dic)
    
    variables = [
            'nombre',
            'precio normal',
            'precio oferta',
            'marca',
            'peso (kg)',
            'memoria interna',
            'memoria ram',
            'procesador',
            'tipo procesador',
            'camara frontal',
            'camara posterior rango',
            'camara posterior',
            'capacidad de bateria',
            'resolución de la pantalla',
            'tamaño de pantalla rango',
            'tamaño de la pantalla',
            'sistema operativo rango',
            'sistema operativo',
            'compañia',
            'resistente al agua',
            'tipo de conector',
            'conectividad',
            'entrada de audio',
            'bluetooth',
            'tipo de pantalla',
            'sim',
            'cantidad de cámaras',
            'lector de huella digital',
            'zoom digital (x)',
            'usb',
            'nfc',
            'zona wi-fi',
            'localizacion',
            'chip de compañia incluido',
            'flash',
            'contrato',
            'enfoque automatico',
            'radio',
            'formatos video',
            'reproduce formato(s) de audio',
            'velocidad cpu',
            'bateria',
            'garantia',
            'tipo de producto',
            'modelo',
            'alto (cm)',
            'ancho (cm)',
            'largo (cm)'
            ]
    
    # emparejamos caracteristicas y variables
    
    matched_elements = {}
    for var in variables:
        if var in dic_var:
            matched_elements[var] = dic_var[var]
        else:
            matched_elements[var]=""

    return matched_elements 

def append_csv(data:dict):
    if not (os.path.exists("data.csv")):
        field = [
            'nombre',
            'precio normal',
            'precio oferta',
            'marca',
            'peso (kg)',
            'memoria interna',
            'memoria ram',
            'procesador',
            'tipo procesador',
            'camara frontal',
            'camara posterior rango',
            'camara posterior',
            'capacidad de bateria',
            'resolución de la pantalla',
            'tamaño de pantalla rango',
            'tamaño de la pantalla',
            'sistema operativo rango',
            'sistema operativo',
            'compañia',
            'resistente al agua',
            'tipo de conector',
            'conectividad',
            'entrada de audio',
            'bluetooth',
            'tipo de pantalla',
            'sim',
            'cantidad de cámaras',
            'lector de huella digital',
            'zoom digital (x)',
            'usb',
            'nfc',
            'zona wi-fi',
            'localizacion',
            'chip de compañia incluido',
            'flash',
            'contrato',
            'enfoque automatico',
            'radio',
            'formatos video',
            'reproduce formato(s) de audio',
            'velocidad cpu',
            'bateria',
            'garantia',
            'tipo de producto',
            'modelo',
            'alto (cm)',
            'ancho (cm)',
            'largo (cm)'
        ]

        with open(r'data.csv','a',newline='') as f:
            writter = csv.writer(f)
            writter.writerow(field)

    with open(r'data.csv','a',newline='') as fw:
        print(f"Escribiendo {data['nombre']}")
        writter_w = csv.writer(fw)
        writter_w.writerow(list(data.values()))

if __name__ == "__main__":
    all_links = get_all_links()

    for link in all_links:
        info = get_info_from_link(link)
        append_csv(info)
    
    
    
    
    
