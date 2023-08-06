from django.conf.urls import patterns, include, url

from molo.commenting import views


urlpatterns = patterns(
    '',
    url(r'molo/report/(\d+)/$', views.report, name='molo-comments-report'),
    url(r'^comments/reported/(?P<comment_pk>\d+)/$',
        views.report_response, name='report_response'),

    url(r'molo/post/$', views.post_molo_comment, name='molo-comments-post'),
    url(
        r'molo/(?P<page_id>\d+)/comments/$',
        views.view_more_article_comments,
        name='more-comments'),
    url(r'', include('django_comments.urls')),
)
