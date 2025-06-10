from django.shortcuts import render
from imsapp.models import *
from imsapp.serializers import *
from rest_framework import viewsets
from rest_framework.response import Response
# Create your views here.
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



     
     







     

