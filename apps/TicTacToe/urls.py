from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    'TicTacToe.views',
    url(r'^$', 'main', name='main'),
    url(r'move/(?P<board_id>\d{9})/?$', 'ajax_get_move', name='get_move'),
    url(r'win/(?P<board_id>\d{9})/?$', 'ajax_check_winner', name='check_winner'),
    
)

urlpatterns += staticfiles_urlpatterns()
