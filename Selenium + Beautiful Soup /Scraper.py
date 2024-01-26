from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from textwrap import wrap
import os


def get_internal_links(soup, base_url):   #this function checks for all internal links
    links = set()
    for link in soup.find_all('a', href=True):
        full_url = urljoin(base_url, link['href'])
        if full_url.startswith(base_url):
            links.add(full_url)
    return links


def get_page_content(driver, url):      #grabbing the text from the page
    driver.get(url)
    return driver.page_source


def create_pdf(content, filename):
    pdf = canvas.Canvas(filename, pagesize=letter)
    pdf.setTitle(filename)

    # Define margins
    left_margin = 50

    #right_margin = 500
    bottom_margin = 50
    top_margin = 750

    # Define starting position
    x = left_margin
    y = top_margin

    for text in content:
        lines = wrap(text, 80)  # Wrap text at 80 characters
        for line in lines:
            if y <= bottom_margin:
                pdf.showPage()
                y = top_margin
            pdf.drawString(x, y, line)
            y -= 12  # Decrease Y coordinate to move to the next line

    pdf.save()
    print(f"PDF saved as {filename}")


def main():
    base_url = input("Enter URL: ")
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get(base_url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    internal_links = get_internal_links(soup, base_url)

    all_content = [BeautifulSoup(get_page_content(driver, base_url), 'html.parser').get_text()]

    for link in internal_links:
        all_content.append(BeautifulSoup(get_page_content(driver, link), 'html.parser').get_text())

    # Filename based on webpage name
    base_filename = base_url.split('//')[-1].split('/')[0].replace('.', '_')
    filename = f"{base_filename}.pdf"
    counter = 1
    while os.path.exists(filename):
        filename = f"{base_filename}_{counter}.pdf"
        counter += 1

    create_pdf(all_content, filename)
    driver.quit()


if __name__ == "__main__":
    main()
