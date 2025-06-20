from django.urls import path , include
from imsapp.views import *
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from .views import MyTokenObtainPairView 
from rest_framework_simplejwt.views import TokenRefreshView
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
router.register(r"ticket",InciTicketViewSet,basename="ticket")
router.register(r"ticket-update",TicketUpdateViewSet , basename="tick")
router.register(r"t",allticketViewSet,basename="response")

urlpatterns = [
    path("",include(router.urls)),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('access/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/',LogoutView.as_view() , name= 'customelogout'),
    path('change/',ChangePassword.as_view() , name= 'change_password'),
    path('mail/',SendOTP.as_view() , name='send_otp'),
    path('verify/',VerifyOTP.as_view(), name='varify_otp'),
    path('forget/',forgetPassword.as_view() , name='forget_password')
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)