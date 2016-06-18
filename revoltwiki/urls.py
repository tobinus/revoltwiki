from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('api_rest.urls')),
    url(r'^graphql', include('api_graphql.urls')),
    url(r'^graphiql', include('django_graphiql.urls')),
]
