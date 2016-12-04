from django.conf.urls import url
from qa.views import index, question, profile, index_hot, tags, login_page, signup_page, ask_question, logout_user
from django.views.static import serve

urlpatterns = [
    url(r'^$', index, name='home'),
    url(r'^hot/', index_hot, name='popular_home'),
    url(r'^uploads/(?P<path>.*)$', serve, {'document_root': 'uploads/'}),
    url(r'^question/(?P<pk>\d+)/', question, name='question'),
    url(r'^tag/(?P<slug>.+)/', tags, name="tags"),
    url(r'^login/', login_page, name="login_page"),
    url(r'^signup/', signup_page, name="signup_page"),
    url(r'^ask/', ask_question, name="ask_page"),
    url(r'^profile/(?P<name>.*)/', profile, name='profile_page'),
    url(r'logout/', logout_user, name='logout'),
    # url(r'^popular/', popular_questions, name='popular_questions'),
]
