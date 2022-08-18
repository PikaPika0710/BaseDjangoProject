from rest_framework import routers

from api_task.views import TaskViewSet

app_name = 'api_task'

router = routers.SimpleRouter(trailing_slash=True)
router.register(r'', TaskViewSet, basename='task')

urlpatterns = router.urls
