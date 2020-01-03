import datetime
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext, Context
from django.views import generic
from shel.forms import MemberRegModelForm, GroupRegModelForm, EditProfileForm
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse_lazy, reverse

from shel.models import Group, Post, Membership, Person, visitedPost
from .forms import LoginForm


def index_view(request):
    return render_to_response("index.html", {}, context_instance=RequestContext(request))


def signup(request):
    if request.method == 'POST':
        member = MemberRegModelForm(request.POST, request.FILES)
        if member.is_valid():
            member.image = request.FILES['image']
            member.save()
            return HttpResponseRedirect('/thanks/')

        return render_to_response('signup.html', {'form': member}, context_instance=RequestContext(request))

    else:
        form = MemberRegModelForm()
        return render_to_response('signup.html', {'form': form}, context_instance=RequestContext(request))


def thanks(request):
    return render_to_response('thanks.html', {}, context_instance=RequestContext(request))


def main_after_login(request):
    if request.method == "GET":
        if request.user.userProfile:
            mark = None
            groups = []
            for l in Group.objects.filter(admin=request.user.userProfile).all():
                groups.append(l)

            for k in Group.objects.all():
                for m in k.groupid.all().filter(isAccepted=True):
                    if m.person.pk == request.user.userProfile.pk:
                        groups.append(Group.objects.get(pk = m.group.pk))

            if request.GET.get('groupId'):
                posts = Post.objects.filter(group__id=request.GET.get('groupId'))
                for p in posts:
                    if p.visited.all().__len__() == 0:
                        tmp = visitedPost(member=Person.objects.get(pk = request.user.userProfile.pk),
                                              post = Post.objects.get(pk=p.pk))
                        tmp.save()
                    else:
                        for v in p.visited.all():
                            if v.member.pk != request.user.userProfile.pk:
                                tmp = visitedPost(member=Person.objects.get(pk = request.user.userProfile.pk),
                                                  post = Post.objects.get(pk=p.pk))
                                tmp.save()
                groupNotif = [];
                for g in groups:
                    visited = 0
                    all_post = 0
                    if g.pk == request.GET.get('groupId'):
                        groupNotif.append(0)
                    else:
                        if request.GET.get('mark'):
                             mark = True
                             for v in g.groupname.all():
                                b = False
                                for w in v.visited.all():
                                    if w.member.pk == request.user.userProfile.pk:
                                        b = True
                                        break
                                if b == False:
                                    tmp = visitedPost(member=Person.objects.get(pk = request.user.userProfile.pk),
                                                  post = Post.objects.get(pk=v.pk))
                                    tmp.save()
                             groupNotif.append(0)
                        else:
                            for ipost in g.groupname.all():
                                all_post +=1
                                for jpost in ipost.visited.all():
                                    if jpost.member.pk == request.user.userProfile.pk:
                                        visited += 1
                            if((all_post-visited)<0):
                             groupNotif.append(0)
                            else:
                              groupNotif.append((all_post-visited))
                groupNotif.reverse()
                return render_to_response("firstPage.html", {'mark':mark,'groups': groups, 'posts': posts.order_by('date'), 'groupId':request.GET.get('groupId'), 'notif':groupNotif},
                                          context_instance=RequestContext(request))
            else:
                groupNotif = [];
                for g in groups:
                    visited = 0
                    all_post = 0
                    print('-----------------')
                    print(g.name)
                    if request.GET.get('mark'):
                        mark = True;
                        for v in g.groupname.all():
                                b = False
                                for w in v.visited.all():
                                    if w.member.pk == request.user.userProfile.pk:
                                        b = True
                                        break

                                if b == False:
                                    print()
                                    tmp = visitedPost(member=Person.objects.get(pk = request.user.userProfile.pk),
                                                  post = Post.objects.get(pk=v.pk))
                                    tmp.save()
                        groupNotif.append(0)
                    else:
                        for ipost in g.groupname.all():
                            all_post +=1
                            for jpost in ipost.visited.all():
                                if jpost.member.pk == request.user.userProfile.pk:
                                    visited += 1
                        if((all_post-visited)<0):
                             groupNotif.append(0)
                        else:
                              groupNotif.append((all_post-visited))

                groupNotif.reverse()
                return render_to_response("firstPage.html", {'mark':mark,'groups': groups,
                                                             'posts': None, 'notif':groupNotif},
                                          context_instance=RequestContext(request))
        else:
            return render_to_response("firstPage.html", {}, context_instance=RequestContext(request))
    else:
        groups = []
        for l in Group.objects.filter(admin=request.user.userProfile).all():
            groups.append(l)

        for k in Group.objects.all():
            for m in k.groupid.all().filter(isAccepted=True):
                if m.person.pk == request.user.userProfile.pk:
                    groups.append(Group.objects.get(pk = m.group.pk))

        groupId = request.POST.get("gid", "")
        posts = Post.objects.filter(group__id=int(groupId))
        message = request.POST['message']
        post = Post(text=message, date=datetime.datetime.now(),creator=request.user.userProfile,group= Group.objects.get(id=int(groupId)))
        post.save()
        groupNotif = [];
        for g in groups:
            visited = 0
            all_post = 0
            if g.pk == request.GET.get('groupId'):
                groupNotif.append(0)
            else:
                for ipost in g.groupname.all():
                    all_post +=1
                    for jpost in ipost.visited.all():
                        if jpost.member.pk == request.user.userProfile.pk:
                            visited += 1
                    groupNotif.append((all_post-visited))
        groupNotif.reverse()
        return render_to_response("firstPage.html", {'groups': groups, 'posts': posts.order_by('date'), 'groupId': groupId,  'notif':groupNotif},
                                          context_instance=RequestContext(request))

def make_group(request):
    if request.method == 'POST':
        group = GroupRegModelForm(request.POST, request.FILES, user=request.user.userProfile)
        if group.is_valid():
            group.save()
            return HttpResponseRedirect('/mainAfterLogin/')

        return render(request, 'profile.html', {'form': group})

    else:
        form = GroupRegModelForm()
        return render(request, 'profile.html', {'form': form})




class LoginView(generic.FormView):
    form_class = LoginForm
    success_url = '/mainAfterLogin/'
    template_name = 'login.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(self.request, user)
            return super(LoginView, self).form_valid(form)
        else:
            return self.form_invalid(form)

def log_out(request):
    logout(request)
    return render(request, "index.html")

def search(request):
    query = request.GET['q']

    groups=Group.objects.filter(name__contains=query).exclude(admin=request.user.userProfile)
 #   t = loader.get_template('template/results.html')
  #  c = Context({ 'query': query,})
    return render(request, 'results.html', { 'groups': groups})
   # return HttpResponse(t.render(c))
def sendrequest(request):
    groupId = request.POST.get("gid", "")
    pid = request.user.userProfile.pk;
    membershipRequest = Membership(person=Person.objects.get(pk=pid), group=Group.objects.get(pk=groupId),isAccepted=False)
    membershipRequest.save()
    return render(request, "sendrequest.html")

def karbari(request):
    if request.method == "GET":
        query = request.GET.get("q","")
        if query=="":
            searchResult=None
        else:
            searchResult=[]
            for tmp in Group.objects.filter(name__contains=query).exclude(admin=request.user.userProfile):
                b = False
                for tmp2 in request.user.userProfile.groupmember.all():
                    if tmp.pk == tmp2.group.pk:
                        b = True
                        break
                if b == False:
                        searchResult.append(Group.objects.get(pk=tmp.pk))

        groups = request.user.userProfile.groupadmin.all()
        requests=[]
        for g in groups:
            for m in g.groupid.all().exclude(isAccepted=True):
                requests.append(m)

        return render(request, "karbari.html", {'req':requests, 'searchResult':searchResult, 'person':request.user.userProfile})
    else:

         rid = request.POST.get("rid", "")
         oneReq = Membership.objects.get(pk = rid)
         if ("accept"==request.POST.get("accept", "")):
          oneReq.isAccepted = True
         elif ("reject"==request.POST.get("reject", "")):
           oneReq.isAccepted = False
         oneReq.save()
         groups = request.user.userProfile.groupadmin.all()
         requests=[]
         for g in groups:
            for m in g.groupid.all().filter(isAccepted__isnull=True):
                requests.append(m)

         return render(request, "karbari.html", {'req':requests,'searchResult':None,'person':request.user.userProfile})






def edit_profile(request):

    user = request.user
    form = EditProfileForm(request.POST or None, initial={'displayed_name':user.userProfile.displayed_name, 'image':user.userProfile.image})
    if request.method == 'POST':
        if form.is_valid():
            if request.POST['displayed_name']:
                user.userProfile.displayed_name = request.POST['displayed_name']
            if request.POST['image']:
                user.userProfile.image = request.POST['image']
            user.userProfile.save()
            return render(request, "karbari.html",{'person':request.user.userProfile})

    context = {
        "form": form
    }
    return render(request, "edit_profile.html", context)