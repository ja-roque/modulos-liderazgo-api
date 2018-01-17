from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from bs4 import BeautifulSoup
from django.http import JsonResponse
from pathlib import Path


import os
import re


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
	__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

	def get(self, request):

		slideObject = []
		contents = Path(os.path.join(self.__location__, "doc1.txt")).read_text()

		slidelist = re.findall('<slide>(.*?)</slide>', contents.replace('\n', '').replace('\t', ''), flags= re.DOTALL)
		
		for slide in slidelist:
			 
			fraglist = re.findall('<frag>(.*?)</frag>', slide.replace('\n', '').replace('\t', ''), flags= re.DOTALL)				
			slideObject.append(fraglist)
			pass
						
		return JsonResponse(slideObject, safe=False)