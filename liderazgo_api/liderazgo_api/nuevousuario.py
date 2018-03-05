from modules.models 		import Modules
from company.models 		import Company
from exam.models 			import Exam
from session.models 		import Session
from userprofile.models 	import Userprofile
from django.contrib.auth.models import User


Username 	= 'ricardosuarez'
Email 		= 'carlos.ricardo.suarez.leon@gmail.com'
Password 	= 'elearning1'

selectedCompanyID = 1

newModules 	= 	Modules.objects.create(sessionReached=1)

newUser 	= 	User.objects.create_user(username=Username,
		                                email=Email,
		                                password=Password
                )
# newUser 	= User.objects.get(id=6)

for x in range(1,13):
	theExam = Exam.objects.create( user=newUser, examScore=0, attempts=0)

	Session.objects.create(sessionNumber=x, presentationDone=False, docDone=False, slideReached=0, pageReached=0, examID_id=theExam.id, modulesID_id=newModules.id, videoDone=False,user=newUser)
	pass

Area= "Executive"
Department="Finances Management"
Exp=9
Role='Owner'
selectedCompanyID=1


newUserProfile 	=	Userprofile.objects.create(modulesID_id=newModules.id, 
								companyID_id=selectedCompanyID, 
								userID_id=newUser.id,
								isActive=True,
								isAdmin=False,
								area=Area,
								department=Department,
								expYears=Exp,
								role=Role,
					)