from modules.models 		import Modules
from company.models 		import Company
from exam.models 			import Exam
from session.models 		import Session
from userprofile.models 	import Userprofile
from django.contrib.auth.models import User
import csv

with open('./new_users_csvs/usuariospruebas.csv', 'r') as f:
  reader = csv.reader(f)
  user_list = list(reader)

print(user_list)


for userData in user_ist:
	try:
		Username 	= userData[0]
		Email 		= userData[1]
		Password 	= userData[2]
		Firstname	= userData[3]
		Lastname	= userData[4]
		Role 		= userData[5]
		Area 		= userData[6]
		Department 	= userData[7]
		Exp 		= userData[8]

		newModules 	= 	Modules.objects.create(sessionReached=1)

		newUser 	= 	User.objects.create_user(username=Username,
				                                email=Email,
				                                password=Password
		                )

		for x in range(1,13):
			theExam = Exam.objects.create( user=newUser, examScore=0, attempts=0)

			Session.objects.create(sessionNumber=x, presentationDone=False, docDone=False, slideReached=0, pageReached=0, examID_id=theExam.id, modulesID_id=newModules.id, videoDone=False,user=newUser)
			pass


		selectedCompanyID=3


		newUserProfile 	=	Userprofile.objects.create(modulesID_id=newModules.id, 
										companyID_id=selectedCompanyID,
										firstname=Firstname,
										lastname=Lastname,
										userID_id=newUser.id,
										isActive=True,
										isAdmin=False,
										area=Area,
										department=Department,
										expYears=Exp,
										role=Role,
							)
		print('User ' + Username + ' Created!')
		pass
	except Exception as e:
		print(e)
		raise e
	