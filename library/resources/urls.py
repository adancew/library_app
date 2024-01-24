from django.urls import path

from resources.views import (
    index,
    resource_detail,
    resource_edit,
    resource_enter_pick,
    resource_enter,
    resource_delete
)

app_name = 'resources'

urlpatterns = [
    # borrow urls
    path('', index, name="resources-index"),
    path('enter/', resource_enter_pick, name="resources-enter-pick"),
    path('enter/<str:res_type>', resource_enter, name="resources-enter"),
    path('<int:resource_id>/', resource_detail, name="resource-detail"),
    path('<int:resource_id>/edit', resource_edit, name="resource-edit"),
    path('<int:resource_id>/delete', resource_delete, name="resource-delete"),

]
