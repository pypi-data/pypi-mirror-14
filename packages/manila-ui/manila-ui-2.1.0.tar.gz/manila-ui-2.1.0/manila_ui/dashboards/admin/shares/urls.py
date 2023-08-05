# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from django.conf.urls import patterns  # noqa
from django.conf.urls import url  # noqa

from manila_ui.dashboards.admin.shares import views
from manila_ui.dashboards.project.shares.security_services \
    import views as project_sec_services_views
from manila_ui.dashboards.project.shares.share_networks\
    import views as project_share_net_views
from manila_ui.dashboards.project.shares.snapshots\
    import views as project_snapshot_views

urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<share_id>[^/]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^snapshots/(?P<snapshot_id>[^/]+)$',
        project_snapshot_views.SnapshotDetailView.as_view(),
        name='snapshot-detail'),
    url(r'^share_networks/(?P<share_network_id>[^/]+)$',
        project_share_net_views.Detail.as_view(),
        name='share_network_detail'),
    url(r'^security_services/(?P<sec_service_id>[^/]+)$',
        project_sec_services_views.Detail.as_view(),
        name='security_service_detail'),
    url(r'^create_type$', views.CreateShareTypeView.as_view(),
        name='create_type'),
    url(r'^manage_share_type_access/(?P<share_type_id>[^/]+)$',
        views.ManageShareTypeAccessView.as_view(),
        name='manage_share_type_access'),
    url(r'^update_type/(?P<share_type_id>[^/]+)/extra_specs$',
        views.UpdateShareTypeView.as_view(),
        name='update_type'),
    url(r'^share_servers/(?P<share_server_id>[^/]+)$',
        views.ShareServDetail.as_view(),
        name='share_server_detail'),
    url(r'^manage$', views.ManageShareView.as_view(), name='manage'),
    url(r'^unmanage/(?P<share_id>[^/]+)$', views.UnmanageShareView.as_view(),
        name='unmanage'),
)
