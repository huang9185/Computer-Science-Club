from django import forms
from django.shortcuts import render

from . import util

import random
import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    if util.get_entry(title) is None:
        content = None
    else:
        content = convert(util.get_entry(title))
    
    return render(request, "encyclopedia/entry.html", {
        "content": content,
        "title": title
    })


def edit(request):
    if request.method == "GET":
        title = request.GET.get('title')
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": util.get_entry(title)
        })
    elif request.method == "POST":
        title = request.POST["title"]
        util.save_entry(title, request.POST["content"])
        return entry(request, title)

def getRandom(request):
    entries = util.list_entries()
    title = random.choice(entries)
    return entry(request, title)

def search(request):
    searchInput = request.POST['searchInput']

    if not util.get_entry(searchInput):
        return render(request, "encyclopedia/search.html", {
            "substring": searchInput,
            "entries": util.list_entries()
        })
    
    return entry(request, searchInput)

def new(request):
    existed = False

    if request.method == "POST":
        title = request.POST["title"]

        if util.get_entry(title) is None:
            util.save_entry(title, request.POST["content"])
            return entry(request, title)
        else:
            existed = True

    return render(request, "encyclopedia/new.html", {
        "existed": existed
    })


def convert(content):
    return markdown2.markdown(content)
