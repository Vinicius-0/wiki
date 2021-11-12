from django.shortcuts import render

from . import util

from django.http import HttpResponseRedirect
from django.urls import reverse

import markdown2

import secrets


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def item(request, wikiPage):
    entry = util.get_entry(wikiPage)
    if entry == None:
        return render(request, "errorPage/index.html", {
            "wikiPage": wikiPage.capitalize(),
        })
    else:
        return render(request, "itemPage/index.html", {
            "entries": util.get_entry(wikiPage),
            "wikiPage": wikiPage,
            "content": markdown2.markdown(util.get_entry(wikiPage))
        })


def search(request):
    value = request.GET.get('q', '')
    entry = util.get_entry(value)
    if entry != None:
        return HttpResponseRedirect(reverse("item", kwargs={"wikiPage": value}))
    else:
        entries = []
        for entry in util.list_entries():
            if value.lower() in entry.lower():
                entries.append(entry)

        return render(request, "search/index.html", {
            "entries": entries,
            "value": value
        })


def random(request):
    entries = util.list_entries()
    randomEntry = secrets.choice(entries)
    return HttpResponseRedirect(reverse("item", kwargs={"wikiPage": randomEntry}))
