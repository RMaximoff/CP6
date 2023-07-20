from django.http import HttpResponse
from django.shortcuts import render


def reg(request):
    return HttpResponse("Домашняя страница")
