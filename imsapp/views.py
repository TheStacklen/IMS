from django.shortcuts import render
from imsapp.models import *
from imsapp.serializers import *
from rest_framework import viewsets 
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import authentication_classes , permission_classes
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
#for customize access token
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer 
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import EmailMessage

# Create your views here.
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
class RoleViewset(viewsets.ModelViewSet):
     queryset=Role.objects.all()
     serializer_class=RoleSerializer

class DeptViewset(viewsets.ModelViewSet):
     queryset=Department.objects.all()
     serializer_class=DeptSerializer
    
class DesigViewset(viewsets.ModelViewSet):
     queryset=Designation.objects.all()
     serializer_class=DesigSerializer

class ContribFactViewset(viewsets.ModelViewSet):
     queryset=ContributingFactor.objects.all()
     serializer_class=ContribFactSerializer

class InciTypeViewset(viewsets.ModelViewSet):
     queryset=IncidentType.objects.all()
     serializer_class=IncidentTypeSerializer

class StatusViewSet(viewsets.ModelViewSet):
     queryset=Status.objects.all()
     serializer_class=StatusSerializer

class POCViewSet(viewsets.ModelViewSet):
     queryset=DepartmentPOC.objects.all()
     serializer_class=DeptPOCSerializer

class StackHolderViewSet(viewsets.ModelViewSet):
     queryset=StackHolder.objects.all()
     serializer_class=StackHolderSerializer

class ImmeActionViewSet(viewsets.ModelViewSet):
     queryset=ImmediateAction.objects.all()
     serializer_class=ImmediateActionSerializer

class ImprovementRecomViewSet(viewsets.ModelViewSet):
     queryset=ImprovementRecommendations.objects.all()
     serializer_class=ImmprovementRecomSerializer

class FollowUpActionViewSet(viewsets.ModelViewSet):
     queryset=FollowUpActions.objects.all()
     serializer_class=FollowUpActionsSerializer

class IncidentStatusViewSet(viewsets.ModelViewSet):
     queryset=IncidentStatus.objects.all()
     serializer_class=IncidentStatusSerializer

class IncidentEvidenceViewSet(viewsets.ModelViewSet):
     queryset=IncidentEvidence.objects.all()
     serializer_class=IncidentEvidenceSerializer

class EmpViewSet(viewsets.ModelViewSet):
     queryset=Employee.objects.all()
     serializer_class=EmployeeSerializer

class InciTicketViewSet(viewsets.ModelViewSet):
     queryset=IncidentTicket.objects.all()
     serializer_class=IncidentTicketSerializer

class TicketUpdateViewSet(viewsets.ModelViewSet):
    queryset = IncidentTicket.objects.all()
    serializer_class = POCUpdateSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class LogoutView(APIView):
     permission_classes=[IsAuthenticated]
     def post(self,request):
          refresh_token_value=request.data.get("refresh")
          token=RefreshToken(refresh_token_value)
          token.blacklist()
          return Response("Logged out successfully.")

class ChangePassword(APIView):
     permission_classes=[IsAuthenticated]
     def post(self,request):
        user = request.user
     #    print("\n"*3)
     #    print(user.first_name)
     #    print("\n"*3)
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        com_password = request.data.get('confirm_password')
        if not user.check_password(old_password):
            return Response("Old password is incorrect")
        if new_password!=com_password:
             return Response("New password and confirm password do not match")
        user.set_password(new_password)
        user.save()
        return Response("Password changed successfully")
     
import random 
sent_otp=" "
stored_email = " "
otp_verified= False
class SendOTP(APIView):
     def post(self,request):              
          email=request.data['to']
          print("\n"*5)
          print(email)
          global stored_email , sent_otp , otp_verified
          otp=str(random.randint(1000, 9999) )
          otp_verified=False
          sent_otp=otp # store otp globlly
          stored_email=email # store email globlly
          print("OTP Is :",sent_otp)
          emailw=EmailMessage(
               'Test email Subject',
               f'Your OTP is: {otp}',
               settings.EMAIL_HOST_USER,
               [email]
          )
          emailw.send(fail_silently=False)
          return Response({'status':True,'message':'OTP sent successfully'}) 

class VerifyOTP(APIView):
     def post(self,request):
          global otp_verified #for use 
          entered_otp=request.data.get("otp")
          if sent_otp == entered_otp:
                otp_verified = True 
                return Response('OTP verified successfully')
          return Response("Invalid OTP")

class forgetPassword(APIView):
     def post(self , request):
          global otp_verified , sent_otp , stored_email #for use
          new_password=request.data.get('new_password')
          confirm_password=request.data.get('confirm_password')
          if not otp_verified:
            return Response("OTP not verified")
          
          if new_password!= confirm_password:
                return Response('New Password and Confirm Password do not Match')
          try:
              user=CustomUser.objects.get(email=stored_email)
              user.set_password(new_password)
              user.save()
              otp_verified = False
              sent_otp = ""
              stored_email = ""
              return Response("reset password successfully")
          except CustomUser.DoesNotExist:
               return Response("user not found")
          
class allticketViewSet(viewsets.ModelViewSet):
     queryset = IncidentTicket.objects.all()
     serializer_class = IncidentSerializer


          


     

    







     
     







     

