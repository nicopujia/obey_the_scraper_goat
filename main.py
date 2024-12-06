import re
from io import BytesIO

import requests
from bs4 import BeautifulSoup
from pypdf import PdfWriter
from weasyprint import CSS, HTML

BASE_URL = "https://www.obeythetestinggoat.com"


def main():
    response = requests.get(f"{BASE_URL}/pages/book.html")
    soup = BeautifulSoup(response.text, "lxml")
    merger = PdfWriter()
    for a in soup.select("h3 + ul > li > a"):
        print(a.text)
        pdf = BytesIO(chapter_to_pdf(a))
        merger.append(pdf)
        pdf.close()
    merger.write("Test-driven web development with Python.pdf")
    merger.close()


def chapter_to_pdf(a, target=None):
    response = requests.get(BASE_URL + a["href"])
    soup = BeautifulSoup(response.text, "lxml")
    content = str(soup.find(id="content"))
    stylesheets = []
    for link in soup.head.find_all("link", {"rel": "stylesheet"}):
        href = str(link["href"])
        if not re.match(r"^http(s)?://", href):
            href = f"{BASE_URL}/book{href.lstrip(".")}"
        stylesheets.append(CSS(href))
    return HTML(string=content).write_pdf(target, stylesheets=stylesheets)


if __name__ == "__main__":
    main()
