from django.contrib import admin
from imsapp.models import *
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Role)
admin.site.register(Department)
admin.site.register(Designation)
admin.site.register(DepartmentPOC)
admin.site.register(Employee)
admin.site.register(IncidentTicket)
admin.site.register(ImmediateAction)
admin.site.register(Status)