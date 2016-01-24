"""BookXchange URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'', include('home.urls')),
    url(r'^myhome/$', 'myhome.views.userhome', name='userhome'),
    url(r'^myhome/logout$', 'myhome.views.loguserout', name='logout'),
    url(r'^myhome/search$', 'search.views.search', name='search'),
    url(r'^myhome/search/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/library/$','library.views.seelibrary',name='seelibrary'),
    url(r'^myhome/editprofile$', 'myhome.views.profileEdit', name='editprofile'),
    url(r'^myhome/editaddress$', 'myhome.views.addressEdit', name='editaddress'),
    url(r'^myhome/editpreference$', 'myhome.views.preferenceEdit', name='editpreference'),
    url(r'^myhome/search/searchall$', 'search.views.searchall', name='searchall'),
    url(r'^myhome/primaryaddress/(?P<addressId>\d+)$', 'myhome.views.primaryAddress', name='setaddressprimary'),
    url(r'^myhome/deleteaddress/(?P<addressId>\d+)$', 'myhome.views.deleteAddress', name='deleteaddress'),
    url(r'^myhome/wishlist$', 'myhome.views.wishlist', name='wishlist'),
    url(r'^myhome/readlist$', 'myhome.views.readlist', name='readlist'),
    url(r'^myhome/deletelistbook/(?P<bookListId>\d+)(?P<url>.*)$', 'myhome.views.deleteListBook', name='deletelistbook'),
    url(r'^myhome/readlistbook/(?P<bookListId>\d+)$', 'myhome.views.readListBook', name='readlistbook'),
    url(r'^myhome/mylibrary$', 'library.views.mylib', name='mylib'),
    url(r'^myhome/mylibrary$', 'library.views.mylib', name='mylib'),
    url(r'^myhome/mylibrary/delete.(?P<userBookId>\d+)$','library.views.deleteUserBook', name='deleteBook'),
    url(r'^myhome/mylibrary/change.(?P<userBookId>\d+)$','library.views.changeAvailable', name='avail'),
    url(r'^myhome/mylibrary/send.(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}).(?P<userBookId>\d+)$','library.views.sendRequest', name='sendrequest'),
    url(r'^myhome/search/seeNotification$', 'search.views.seeNotification', name='seeNotification'),
    url(r'^myhome/chatsmsg.(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})$','chat.views.sendChatMessage', name='sendmsg'),
    url(r'^myhome/chatsmsgrecieve$','chat.views.recieved', name='recieved'),
    #url(r'^myhome/chatstype.(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})$','chat.views.typing', name='type'),
    #url(r'^myhome/chatsnottype.(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})$','chat.views.nottyping', name='nottype'),
    url(r'^myhome/chats$','chat.views.chat_list', name='chats'),
    url(r'^myhome/chats/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})$','chat.views.chat', name='chatuser'),
    url(r'^myhome/follow_(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})$', 'chat.views.follow', name='follow'),
    url(r'^myhome/unfollow_(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})$', 'chat.views.unfollow', name='unfollow'),
    url(r'^sharefb.(?P<bookListId>\d+).(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})_read_book$','myhome.views.sharefb', name='sharefb'),
    url(r'^ourlibrary$', 'library.views.theLibrary', name='thelib'),
    url(r'^ourlibrary/(?P<bookId>\d+)$', 'library.views.displayBook', name='getBookDetails'),
    url(r'^ourlibrary/(?P<bookId>\d+)/comments$','library.views.comments',name = 'comments'),
    url(r'^ourlibrary/(?P<bookId>\d+)/rating$','library.views.rating',name = 'ratings'),
    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
