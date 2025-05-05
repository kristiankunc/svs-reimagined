from .views.projects import urlpatterns as project_urls
from .views.root import urlpatterns as root_urls

urlpatterns = []
urlpatterns += root_urls
urlpatterns += project_urls
