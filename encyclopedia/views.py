from django.shortcuts import render

from . import util
import markdown2

def entry_page(request,title):
    content=util.get_entry(title)
    if content is None:
        return render(request,"encyclopedia/error.html",{"message":"The requested page was not found."})
    else:
        return render(request, "encyclopedia/entry.html", {
        "title":title,
        "content":markdown2.markdown(content)
    })

def search(request):
    query = request.GET.get("q")
    entries = util.list_entries()
    results = [entry for entry in entries if query.lower() in entry.lower()]

    if len(results) == 1 and results[0].lower() == query.lower():
        return entry_page(request, results[0])
    
    return render(request, "encyclopedia/search.html", {
        "query": query,
        "results": results
    })
from django import forms

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea, label="Content")

def new_page(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title) is not None:
                return render(request, "encyclopedia/new_page.html", {
                    "form": form,
                    "error": "Page with this title already exists."
                })
            util.save_entry(title, content)
            return entry_page(request, title)
    else:
        form = NewPageForm()

    return render(request, "encyclopedia/new_page.html", {
        "form": form
    })

def edit_page(request, title):
    if request.method == "POST":
        content = request.POST["content"]
        util.save_entry(title, content)
        return entry_page(request, title)

    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "The requested page was not found."
        })
    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "content": content
    })

import random

def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return entry_page(request, random_entry)

def index(request):
    entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })





