from django.urls import path , include
from imsapp.views import *
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register(r"role",RoleViewset )
router.register(r"dept",DeptViewset )
router.register(r"desig",DesigViewset )
router.register(r"contrib",ContribFactViewset)
router.register(r"indenttype",InciTypeViewset)
router.register(r"poc",POCViewSet)
router.register(r"stack",StackHolderViewSet)
router.register(r"immediateaction",ImmeActionViewSet)
router.register(r"immprovementrecom",ImprovementRecomViewSet)
router.register(r"followupaction",FollowUpActionViewSet)
router.register(r"status",StatusViewSet)
router.register(r"incidentstatus",IncidentStatusViewSet)
router.register(r"incidentevidence",IncidentEvidenceViewSet)
router.register(r"employee",EmpViewSet)
router.register(r"ticket",InciTicketViewSet)



urlpatterns = [
    path("",include(router.urls))
]