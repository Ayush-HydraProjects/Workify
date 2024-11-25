from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from users.layoff_prediction_model.predict import predict
from django.http import JsonResponse
from .models import LayoffPrediction
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm, LayoffPredictionForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


def home(request):
    return render(request, 'users/home.html')


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)
    
class CustomAdminLoginView(LoginView):
    form_class = LoginForm
    template_name = 'users/adminlogin.html'  # Use your custom login template

    # Predefined credentials
    ADMIN_USERNAME = 'workifyadmin'
    ADMIN_PASSWORD = 'shivam1001'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        # Check if the credentials match the predefined ones
        if username != self.ADMIN_USERNAME or password != self.ADMIN_PASSWORD:
            form.add_error(None, "Invalid credentials for admin login.")
            return self.form_invalid(form)

        # Authenticate and log in the user
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)

            self.request.session.set_expiry(0)
            self.request.session.modified = True

            return HttpResponseRedirect(self.get_success_url())
        else:
            form.add_error(None, "Invalid credentials.")
            return self.form_invalid(form)

    def get_success_url(self):
        # Redirect to the admin dashboard or another secure page
        return reverse_lazy('users-admindashboard')

 
class AdminDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'users/admindashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch all LayoffPrediction data
        predictions = LayoffPrediction.objects.all()
        context['predictions'] = predictions
        return context


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def layoff_prediction_form(request):
    prediction_instance = None

    try:
        prediction_instance = LayoffPrediction.objects.get(user=request.user)
    except LayoffPrediction.DoesNotExist:
        pass
    if request.method == 'POST':
        form = LayoffPredictionForm(request.POST, instance=prediction_instance)
        if form.is_valid(): 
            data = form.cleaned_data
            print(data)
            # Convert to JSON serializable types
            formatted_data = {
                'Age': int(data.get('age')),
                'EducationField': int(data.get('education_field')),
                'JobRole': int(data.get('job_role')),
                'Department': int(data.get('department')),
                'Industry': int(data.get('industry')),
                'Stage': int(data.get('stage')),
                'Education': int(data.get('education')),
                'Funds_Raised(m)': float(data.get('funds_raised')),
                'PerformanceRating': int(data.get('performance_rating')),
                'JobSatisfaction': int(data.get('job_satisfaction')),
                'JobInvolvement': int(data.get('job_involvement')),
                'YearsAtCompany': int(data.get('years_at_company')),
                'YearsInCurrentRole': int(data.get('years_in_current_role')),
                'YearsWithCurrManager': int(data.get('years_with_curr_manager')),
                'MonthlyIncome': int(data.get('monthly_income')),
                'NumCompaniesWorked': int(data.get('num_companies_worked')),
                'Gender': int(data.get('gender')),
            }

            # Call the prediction function with formatted data
            prediction = predict(formatted_data)
            formdata = form.save(commit=False)  # Do not save yet
            formdata.user = request.user       # Assign the logged-in user
            formdata.prediction_percentage=prediction
            formdata.save()
            return JsonResponse({'prediction': f"{prediction:.2f}"})
    else:
        form = LayoffPredictionForm(instance=prediction_instance)
    
    return render(request, 'users/layoff_prediction_form.html', {'form': form})

def success_view(request):
    return render(request, 'users/success.html')
