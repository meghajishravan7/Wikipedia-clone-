from django.shortcuts import render
import markdown
import random
from . import util


def md_converter(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    html_content = md_converter(title)
    if html_content == None:
        return render(request, 'encyclopedia/error.html', {
            'msg': 'This entry does not exists'
        })
    else:
        return render(request, 'encyclopedia/entry.html', {
            'title': title,
            'content': html_content
        })


def search(request):
    if request.method == 'POST':
        title = request.POST['q']
        html_content = md_converter(title)
        if html_content is not None:
            return render(request, 'encyclopedia/entry.html', {
                'title': title,
                'content': html_content
            })
        else:
            entries = util.list_entries()
            dummy = []
            for entry in entries:
                if title.lower() in entry.lower():
                    dummy.append(entry)
            return render(request, 'encyclopedia/search.html', {
                'entries': dummy
            })


def new(request):
    if request.method == 'GET':
        return render(request, 'encyclopedia/newpage.html')
    else:
        title = request.POST['title']
        content = request.POST['content']
        check = util.get_entry(title)
        if check is not None:
            return render(request, 'encyclopedia/error.html', {
                'msg': 'This page already exists'
            })
        else:
            util.save_entry(title, content)
            html_content = md_converter(title)
            return render(request, 'encyclopedia/entry.html', {
                'title': title,
                'content': html_content
            })


def edit(request):
    if request.method == 'POST':
        title = request.POST['edit_title']
        content = util.get_entry(title)
        return render(request, 'encyclopedia/edit.html', {
            'title': title,
            'content': content
        })


def save(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        html_content = md_converter(title)
        return render(request, 'encyclopedia/entry.html', {
            'title': title,
            'content': html_content
        })


def random_page(request):
    entries = util.list_entries()
    random_one = random.choice(entries)
    html_content = md_converter(random_one)
    return render(request, 'encyclopedia/entry.html', {
        'title': random_one,
        'content': html_content
    })
