from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from rango.models import Category, Page
from rango.forms import CategoryForm
from rango.forms import UserForm, UserProfilForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth import logout

def encode_url(str):
    return str.replace(' ', '_')

def decode_url(str):
    return str.replace('_', ' ')

def index(request):
    context = RequestContext(request)
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {'categories': category_list,
    				'pages': page_list}

    response = render_to_response('rango/index.html', context_dict, context)
    visits = int(request.COOKIES.get('visits', '0'))
    if 'last_visit' in request.COOKIES:
        last_visit = request.COOKIES['last_visit']
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
# -----> If it's been more than a day since the last visit reassign the value of the cookie to +1 of what it was before and update the last visit cookie, too.
        if (datetime.now() - last_visit_time).days > 0:
            response.set_cookie('visits', visits+1)     
            response.set_cookie('last_visit', datetime.now())
        else:
            response.set_cookie('last_visit', datetime.now())               

    for category in category_list:
    	category.url = encode_url(category.name)

    return response

@login_required
def add_category(request):
    context = RequestContext(request)
    context_dict = {}

    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print form.errors
    else:
        form = CategoryForm()
    context_dict['form'] = form
    return render_to_response('rango/add_category.html', context_dict, context)


def category(request, category_name_url):
    context = RequestContext(request)
    category_name = decode_url(category_name_url)
    context_dict = {'category_name': category_name, 'category_name_url': category_name_url}
    cat_list = get_category_list()
    context_dict['cat_list'] = cat_list
    try:
        category = Category.objects.get(name__iexact=category_name)
        context_dict['category'] = category
        pages = Page.objects.filter(category=category).order_by('-views')
        context_dict['pages'] = pages
    except Category.DoesNotExist:
        pass
    if request.method == 'POST':
        query = request.POST.get('query')
        if query:
            query = query.strip()
            result_list = run_query(query)
            context_dict['result_list'] = result_list
    return render_to_response('rango/category.html', context_dict, context)


@login_required
def add_page(request, category_name_url):
    context = RequestContext(request)
    cat_list = get_category_list()
    context_dict = {}
    context_dict['cat_list'] = cat_list

    category_name = decode_url(category_name_url)
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            try:
                cat = Category.objects.get(name=category_name)
                page.category = cat
            except Category.DoesNotExist:
                return render_to_response( 'rango/add_page.html',
                                          context_dict,
                                          context)
            page.views = 0
            page.save()
            return category(request, category_name_url)
        else:
            print form.errors
    else:
        form = PageForm()
    context_dict['category_name_url']= category_name_url
    context_dict['category_name'] =  category_name
    context_dict['form'] = form
    return render_to_response( 'rango/add_page.html',
                               context_dict,
                               context)    	


def register(request):
    context = RequestContext(request)

    registered = False #Set to False initially. Code changes value to True when registration succeeds.
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfilForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password) # Hash the password with the set_password method.
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True

        else:
            
            print user_form.errors, profile_form.errors

    else:
        user_form = UserForm()
        profile_form = UserProfilForm()

    return render_to_response(
            'rango/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)                


def login_view(request):
    context = RequestContext(request)
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                return HttpResponse("Your Rango account is disabled.")
                
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")            

    else:
        return render_to_response('rango/login.html', {}, context)   


@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!" )             


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/rango/')
