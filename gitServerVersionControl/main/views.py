from django.shortcuts import render, redirect

from django.core.exceptions import ObjectDoesNotExist

from .functions import *
from .models import Repository

version = "1.0.0"


def index(request):
    context = defaultContext()
    #print(type(Repository))
    repos = Repository.objects.all()
    print(repos)
    repoList = []
    for x in repos:
        cont = parse_repo({}, x)
        cont = list(cont.values())
        repoList.append(cont)
    context.update({'repo': repoList})



    return render(request, 'main/index.html', context)


def error_repodoesnotexist(request):
    context = defaultContext()
    return render(request, 'error/repodoesnotexist.html', context)



def repo_start(request, id):
    context = defaultContext()
    id = str(id)

    try:
        repo = Repository.objects.get(code=id)
    except ObjectDoesNotExist:
        return redirect('/error/repodoesnotexist')
    context = parse_repo(context, repo)

    start_service(context["fullName"])

    repo.running = True
    repo.save()

    return redirect(f'/repo/{id}')

def repo_stop(request, id):
    context = defaultContext()
    id = str(id)
    try:
        repo = Repository.objects.get(code=id)
    except ObjectDoesNotExist:
        return redirect('/error/repodoesnotexist')
    context = parse_repo(context, repo)

    stop_service(context["fullName"])

    repo.running = False
    repo.save()
    
    return redirect(f'/repo/{id}')

def repo_enable(request, id):
    context = defaultContext()
    id = str(id)
    try:
        repo = Repository.objects.get(code=id)
    except ObjectDoesNotExist:
        return redirect('/error/repodoesnotexist')
    context = parse_repo(context, repo)

    enable_service(context["fullName"])

    repo.enable = True
    repo.save()
    
    return redirect(f'/repo/{id}')

def repo_disable(request, id):
    context = defaultContext()
    id = str(id)
    try:
        repo = Repository.objects.get(code=id)
    except ObjectDoesNotExist:
        return redirect('/error/repodoesnotexist')
    context = parse_repo(context, repo)

    disable_service(context["fullName"])

    repo.enable = False
    repo.save()
    
    return redirect(f'/repo/{id}')




def genRepo(request):
    context = defaultContext()
    #print(type(Repository))
    #repos = Repository.objects.all()
    #context.update({'repo': ''})

    
    if request.method == 'POST':
        #print("\n\npost\n\n")
        if 'cr_url' in request.POST:


            #repo = ["Name", "Description", "code", "Owner Name", "Keep Number", "url", "cTag", "serviceFilePath", "startCommand", "List of Tags"]
            repo = ["","","","","-1","","","", "", ""]


            url = str(request.POST.get('cr_url'))
            description = str(request.POST.get('cr_description'))
            startCommand = str(request.POST.get('cr_startCommand'))

            repo[5] = url
            repo[1] = description
            repo[8] = startCommand


            urlParse = url.lstrip("https://").strip("/")
            urlParse = urlParse.split("/")
            print(f"\n\n{urlParse}\n\n")


            repo[0] = urlParse[2]
            repo[3] = urlParse[1]

            codeList = []
            repos = Repository.objects.all()
            for x in repos:
                codeList.append(x.code)

            print(codeList)

            code = genCode(6, codeList)

            repo[7] = f"{urlParse[1]}_{urlParse[2]}_{code}"
            repo[2] = code

            
            tags = getTags(url)
            repo[9] = tags
            repo[6] = tags[-1]

            
            #repo = ["0Name", "1Description", "2code", "3Owner Name", "4Keep Number", "5url", "6cTag", "7serviceFilePath", "8startCommand", "9List of Tags"]

            REPO = Repository.objects.create(name = repo[0], description = repo[1], owner = repo[3], fullName = repo[7], keepNumber = repo[4], startCommand = repo[8], url = repo[5], cTag = repo[6], code = repo[2])

            repository = parse_repo({}, REPO)

            generate_repository(repository["url"], repository["cTag"],repository["fullName"], repository["startCommand"], repository["description"])


            context.update({"repo": repo})

            #print(f"\n\n{repo}\n\n")
    else:
        return redirect('/')



    return render(request, 'main/genRepo.html', context)

def repo(request, id):
    context = defaultContext()
    id = str(id)

    try:
        repo = Repository.objects.get(code=id)
    except ObjectDoesNotExist:
        return redirect('/error/repodoesnotexist')

    context = parse_repo(context, repo)


    return render(request, 'main/repo.html', context)



def repo_journalctl(request, id):
    context = defaultContext()
    id = str(id)
    try:
        repo = Repository.objects.get(code=id)
    except ObjectDoesNotExist:
        return redirect('/error/repodoesnotexist')
    context = parse_repo(context, repo)
    journalctl = journalctl_service(context["fullName"])
    #print(journalctl)
    journalctl = journalctl.split("\n")
    #print(journalctl)
    context.update({"journalctl": journalctl})


    return render(request, 'main/journalctl.html', context)

def repo_gen(request, id):
    context = defaultContext()
    try:
        repo = Repository.objects.get(code=id)
    except ObjectDoesNotExist:
        return redirect('/error/repodoesnotexist')
    context= parse_repo(context, repo)




    return redirect(f'/repo/{id}')
