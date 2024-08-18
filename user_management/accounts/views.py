from django.shortcuts import render, redirect
from .forms import SignupForm, LoginForm, PostForm, EditForm
from .models import CustomUser , Post, Category
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView ,DeleteView
from django.urls import reverse_lazy



def home(request):
    return render(request, 'signup.html')



def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        
        email = request.POST.get('email')
        username = request.POST.get('username')

        # Checks if the user already exists
        if CustomUser.objects.filter(email=email).exists() or CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'User already exists! try a different username.')
            return redirect('signup')

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Signup successful!')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match')
  
        
    else:
        form = SignupForm()
    
    return render(request, 'signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user_type = form.cleaned_data.get('user_type')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user_type and user.user_type != user_type:
                    messages.error(request, 'User type does not match.')
                    return redirect('login')
                auth_login(request, user)
               
                
                # Checks user type and redirect accordingly
                if hasattr(user, 'user_type'):
                    if user.user_type == 'Doctor':
                        return redirect('doctor_dashboard')
                    elif user.user_type == 'Patient':
                        return redirect('patient_dashboard')
                else:
                    # Fallback if user_type is not set
                    return redirect('dashboard')

            else:
                messages.error(request, 'Invalid email or password.')

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'dashboard.html', {'user': request.user})


def doctor_dashboard(request):
    if request.user.user_type != 'Doctor':
        return redirect('login')
   
    show_drafts = request.GET.get('show_drafts', 'false') == 'true'
  
    if show_drafts:
        posts = Post.objects.filter(author=request.user, status=Post.DRAFT).order_by('-created_at')
    else:
         posts = Post.objects.filter(status=Post.PUBLISHED).order_by('-created_at')
        
    cat_menu = Category.objects.all()
    
    published = Post.objects.filter(author=request.user, status=Post.PUBLISHED)
    return render(request, 'doctor_dashboard.html', {'object_list': posts, 'user': request.user,'cat_menu': cat_menu, 'published' : published})


def CategoryView(request, cats):
    category_posts = Post.objects.filter(category=cats)
    cat_menu = Category.objects.all()
    return render(request,'categories.html',{'cats':cats,'category_posts':category_posts, 'cat_menu': cat_menu})

class addCategoryView(CreateView):
    model = Category
    template_name = 'addcategory.html'
    fields = '__all__'
    success_url = reverse_lazy('doctor_dashboard')
    

class updatePostView(UpdateView):
    model = Post
    form_class = EditForm
    template_name = 'updatepost.html'
  

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class deletePostView(DeleteView):
    model = Post
    template_name = 'deletepost.html'
    success_url = reverse_lazy('doctor_dashboard')
    fields = '__all__'

class articleDetailView(DetailView):
    model = Post
    template_name = 'article_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
         cat_menu = Category.objects.all()
         context = super(articleDetailView,self).get_context_data(**kwargs)
         context["cat_menu"] = cat_menu
         return context

class addPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'addpost.html'
   


def patient_dashboard(request):
    if request.user.user_type != 'Patient':
        return redirect('login')
    posts = Post.objects.filter(status=Post.PUBLISHED).order_by('-created_at')
    cat_menu = Category.objects.all()

    
    return render(request, 'patient_dashboard.html', {'posts': posts, 'user': request.user,'cat_menu': cat_menu})
    
def draft_posts(request):
    if request.user.user_type != 'Doctor':
        return redirect('login')

    drafts = Post.objects.filter(author=request.user,status=Post.DRAFT)
    return render(request, 'draft.html', {'object_list': drafts})