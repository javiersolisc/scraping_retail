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
    
    link_list = html_soup.find_all('a', {'class':'Showcase__name'})
    
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
    for i in range(1,40):
        print(f"Processing... Page: {i}")
        sleep(0.2)
        url_base = f"https://www.plazavea.com.pe/tecnologia/telefonia/celulares-y-smartphones?page={i}"
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
        nombre = html_soup.find ("h1",{'class':'ProductCard__name'}).text
    except:
        nombre = " "
        
    #obtener la marca
    try:
        marca0 = html_soup.find('span',{'class':'ProductCard__brand'}).text
    except:
        marca0 = " "
        
    #obtener regular
    try:
        precio_normal = html_soup.find('div',{'class':'ProductCard__price ProductCard__price--online'}).text
    except:
        precio_normal = " "
        
    #obtener el precio oferta
    try:
        precio_oferta = html_soup.find('div',{'class':'ProductCard__price ProductCard__price--oh'}).text
    except:
        precio_oferta = " "
        
    #obtener las especificaciones
    
    tds = []
    for header in html_soup.find_all('th'):
            tds.append(normalize(header.text))
    
    specs = []
    for caracteristicas in html_soup.find_all('td'):
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
            'alto',
            'alto con base',
            'ancho',
            'bateria',
            'camara frontal',
            'camara principal',
            'color',
            'conexión bluetooth',
            'conexion wi fi',
            'dual sim',
            'enfoque automatico',
            'garantia',
            'incluye',
            'memoria expandible',
            'memoria interna',
            'memoria ram',
            'modelo',
            'nucleos del procesador',
            'procesador',
            'profundidad',
            'radio',
            'resistente al agua',
            'resolucion de pantalla',
            'resolucion video',
            'sistema operativo',
            'tamaño pantalla celulares',
            'tecnologia celular',
            'tipo de pantalla',
            'velocidad del procesador',
            'vendido por'
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
            'alto',
            'alto con base',
            'ancho',
            'bateria',
            'camara frontal',
            'camara principal',
            'color',
            'conexión bluetooth',
            'conexion wi fi',
            'dual sim',
            'enfoque automatico',
            'garantia',
            'incluye',
            'memoria expandible',
            'memoria interna',
            'memoria ram',
            'modelo',
            'nucleos del procesador',
            'procesador',
            'profundidad',
            'radio',
            'resistente al agua',
            'resolucion de pantalla',
            'resolucion video',
            'sistema operativo',
            'tamaño pantalla celulares',
            'tecnologia celular',
            'tipo de pantalla',
            'velocidad del procesador',
            'vendido por'
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
