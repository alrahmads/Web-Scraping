import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

url = "https://www.tokopedia.com/search?st=&q=emina"

data=[]
driver = webdriver.Chrome()
driver.get(url)

for i in range(20):
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#zeus-root")))
    time.sleep(2)

    for j in range(10):
        driver.execute_script("window.scrollBy(0, 250)")
        time.sleep(1)

    driver.execute_script("window.scrollBy(50, 0)")
    time.sleep(1)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    for item in soup.findAll('div', class_="css-1asz3by"):
        nama_produk = item.find('div', class_="css-3um8ox").text
        harga = item.find('div', class_="css-h66vau").text

        for item2 in item.findAll('div', class_='css-1rn0irl'):
            toko = item2.findAll('span', class_='css-1kdc32b.flip')
            if len(toko) > 0:
                toko = item2.findAll('span', class_='css-1kdc32b.flip')[0].text
            else:
                toko = " "

            lokasi = item2.findAll('span', class_='css-1kdc32b.flip')
            if len(lokasi) > 0:
                lokasi = item2.findAll('span', class_='css-1kdc32b flip')[0].text
            else:
                lokasi = " "


        rating = item.findAll('span', class_='css-t70v7i')
        if len(rating) > 0:
            rating = item.find('span', class_='css-t70v7i').text
        else:
            rating = "0"
    
        terjual = item.findAll('span', class_='css-1sgek4h')
        if len(terjual) > 0:
            terjual = item.find('span', class_="css-1sgek4h").text
        else:
            terjual = "0"
    
data.append(
    (toko, lokasi, nama_produk, harga, terjual, rating)
            )
    
time.sleep(2)
driver.find_element(By.CSS_SELECTOR, "button[aria-label^='Laman berikutnya']").click()
time.sleep(3)

df = pd.DataFrame(data, columns=['Toko', 'Lokasi', 'Nama Barang', 'Harga', 'Terjual', 'Rating'])
print(df)

driver.close()

#saving the excel
df.to_excel('tokopedia_scraping.xlsx', index=False)
print('Data Telah Tersimpan')