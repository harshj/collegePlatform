from django.conf.urls import url
from .views import signup,activate,login,profile,moredetail,modifynews,deletenews,like,unlike,bookmark,unbookmark,editprofile,editprofileredirect
# logout,forgot_password, reset_password, login, home
urlpatterns = [
    #url(r'^logout/$', logout, name ="logout" ),
    url(r'^signup/$', signup, name ="signup" ),
    #url(r'^forgot-password/$', forgot_password, name ="forgot-password" ),
    #url(r'^reset/(?P<id>\d+)/(?P<otp>\d{4})/$', reset_password, name='reset-password'),
    url(r'^activate/(?P<id>\d+)/(?P<otp>\d{4})/$', activate, name='activate-account'),
    url(r'login/$',login,name="login"),
    url(r'profile/(?P<id>\d+)/$',profile,name="profile"),
    url(r'like/(?P<id1>\d+)/(?P<id2>\d+)/$',like,name='like'),
    url(r'unlike/(?P<id2>\d+)/$',unlike,name='unlike'),
    url(r'bookmark/(?P<id2>\d+)/$',bookmark,name='bookmark'),
    url(r'unbookmark/(?P<id1>\d+)/(?P<id2>\d+)/$',unbookmark,name='unbookmark'),
    url(r'moredetail/(?P<id1>\d+)/(?P<id2>\d+)/$',moredetail,name='moredetail'),
    url(r'modifynews/(?P<id1>\d+)/(?P<id2>\d+)/$',modifynews,name='modifynews'),
    url(r'deletenews/(?P<id1>\d+)/(?P<id2>\d+)/$',deletenews,name='deletenews'),
    url(r'editprofileredirect/(?P<id1>\d+)/$',editprofileredirect,name='editprofileredirect'),
    url(r'editprofile/$',editprofile,name='editprofile')
    #url(r'^(?P<id>\d+)/home/$', home, name = "home"),
]