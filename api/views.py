from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from main.models import Subject, Unit, Topic
from .serializers import (
    SubjectSerializer,
    UnitSerializer,
    TopicSerializer
)
from django.http import JsonResponse

def health(request):
    return JsonResponse({
        "status": "ok",
        "service": "VedaPortal API",
    })


@api_view(['GET'])
def subjects_api(request):
    subjects = Subject.objects.all()
    serializer = SubjectSerializer(subjects, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def units_api(request, subject_id):
    units = Unit.objects.filter(subject_id=subject_id)
    serializer = UnitSerializer(units, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def topics_api(request, unit_id):
    topics = Topic.objects.filter(unit_id=unit_id)
    serializer = TopicSerializer(topics, many=True)
    return Response(serializer.data)
