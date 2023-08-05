# django-blogposts
Simple django blogposts app.

installation

# first step
```
pip install django-blogposts
```

# second step
```
Add into settings.py INSTALL_APPS
'django_blogposts'
```

# third step
```
$ python manage.py collectstatic
$ python manage.py migrate
```

# fourth step
```
Add into urls.py

url(r'^blog/', include('django_blogposts.urls')),

```

# fifth step
```
all templates extends from base.html. If you doesn't have it, create it or override templates
```

# optionaly
```
you can use sitemap

from django_blogposts.sitemap import BlogPostSitemap

By default django-blogposts provides with categories and tags. If you dont want use categories or tags setup in settings.py

BLOGPOSTS_USE_CATEGORIES = False

BLOGPOSTS_USE_TAGS = False

if you want to use ckeditor for editing short_content and content of post, you can install it and add into install apps


you can use search if you send request to /?q=example+of+query
```