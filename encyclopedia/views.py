from django.shortcuts import render

from . import util

from django import forms
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


def new(request):
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            if util.get_entry(title) == None or form.cleaned_data['edit'] == True:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("item", kwargs={"wikiPage": title}))
            else:
                return render(request, 'newPage/index.html', {'form': form, 'error': True, 'title': title})
    else:
        form = EntryForm()
    return render(request, 'newPage/index.html', {'form': form, 'error': False})


class EntryForm(forms.Form):
    title = forms.CharField(
        label='', max_length=100, widget=forms.Textarea(attrs={'placeholder': 'Wiki title', 'style': 'height: 30px;'}))
    content = forms.CharField(
        label='', widget=forms.Textarea(attrs={'placeholder': 'Wiki Content', 'style': 'height: 90px;'}))
    edit = forms.BooleanField(
        initial=False, required=False, widget=forms.HiddenInput())


def edit(request, wikiPage):
    page = util.get_entry(wikiPage)
    form = EntryForm()
    form.fields['title'].initial = wikiPage
    form.fields['content'].initial = page
    form.fields['edit'].initial = True
    form.fields['title'].widget = forms.HiddenInput()
    return render(request, 'newPage/index.html', {'form': form, 'title': form.fields['title'].initial, 'edit': form.fields['edit'].initial})
