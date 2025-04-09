# # accounts/views.py
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth import login, authenticate
# from django.urls import reverse
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required

# from .forms import UserRegistrationForm, EventCreationForm, EventPrivacyForm, EventForm
# from .models import Users, Events, Universities, RSOs, StudentsRSOs, RSOEvents, EventCreation, Comments

# def get_university_from_email(user_email):
#     if '@' in user_email and '.edu' in user_email:
#         domain = user_email.split('@')[1]
#         return domain.split('.edu')[0]
#     return None

# @login_required
# def home(request):
#     # Build the events queryset based on the user role
#     user = request.user
#     if user.role == 'SuperAdmin':
#         events = Events.objects.all()
#     else:
#         email_university = get_university_from_email(user.email)
#         public_events = Events.objects.filter(
#             event_id__in=EventCreation.objects.filter(privacy='Public').values_list('event_id', flat=True)
#         )
#         private_event_ids = EventCreation.objects.filter(
#             privacy='Private',
#             admin__email__icontains=f'@{email_university}.edu'
#         ).values_list('event_id', flat=True)
#         private_events = Events.objects.filter(event_id__in=private_event_ids)
#         user_rso_ids = StudentsRSOs.objects.filter(uid=user).values_list('rso_id', flat=True)
#         rso_event_ids = RSOEvents.objects.filter(rso_id__in=user_rso_ids).values_list('event_id', flat=True)
#         rso_events = Events.objects.filter(event_id__in=rso_event_ids)
#         events = public_events | private_events | rso_events

#     events = events.distinct()
#     # Pass available RSOs to the template so that we don’t call model methods in the template.
#     available_rsos = RSOs.objects.exclude(members=user)
#     return render(request, 'accounts/home.html', {
#         'events': events,
#         'available_rsos': available_rsos,
#     })

# def login_view(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('accounts:home')
#             else:
#                 form.add_error(None, 'Invalid login credentials')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'accounts/login.html', {'form': form})

# def register(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             role = form.cleaned_data.get('role')
#             if role == 'admin':
#                 user.is_staff = True
#             elif role == 'superadmin':
#                 user.is_superuser = True
#             user.save()
#             login(request, user)
#             return redirect('accounts:home')
#     else:
#         form = UserRegistrationForm()
#     return render(request, 'accounts/register.html', {'form': form})

# Similarly, define create_event, create_rso, join_rso, leave_rso, add_comment, edit_comment, delete_comment…
# (Ensure that there is only one definition for each view, and that home() is defined exactly once.)

# accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import UserRegistrationForm, EventCreationForm, EventPrivacyForm, EventForm
from .models import Users, Events, Universities, RSOs, StudentsRSOs, RSOEvents, EventCreation, Comments

def get_university_from_email(user_email):
    if '@' in user_email and '.edu' in user_email:
        domain = user_email.split('@')[1]
        return domain.split('.edu')[0]
    return None

@login_required
def create_rso(request):
    if request.method == 'POST':
        rso_name = request.POST.get('name')
        uni_name = get_university_from_email(request.user.email)
        university = Universities.objects.filter(name__icontains=uni_name).first()
        if not university:
            messages.error(request, "Could not match your email to any university.")
            return redirect('home')
        if RSOs.objects.filter(name=rso_name, university=university).exists():
            messages.error(request, "RSO already exists at your university.")
            return redirect('home')
        new_rso = RSOs.objects.create(name=rso_name, university=university, admin=request.user)
        new_rso.members.add(request.user)
        new_rso.update_status()
        messages.success(request, "RSO created successfully.")
        return redirect('home')
    return render(request, 'accounts/create_rso.html')

@login_required
def join_rso(request, rso_id):
    rso = get_object_or_404(RSOs, pk=rso_id)
    if request.user in rso.members.all():
        messages.info(request, "Already a member of this RSO.")
    else:
        rso.members.add(request.user)
        rso.update_status()
        messages.success(request, "Successfully joined the RSO.")
    return redirect('home')

@login_required
def leave_rso(request, rso_id):
    rso = get_object_or_404(RSOs, pk=rso_id)
    if request.user in rso.members.all():
        rso.members.remove(request.user)
        rso.update_status()
        messages.success(request, "Left the RSO successfully.")
    else:
        messages.info(request, "You're not a member of this RSO.")
    return redirect('home')

@login_required
def create_event(request):
    from .models import Locations  # Import Locations

    if request.method == 'POST':
        event_form = EventForm(request.POST)
        privacy_form = EventPrivacyForm(request.POST)

        # Assume you also include extra location fields in your HTML form:
        location_name = request.POST.get('location_name', '').strip()
        location_address = request.POST.get('address', '').strip()
        location_longitude = request.POST.get('longitude', '').strip()
        location_latitude = request.POST.get('latitude', '').strip()

        if event_form.is_valid() and privacy_form.is_valid():
            event = event_form.save(commit=False)
            privacy = privacy_form.cleaned_data['privacy']

            # If location details are provided, use them:
            if location_name and location_address and location_longitude and location_latitude:
                try:
                    longitude_val = float(location_longitude)
                    latitude_val = float(location_latitude)
                except ValueError:
                    event_form.add_error(None, "Invalid longitude or latitude values.")
                    return render(request, 'accounts/event_creation.html', {
                        'event_form': event_form,
                        'privacy_form': privacy_form
                    })
                # Try to find a matching location (simple lookup by name)
                location, created = Locations.objects.get_or_create(
                    lname=location_name,
                    defaults={
                        'address': location_address,
                        'longitude': longitude_val,
                        'latitude': latitude_val,
                    }
                )
                event.lname = location
            else:
                # If no location details are provided, you might want to assign a default,
                # or add an error telling the user they must fill in a location.
                event_form.add_error(None, "Please provide location details.")
                return render(request, 'accounts/event_creation.html', {
                    'event_form': event_form,
                    'privacy_form': privacy_form
                })

            # Determine and assign the university based on privacy.
            if privacy != 'Public':
                uni_name = get_university_from_email(request.user.email)
                university = Universities.objects.filter(name__icontains=uni_name).first()
                if not university:
                    event_form.add_error(None, "Could not find a matching university for your email.")
                    return render(request, 'accounts/event_creation.html', {
                        'event_form': event_form,
                        'privacy_form': privacy_form
                    })
                event.university = university
            else:
                event.university = Universities.objects.first()

            # Validate and save the event.
            try:
                event.full_clean()  # Runs model validations (like overlapping check)
            except Exception as e:
                event_form.add_error(None, str(e))
                return render(request, 'accounts/event_creation.html', {
                    'event_form': event_form,
                    'privacy_form': privacy_form
                })
            event.save()

            # Create the EventCreation record.
            event_creation = privacy_form.save(commit=False)
            event_creation.event = event
            event_creation.admin = request.user
            event_creation.superadmin = Users.objects.filter(role='SuperAdmin').first()
            event_creation.privacy = privacy
            event_creation.save()

            # If it's a Private event and an RSO is selected, create the RSOEvents record.
            if privacy == 'Private' and privacy_form.cleaned_data.get('rso'):
                RSOEvents.objects.create(event=event, rso=privacy_form.cleaned_data['rso'])

            messages.success(request, "Event created successfully!")
            return redirect('home')

    else:
        event_form = EventForm()
        privacy_form = EventPrivacyForm()

    return render(request, 'accounts/event_creation.html', {
        'event_form': event_form,
        'privacy_form': privacy_form
    })


def home(request):
    if request.user.is_authenticated:
        user = request.user
        if user.role == 'SuperAdmin':
            events = Events.objects.all()
        else:
            email_university = get_university_from_email(user.email)
            public_events = Events.objects.filter(
                event_id__in=EventCreation.objects.filter(privacy='Public').values_list('event_id', flat=True)
            )
            private_event_ids = EventCreation.objects.filter(
                privacy='Private',
                admin__email__icontains=f'@{email_university}.edu'
            ).values_list('event_id', flat=True)
            private_events = Events.objects.filter(event_id__in=private_event_ids)
            user_rso_ids = StudentsRSOs.objects.filter(uid=user).values_list('rso_id', flat=True)
            rso_event_ids = RSOEvents.objects.filter(rso_id__in=user_rso_ids).values_list('event_id', flat=True)
            rso_events = Events.objects.filter(event_id__in=rso_event_ids)
            events = public_events | private_events | rso_events
        events = events.distinct()
        available_rsos = RSOs.objects.exclude(members=user)
    else:
        events = []
        available_rsos = []

    return render(request, 'accounts/home.html', {'events': events, 'available_rsos': available_rsos})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data['role']
            if role == 'admin':
                user.is_staff = True
            elif role == 'superadmin':
                user.is_superuser = True
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid login credentials')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def add_comment(request, event_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        rating = request.POST.get('rating')
        if content and rating:
            event = get_object_or_404(Events, event_id=event_id)
            Comments.objects.create(uid=request.user, event=event, content=content, rating=rating)
            messages.success(request, "Your comment was added successfully!")
        else:
            messages.error(request, "There was an error with your comment.")
    return redirect('home')

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comments, comment_id=comment_id, uid=request.user)
    if request.method == 'POST':
        content = request.POST.get('content')
        rating = request.POST.get('rating')
        if content and rating:
            comment.content = content
            comment.rating = rating
            comment.save()
            messages.success(request, "Your comment was updated successfully!")
            return redirect('home')
        else:
            messages.error(request, "There was an error updating your comment.")
    return render(request, 'accounts/edit_comment.html', {'comment': comment})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comments, comment_id=comment_id, uid=request.user)
    if request.method == 'POST':
        comment.delete()
        messages.success(request, "Your comment was deleted successfully!")
    return redirect('home')


# # from django.shortcuts import render, redirect, get_object_or_404
# # from django.contrib.auth.forms import UserCreationForm
# # from django.contrib.auth import login, authenticate
# # from django.http import HttpResponseForbidden
# # from .forms import UserRegistrationForm, EventCreationForm, EventPrivacyForm, EventForm
# # from django.contrib.auth.forms import AuthenticationForm
# # from django.urls import reverse
# # from django.contrib import messages
# # from .models import Users, Events, Universities, RSOs, StudentsRSOs, RSOEvents, EventCreation, Comments


# # def home(request):
# #     # Check if the user is authenticated
# #     if request.user.is_authenticated:
# #         user = request.user

# #         # SuperAdmin sees everything
# #         if user.role == 'SuperAdmin':
# #             events = Events.objects.all()
# #         else:
# #             email_university = get_university_name_from_email(user.email)

# #             # Public events
# #             public_events = Events.objects.filter(
# #                 event_id__in=EventCreation.objects.filter(privacy='Public').values_list('event_id', flat=True)
# #             )

# #             # Private events for same university
# #             private_event_ids = EventCreation.objects.filter(
# #                 privacy='Private',
# #                 admin__email__icontains=f'@{email_university}.edu'
# #             ).values_list('event_id', flat=True)
# #             private_events = Events.objects.filter(event_id__in=private_event_ids)

# #             # RSO events for RSOs the user is in
# #             user_rso_ids = StudentsRSOs.objects.filter(uid=user).values_list('rso_id', flat=True)
# #             rso_event_ids = RSOEvents.objects.filter(rso_id__in=user_rso_ids).values_list('event_id', flat=True)
# #             rso_events = Events.objects.filter(event_id__in=rso_event_ids)

# #             # Combine all events
# #             events = public_events | private_events | rso_events

# #         events = events.distinct()  # avoid duplicates
# #     else:
# #         # If the user is not authenticated, return an empty events list
# #         events = []

# #     return render(request, 'accounts/home.html', {'events': events})

# # def get_university_name_from_email(email):
# #     if '@' in email and '.edu' in email:
# #         domain = email.split('@')[1]
# #         return domain.split('.edu')[0]  # 'name' from abc@name.edu
# #     return None



# # def register(request):
# #     if request.method == 'POST':
# #         form = UserRegistrationForm(request.POST)
# #         if form.is_valid():
# #             user = form.save()  # Saves the user and hashes the password
# #             role = form.cleaned_data['role']
# #             if role == 'admin':
# #                 user.is_staff = True
# #             elif role == 'superadmin':
# #                 user.is_superuser = True
# #             user.save()  # Save changes to user
# #             login(request, user)  # Log the user in
# #             return redirect('home')  # Redirect to home page
# #     else:
# #         form = UserRegistrationForm()

# #     return render(request, 'accounts/register.html', {'form': form})


# # def login_view(request):
# #     if request.method == 'POST':
# #         form = AuthenticationForm(request, data=request.POST)
# #         if form.is_valid():
# #             # Get the cleaned data
# #             username = form.cleaned_data['username']
# #             password = form.cleaned_data['password']

# #             # Authenticate the user
# #             user = authenticate(request, username=username, password=password)

# #             if user is not None:
# #                 # Log the user in
# #                 login(request, user)
# #                 return redirect('home')  # Redirect to home or another page after login
# #             else:
# #                 # Invalid credentials
# #                 form.add_error(None, 'Invalid login credentials')
# #     else:
# #         form = AuthenticationForm()

# #     return render(request, 'accounts/login.html', {'form': form})


# # def create_event(request):
# #     if request.method == 'POST':
# #         event_form = EventForm(request.POST)
# #         privacy_form = EventPrivacyForm(request.POST)

# #         if event_form.is_valid() and privacy_form.is_valid():
# #             event = event_form.save(commit=False)
# #             privacy = privacy_form.cleaned_data['privacy']

# #             # For non-public events (Private or RSO), assign university
# #             if privacy != 'Public':
# #                 uni_name = get_university_name_from_email(request.user.email)
# #                 university = Universities.objects.filter(name__icontains=uni_name).first()
# #                 if not university:
# #                     event_form.add_error(None, "Could not find matching university for your email.")
# #                     return render(request, 'accounts/event_creation.html', {
# #                         'event_form': event_form,
# #                         'privacy_form': privacy_form
# #                     })
# #                 event.university = university
# #             else:
# #                 # Handle public events' university assignment
# #                 # You might need to assign a default university for public events
# #                 event.university = Universities.objects.first()  # or some default

# #             event.save()

# #             # Create EventCreation record
# #             creation = EventCreation.objects.create(
# #                 event=event,
# #                 admin=request.user,
# #                 superadmin=Users.objects.filter(role='SuperAdmin').first(),
# #                 privacy=privacy
# #             )

# #             # If it's a Private event with an RSO selected
# #             if privacy == 'Private' and privacy_form.cleaned_data.get('rso'):
# #                 RSOEvents.objects.create(
# #                     event=event,
# #                     rso=privacy_form.cleaned_data['rso']
# #                 )

# #             return redirect('home')
# #     else:
# #         event_form = EventForm()
# #         privacy_form = EventPrivacyForm()

# #     return render(request, 'accounts/event_creation.html', {
# #         'event_form': event_form,
# #         'privacy_form': privacy_form
# #     })

# # def add_comment(request, event_id):
# #     if not request.user.is_authenticated:
# #         return HttpResponse('')  # Blank response

# #     event = get_object_or_404(Events, event_id=event_id)

# #     if request.method == 'POST':
# #         content = request.POST.get('content')
# #         rating = request.POST.get('rating')

# #         if content and rating:
# #             Comments.objects.create(
# #                 uid=request.user,
# #                 event=event,
# #                 content=content,
# #                 rating=rating
# #             )
# #             messages.success(request, 'Your comment was added successfully!')
# #         else:
# #             messages.error(request, 'There was an error with your comment.')

# #     return redirect('home')


# # def edit_comment(request, comment_id):
# #     if not request.user.is_authenticated:
# #         return HttpResponse('')  # Blank response

# #     comment = get_object_or_404(Comments, comment_id=comment_id, uid=request.user)

# #     if request.method == 'POST':
# #         content = request.POST.get('content')
# #         rating = request.POST.get('rating')

# #         if content and rating:
# #             comment.content = content
# #             comment.rating = rating
# #             comment.save()
# #             messages.success(request, 'Your comment was updated successfully!')
# #             return redirect('home')
# #         else:
# #             messages.error(request, 'There was an error updating your comment.')

# #     # Simple form data for editing (you can customize this HTML or template later)
# #     return render(request, 'accounts/edit_comment.html', {
# #         'comment': comment
# #     })


# # def delete_comment(request, comment_id):
# #     if not request.user.is_authenticated:
# #         return HttpResponse('')  # Blank response

# #     comment = get_object_or_404(Comments, comment_id=comment_id, uid=request.user)

# #     if request.method == 'POST':
# #         comment.delete()
# #         messages.success(request, 'Your comment was deleted successfully!')

# #     return redirect('home')