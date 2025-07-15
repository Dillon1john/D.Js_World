from django.shortcuts import render, redirect

from django.views.generic import TemplateView,  ListView, DetailView
from .models import *
from django.views import View
from django.contrib import messages
from .forms import ContactForm
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from datetime import datetime


# Create your views here.

def send_contact_email(name, email, subject, message):
    """
    Send contact form email to vendor with sender's information and message

    Args:
        name: String containing sender's full name
        email: String containing sender's email address
        subject: String containing email subject
        message: String containing the message content
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # Prepare context for email template
        email_context = {
            'name': name,
            'email': email,
            'subject': subject,
            'message': message,
            'timestamp': datetime.now()
        }

        # Render email templates
        email_subject = f'Contact Form Message: {subject}'
        html_message = render_to_string(
            'portfolio/email/contact_form_email.html',
            email_context
        )

        # Create plain text version
        plain_message = f"""
        New Contact Form Message

        From: {name}
        Email: {email}
        Subject: {subject}

        Message:
        {'=' * 50}
        {message}
        {'=' * 50}

        This message was sent via the website contact form on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """

        # Debug: Print the email settings
        print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
        print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
        
        # Send the email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.VENDOR_EMAIL, settings.DEVELOPER_EMAIL],
            html_message=html_message,
            fail_silently=False
        )

        return True

    except Exception as e:
        # Log the error (you might want to use proper logging here)
        print(f"Failed to send contact form email: {str(e)}")
        return False


class HomeView(TemplateView):
    template_name = 'Portfolio/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        return context


class ProjectListView(ListView):
    model = Project
    template_name = 'Portfolio/allProjects.html'
    ordering = ['title']
    context_object_name = 'projects'
    paginate_by = 6
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['languages'] = Language.objects.all()
        context['selected_category'] = self.request.GET.get('category', 'all')
        context['selected_language'] = self.request.GET.get('language', 'all')
        return context


class ProjectDetailView(DetailView):
    template_name = 'Portfolio/projectDetail.html'
    model = Project
    technologies = Project.technologies
    context_object_name = 'project'

    def split_and_sort(self, input_string):
        # Split the string by comma and strip whitespace
        split_list = [item.strip() for item in input_string.split(',')]
        # Return sorted list
        return sorted(split_list)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs['pk']
        technologies = Project.objects.get(pk=project_id).technologies
        languages = Project.objects.get(pk=project_id).programming_language.all()
        context['technologies'] = self.split_and_sort(technologies)
        context['languages'] = languages
        return context


class ContactView(View):
    def get(self, request):
        # Clear any existing messages
        storage = messages.get_messages(request)
        storage.used = True
        contact_form = ContactForm()
        return render(request, 'portfolio/contact.html', {'contact_form': contact_form})

    def post(self, request):
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            name = contact_form.cleaned_data['name']
            email = contact_form.cleaned_data['email']
            subject = contact_form.cleaned_data['subject']
            message = contact_form.cleaned_data['message']

            # Get current timestamp
            timestamp = timezone.now()

            # Clear any existing messages
            storage = messages.get_messages(request)
            storage.used = True

            # Send email
            if send_contact_email(name, email, subject, message):
                # Format the timestamp for display
                formatted_time = timestamp.strftime("%B %d, %Y at %I:%M %p")
                messages.success(
                    request,
                    f'Your message was sent successfully on {formatted_time}!'
                )
            else:
                messages.error(
                    request,
                    'Failed to send email. Please try again later.'
                )

            return redirect('contact')

        return render(request, 'portfolio/contact.html', {'contact_form': contact_form})