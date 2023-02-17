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
    
    link_list = html_soup.find_all('a', {'class':'jsx-1327784995 jsx-97019337 pod-link'})
    
    urls_items = []
    for item in link_list:
        urls_items.append(item['href'])
    return urls_items

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

#Obtener los links por paginas

def get_all_links():
    link_all = []
    for i in range(1,2):
        print(f"Processing... Page: {i}")
        sleep(0.2)
        url_base = f"https://www.falabella.com.pe/falabella-pe/category/cat760706/Celulares-y-Telefonos?page={i}"
        link_list_page = get_links_from_page(url_base)
        link_all.extend(link_list_page)
    
    return link_all

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
        nombre = html_soup.find ("div",{'class':'jsx-1442607798 product-name fa--product-name false'}).text
    except:
        nombre = " "
        
    #obtener la marca
    try:
        marca0 = html_soup.find('a',{'class':'jsx-1874573512 product-brand-link'}).text
    except:
        marca0 = " "
        
    #obtener regular
    try:
        precio_normal = html_soup.find('li',{'class':'jsx-2797633547 prices-1'}).text
    except:
        precio_normal = " "
        
    #obtener el precio oferta
    try:
        precio_oferta = html_soup.find('li',{'class':'jsx-2797633547 prices-0'}).text
    except:
        precio_oferta = " "
        
    #obtener las especificaciones
      
    tds = []
    for header in html_soup.find_all('td',{'class':'jsx-428502957 property-name'}):
            tds.append(normalize(header.text))
    
    specs = []
    for caracteristicas in html_soup.find_all('td',{'class':'jsx-428502957 property-value'}):
        specs.append(caracteristicas.text)
    

    datos = [nombre, marca0, precio_normal, precio_oferta]
    datos.extend(specs)
    nombre_de_var = ['nombre del producto','marca0','precio normal', 'precio oferta']
    nombre_de_var.extend(tds)
    
    elements = dict(zip(nombre_de_var,datos))
    
    variables = [
            'nombre del producto',
            'marca0',
            'precio normal',
            'precio oferta',
            'camara posterior',
            'camara frontal',
            'tamaño de la pantalla',
            'memoria interna',
            'nucleos del procesador',
            'memoria expandible',
            'velocidad del procesador',
            'memoria ram',
            'tipo de pantalla',
            'sistema operativo',
            'lector de huella',
            'gps integrado',
            'conexion bluetooth',
            'resistente al agua',
            'conectividad',
            'marca',
            'modelo',
            'tipo',
            'alto',
            'ancho',
            'profundidad',
            'peso',
            'garantia del proveedor',
            'condicion del producto'
        ]
    
    # emparejamos caracteristicas y variables
    
    matched_elements = {}
    for var in variables:
        if var in elements:
            matched_elements[var] = elements[var]
        else:
            matched_elements[var]=""

    return matched_elements 

def append_csv(data:dict):
    if not (os.path.exists("data.csv")):
        field = [
            'nombre del producto',
            'marca0',
            'precio normal',
            'precio oferta',
            'camara posterior',
            'camara frontal',
            'tamaño de la pantalla',
            'memoria interna',
            'nucleos del procesador',
            'memoria expandible',
            'velocidad del procesador',
            'memoria ram',
            'tipo de pantalla',
            'sistema operativo',
            'lector de huella',
            'gps integrado',
            'conexion bluetooth',
            'resistente al agua',
            'conectividad',
            'marca',
            'modelo',
            'tipo',
            'alto',
            'ancho',
            'profundidad',
            'peso',
            'garantia del proveedor',
            'condicion del producto'
        ]

        with open(r'data.csv','a',newline='') as f:
            writter = csv.writer(f)
            writter.writerow(field)

    with open(r'data.csv','a',newline='') as fw:
        print(f"Escribiendo {data['nombre del producto']}")
        writter_w = csv.writer(fw)
        writter_w.writerow(list(data.values()))

if __name__ == "__main__":
    all_links = get_all_links()

    for link in all_links:
        info = get_info_from_link(link)
        append_csv(info)