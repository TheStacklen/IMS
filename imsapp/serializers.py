from rest_framework import serializers
from imsapp.models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer 

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
        fields=["action_title","responsible_emp_id"]

class FollowUpActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model=FollowUpActions
        fields=["actions_title","responsible_emp_id"]

class IncidentStatusSerializer(serializers.ModelSerializer):
    status_name = serializers.CharField(source='status_id.name', read_only=True)
    class Meta:
        model = IncidentStatus
        fields = ["date_created", "status_name"]

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

        password = validated_data["user_id"].pop("password")
        user_data = validated_data.pop('user_id')
        # Create user
        user = CustomUser.objects.create(**user_data)
        user.set_password(password)
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

    class Meta:
        model=IncidentTicket
        fields=["id","requestor_id","report_type","location","department_id","description","contributing_factor",
                "individual_involved","witnesses","imme_action","Assigned_POC","incident_status","potential_severity","likelihood_of_recurrence",
                "risk_level","recommendation","follow"
                ]
    def create(self,validated_data):
        contrib_factor=validated_data.pop("contributing_factor")
        indi_involved=validated_data.pop("individual_involved")
        witnesses=validated_data.pop("witnesses")
        ImmediateActions=validated_data.pop("imme_action")
        
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
        # print(statuss.name)
        return ticket
    
class ImmprovementRecomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImprovementRecommendations
        fields = ["action_title", "responsible_emp_id"]

class FollowUpActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowUpActions
        fields = ["actions_title", "responsible_emp_id"]

class POCUpdateSerializer(serializers.ModelSerializer):
    recommendation = ImmprovementRecomSerializer(many=True)
    follow = FollowUpActionsSerializer(many=True)

    class Meta:
        model = IncidentTicket
        fields = ['potential_severity', 'likelihood_of_recurrence', 'risk_level', 'recommendation', 'follow']
    def update(self, instance, validated_data):
        improvement_data = validated_data.pop('recommendation', [])
        followup_data = validated_data.pop('follow', [])

        instance.potential_severity = validated_data.get('potential_severity', instance.potential_severity)
        instance.likelihood_of_recurrence = validated_data.get('likelihood_of_recurrence', instance.likelihood_of_recurrence)
        instance.risk_level = validated_data.get('risk_level', instance.risk_level)
        instance.save()

        instance.recommendation.all().delete()
        instance.follow.all().delete()

        for item in improvement_data:
            ImprovementRecommendations.objects.create(
                action_title=item['action_title'],
                responsible_emp_id=item['responsible_emp_id'],
                incident_id=instance
            )

        for item in followup_data:
            FollowUpActions.objects.create(
                actions_title=item['actions_title'],
                responsible_emp_id=item['responsible_emp_id'],
                incident_id=instance
            )

        return instance
    
#Customize Token 
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # add Custome Fields
        token['first_name']=user.first_name
        token['last_name']=user.last_name
        token['emp_id']=user.employee.emp_id
        return token
    
class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model=IncidentTicket
        fields=["id"]
    def to_representation(self,instance):
        response= super().to_representation(instance)
        response["potential_severity"]=instance.potential_severity
        response["likelihood_of_recurrence"]=instance.likelihood_of_recurrence
        response["risk_level"]=instance.risk_level
        response["reporter"]={"name": instance.requestor_id.user_id.first_name + instance.requestor_id.user_id.last_name,
                              "Designation":instance.requestor_id.desig_id.name}
        response["Report Type"]=instance.report_type.name
        response["Department"]={"id":instance.department_id.id,"name":instance.department_id.name}
        response["inci_status"]=[i for i in IncidentStatusSerializer(instance.inci_status.all() , many=True).data]
        response["Location"]=instance.location
        response["Occurance_date"]=instance.occurrence_date
        response["description"]=instance.description
        if instance.Assigned_POC is not None:
            response["AssignedPOC"]={"name":instance.Assigned_POC.employee_id.user_id.first_name}
        else:
            response["AssignedPOC"]=""
        # print([i["name"] for i in ContribFactSerializer(instance.contributing_factor , many=True).data])
        response["contributing_factor"]=[i["name"] for i in ContribFactSerializer(instance.contributing_factor , many=True).data]
        response["imme_action"]=[i for i in ImmediateActionSerializer(instance.imme_action.all() , many=True).data]
        response["witnesses"]=[i["user_id"]["first_name"] for i in EmployeeSerializer(instance.witnesses , many=True).data]
        response["individual_involved"]=[i["user_id"]["first_name"] for i in EmployeeSerializer(instance.individual_involved.all(), many=True).data]
        response["inci_evidence"]=[i for i in IncidentEvidenceSerializer(instance.inci_evidence.all() , many=True).data]
        response["recommendation"]=[i for i in ImmprovementRecomSerializer(instance.recommendation.all() ,many=True).data]
        response["follow"]=[i for i in FollowUpActionsSerializer(instance.follow , many=True).data]
        return response
    




    











        


    















