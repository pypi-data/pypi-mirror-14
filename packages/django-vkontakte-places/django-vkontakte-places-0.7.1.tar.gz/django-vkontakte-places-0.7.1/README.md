Django Vkontakte Places
=======================

[![PyPI version](https://badge.fury.io/py/django-vkontakte-places.png)](http://badge.fury.io/py/django-vkontakte-places) [![Build Status](https://travis-ci.org/ramusus/django-vkontakte-places.png?branch=master)](https://travis-ci.org/ramusus/django-vkontakte-places) [![Coverage Status](https://coveralls.io/repos/ramusus/django-vkontakte-places/badge.png?branch=master)](https://coveralls.io/r/ramusus/django-vkontakte-places)

Приложение позволяет взаимодействовать с географическими объектами Вконтакте, такими как страны и города через Вконтакте API используя стандартные модели Django

Установка
---------

    pip install django-vkontakte-places

В `settings.py` необходимо добавить:

    INSTALLED_APPS = (
        ...
        'oauth_tokens',
        'taggit',
        'vkontakte_api',
        'vkontakte_places',
    )

    # oauth-tokens settigs
    OAUTH_TOKENS_HISTORY = True                                         # to keep in DB expired access tokens
    OAUTH_TOKENS_VKONTAKTE_CLIENT_ID = ''                               # application ID
    OAUTH_TOKENS_VKONTAKTE_CLIENT_SECRET = ''                           # application secret key
    OAUTH_TOKENS_VKONTAKTE_SCOPE = ['ads,wall,photos,friends,stats']    # application scopes
    OAUTH_TOKENS_VKONTAKTE_USERNAME = ''                                # user login
    OAUTH_TOKENS_VKONTAKTE_PASSWORD = ''                                # user password
    OAUTH_TOKENS_VKONTAKTE_PHONE_END = ''                               # last 4 digits of user mobile phone

Покрытие методов API
--------------------

* [places.getCountries](http://vk.com/dev/places.getCountries) – возвращает список стран;
* [places.getCities](http://vk.com/dev/places.getCities) – возвращает список городов;
* [places.getRegions](http://vk.com/dev/places.getRegions) – возвращает список регионов;
* [places.getCountryById](http://vk.com/dev/places.getCountryById) – возвращает информацию о странах по их id;
* [places.getCityById](http://vk.com/dev/places.getCityById) – возвращает информацию о городах по их id;
* [places.getStreetById](http://vk.com/dev/places.getStreetById) – возвращает информацию об улицах по их id;

В планах:

* [places.getById](http://vk.com/dev/places.getById) – возвращает информацию о местах;
* [places.search](http://vk.com/dev/places.search) – возвращает список найденных мест;
* [places.getCheckins](http://vk.com/dev/places.getCheckins) – возвращает список отметок;
* [places.getTypes](http://vk.com/dev/places.getTypes) – возвращает список типов мест;