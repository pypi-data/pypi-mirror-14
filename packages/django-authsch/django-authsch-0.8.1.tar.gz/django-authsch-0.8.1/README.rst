===============
Auth.sch kliens
===============

Leírás
------

Egyszerűen használható auth.sch kliens. Saját felhasználói modellel is működik, mivel a
``django.contrib.auth.get_user_model`` által visszaadott felhasználói modell-t használja. Azzal a kikötéssel, hogy az
auth.sch-ban használt internal_id-t tárolni kell a user modellben (méghozzá ``unique=True`` megkötéssel).

Függőségek
----------
A django-authsch a requests csomagtól függ. Ezt használja az auth.sch-val folytatott HTTP kommunikációra. Telepíteni a
pip csomagkezelővel tudjuk:

.. code-block:: bash

    pip install requests

Telepítés
---------
Telepíteni egyszerűen a PyPI-ből a ``pip`` segítségével.

.. code-block:: bash

    pip install django-authsch

Konfigurálás
------------
Az auth.sch használatához elengedhetetlen, hogy a kliens azonosító:kulcs párokat, az internal_id-t valamint a kért scope-okat
bekonfiguráljuk. Ezen felül beállíthatjuk, hogy a felhasználói modellben melyik mezőben tároljuk a refresh_token-t. Ha
nem adunk meg refresh_token mező nevet, akkor a django-authsch nem próbálja meg elmenteni a refresh tokent.

Konfigurálni mindent a ``settings.py``-ban lehet.

.. code-block:: python

    AUTH_SCH = {
        'CLIENT_ID': 'yourClientIdFromhttps://auth.sch.bme.hu/console/index',   # kötelező megadni
        'SECRET_KEY': 'yourAwesomeSecretKeyyAlsoFromAuthSCH',   # kötelező megadni
        'SCOPES': [     # kötelező megadni a kért scope-okat
            'basic',
            'displayName',
            'egyszerű',
            'felsorolása',
            'a',
            'kért',
            'scope-oknak',
            'nuff',
            'said'
        ],
        'INTERNAL_ID_FIELD_NAME': 'auth_sch_internal_id',   # Ez a default beállítás, ha ettől nem különbözik, akkor nem kötelező megadni
        'REFRESH_TOKEN_FIELD_NAME': 'refresh_token' # Ez a default beállítás, ha ettől nem különbözik, akkor nem kötelező megadni
    }

Használat
---------
Az auth.sch leírása szerint a felhasználó beléptetéséhez össze kell állítani a megfelelő url-t a ``CLIENT_ID`` és a
``SCOPES`` (+-szal felsorolva) alapján:

https://auth.sch.bme.hu/site/login?response_type=code&client_id=**<IdeJönACLIENT_ID>**&state=asd123&scope=**<IdeJönnekAScope-ok>**

Ezt az url-t a mellékelt html template tag segítségével lehet a legegyszerűbben előállítani.

.. code-block:: django

    {% load authsch_tags %}
    <a href="{% authsch_login_url %}">Login with auth.sch</a>

Ez után kell elkészíteni a callback View-t. Ez lesz az, amire az auth.sch visszairányítja a felhasználót, és get
paraméterként megadja az access_token lekéréséhez szükséges kódot.

.. code-block:: python

    class MyCallbackView(CallbackView):
        success_url = 'ide irányítod a felhasználót, ha sikeres volt a bejelentkezés'   # Kötelező
        error_url = 'ide irányítod a felhasználót, ha sikertelen volt a bejelentkezés'  # Kötelező

        # Ezeket nem kötelező megadni
        acquire_access_token_url = 'https://auth.sch.bme.hu/oauth2/token'   # Nem kötelező megadni
        auth_sch_profile_url = 'https://auth.sch.bme.hu/api/profile/'       # Nem kötelező megadni
        internal_id_field_name = None       # Nem kötelező megadni, felülírja a settings.py-ban beállított INTERNAL_ID_FIELD_NAME-t
        refresh_token_field_name = None     # Nem kötelező megadni, felülírja a settings.py-ban beállított REFRESH_TOKEN_FIELD_NAME-t

Modell-ek
---------
Az egyetlen modell a csomagban a ``AbstractAuthSchBase``. Ez egy olyan absztrakt modell, ami tartalmazza a működéshez
elengedhetetlen internal_id-t, valamint a refresh token tárolásához használt refresh_token mezőt. Ebből (is) örököltetve
a felhasználói modellt biztosan működni fog.
