from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    'TicTacToe.views',
    url(r'^$', 'main', name='main'),
    url(r'move/(?P<board_id>\d{9})/$', 'ajax_get_move', name='get_move'),
    
)
