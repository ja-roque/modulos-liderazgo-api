from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from bs4 import BeautifulSoup
from django.http import JsonResponse
from pathlib import Path


import os
import re

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

		contents = Path(os.path.join(self.__location__, "doc" + documentId + ".txt")).read_text()

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

		contents = os.listdir(os.path.join(self.__location__, "presentations/module_" + presentationId))
		
		# Ordering lambda: https://stackoverflow.com/questions/23724653/ordered-os-listdir-in-python
		orderedContents = sorted(contents, key=lambda x: (int(re.sub('\D','',x)),x))		
						
		return JsonResponse(orderedContents, safe=False)