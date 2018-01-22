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
from pathlib import Path
# =========================================
# =========================================




class docObject(object):
    def __init__(self, title, slides):
        self.title = title
        self.slides = slides

class RestrictedView(APIView):
	permission_classes = (IsAuthenticated, )
	authentication_classes = (JSONWebTokenAuthentication, )

	def get(self, request):
		data = {
		'id': request.user.id,
		'username': request.user.username,
		'token': str(request.auth)
		}
		return Response(data)

class getDoc(APIView):
	# This endpoint gets a number from uri to identify which document to return in form of array.
	__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

	def get(self, request):
		documentId = request.query_params['id']
		slideObject = []

		contents = Path('/home/modulos_api/content/docs/doc' + documentId + ".txt").read_text()

		doctitle	= re.findall('<title>(.*?)</title>', contents.replace('\n', '').replace('\t', ''), flags= re.DOTALL)
		slidelist = re.findall('<slide>(.*?)</slide>', contents.replace('\n', '').replace('\t', ''), flags= re.DOTALL)
		
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
		presentationId = request.query_params['id']
		slideObject = []

		contents = os.listdir('/home/modulos_api/content/presentations/module_' + presentationId)

		# Ordering lambda: https://stackoverflow.com/questions/23724653/ordered-os-listdir-in-python
		orderedContents = sorted(contents, key=lambda x: (int(re.sub('\D','',x)),x))		
						
		return JsonResponse(orderedContents, safe=False)

class getUserModules(APIView):
	permission_classes = (IsAuthenticated, )
	authentication_classes = (JSONWebTokenAuthentication, )

	def get(self, request):
		data = {
		'id': request.user.id,
		'username': request.user.username,
		'token': str(request.auth)
		}

		requestingUser = User.objects.get(id=data['id'])

		userProfile = Userprofile.objects.get(userID=requestingUser)
		userModules = Modules.objects.get(id=userProfile.modulesID_id)

		return Response(model_to_dict(userModules))

