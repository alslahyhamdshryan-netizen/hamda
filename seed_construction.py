import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "exchange_backend.settings")
import django
django.setup()
from datetime import date, timedelta
from django.contrib.auth.models import User
from exchange_backend.models import ConstructionClient, ConstructionProject, ProjectTask, ConstructionIssue
user = User.objects.filter(is_superuser=True).first() or User.objects.first()
if not user:
    user = User.objects.create_superuser("admin", "admin@example.com", "Admin@12345")
client_data=[("شركة أفق العقارية","محمد العتيبي"),("مجموعة المدار","سارة القحطاني"),("م. خالد السالم","خالد السالم")]
clients=[]
for name, contact in client_data:
    c,_=ConstructionClient.objects.get_or_create(organization_name=name, defaults={"contact_name":contact})
    clients.append(c)
projects=[
    ("PRJ-024","مجمع النخبة السكني",clients[0],"الرياض — حي النرجس",6850000,5230000,3510000,64,71,"active"),
    ("PRJ-021","مركز الأعمال الإداري",clients[1],"جدة — طريق الملك",4120000,3250000,1870000,43,39,"active"),
    ("PRJ-018","فيلا الياسمين",clients[2],"الرياض — الياسمين",1980000,1540000,880000,28,46,"on_hold"),
]
created=[]
for code,name,client,location,contract,budget,actual,progress,planned,status in projects:
    p,_=ConstructionProject.objects.update_or_create(code=code,defaults={"name":name,"client":client,"location":location,"manager":user,"contract_value":contract,"budget":budget,"actual_cost":actual,"progress":progress,"planned_progress":planned,"status":status,"start_date":date(2026,2,1),"end_date":date(2026,11,22)})
    created.append(p)
for p,name,phase,progress,status,critical,days in [(created[0],"أعمال العزل المائي للأسطح","العزل",52,"progress",True,3),(created[0],"توريد وتركيب الألمنيوم","الواجهات",20,"progress",True,8),(created[2],"اعتماد المخططات الكهربائية","الكهرباء",0,"blocked",False,-2)]:
    ProjectTask.objects.update_or_create(project=p,name=name,defaults={"phase":phase,"progress":progress,"status":status,"is_critical":critical,"end_date":date.today()+timedelta(days=days)})
issues=[(created[0],"تأخر توريد السيراميك الرئيسي","مخاطر","high",2),(created[2],"ملاحظة جودة في تمديدات السباكة","جودة","medium",5)]
for p,title,typ,priority,days in issues:
    ConstructionIssue.objects.get_or_create(project=p,title=title,defaults={"issue_type":typ,"priority":priority,"due_date":date.today()+timedelta(days=days)})
print("construction demo seeded")
