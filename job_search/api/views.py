from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .serializers import SkillSerializer
from rest_framework.views import APIView
from .project import clean,rec
from django.http import HttpResponse

# Create your views here.

class JobView(APIView):
    def get(self,request):
        job = rec.recommend(request.query_params.get('job'))
        return HttpResponse(job,status=status.HTTP_200_OK)

class SkillView(APIView):
    def post(self,request):
        print(request.data)
        serializer = SkillSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            company = serializer.validated_data['company']
            employee = serializer.validated_data['employee']
            data = {'company':company,'employee':employee}
            result = clean.match(data)
            print(result)
            return Response(result,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)