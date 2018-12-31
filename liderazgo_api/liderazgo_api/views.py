from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.http import JsonResponse
from django.forms.models import model_to_dict


# =========================================
# Model importing
# =========================================
from modules.models 		import Modules
from company.models 		import Company
from videos.models 			import Video
from exam.models 			import Exam
from session.models 		import Session
from userprofile.models 	import Userprofile
from django.contrib.auth.models import User
# =========================================
# =========================================


# =========================================
# Endpoint utilities
# =========================================
import os
import re
import csv
from django.db.models import Avg, Max, Min
from datetime import date
from pathlib import Path
# =========================================
# =========================================


class examReport(object):
    def __init__(self, sList, EDList, aList):
        self.scoresList 	= sList
        self.elapsedDaysList= EDList
        self.attemptsList 	= aList

class docObject(object):
    def __init__(self, title, slides):
        self.title 	= title
        self.slides = slides

class examObject(object):
    def __init__(self, questions):
        self.questions = questions        

class RestrictedView(APIView):
	permission_classes 		= (IsAuthenticated, )
	authentication_classes 	= (JSONWebTokenAuthentication, )

	def get(self, request):
		data = {
		'id': 		request.user.id,
		'username': request.user.username,
		'token': 	str(request.auth)
		}
		return Response(data)

class getDoc(APIView):
	# This endpoint gets a number from uri to identify which document to return in form of array.
	__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

	def get(self, request):
		documentId 	= request.query_params['id']
		slideObject = []

		contents 	= Path('/home/modulos_api/content/docs/doc' + documentId + ".txt").read_text()

		doctitle	= re.findall('<title>(.*?)</title>', contents.replace('\n', '').replace('\t', ''), flags= re.DOTALL)
		slidelist 	= re.findall('<slide>(.*?)</slide>', contents.replace('\n', '').replace('\t', ''), flags= re.DOTALL)
		
		for slide in slidelist:
			
			fraglist = re.findall('<frag>(.*?)</frag>', slide.replace('\n', '').replace('\t', ''), flags= re.DOTALL)				
			slideObject.append(fraglist)
			pass

		toReturn = docObject(doctitle[0], slideObject)
						
		return JsonResponse(toReturn.__dict__, safe=False)

class getPresentation(APIView):
	# This endpoint gets a number from uri to identify which document to return in form of array.
	__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
	

	def get(self, request):

		try:
			with open('./liderazgo_api/presentations/video_links.csv', 'r') as f:
				reader = csv.reader(f)
				video_links_list = list(reader)
			pass
		except Exception as e:
			raise e	

		presentationId 	= request.query_params['id']
		slideObject 	= []

		contents = os.listdir('/home/modulos_api/content/presentations/module_' + presentationId)

		# Ordering lambda: https://stackoverflow.com/questions/23724653/ordered-os-listdir-in-python
		orderedContents = sorted(contents, key=lambda x: (int(re.sub('\D','',x)),x))
		for index, slide in enumerate(orderedContents):
			orderedContents[index] = {'slide': slide, 'link': ''}
			pass	
		
		for video_link in video_links_list:
			pass
		
		if any(video_link[0] == presentationId for video_link in video_links_list):
			
			for i, video_link in enumerate(video_links_list):
				if video_link[0] == presentationId:
					orderedContents[ int(video_link[1])-1 ] = {'slide':orderedContents[ int(video_link[1])-1 ]['slide'], 'link':video_link[2]}										

		return JsonResponse(orderedContents, safe=False)

class getExam(APIView):
	# This endpoint gets a number from uri to identify which exam to return in form of array.
	__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

	def get(self, request):
		examId 		= request.query_params['id']
		examArray	= []
		contents 	= Path('/home/modulos_api/content/exams/exam' + examId + ".txt").read_text()
		questions	= re.findall('<question>(.*?)</question>', contents.replace('\n', '').replace('\t', ''), flags= re.DOTALL)
		
		for question in questions:
			questionObject 	= []
			theQuestion 	= re.findall('<q>(.*?)</q>', question.replace('\n', '').replace('\t', ''), flags= re.DOTALL)
			choices 		= re.findall('<a>(.*?)</a>', question.replace('\n', '').replace('\t', ''), flags= re.DOTALL)
			correctAnswer 	= re.findall('<correct-index>(.*?)</correct-index>', question.replace('\n', '').replace('\t', ''), flags= re.DOTALL)

			questionObject.append(theQuestion[0])
			questionObject.append(choices)
			questionObject.append(correctAnswer[0])

			examArray.append(questionObject)
			pass

		toReturn = examObject(examArray)						
		return JsonResponse(toReturn.__dict__, safe=False)

class getTest(APIView):
	# This endpoint gets a number from uri to identify which exam to return in form of array.
	__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

	def get(self, request):
		testId 		= request.query_params['id']
		testArray	= []
		contents 	= Path('/home/modulos_api/content/tests/tests.txt').read_text()
		print(contents)
		testLink	= re.findall('<test_'+testId+'>(.*?)</test_'+testId+'>', contents.replace('\n', '').replace('\t', ''), flags= re.DOTALL)

		toReturn = testLink						
		return JsonResponse(toReturn, safe=False)

class getBibliografia(APIView):
	# This endpoint gets a number from uri to identify which document to return in form of array.
	__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

	def get(self, request):
		bibliografiaId 	= request.query_params['id']	

		contents = os.listdir('/home/modulos_api/content/bibliografias/module_' + bibliografiaId)

		# Ordering lambda: https://stackoverflow.com/questions/23724653/ordered-os-listdir-in-python
		orderedContents = sorted(contents, key=lambda x: (int(re.sub('\D','',x)),x))		
						
		return JsonResponse(orderedContents, safe=False)

class getDinamica(APIView):
	# This endpoint gets a number from uri to identify which document to return in form of array.
	__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

	def get(self, request):
		dinamicaId 	= request.query_params['id']
		slideObject 	= []

		contents = os.listdir('/home/modulos_api/content/dinamicas/module_' + dinamicaId)

		# Ordering lambda: https://stackoverflow.com/questions/23724653/ordered-os-listdir-in-python
		orderedContents = sorted(contents, key=lambda x: (int(re.sub('\D','',x)),x))		
						
		return JsonResponse(orderedContents, safe=False)

class getVideo(APIView):
	# This endpoint gets a number from uri to identify which exam to return in form of array.
	__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

	def get(self, request):
		videoId 	= request.query_params['id']
		videoString = ''
		videoString = Video.objects.get(id=videoId)
					
		return JsonResponse(model_to_dict(videoString), safe=False)

class getUserModules(APIView):
	permission_classes 		= (IsAuthenticated, )
	authentication_classes 	= (JSONWebTokenAuthentication, )

	def get(self, request):
		data = {
		'id': request.user.id,
		'sessionNumber': request.query_params['sessionnumber']
		}

		requestingUser 	= User.objects.get(id=data['id'])
		userProfile 	= Userprofile.objects.get(userID=requestingUser)
		userModules 	= Modules.objects.get(id=userProfile.modulesID_id)
		sessions		= Session.objects.filter(modulesID=userModules).order_by('sessionNumber')

		currentSession	= Session.objects.get(modulesID=userModules, sessionNumber=int(data['sessionNumber']))
		# If there's no start date in the actual session create one.
		if (currentSession.startDate == None):
			currentSession.startDate = date.today()
			currentSession.save()
			print(model_to_dict(currentSession))
			print(date.today())
			pass

		return Response(model_to_dict(userModules))

class getUserReport(APIView):
	permission_classes 		= (IsAuthenticated, )
	authentication_classes 	= (JSONWebTokenAuthentication, )	

	def get(self, request):
		data = {
		'id': request.user.id,
		'requested_user_profile': request.query_params.get('user_profile_id')
		}

		requestingUser 	= User.objects.get(id = data['id'])
		userProfile 	= Userprofile.objects.get(userID= (data['requested_user_profile'] if data['requested_user_profile'] != None else requestingUser))
		userModules 	= Modules.objects.get(id=userProfile.modulesID_id)
		sessions		= Session.objects.filter(modulesID=userModules).order_by('sessionNumber')

		examList 		= [Session.examID_id for Session in sessions]						
		exams 			= Exam.objects.filter(id__in=examList).order_by('id')
		
		examScoreList	= [Exam.examScore for Exam in exams]
		examAttemptsList= [Exam.attempts for Exam in exams]
		# Lets make sure that we just calculate date diff for real INT values, if a None is present, the whole users reports screen will crash.
		sessionElapsedDaysList	= [(Session.endDate - Session.startDate).days if Session.endDate != None and Session.startDate != None else 0 for Session in sessions]

		profileDict		= model_to_dict(userProfile)
		userReport 		= examReport(examScoreList, sessionElapsedDaysList, examAttemptsList)

		return JsonResponse({ 'perfil': profileDict, 'reporte': userReport.__dict__}, safe=False)

class getAllReports(APIView):
	permission_classes 		= (IsAuthenticated, )
	authentication_classes 	= (JSONWebTokenAuthentication, )	

	def get(self, request):
		data = {
		'id': request.user.id
		}

		# requestingUser 	= User.objects.get(id=data['id'])
		requestingUser 	= User.objects.get(id=2)
		userProfile 	= Userprofile.objects.get(userID=requestingUser)
		companyUsers	= Userprofile.objects.filter(companyID=userProfile.companyID).order_by('firstname')
		# realUsers 		= User.objects.filter(id__in=[userID['userID'] for userID in list(companyUsers.values('userID'))])
		realUsers 		= User.objects.filter(id__in=companyUsers.values_list('userID', flat=True))
		sessions 		= Session.objects.filter(user__in=realUsers).order_by('sessionNumber')

		sessionElapsedDaysAllList	= []

		examScoreAvgList			= []
		examAttemptsAvgList 		= []
		sessionElapsedDaysAvgList 	= []

		examScoreMaxList 			= []
		examAttemptsMaxList 		= []
		sessionElapsedDaysMaxList 	= []

		examScoreMinList 			= []
		examAttemptsMinList 		= []
		sessionElapsedDaysMinList 	= []

		startDates  = []
		endDates	= []	

		# Things get a bit ugly here, this should be improved, basically here we calculate all the avarages and sums and mins of the whole set of users for the admin 
		# screen not yet released for public.
		for x in range(1,13):
			examScoreAvgList.append(Exam.objects.filter(id__in=sessions.filter(sessionNumber=x).values_list('examID_id', flat=True)).aggregate(Avg('examScore')))
			examAttemptsAvgList.append(Exam.objects.filter(id__in=sessions.filter(sessionNumber=x).values_list('examID_id', flat=True)).aggregate(Avg('attempts')))
			examScoreMaxList.append(Exam.objects.filter(id__in=sessions.filter(sessionNumber=x).values_list('examID_id', flat=True)).aggregate(Max('examScore')))
			examAttemptsMaxList.append(Exam.objects.filter(id__in=sessions.filter(sessionNumber=x).values_list('examID_id', flat=True)).aggregate(Max('attempts')))
			examScoreMinList.append(Exam.objects.filter(id__in=sessions.filter(sessionNumber=x).values_list('examID_id', flat=True)).aggregate(Min('examScore')))
			examAttemptsMinList.append(Exam.objects.filter(id__in=sessions.filter(sessionNumber=x).values_list('examID_id', flat=True)).aggregate(Min('attempts')))
			startDates.append(sessions.filter(sessionNumber=x).values_list('startDate', flat=True))
			endDates.append(sessions.filter(sessionNumber=x).values_list('endDate', flat=True))

		for x in range(0,12):
			sessionElapsedDaysAllList.append([(endDates[x][y] - startDates[x][y]).days if endDates[x][y] != None else 0 for y in range(0, len(startDates[0]))])
			sessionElapsedDaysAvgList.append(mean(sessionElapsedDaysAllList[x]))
			sessionElapsedDaysMaxList.append(max(sessionElapsedDaysAllList[x]))
			sessionElapsedDaysMinList.append(min(sessionElapsedDaysAllList[x]))				

		response 		= 	{'avgs':	{'scores': [theList['examScore__avg']for theList in examScoreAvgList], 'attempts': [theList['attempts__avg']for theList in examAttemptsAvgList], 'days': sessionElapsedDaysAvgList},
							'maxes':	{'scores': [theList['examScore__max']for theList in examScoreMaxList], 'attempts': [theList['attempts__max']for theList in examAttemptsMaxList], 'days': sessionElapsedDaysMaxList},
							'mins': 	{'scores': [theList['examScore__min']for theList in examScoreMinList], 'attempts': [theList['attempts__min']for theList in examAttemptsMinList], 'days': sessionElapsedDaysMinList}}
		return JsonResponse(response, safe=False)


class getAllUsers(APIView):
	permission_classes 		= (IsAuthenticated, )
	authentication_classes 	= (JSONWebTokenAuthentication, )	

	def get(self, request):
		data = {
		'id': request.user.id
		}

		requestingUser 	= User.objects.get(id=data['id'])
		userProfile 	= Userprofile.objects.get(userID=requestingUser)
		companyUsers	= Userprofile.objects.filter(companyID=userProfile.companyID).order_by('firstname')
		userList		= [model_to_dict(userProfile) for userProfile in companyUsers]		
		return JsonResponse(userList, safe=False)

class postExamScore(APIView):
	permission_classes 		= (IsAuthenticated, )
	authentication_classes 	= (JSONWebTokenAuthentication, )

	def post(self, request):
		data = {
			'id': request.user.id,
			'examData' : request.data
		}

		try:
			requestingUser 		= User.objects.get(id=data['id'])
			userProfile 		= Userprofile.objects.get(userID=requestingUser)
			userModules 		= Modules.objects.get(id=userProfile.modulesID_id)
			sessionToSetScore 	= Session.objects.get(modulesID=userModules, sessionNumber=data['examData']['sessionNumber'])
			examToSetScore 		= Exam.objects.get(id=sessionToSetScore.examID_id);					

			# This condition sets whether the user is allowed to go to next module or not.
			# It checks if its score was greater than the default passing score (70 (%))
			if data['examData']['Score'] > 70:
				# Determine if user has already coursed that exam or not, if yes, then dont update the session reached value.
				if userModules.sessionReached 	== data['examData']['sessionNumber']:
					sessionToSetScore.endDate	= date.today()
					userModules.sessionReached 	= data['examData']['sessionNumber'] + 1

					sessionToSetScore.save()
					userModules.save()
					pass				
				pass

			examToSetScore.examScore 	= data['examData']['Score']
			examToSetScore.attempts 	= examToSetScore.attempts+1
			examToSetScore.save()

			return Response('Exam score saved successfully')
			pass
		except Exception as e:
			raise e
			return Response('An error occured')

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

			


		

