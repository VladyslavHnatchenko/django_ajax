from django import forms
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from django.views.generic import View, CreateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import Room


class RoomList(View):
    def get(self, request):
        rooms = list(Room.objects.all().values())
        data = dict()
        data['rooms'] = rooms
        return JsonResponse(data)


class RoomDetail(View):
    def get(self, request, pk):
        room = get_object_or_404(Room, pk=pk)
        data = dict()
        data['room'] = model_to_dict(room)
        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class RoomCreate(CreateView):
    def post(self, request):
        data = dict()
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save()
            data['room'] = model_to_dict(room)
        else:
            data['error'] = "Form is not valid!"
        return JsonResponse(data)


class RoomUpdate(View):
    def post(self, request, pk):
        data = dict()
        room = Room.objects.get(pk=pk)
        form = RoomForm(instance=room, data=request.POST)
        if form.is_valid():
            room = form.save()
            data['room'] = model_to_dict(room)
        else:
            data['error'] = "Form is not valid!"
        return JsonResponse(data)


class RoomDelete(View):
    def post(self, request, pk):
        data = dict()
        room = Room.objects.get(pk=pk)
        if room:
            room.delete()
            data['message'] = "Room deleted!"
        else:
            data['message'] = "Error!"
        return JsonResponse(data)
