import requests
from bs4 import BeautifulSoup
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="dfs"
)
cursor = db.cursor()

visited = set()

def dfs(url):
    if url in visited:
        print(f"Sudah Dikunjungi: {url}")
        return
    
    print(f"Mengunjungi: {url}")
    visited.add(url)

    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"Error saat Mengunjungi {url}: {e}")
        return

    title = soup.title.string if soup.title else "DFS"

    paragraph = soup.find('p')
    content = paragraph.text if paragraph else "Tidak ada konten"

    try:
        cursor.execute("INSERT INTO dfs (url, title, content) VALUES (%s, %s, %s)", (url, title, content))
        db.commit()
        print(f"✅ Disimpan: {url} | {title} | {content}")
    except mysql.connector.Error as err:
        print(f"❌ Error saat menyimpan ke database: {err}")

    for link in soup.find_all('a', href=True):
        next_url = f"http://localhost{link['href']}"
        print(f"🔗 Menemukan link: {next_url}")
        dfs(next_url)

dfs("http://localhost/dfs/index.html")
dfs("http://localhost/dfs/about.html")
dfs("http://localhost/dfs/services.html")
dfs("http://localhost/dfs/contact.html")


cursor.close()
db.close()

