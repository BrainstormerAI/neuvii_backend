from django.contrib.admin import AdminSite
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.template.response import TemplateResponse
from django.contrib import messages
from datetime import datetime

class NeuviiAdminSite(AdminSite):
    """
    Custom admin site for Neuvii with role-based access control
    """
    site_header = "Neuvii Therapy Management System"
    site_title = "Neuvii Admin Portal"
    index_title = "Administration Dashboard"

    def get_app_list(self, request, app_label=None):
        """
        Customize the admin index page app list based on user role
        """
        app_list = super().get_app_list(request, app_label)

        if not request.user.is_authenticated or not request.user.role:
            return app_list

        role_name = request.user.role.name.lower()

        # Restructure app list based on role
        if role_name == 'neuvii admin':
            return self.get_neuvii_admin_apps(app_list, request)
        elif role_name == 'clinic admin':
            return self.get_clinic_admin_apps(app_list, request)
        elif role_name == 'therapist':
            return self.get_therapist_apps(app_list, request)
        elif role_name == 'parent':
            return self.get_client_apps(app_list, request)

        return app_list

    def get_neuvii_admin_apps(self, app_list, request):
        """Full access for Neuvii Admin with properly structured sidebar"""
        custom_apps = []

        # Clinic Management Section
        clinic_models = []
        for app in app_list:
            if app['app_label'] == 'clinic':
                for model in app['models']:
                    if model['object_name'] == 'Clinic':
                        model['perms'] = {
                            'add': True,
                            'change': True,
                            'delete': True,
                            'view': True
                        }
                        model['name'] = 'Clinics'
                        clinic_models.append(model)

        if clinic_models:
            custom_apps.append({
                'name': 'Clinic Management',
                'app_label': 'clinic_management',
                'app_url': reverse('admin:app_list', kwargs={'app_label': 'clinic'}),
                'has_module_perms': True,
                'models': clinic_models
            })

        # Therapy Management Section
        therapy_models = []
        for app in app_list:
            if app['app_label'] == 'therapy':
                for model in app['models']:
                    if model['object_name'] == 'TherapistProfile':
                        model['perms'] = {
                            'add': True,
                            'change': True,
                            'delete': True,
                            'view': True
                        }
                        model['name'] = 'Therapies'
                        therapy_models.append(model)

        if therapy_models:
            custom_apps.append({
                'name': 'Therapy Management',
                'app_label': 'therapy_management',
                'app_url': reverse('admin:app_list', kwargs={'app_label': 'therapy'}),
                'has_module_perms': True,
                'models': therapy_models
            })

        # Client Management Section
        client_models = []
        for app in app_list:
            if app['app_label'] == 'therapy':
                for model in app['models']:
                    if model['object_name'] == 'ParentProfile':
                        model['perms'] = {
                            'add': True,
                            'change': True,
                            'delete': True,
                            'view': True
                        }
                        model['name'] = 'Clients'
                        client_models.append(model)

        if client_models:
            custom_apps.append({
                'name': 'Client Management',
                'app_label': 'client_management',
                'app_url': reverse('admin:app_list', kwargs={'app_label': 'therapy'}),
                'has_module_perms': True,
                'models': client_models
            })

        # Child Management Section
        child_models = []
        for app in app_list:
            if app['app_label'] == 'therapy':
                for model in app['models']:
                    if model['object_name'] == 'Child':
                        model['perms'] = {
                            'add': True,
                            'change': True,
                            'delete': True,
                            'view': True
                        }
                        model['name'] = 'Children'
                        child_models.append(model)

        if child_models:
            custom_apps.append({
                'name': 'Child Management',
                'app_label': 'child_management',
                'app_url': reverse('admin:app_list', kwargs={'app_label': 'therapy'}),
                'has_module_perms': True,
                'models': child_models
            })

        # Assignment Management Section
        assignment_models = []
        for app in app_list:
            if app['app_label'] == 'therapy':
                for model in app['models']:
                    if model['object_name'] == 'Assignment':
                        model['perms'] = {
                            'add': True,
                            'change': True,
                            'delete': True,
                            'view': True
                        }
                        model['name'] = 'Assignments'
                        assignment_models.append(model)

        if assignment_models:
            custom_apps.append({
                'name': 'Assignment Management',
                'app_label': 'assignment_management',
                'app_url': reverse('admin:app_list', kwargs={'app_label': 'therapy'}),
                'has_module_perms': True,
                'models': assignment_models
            })

        # Goal Management Section
        goal_models = []
        for app in app_list:
            if app['app_label'] == 'therapy':
                for model in app['models']:
                    if model['object_name'] == 'Goal':
                        model['perms'] = {
                            'add': True,
                            'change': True,
                            'delete': True,
                            'view': True
                        }
                        model['name'] = 'Goals'
                        goal_models.append(model)

        if goal_models:
            custom_apps.append({
                'name': 'Goal Management',
                'app_label': 'goal_management',
                'app_url': reverse('admin:app_list', kwargs={'app_label': 'therapy'}),
                'has_module_perms': True,
                'models': goal_models
            })

        # Task Management Section
        task_models = []
        for app in app_list:
            if app['app_label'] == 'therapy':
                for model in app['models']:
                    if model['object_name'] == 'Task':
                        model['perms'] = {
                            'add': True,
                            'change': True,
                            'delete': True,
                            'view': True
                        }
                        model['name'] = 'Tasks'
                        task_models.append(model)

        if task_models:
            custom_apps.append({
                'name': 'Task Management',
                'app_label': 'task_management',
                'app_url': reverse('admin:app_list', kwargs={'app_label': 'therapy'}),
                'has_module_perms': True,
                'models': task_models
            })

        return [app for app in custom_apps if app.get('models')]

    def get_clinic_admin_apps(self, app_list, request):
        """Restricted access for Clinic Admin - NO Assignment, Goal, or Task sections"""
        allowed_apps = []

        # Clinic Management Section
        clinic_models = []
        for app in app_list:
            if app['app_label'] == 'clinic':
                for model in app['models']:
                    if model['object_name'] == 'Clinic':
                        clinic_model = model.copy()
                        clinic_model['perms'] = {
                            'add': False,
                            'change': True,
                            'delete': False,
                            'view': True
                        }
                        clinic_model['name'] = 'My Clinics'
                        clinic_models.append(clinic_model)

        if clinic_models:
            allowed_apps.append({
                'name': 'Clinic Management',
                'app_label': 'clinic_management',
                'app_url': reverse('admin:app_list', kwargs={'app_label': 'clinic'}),
                'has_module_perms': True,
                'models': clinic_models
            })

        # Therapy Management Section
        therapy_models = []
        for app in app_list:
            if app['app_label'] == 'therapy':
                for model in app['models']:
                    if model['object_name'] == 'TherapistProfile':
                        therapy_model = model.copy()
                        therapy_model['perms'] = {
                            'add': True,
                            'change': True,
                            'delete': False,
                            'view': True
                        }
                        therapy_model['name'] = 'Therapies'
                        therapy_models.append(therapy_model)

        if therapy_models:
            allowed_apps.append({
                'name': 'Therapy Management',
                'app_label': 'therapy_management',
                'app_url': reverse('admin:app_list', kwargs={'app_label': 'therapy'}),
                'has_module_perms': True,
                'models': therapy_models
            })

        # Client Management Section
        client_models = []
        for app in app_list:
            if app['app_label'] == 'therapy':
                for model in app['models']:
                    if model['object_name'] == 'ParentProfile':
                        client_model = model.copy()
                        client_model['perms'] = {
                            'add': True,
                            'change': True,
                            'delete': False,
                            'view': True
                        }
                        client_model['name'] = 'Clients'
                        client_models.append(client_model)

        if client_models:
            allowed_apps.append({
                'name': 'Client Management',
                'app_label': 'client_management',
                'app_url': reverse('admin:app_list', kwargs={'app_label': 'therapy'}),
                'has_module_perms': True,
                'models': client_models
            })

        # Child Management Section
        child_models = []
        for app in app_list:
            if app['app_label'] == 'therapy':
                for model in app['models']:
                    if model['object_name'] == 'Child':
                        child_model = model.copy()
                        child_model['perms'] = {
                            'add': True,
                            'change': True,
                            'delete': False,
                            'view': True
                        }
                        child_model['name'] = 'Children'
                        child_models.append(child_model)

        if child_models:
            allowed_apps.append({
                'name': 'Child Management',
                'app_label': 'child_management',
                'app_url': reverse('admin:app_list', kwargs={'app_label': 'therapy'}),
                'has_module_perms': True,
                'models': child_models
            })

        return allowed_apps

    def get_therapist_apps(self, app_list, request):
        """Restricted access for Therapists - Profile and assigned children management"""
        allowed_apps = []

        # Profile Information Section
        profile_models = []
        for app in app_list:
            if app['app_label'] == 'therapy':
                for model in app['models']:
                    if model['object_name'] == 'TherapistProfile':
                        profile_model = model.copy()
                        profile_model['perms'] = {
                            'add': False,
                            'change': True,
                            'delete': False,
                            'view': True
                        }
                        profile_model['name'] = 'My Profile'
                        profile_models.append(profile_model)

        if profile_models:
            allowed_apps.append({
                'name': 'Profile Information',
                'app_label': 'profile_info',
                'app_url': reverse('admin:app_list', kwargs={'app_label': 'therapy'}),
                'has_module_perms': True,
                'models': profile_models
            })

        # Child Management Section
        child_models = []
        for app in app_list:
            if app['app_label'] == 'therapy':
                for model in app['models']:
                    if model['object_name'] == 'Child':
                        child_model = model.copy()
                        child_model['perms'] = {
                            'add': False,
                            'change': True,
                            'delete': False,
                            'view': True
                        }
                        child_model['name'] = 'My Children'
                        child_models.append(child_model)

        if child_models:
            allowed_apps.append({
                'name': 'Child Management',
                'app_label': 'child_management',
                'app_url': reverse('admin:app_list', kwargs={'app_label': 'therapy'}),
                'has_module_perms': True,
                'models': child_models
            })

        # Assignment Management Section
        assignment_models = []
        for app in app_list:
            if app['app_label'] == 'therapy':
                for model in app['models']:
                    if model['object_name'] == 'Assignment':
                        assignment_model = model.copy()
                        assignment_model['perms'] = {
                            'add': True,
                            'change': True,
                            'delete': False,
                            'view': True
                        }
                        assignment_model['name'] = 'My Assignments'
                        assignment_models.append(assignment_model)

        if assignment_models:
            allowed_apps.append({
                'name': 'Assignment Management',
                'app_label': 'assignment_management',
                'app_url': reverse('admin:app_list', kwargs={'app_label': 'therapy'}),
                'has_module_perms': True,
                'models': assignment_models
            })

        # Goal Management Section
        goal_models = []
        for app in app_list:
            if app['app_label'] == 'therapy':
                for model in app['models']:
                    if model['object_name'] == 'Goal':
                        goal_model = model.copy()
                        goal_model['perms'] = {
                            'add': True,
                            'change': True,
                            'delete': False,
                            'view': True
                        }
                        goal_model['name'] = 'My Goals'
                        goal_models.append(goal_model)

        if goal_models:
            allowed_apps.append({
                'name': 'Goal Management',
                'app_label': 'goal_management',
                'app_url': reverse('admin:app_list', kwargs={'app_label': 'therapy'}),
                'has_module_perms': True,
                'models': goal_models
            })

        # Task Management Section
        task_models = []
        for app in app_list:
            if app['app_label'] == 'therapy':
                for model in app['models']:
                    if model['object_name'] == 'Task':
                        task_model = model.copy()
                        task_model['perms'] = {
                            'add': True,
                            'change': True,
                            'delete': False,
                            'view': True
                        }
                        task_model['name'] = 'My Tasks'
                        task_models.append(task_model)

        if task_models:
            allowed_apps.append({
                'name': 'Task Management',
                'app_label': 'task_management',
                'app_url': reverse('admin:app_list', kwargs={'app_label': 'therapy'}),
                'has_module_perms': True,
                'models': task_models
            })

        return allowed_apps

    def get_client_apps(self, app_list, request):
        """Restricted access for Clients/Parents - Profile and children view-only"""
        allowed_apps = []

        # Profile Information Section
        profile_models = []
        for app in app_list:
            if app['app_label'] == 'therapy':
                for model in app['models']:
                    if model['object_name'] == 'ParentProfile':
                        profile_model = model.copy()
                        profile_model['perms'] = {
                            'add': False,
                            'change': True,
                            'delete': False,
                            'view': True
                        }
                        profile_model['name'] = 'My Profile'
                        profile_models.append(profile_model)

        if profile_models:
            allowed_apps.append({
                'name': 'Profile Information',
                'app_label': 'profile_info',
                'app_url': reverse('admin:app_list', kwargs={'app_label': 'therapy'}),
                'has_module_perms': True,
                'models': profile_models
            })

        # Child Management Section
        child_models = []
        for app in app_list:
            if app['app_label'] == 'therapy':
                for model in app['models']:
                    if model['object_name'] == 'Child':
                        child_model = model.copy()
                        child_model['perms'] = {
                            'add': False,
                            'change': False,
                            'delete': False,
                            'view': True
                        }
                        child_model['name'] = 'My Children'
                        child_models.append(child_model)

        if child_models:
            allowed_apps.append({
                'name': 'Child Management',
                'app_label': 'child_management',
                'app_url': reverse('admin:app_list', kwargs={'app_label': 'therapy'}),
                'has_module_perms': True,
                'models': child_models
            })

        # Goal Management Section (View-only)
        goal_models = []
        for app in app_list:
            if app['app_label'] == 'therapy':
                for model in app['models']:
                    if model['object_name'] == 'Goal':
                        goal_model = model.copy()
                        goal_model['perms'] = {
                            'add': False,
                            'change': False,
                            'delete': False,
                            'view': True
                        }
                        goal_model['name'] = 'Children Goals'
                        goal_models.append(goal_model)

        if goal_models:
            allowed_apps.append({
                'name': 'Goal Management',
                'app_label': 'goal_management',
                'app_url': reverse('admin:app_list', kwargs={'app_label': 'therapy'}),
                'has_module_perms': True,
                'models': goal_models
            })

        # Task Management Section (View-only)
        task_models = []
        for app in app_list:
            if app['app_label'] == 'therapy':
                for model in app['models']:
                    if model['object_name'] == 'Task':
                        task_model = model.copy()
                        task_model['perms'] = {
                            'add': False,
                            'change': False,
                            'delete': False,
                            'view': True
                        }
                        task_model['name'] = 'Children Tasks'
                        task_models.append(task_model)

        if task_models:
            allowed_apps.append({
                'name': 'Task Management',
                'app_label': 'task_management',
                'app_url': reverse('admin:app_list', kwargs={'app_label': 'therapy'}),
                'has_module_perms': True,
                'models': task_models
            })

        # Assignment Management Section (View-only)
        assignment_models = []
        for app in app_list:
            if app['app_label'] == 'therapy':
                for model in app['models']:
                    if model['object_name'] == 'Assignment':
                        assignment_model = model.copy()
                        assignment_model['perms'] = {
                            'add': False,
                            'change': False,
                            'delete': False,
                            'view': True
                        }
                        assignment_model['name'] = 'Children Assignments'
                        assignment_models.append(assignment_model)

        if assignment_models:
            allowed_apps.append({
                'name': 'Assignment Management',
                'app_label': 'assignment_management',
                'app_url': reverse('admin:app_list', kwargs={'app_label': 'therapy'}),
                'has_module_perms': True,
                'models': assignment_models
            })

        return allowed_apps

    def index(self, request, extra_context=None):
        """Customize the admin index page"""
        if not request.user.is_authenticated:
            return self.login(request)

        context = {
            'title': self.index_title,
            'subtitle': None,
            'current_time': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC'),
        }

        if request.user.role:
            role_name = request.user.role.name
            context.update({
                'user_role': role_name,
                'subtitle': f"{role_name} Dashboard",
            })

            if role_name == 'Neuvii Admin':
                from clinic.models import Clinic
                from therapy.models import TherapistProfile, ParentProfile, Child
                context.update({
                    'total_clinics': Clinic.objects.count(),
                    'active_clinics': Clinic.objects.filter(is_active=True).count(),
                    'total_therapists': TherapistProfile.objects.count(),
                    'total_clients': ParentProfile.objects.count(),
                    'total_children': Child.objects.count(),
                })
            elif role_name == 'Clinic Admin':
                if hasattr(request.user, 'clinic_admin'):
                    clinic = request.user.clinic_admin
                    from therapy.models import TherapistProfile, ParentProfile, Child
                    context.update({
                        'clinic_name': clinic.name,
                        'clinic_therapists': TherapistProfile.objects.filter(clinic=clinic).count(),
                        'clinic_children': Child.objects.filter(clinic=clinic).count(),
                    })

        if extra_context:
            context.update(extra_context)

        return super().index(request, context)

# Create the custom admin site instance
neuvii_admin_site = NeuviiAdminSite(name='neuvii_admin')

# Register your models with the custom admin site
from clinic.admin import ClinicAdmin
from clinic.models import Clinic
from users.admin import CustomUserAdmin, RoleAdmin, GroupAdmin
from users.models import User, Role
from django.contrib.auth.models import Group
from therapy.admin import TherapistProfileAdmin, ParentProfileAdmin, ChildAdmin, AssignmentAdmin, GoalAdmin, TaskAdmin
from therapy.models import TherapistProfile, ParentProfile, Child, Assignment, Goal, Task

# Register models
neuvii_admin_site.register(User, CustomUserAdmin)
neuvii_admin_site.register(Role, RoleAdmin)
neuvii_admin_site.register(Group, GroupAdmin)
neuvii_admin_site.register(Clinic, ClinicAdmin)
neuvii_admin_site.register(TherapistProfile, TherapistProfileAdmin)
neuvii_admin_site.register(ParentProfile, ParentProfileAdmin)
neuvii_admin_site.register(Child, ChildAdmin)
neuvii_admin_site.register(Assignment, AssignmentAdmin)
neuvii_admin_site.register(Goal, GoalAdmin)
neuvii_admin_site.register(Task, TaskAdmin)