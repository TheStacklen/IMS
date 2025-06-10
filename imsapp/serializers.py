from rest_framework import serializers
from imsapp.models import *

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=["first_name","last_name","email","password"]

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Role
        fields="__all__"

class DeptSerializer(serializers.ModelSerializer):
    class Meta:
        model=Department
        fields="__all__"
    
class DesigSerializer(serializers.ModelSerializer):
    class Meta:
        model=Designation
        fields="__all__"
    
class ContribFactSerializer(serializers.ModelSerializer):
    class Meta:
        model=ContributingFactor
        fields="__all__"

class IncidentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=IncidentType
        fields="__all__"

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model=Status
        fields=["name"]

class DeptPOCSerializer(serializers.ModelSerializer):
    class Meta:
        model=DepartmentPOC
        fields="__all__"

class StackHolderSerializer(serializers.ModelSerializer):
    class Meta:
        model=StackHolder
        fields="__all__"
class ImmediateActionSerializer(serializers.ModelSerializer):
    class Meta:
        model=ImmediateAction
        fields="__all__"

class ImmprovementRecomSerializer(serializers.ModelSerializer):
    class Meta:
        model=ImprovementRecommendations
        fields="__all__"

class FollowUpActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model=FollowUpActions
        fields="__all__"

class IncidentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model=IncidentStatus
        fields="__all__"

class IncidentEvidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model=IncidentEvidence
        fields="__all__"

class EmployeeSerializer(serializers.ModelSerializer):
    user_id=CustomUserSerializer()
    class Meta:
        model = Employee
        fields = "__all__"
    def create(self, validated_data):

        user_data =validated_data.pop('user_id')
        # Create user
        user = CustomUser.objects.create(**user_data)
        user.save()
        # Create employee
        employee = Employee.objects.create(user_id=user, **validated_data)
        employee.save()
        return employee
    
#Payload for ticket
'''
{
  "requestor_id": 1,
  "report_type": 1,
  "location": "k",
"department_id":1,
  "description": "llllll",
  "contributing_factor": [1],
  "individual_involved": [1],
  "witnesses": [1],
  "imme_action": [
    {
      "emp_id": [1],
      "discription": "k"
    },
    {
      "emp_id": [2],
      "discription": "jjj"
    }
  ]

}
'''
class ImmediateActionSerializer(serializers.ModelSerializer):
    class Meta:
        model=ImmediateAction
        exclude=["incident_id"]

class IncidentTicketSerializer(serializers.ModelSerializer):
    imme_action=ImmediateActionSerializer(many=True, required=False)
    incident_status=StatusSerializer(required=False,many=True)
    # incident_status=StatusSerializer(required=False)
    class Meta:
        model=IncidentTicket
        fields=["id","requestor_id","report_type","location","department_id","description","contributing_factor","individual_involved","witnesses","imme_action","Assigned_POC","incident_status"]
    def create(self,validated_data):
        contrib_factor=validated_data.pop("contributing_factor")
        indi_involved=validated_data.pop("individual_involved")
        witnesses=validated_data.pop("witnesses")
        ImmediateActions=validated_data.pop("imme_action")
        # print("\n"*4)
        # print(incident_status)
        # print("\n"*4)
        #Assign POC
        dept = validated_data.get("department_id")
        pocs = dept.poc.first()
        validated_data["Assigned_POC"] = pocs
        ticket=IncidentTicket.objects.create(**validated_data)
        for i in contrib_factor:
            ticket.contributing_factor.add(i)
        for i in indi_involved:
            ticket.individual_involved.add(i)
        for i in witnesses:
            ticket.witnesses.add(i)
        for action_data in ImmediateActions:
            # print(action_data)
            employees=action_data.pop("emp_id")
            action=ImmediateAction.objects.create(incident_id=ticket,**action_data)
            # action.emp_id.set(employees)
            for i in employees:
                action.emp_id.add(i) 
        
        statuss=Status.objects.get(id=2)
        IncidentStatus.objects.create(status_id=statuss, incident_id=ticket)
        print(statuss.name)
        return ticket


        


    















