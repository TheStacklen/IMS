from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _
# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)
    
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    first_name=models.CharField( max_length=40)
    last_name=models.CharField(max_length=30)
    role=models.ForeignKey('role',on_delete=models.CASCADE , null=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()
    def __str__(self):
        return self.email
    
class IncidentTicket(models.Model):
    id=models.AutoField(primary_key=True)
    requestor_id=models.ForeignKey('Employee',on_delete=models.CASCADE)
    report_type=models.ForeignKey('IncidentType', on_delete=models.CASCADE)
    occurrence_date=models.DateTimeField(auto_now_add=True)
    location=models.CharField(max_length=50)
    contributing_factor=models.ManyToManyField('ContributingFactor',db_table="incidentFactor")
    evidence=models.FileField(upload_to="file" , blank=True , null=True)
    department_id=models.ForeignKey('Department', on_delete=models.CASCADE)
    Assigned_POC=models.ForeignKey('DepartmentPOC',on_delete=models.CASCADE , null=True)
    description = models.CharField(max_length=100) 
    witnesses=models.ManyToManyField('Employee',db_table="Witnesses" , related_name="wit")
    individual_involved=models.ManyToManyField('Employee',db_table="IndividualInvolved",related_name="individual_invo")
    improvement_recommendations=models.ManyToManyField('Employee',through='ImprovementRecommendations' , related_name="improvement_recom" ,null=True)
    incident_status=models.ManyToManyField('Status', through="IncidentStatus" ,related_name="inci_status" , null=True)
    followup_actions=models.ManyToManyField('Employee',through="FollowUpActions",related_name="follow_actions" , null=True)
    potential_severity=models.CharField(max_length=50 , null=True)
    likelihood_of_recurrence=models.CharField(max_length=70 , null=True)
    risk_level=models.CharField( max_length=100 , null=True)
    
class ImmediateAction(models.Model):
    id=models.AutoField(primary_key=True)
    emp_id=models.ManyToManyField('Employee' , db_table="ImmediateActionEmployee" , related_name="iae")
    incident_id=models.ForeignKey('IncidentTicket', on_delete=models.CASCADE , related_name="imme_action")
    discription=models.CharField(max_length=80)

class ImprovementRecommendations(models.Model):
    id=models.AutoField(primary_key=True)
    action_title=models.CharField(max_length=50)
    action_description=models.CharField(max_length=50)
    responsible_emp_id=models.ForeignKey('Employee',on_delete=models.CASCADE)
    incident_id=models.ForeignKey('IncidentTicket',on_delete=models.CASCADE)

class FollowUpActions(models.Model):
    id=models.AutoField(primary_key=True)
    date_complete=models.DateField(auto_now_add=True)
    actions_title=models.CharField(max_length=70)
    date_completed=models.DateTimeField(auto_now_add=True)
    responsible_emp_id=models.ForeignKey('employee',on_delete=models.CASCADE)
    incident_id=models.ForeignKey('IncidentTicket',on_delete=models.CASCADE)

class Status(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField( max_length=50)

class IncidentStatus(models.Model):
    id=models.AutoField(primary_key=True)
    status_id=models.ForeignKey('Status' , on_delete=models.CASCADE)
    incident_id=models.ForeignKey('IncidentTicket' , on_delete=models.CASCADE)
    date_created=models.DateTimeField()

class IncidentEvidence(models.Model):
    id=models.AutoField(primary_key=True)
    incident_id=models.ForeignKey('IncidentTicket', on_delete=models.CASCADE , related_name="inci_evidence")
    file=models.FileField(upload_to="file" , blank=True , null=True)

class Employee(models.Model):
    emp_id=models.AutoField(primary_key=True)
    job_title=models.CharField(max_length=40)
    contact=models.BigIntegerField(null=True)
    desig_id=models.ForeignKey('Designation',on_delete=models.CASCADE, related_name="designations")
    user_id=models.OneToOneField("CustomUser", on_delete = models.CASCADE , related_name="employee")

class IncidentType(models.Model):
    name=models.CharField(max_length=30)
    id=models.IntegerField(primary_key=True)
    department_id=models.ForeignKey('Department', on_delete=models.CASCADE)

class ContributingFactor(models.Model):
    id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=25)

class Department(models.Model):
    id=models.IntegerField(primary_key=True)
    name=models.CharField( max_length=50)

class DepartmentPOC(models.Model):
    POC_id=models.IntegerField(primary_key=True)
    department_id=models.ForeignKey('Department', on_delete=models.CASCADE ,related_name="poc")
    employee_id=models.ForeignKey('Employee', on_delete=models.CASCADE , related_name="dept")

class Designation(models.Model):
    id=models.IntegerField(primary_key=True)
    name=models.CharField( max_length=50)
    department_id=models.ForeignKey('Department', on_delete=models.CASCADE)

class Role(models.Model):
    id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=50)

class StackHolder(models.Model):
    id=models.IntegerField(primary_key=True)
    user_id=models.ForeignKey(CustomUser ,on_delete=models.CASCADE)
