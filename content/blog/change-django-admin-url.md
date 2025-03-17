---
title: "Changing the Django admin URL"
description: "A simple change than can protect you and your site from basic brute force attacks."
image: ""
tags: ["django", "security"]
publication_date: "2024-08-15"
pubDate: "Thu, 15 Aug 2024 00:00:00 +0000"
---

The most well-known URL for every Django developer is the default admin URL. It is the page where developers and site administrators will spent a considerable amount of time managing their applications since it provides access to a wide array of functionalities and information. That's why, if you are monitoring your logs, you'll likely notice a recurring pattern of requests to this URL, as well as to admin URLs for other platforms such as WordPress.

Fortunately, changing the default URL is really simple, and it can provide some level of protection for your site. Most of these attacks are automated, and unless your site is being specifically targeted, they will encounter a few 404 pages and just move on.

The most simple way to change this URL path is to hardcode the new path into the main urls.py file like this:

```python
from django.contrib import admin
from django.urls import path

urlpatterns = [
 path('secret-admin/', admin.site.urls),
 # other paths
]
```

However, I prefer to use environment variables. Typically, I define a variable like DJANGO_ADMIN_URL in my settings.py file, and then I simply import it into my urls.py file, and it's done.

```python
from django.conf import settings
from django.contrib import admin
from django.urls import path

urlpatterns = [
 path(settings.DJANGO_ADMIN_URL, admin.site.urls),
 #…
]
```
