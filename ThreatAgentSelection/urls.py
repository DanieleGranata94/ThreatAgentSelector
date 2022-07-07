
from django.contrib import admin
from django.urls import path

from ThreatAgentSelection import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('threat_agent_wizard', views.threat_agent_wizard, name='threat_agent_wizard'),
    path('threat_agent_generation', views.threat_agent_generation,name='threat_agent_generation'),

]
