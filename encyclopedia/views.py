from django.shortcuts import render

from . import util

import markdown2


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
