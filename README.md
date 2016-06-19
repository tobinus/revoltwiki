[![Stories in Ready](https://badge.waffle.io/RadioRevolt/revoltwiki.png?label=ready&title=Ready)](https://waffle.io/RadioRevolt/revoltwiki) [![Build Status](https://travis-ci.org/RadioRevolt/revoltwiki.svg?branch=develop)](https://travis-ci.org/RadioRevolt/revoltwiki)

# revoltwiki 

## Oppsett

Klon repoet, f.eks.: `git clone git@github.com:RadioRevolt/revoltwiki.git`
Sett opp virituelt miljø med python3, f.eks.: `mkvirtualenv -p python3 revoltwiki`
Bruk det virituelle miljøet, f.eks.: `workon revoltwiki`
Installer avhengighetene: `pip install -r requirements.txt`
Kjør migrasjonene for å opprette databasen: `python manage.py migrate`
Last inn testdata: `python manage.py loaddata dummy_data.json`

Om du vil ha en superbruker du kan logge inn på: `python manage.py createsuperuser`

## Arbeidsflyt

Alt av commits og issues (samt kommentarer på issues) skal være på norsk. All kode skal være på engelsk.

### Features

Dette skjer fra develop-branchen

1. Finn et issue som er 'ready' på [scrum-tavlen](https://waffle.io/RadioRevolt/revoltwiki), eventuelt lag et nytt issue.
2. Assign deg selv til issuet (enten via scrum-tavlen eller via github)
3. Lag en ny branch som heter 'feature/noe-fornuftig' som brancher ut fra develop
4. Husk å skrive tester om du lager ny funksjonalitet
5. Når du er ferdig test at alt virker (`python manage.py test`)
6. Lag en pull-request

### Hotfixer

Dette skjer fra master-branchen

1. Sleng inn et issue (om det er tid)
2. Lag en branch som heter 'hotfix/noe-fornuftig' som brancher fra master
3. Når du er ferdig test at alt virker (`python manage.py test`)
4. Lag en pull-request

## Prosjektoversikt

Prosjektet er delt in i flere django-apper. Hver app har en helt isolert funksjonalitet.

### revoltwiki

Dette er hovedappen, der URL-konfigurasjonen og instillingene ligger.

### api_graphql

Her er GraphQL-APIet som ligger på `/graphql`.
Det er litt rotete akkurat nå og all logikk ligger i `schema.py`.

Se [Graphene (pythonimplementasjonen av GraphQL) sin dokumentasjon](http://graphene-python.org/docs/quickstart/) for mer info.
Det er ganske vanilje-oppsett.

### api_rest

Dette er selve kjernen. På sikt hadde det vært fint å få erstattet alt dette med GraphQL, men jeg fikk ikke mutasjoner i GraphQL til å fungere.

Den er laget med [Django REST Framework](http://www.django-rest-framework.org/).
Dokumentasjonen er litt rotete, men søkefunksjonen fungerer ok om man leter etter en spesifikk metode eller liknende.

Selve strukturen ligger i `serializers.py`. Den er satt opp ganske standard, og sier mye seg selv.

Denne strukturen benyttes så av kontrolleren, som ligger i `views.py` (django <3).
Den er litt mer komplisert, men jeg skal få dokumentert det så rasket som mulig.

Kontrolleren (`views.py`) benytter igjen tilgangene som ligger i `permissions.py`.
Denne er ganske godt dokumentert. Jeg vet at flere av if-ene der kan slås sammen, men helst ikke gjør det.
Det er et ganske stort poeng at tilgangene blir riktig, og da er det best å skrive det sånn at det er lett å se at det blir korrekt.

### data_models

Her er databasemodellen (og migrasjoner i `migrations/`-mappen). Alt ligger i `models.py` og er ganske standard Django.

### frontend_django

Her tenkte jeg å lage en rask og stygg django-frontend for wikien. Så kan den leve inntil en bedre (f.eks. React) kommer på plass.