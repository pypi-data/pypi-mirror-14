from django.contrib.auth.models import User, Group, Permission
from django.conf import settings
from django.db import connection
from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test

# Third party imports.
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route,detail_route
from rest_framework.pagination import PageNumberPagination
from django_comments.models import Comment

# local app related imports
from .models import Issues, increment_issue_number
from .serializers import IssuesSerializer
from .utils import send_mail_data
from .decorators import user_in_group_required

class StandardIssueResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 25

# API for issues
class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issues.objects.all()
    serializer_class = IssuesSerializer
    pagination_class = StandardIssueResultsSetPagination

    def get_queryset(self):
        return Issues.objects.filter(issue_owner=self.request.user)

    def create(self, request, *args, **kwargs):
        request.data['issue_owner'] = request.user
        request.data['issue_no'] = increment_issue_number()
        try:
            request.user.employee
            request.data['owner_role'] = "Employee"
        except:
            request.data['owner_role'] = "Consultant"

        issue = Issues.objects.create(title=request.data['title'], issue_owner=request.user, issue_no=increment_issue_number(),
                                      owner_phone_number=request.data['owner_phone_number'], description=request.data['description'],
                                      status=request.data['status'], issue_priority=request.data['issue_priority'], classification=request.data['classification'], owner_role=request.data['owner_role'], snapshot=request.FILES.get('snapshot[0]'))
        tenant = connection.get_tenant()
        url = tenant.domain_url
        link = "http://" + url + "/api/issue-details/" + str(issue.id)
        issues = Issues.objects.filter(issue_owner=self.request.user)
        context = {"type":"Issue_Assigned", "template":"IssueCreated", "link":link, "issue_no": issue.issue_no, "issue_title":issue.title, "descrption":issue.description, "created_by":issue.issue_owner.username, "priority":issue.issue_priority, "classification":issue.classification, "email_to":['abhinav.sohani@consultadd.in', 'chinmay.deshpande@consultadd.in'], "created_at":issue.created}
        send_mail_data(context)
        results = IssuesSerializer(issues, many=True)
        return Response(results.data, status="200")


    @list_route(methods=["GET"])
    def issues_by_user(self, request):
        """
        Returns the issues created by logged in user.
        :param: current user
        """
        user = request.user
        issues = Issues.objects.filter(issue_owner=user)
        serializer = self.get_serializer(issues, many=True)
        return Response({"results":[serializer.data]})

    @list_route(methods=["GET"])
    def issues_by_status(self, request):
        """
        Returns the issues of particular status.
        :param: status ex: status=open
        """
        status = request.query_params.get("status", None)
        issues = Issues.objects.filter(status__icontains=status)
        serializer = self.get_serializer(issues, many=True)
        return Response({"results":[serializer.data]})

    @list_route(methods=["GET"])
    def issues_by_priority(self, request):
        """
        Returns the issues of particular priority.
        :param: priority ex: priority=open
        """
        priority = request.query_params.get("priority", None)
        issues = Issues.objects.filter(issue_priority__icontains=priority)
        serializer = self.get_serializer(issues, many=True)
        return Response({"results":[serializer.data]})

    @list_route(methods=["GET"])
    def issues_by_classification(self, request):
        """
        Returns the issues for on the basis of classification.
        :param: classification ex: classification=query
        """
        classification = request.query_params.get("classification", None)
        issues = Issues.objects.filter(classification__icontains=classification)
        serializer = self.get_serializer(issues, many=True)
        return Response({"results":[serializer.data]})

    @list_route(methods=["GET"])
    def issues_by_status_and_user(self, request):
        """
        Returns the issues on the basis of status of current user.
        :param: status ex: classification=query
        """
        status = request.query_params.get("status", None)
        issues = Issues.objects.filter(issue_owner=request.user,classification__icontains=status)
        serializer = self.get_serializer(issues, many=True)
        return Response({"results":[serializer.data]})

    @list_route(methods=["GET"])
    def issues_by_priority_and_user(self, request):
        """
        Returns the issues of particular priority created by current user.
        :param: priority ex: priority=open
        """
        priority = request.query_params.get("priority", None)
        issues = Issues.objects.filter(issue_owner=request.user, issue_priority__icontains=priority)
        serializer = self.get_serializer(issues, many=True)
        return Response({"results":[serializer.data]})

    @list_route(methods=["GET"])
    def issues_by_classification_and_user(self, request):
        """
        Returns the issues for on the basis of classification created by current user.
        :param: classification ex: classification=query
        """
        classification = request.query_params.get("classification", None)
        issues = Issues.objects.filter(issue_owner=request.user, classification__icontains=classification)
        serializer = self.get_serializer(issues, many=True)
        return Response({"results":[serializer.data]})

    @list_route(methods=["GET"])
    def issues_by_classification_and_user(self, request):
        """
        Returns the issues for on the basis of classification created by current user.
        :param: classification ex: classification=query
        """
        classification = request.query_params.get("classification", None)
        issues = Issues.objects.filter(issue_owner=request.user, classification__icontains=classification)
        serializer = self.get_serializer(issues, many=True)
        return Response({"results":[serializer.data]})
