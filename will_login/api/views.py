from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import api
from api.models import report_api
from api.models import report2_api
from api.serializers import apiSerializer
from api.serializers import reportsSerializer
from api.serializers import filesSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from login.models import ReportModel
from login.models import SingleFileModel
import json
import os
import zipfile
from io import StringIO
import io as stringIOModule
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.decorators import (
    renderer_classes,
    )

@api_view(['GET', 'POST'])
def verify_account(request):
    if request.method == 'GET':
        return Response("Hello")
    if request.method == 'POST':
        serializer = apiSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = authenticate(username= serializer.data['username'], password= serializer.data['password'])
            if user is not None:
                if user.is_active:
                    print("User is valid, active and authenticated")
                    return Response(True)
                else:
                    print("Your account has been disabled!")
                    return Response(False)
            else:
                print("The username and password were incorrect.")
                return Response(False)
    return Response(False)

@api_view(['GET', 'POST'])
@renderer_classes((JSONRenderer,))
def get_reports(request):
    if request.method == 'GET':
        return Response("Hello")
    if request.method == 'POST':
        serializer = apiSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            reports = ReportModel.objects.filter(report_owner=serializer.data['username'])
            rep_names = reports.values('report_title', 'report_body','id',)
            dict_data = [entry for entry in rep_names]
            return Response(dict_data)

    return Response(False)

@api_view(['GET', 'POST'])
@renderer_classes((JSONRenderer,))
def get_files(request):
    if request.method == 'GET':
        return Response("Hello")
    if request.method == 'POST':
        report = ReportModel.objects.get(id=request.data['id'])
        all_files = SingleFileModel.objects.filter(file_report=report)
        files = all_files.values('single_file')
        dict_data = [entry for entry in files]
        return Response(dict_data)
    return Response(False)
