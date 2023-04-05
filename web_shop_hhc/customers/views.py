from django.shortcuts import render, redirect
from .forms import SignupForm


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('redirect.html')
        else:
            form = SignupForm()
        return render(request, 'signup.html', {'form': form})
