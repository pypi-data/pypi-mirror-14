from django.conf.urls import url
from hidash import views

urls = [
     url(r'^charts/(?P<chart_id>\w*\.json)/$', views.dispatch_chart),
     url(r'^charts/(?P<chart_id>\w*\.xls)/$', views.dispatch_xls),
     url(r'^reports/(?P<chart_id>\w*\.pdf)/$', views.dispatch_pdf),
     url(r'^show_reports/$', views.dispatch_group_reports),
      ]
