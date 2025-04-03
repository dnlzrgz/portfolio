---
title: "Web pages to PDF: How to Print PDFs with Selenium."
description: "A simple and updated method for converting webpages into PDF documents using Selenium and Python."
image: ""
tags: ["python", "selenium", "pdf"]
publication_date: "2025-04-03"
pubDate: "Thu, 03 Apr 2025 16:00:00 +0000"
---

While I was working on [curryvitae](/projects/curryvitae.html), a single-file script to generate a CV from a simple HTML file, I ran into the problem of automating the printing process using the browser. Unfortunately, neither ChatGPT nor a DuckDuckGo search provided any useful methods. So, I turned instead to [the official Selenium documentation](https://www.selenium.dev/documentation/webdriver/interactions/print_page/), and luckily, I found what I was looking for.

It turns out that Selenium offers a very simple way to configure and execute the print function without having to worry about obscure methods. So simple that, in fact, we only need a few lines of code:

```python

from selenium import webdriver
from selenium.webdriver.common.print_page_options import PrintOptions

# Create a web driver for Google Chrome.
driver = webdriver.Chrome()

# Instantiate a PrintOptions object.
print_options = PrintOptions()

print_options.orientation = "portrait" # or "landscape"
print_options.page_height = 27.94  # A4 height
print_options.page_width = 21.59  # A4 width

# The page we want to print out.
driver.get("https://dnlzrgz.com/about")

# Printing...
pdf = driver.print_page(print_options)

# Don't forget to close the driver once you have finished with it.
driver.quit()
```

Wait, what!? That's it? Well, it turns out that the `pdf` variable will contain a base64-encoded format of the PDF data. To generate the actual document and save it, we will need to add a couple more lines of code:

```python
import base64

#...

# Decode the base64 data.
pdf_data = base64.b64decode(pdf)

# Save the information in a file.
with open("some_title.pdf", "wb") as f:
  f.write(pdf_data)
```

The entire script will look something like this:

```python
import base64
from selenium import webdriver
from selenium.webdriver.common.print_page_options import PrintOptions


driver = webdriver.Chrome()

print_options = PrintOptions()

print_options.orientation = "portrait" # or "landscape"
print_options.page_height = 27.94  # A4 height
print_options.page_width = 21.59  # A4 width

driver.get("https://dnlzrgz.com/about")

pdf = driver.print_page(print_options)
pdf_data = base64.b64decode(pdf)
with open("some_title.pdf", "wb") as f:
  f.write(pdf_data)

driver.quit()

```
