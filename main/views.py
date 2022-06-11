from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import *

from django.core.mail import EmailMultiAlternatives


# Create your views here.
def index(request):
    context = {'types': TypeProduct.objects.all()}

    return render(request, context=context, template_name='index.html')


class ProductListView(ListView):
    model = Product
    paginate_by = 2
    template_name = "search-type.html"

    def get_queryset(self):
        type_url = self.kwargs['type_url']
        products = Product.objects.filter(type__url__iexact=type_url)
        return products


class ProductDetailView(DetailView):
    model = Product
    template_name = "product-detail.html"


class ProductCreateView(LoginRequiredMixin, CreateView):
    
    login_url = reverse_lazy('login')
    redirect_field_name = 'redirect_to'

    model=Product
    template_name='product-edit.html'
    fields = ['name', 'description', 'price',
              'photo', 'type', 'is_used', 'district']
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        print(ProductOwner.objects.filter(user=self.request.user).first())
        form.instance.user = CustomUser.objects.filter(user=self.request.user).first()
        return super().form_valid(form)


def user_register_view(request):
    if request.method == "GET":
        user_form = UserRegisterForm()
        return render(request, template_name='user-edit.html', context={'form': user_form})
    else:
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            user_form = UserForm(request.POST)
            user_form.save()
            user = user_form.instance
            user.is_active = False
            user.set_password(request.POST['password'])
            user.save()
            
            custom_user_form = CustomUserForm(request.POST)
            custom_user_form.save(commit=False)
            custom_user = custom_user_form.instance
            custom_user.user = user
            custom_user.save()

            print(request.POST['email'])

            import smtplib


            sender = 'musulmon.lolayev.94@gmail.com'
            receiver = 'musulmon.lolayev.94@mail.ru'
            password = 'tkyqniiktvtzqqft'
            smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.ehlo
            smtpserver.login(sender, password)
            msg = f"""You can 
            activate your account by opening this <a href='{reverse_lazy('activate-email')}?code=222&username={request.POST['username']}'> link.</a>
            """
            smtpserver.sendmail(sender, receiver, msg)
            print('Sent')
            smtpserver.close()

            subject, from_email, to = 'Actiavation an account', 'musulmon.lolayev.94@gmail.com', request.POST['email']

            html_content = f"""You can 
            activate your account by opening this <a href='{reverse_lazy('activate-email')}?code=222&username={request.POST['username']}'> link.</a>
            """
            msg = EmailMultiAlternatives(subject, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            return redirect(index)

        else:
            return render(request, template_name='user-edit.html', context={'form': user_register_form})

def login_view(request):
    if request.method == 'GET':
        return render(request, template_name='login.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            red_url = request.GET.get('redirect_to')
            if red_url:
                return redirect(red_url)
            else:
                return redirect('index')
        else:
            return redirect('login')

class UserRegisterView(CreateView):
    model = CustomUser
    template_name = 'user-edit.html'
    fields = "__all__"
    success_url = reverse_lazy("index")


def email_activate(request):
    code = request.GET.get('code')
    username = request.GET.get('username')

    print(code, username)

    if code == '222':
        user = User.objects.filter(username=username).first()
        user.is_active = True
        user.save()

        return redirect('index')
