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
        """Full access for Neuvii Admin with separate sections"""
        custom_apps = []

        # 1. Clinic Management Section
        custom_apps.append({
            'name': 'Clinic Management',
            'app_label': 'clinic_management',
            'app_url': reverse('admin:app_list', kwargs={'app_label': 'clinic'}),
            'has_module_perms': True,
            'models': [{
                'name': 'Clinics',
                'object_name': 'Clinic',
                'perms': {'add': True, 'change': True, 'delete': True, 'view': True},
                'admin_url': reverse('admin:clinic_clinic_changelist'),
                'add_url': reverse('admin:clinic_clinic_add'),
            }]
        })

        # 2. Therapist Management Section
        custom_apps.append({
            'name': 'Therapist Management',
            'app_label': 'therapist_management',
            'app_url': reverse('admin:app_list', kwargs={'app_label': 'therapy'}),
            'has_module_perms': True,
            'models': [{
                'name': 'Therapists',
                'object_name': 'TherapistProfile',
                'perms': {'add': True, 'change': True, 'delete': True, 'view': True},
                'admin_url': reverse('admin:therapy_therapistprofile_changelist'),
                'add_url': reverse('admin:therapy_therapistprofile_add'),
            }]
        })

        # 3. Client Management Section
        custom_apps.append({
            'name': 'Client Management',
            'app_label': 'client_management',
            'app_url': reverse('admin:app_list', kwargs={'app_label': 'therapy'}),
            'has_module_perms': True,
            'models': [{
                'name': 'Clients',
                'object_name': 'ParentProfile',
                'perms': {'add': True, 'change': True, 'delete': True, 'view': True},
                'admin_url': reverse('admin:therapy_parentprofile_changelist'),
                'add_url': reverse('admin:therapy_parentprofile_add'),
            }]
        })

        # 4. Child Management Section
        custom_apps.append({
            'name': 'Child Management',
            'app_label': 'child_management',
            'app_url': reverse('admin:app_list', kwargs={'app_label': 'therapy'}),
            'has_module_perms': True,
            'models': [{
                'name': 'Children',
                'object_name': 'Child',
                'perms': {'add': True, 'change': True, 'delete': True, 'view': True},
                'admin_url': reverse('admin:therapy_child_changelist'),
                'add_url': reverse('admin:therapy_child_add'),
            }]
        })

        # 5. Assignment Management Section
        custom_apps.append({
            'name': 'Assignment Management',
            'app_label': 'assignment_management',
            'app_url': reverse('admin:app_list', kwargs={'app_label': 'therapy'}),
            'has_module_perms': True,
            'models': [{
                'name': 'Assignments',
                'object_name': 'Assignment',
                'perms': {'add': True, 'change': True, 'delete': True, 'view': True},
                'admin_url': reverse('admin:therapy_assignment_changelist'),
                'add_url': reverse('admin:therapy_assignment_add'),
            }]
        })

        # 6. Goal Management Section
        custom_apps.append({
            'name': 'Goal Management',
            'app_label': 'goal_management',
            'app_url': reverse('admin:app_list', kwargs={'app_label': 'therapy'}),
            'has_module_perms': True,
            'models': [{
                'name': 'Goals',
                'object_name': 'Goal',
                'perms': {'add': True, 'change': True, 'delete': True, 'view': True},
                'admin_url': reverse('admin:therapy_goal_changelist'),
                'add_url': reverse('admin:therapy_goal_add'),
            }]
        })

        # 7. Task Management Section
        custom_apps.append({
            'name': 'Task Management',
            'app_label': 'task_management',
            'app_url': reverse('admin:app_list', kwargs={'app_label': 'therapy'}),
            'has_module_perms': True,
            'models': [{
                'name': 'Tasks',
                'object_name': 'Task',
                'perms': {'add': True, 'change': True, 'delete': True, 'view': True},
                'admin_url': reverse('admin:therapy_task_changelist'),
                'add_url': reverse('admin:therapy_task_add'),
            }]
        })

        return custom_apps

    def get_clinic_admin_apps(self, app_list, request):
        """Restricted access for Clinic Admin - NO Assignment, Goal, or Task sections"""
        custom_apps = []

        # 1. Clinic Management Section
        custom_apps.append({
            'name': 'Clinic Management',
            'app_label': 'clinic_management',
            'app_url': reverse('admin:app_list', kwargs={'app_label': 'clinic'}),
            'has_module_perms': True,
            'models': [{
                'name': 'My Clinics',
                'object_name': 'Clinic',
                'perms': {'add': False, 'change': True, 'delete': False, 'view': True},
                'admin_url': reverse('admin:clinic_clinic_changelist'),
                'add_url': None,
            }]
        })

        # 2. Therapist Management Section
        custom_apps.append({
            'name': 'Therapist Management',
            'app_label': 'therapist_management',
            'app_url': reverse('admin:app_list', kwargs={'app_label': 'therapy'}),
            'has_module_perms': True,
            'models': [{
                'name': 'Therapists',
                'object_name': 'TherapistProfile',
                'perms': {'add': True, 'change': True, 'delete': False, 'view': True},
                'admin_url': reverse('admin:therapy_therapistprofile_changelist'),
                'add_url': reverse('admin:therapy_therapistprofile_add'),
            }]
        })

        # 3. Client Management Section
        custom_apps.append({
            'name': 'Client Management',
            'app_label': 'client_management',
            'app_url': reverse('admin:app_list', kwargs={'app_label': 'therapy'}),
            'has_module_perms': True,
            'models': [{
                'name': 'Clients',
                'object_name': 'ParentProfile',
                'perms': {'add': True, 'change': True, 'delete': False, 'view': True},
                'admin_url': reverse('admin:therapy_parentprofile_changelist'),
                'add_url': reverse('admin:therapy_parentprofile_add'),
            }]
        })

        # 4. Child Management Section
        custom_apps.append({
            'name': 'Child Management',
            'app_label': 'child_management',
            'app_url': reverse('admin:app_list', kwargs={'app_label': 'therapy'}),
            'has_module_perms': True,
            'models': [{
                'name': 'Children',
                'object_name': 'Child',
                'perms': {'add': True, 'change': True, 'delete': False, 'view': True},
                'admin_url': reverse('admin:therapy_child_changelist'),
                'add_url': reverse('admin:therapy_child_add'),
            }]
        })

        # NOTE: NO Assignment, Goal, or Task sections for Clinic Admin as requested

        return custom_apps

    def get_therapist_apps(self, app_list, request):
        """Restricted access for Therapists - Profile and assigned children management"""
        custom_apps = []

        # 1. Profile Information Section
        custom_apps.append({
            'name': 'Profile Information',
            'app_label': 'profile_info',
            'app_url': reverse('admin:app_list', kwargs={'app_label': 'therapy'}),
            'has_module_perms': True,
            'models': [{
                'name': 'My Profile',
                'object_name': 'TherapistProfile',
                'perms': {'add': False, 'change': True, 'delete': False, 'view': True},
                'admin_url': reverse('admin:therapy_therapistprofile_changelist'),
                'add_url': None,
            }]
        })

        # 2. Child Management Section
        custom_apps.append({
            'name': 'Child Management',
            'app_label': 'child_management',
            'app_url': reverse('admin:app_list', kwargs={'app_label': 'therapy'}),
            'has_module_perms': True,
            'models': [{
                'name': 'My Children',
                'object_name': 'Child',
                'perms': {'add': False, 'change': True, 'delete': False, 'view': True},
                'admin_url': reverse('admin:therapy_child_changelist'),
                'add_url': None,
            }]
        })

        # 3. Assignment Management Section
        custom_apps.append({
            'name': 'Assignment Management',
            'app_label': 'assignment_management',
            'app_url': reverse('admin:app_list', kwargs={'app_label': 'therapy'}),
            'has_module_perms': True,
            'models': [{
                'name': 'My Assignments',
                'object_name': 'Assignment',
                'perms': {'add': True, 'change': True, 'delete': False, 'view': True},
                'admin_url': reverse('admin:therapy_assignment_changelist'),
                'add_url': reverse('admin:therapy_assignment_add'),
            }]
        })

        # 4. Goal Management Section
        custom_apps.append({
            'name': 'Goal Management',
            'app_label': 'goal_management',
            'app_url': reverse('admin:app_list', kwargs={'app_label': 'therapy'}),
            'has_module_perms': True,
            'models': [{
                'name': 'My Goals',
                'object_name': 'Goal',
                'perms': {'add': True, 'change': True, 'delete': False, 'view': True},
                'admin_url': reverse('admin:therapy_goal_changelist'),
                'add_url': reverse('admin:therapy_goal_add'),
            }]
        })

        # 5. Task Management Section
        custom_apps.append({
            'name': 'Task Management',
            'app_label': 'task_management',
            'app_url': reverse('admin:app_list', kwargs={'app_label': 'therapy'}),
            'has_module_perms': True,
            'models': [{
                'name': 'My Tasks',
                'object_name': 'Task',
                'perms': {'add': True, 'change': True, 'delete': False, 'view': True},
                'admin_url': reverse('admin:therapy_task_changelist'),
                'add_url': reverse('admin:therapy_task_add'),
            }]
        })

        return custom_apps

    def get_client_apps(self, app_list, request):
        """Restricted access for Clients/Parents - Profile and children view-only"""
        custom_apps = []

        # 1. Profile Information Section
        custom_apps.append({
            'name': 'Profile Information',
            'app_label': 'profile_info',
            'app_url': reverse('admin:app_list', kwargs={'app_label': 'therapy'}),
            'has_module_perms': True,
            'models': [{
                'name': 'My Profile',
                'object_name': 'ParentProfile',
                'perms': {'add': False, 'change': True, 'delete': False, 'view': True},
                'admin_url': reverse('admin:therapy_parentprofile_changelist'),
                'add_url': None,
            }]
        })

        # 2. Child Management Section
        custom_apps.append({
            'name': 'Child Management',
            'app_label': 'child_management',
            'app_url': reverse('admin:app_list', kwargs={'app_label': 'therapy'}),
            'has_module_perms': True,
            'models': [{
                'name': 'My Children',
                'object_name': 'Child',
                'perms': {'add': False, 'change': False, 'delete': False, 'view': True},
                'admin_url': reverse('admin:therapy_child_changelist'),
                'add_url': None,
            }]
        })

        # 3. Goal Management Section (View-only)
        custom_apps.append({
            'name': 'Goal Management',
            'app_label': 'goal_management',
            'app_url': reverse('admin:app_list', kwargs={'app_label': 'therapy'}),
            'has_module_perms': True,
            'models': [{
                'name': 'Children Goals',
                'object_name': 'Goal',
                'perms': {'add': False, 'change': False, 'delete': False, 'view': True},
                'admin_url': reverse('admin:therapy_goal_changelist'),
                'add_url': None,
            }]
        })

        # 4. Task Management Section (View-only)
        custom_apps.append({
            'name': 'Task Management',
            'app_label': 'task_management',
            'app_url': reverse('admin:app_list', kwargs={'app_label': 'therapy'}),
            'has_module_perms': True,
            'models': [{
                'name': 'Children Tasks',
                'object_name': 'Task',
                'perms': {'add': False, 'change': False, 'delete': False, 'view': True},
                'admin_url': reverse('admin:therapy_task_changelist'),
                'add_url': None,
            }]
        })

        # 5. Assignment Management Section (View-only)
        custom_apps.append({
            'name': 'Assignment Management',
            'app_label': 'assignment_management',
            'app_url': reverse('admin:app_list', kwargs={'app_label': 'therapy'}),
            'has_module_perms': True,
            'models': [{
                'name': 'Children Assignments',
                'object_name': 'Assignment',
                'perms': {'add': False, 'change': False, 'delete': False, 'view': True},
                'admin_url': reverse('admin:therapy_assignment_changelist'),
                'add_url': None,
            }]
        })

        return custom_apps

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