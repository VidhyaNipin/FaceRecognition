
from django import forms
from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import path
from django.utils.html import format_html

# from . import models
from pathlib import Path

from .models import Profile

import os
import glob

import face_recognition

# imagePaths = [f for f in glob.glob('images/*.jpg')]
KNOWN_FACES_DIR = 'media/profile_images'
# KNOWN_FACES_DIR = 'images' + '*.jpg'
known_faces = []
known_names = []

# Register your models here.


class ImageUploadForm(forms.Form):
    upload_image = forms.ImageField()

    def clean_upload_image(self):
        img = self.cleaned_data['upload_image']
        print(img)
        print("img")


class RequestDemoAdmin(admin.ModelAdmin):
    upload_image = forms.ImageField()
    list_display = [field.name for field in Profile._meta.get_fields()]
    search_fields = ['name', 'phone', 'gender']

    # def image_tag(self, obj):
    #     return format_html('<img src="{}" width="auto" height="200px" />'.format(obj.avatar.url))
    #
    # image_tag.short_description = 'Image'
    #
    # list_display = ['image_tag']
    # readonly_fields = ['image_tag']

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('image-search/', self.search_image), ]
        return new_urls + urls

    def search_image(self, request):

        form = ImageUploadForm()

        if request.method == 'POST':
            print("action is post")
            img = request.FILES['upload_image']
            print(img)

            for filename in os.listdir(KNOWN_FACES_DIR):
                image = face_recognition.load_image_file(os.path.join(KNOWN_FACES_DIR, filename))
                encoding = face_recognition.face_encodings(image)[0]
                known_faces.append(encoding)
                known_names.append(filename)

            unknown_image = face_recognition.load_image_file(img)
            unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

            # Now we can see the two face encodings are of the same person with `compare_faces`!
            results = face_recognition.compare_faces(known_faces, unknown_encoding)
            match = None
            if True in results:
                match = known_names[results.index(True)]
                print({match})
                name = Path(match).stem

                print(name)

                print(results)
                context = {}
                context['user_details'] = Profile.objects.get(id=name)

                return render(request, "admin/test1.html", context)

            else:
                return HttpResponse("Not Found")

        return render(request, "admin/search_image.html", {'form': form})


admin.site.register(Profile, RequestDemoAdmin)