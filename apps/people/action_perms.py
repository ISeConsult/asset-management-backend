from django.contrib.auth.models import Group, Permission
from rest_framework.permissions import SAFE_METHODS, BasePermission
from django.core.exceptions import PermissionDenied
from django.contrib.contenttypes.models import ContentType
from django.contrib import auth

permission_map = {
    "GET": "view_{model_class}",
    "POST": "add_{model_class}",
    "PUT": "change_{model_class}",
    "PATCH": "change_{model_class}",
    "DELETE": "delete_{model_class}",
    "OPTIONS": "view_{model_class}",
}

OPERATIONAL_MODELS = [
    "add_logentry",
    "change_logentry",
    "delete_logentry",
    "view_logentry",
    "add_permission",
    "change_permission",
    "delete_permission",
    "view_permission",
    "add_contenttype",
    "change_contenttype",
    "delete_contenttype",
    "view_contenttype",
    "add_session",
    "change_session",
    "delete_session",
    "view_session",
    "add_requestevent",
    "change_requestevent",
    "delete_requestevent",
    "add_loginevent",
    "change_loginevent",
    "delete_loginevent" "add_crudevent",
    "change_crudevent",
    "delete_crudevent",
    "add_accessattempt",
    "change_accessattempt",
    "delete_accessattempt",
    "view_accessattempt",
    "add_accesslog",
    "change_accesslog",
    "delete_accesslog",
    "view_accesslog",
    "add_accessfailurelog",
    "change_accessfailurelog",
    "delete_accessfailurelog",
    "view_accessfailurelog",
    "add_taskresult",
    "change_taskresult",
    "delete_taskresult",
    "view_taskresult",
    "add_chordcounter",
    "change_chordcounter",
    "delete_chordcounter",
    "view_chordcounter",
    "add_groupresult",
    "change_groupresult",
    "delete_groupresult",
    "view_groupresult",
    "add_crontabschedule",
    "change_crontabschedule",
    "delete_crontabschedule",
    "view_crontabschedule",
    "add_intervalschedule",
    "change_intervalschedule",
    "delete_intervalschedule",
    "view_intervalschedule",
    "add_periodictask",
    "change_periodictask",
    "delete_periodictask",
    "view_periodictask",
    "add_periodictasks",
    "change_periodictasks",
    "delete_periodictasks",
    "view_periodictasks",
    "add_solarschedule",
    "change_solarschedule",
    "delete_solarschedule",
    "view_solarschedule",
    "add_clockedschedule",
    "change_clockedschedule",
    "delete_clockedschedule",
    "view_clockedschedule",
    "add_loginpage",
    "change_loginpage",
    "delete_loginpage",
    "view_loginpage",
]


SUPERUSER_MODELS = [
    "add_organization",
    "change_organization",
    "delete_organization",
    "add_sector",
    "change_sector",
    "delete_sector",
    "view_sector",
    "add_license",
    "delete_license",
    "add_licensetype",
    "change_licensetype",
    "delete_licensetype",
    "view_licensetype",
    "add_licensehistory",
    "change_licensehistory",
    "delete_licensehistory",
    "view_licensehistory",
    "delete_organizationaddressinfo",
    "add_appsetting",
    "delete_appsetting",
]

ADMIN_GROUP_MODELS = [
    "view_organization",
    "change_organizationaddressinfo",
    "add_organizationaddressinfo",
    "view_organizationaddressinfo",
    "change_license",
    "view_license",
    "add_group",
    "change_group",
    "delete_group",
    "add_user",
    "change_user",
    "delete_user",
    "add_userposition",
    "change_userposition",
    "delete_userposition",
    "view_userposition",
    "add_hierarchy",
    "change_hierarchy",
    "delete_hierarchy",
    "add_riskstatus",
    "change_riskstatus",
    "delete_riskstatus",
    "add_keyriskcategory",
    "change_keyriskcategory",
    "delete_keyriskcategory",
    "add_impact",
    "change_impact",
    "delete_impact",
    "add_likelihood",
    "change_likelihood",
    "delete_likelihood",
    "add_impactcategory",
    "change_impactcategory",
    "delete_impactcategory",
    "add_executeproceduresetting",
    "change_executeproceduresetting",
    "delete_executeproceduresetting",
    "add_incidentsetting",
    "change_incidentsetting",
    "delete_incidentsetting",
    "add_issuesetting",
    "change_issuesetting",
    "delete_issuesetting",
    "add_narrativesetting",
    "change_narrativesetting",
    "delete_narrativesetting",
    "add_notificationsetting",
    "change_notificationsetting",
    "delete_notificationsetting",
    "add_planningsetting",
    "change_planningsetting",
    "delete_planningsetting",
    "add_projectsetting",
    "change_projectsetting",
    "delete_projectsetting",
    "add_projecttype",
    "change_projecttype",
    "delete_projecttype",
    "add_walkthroughsetting",
    "change_walkthroughsetting",
    "delete_walkthroughsetting",
    "add_testplansetting",
    "change_testplansetting",
    "delete_testplansetting",
    "add_testingsetting",
    "change_testingsetting",
    "delete_testingsetting",
    "add_sectionsetting",
    "change_sectionsetting",
    "delete_sectionsetting",
    "add_riskproceduresetting",
    "change_riskproceduresetting",
    "delete_riskproceduresetting",
    "add_riskcontrolsetting",
    "change_riskcontrolsetting",
    "delete_riskcontrolsetting",
    "add_resultsetting",
    "change_resultsetting",
    "delete_resultsetting",
    "add_requestsetting",
    "change_requestsetting",
    "delete_requestsetting",
    "add_projecttypesettingsoption",
    "change_projecttypesettingsoption",
    "delete_projecttypesettingsoption",
    "add_signofftype",
    "change_signofftype",
    "delete_signofftype",
    "view_signofftype",
    "add_appoption",
    "change_appoption",
    "delete_appoption",
    "change_appsetting",
    "view_loginevent",
    "view_requestevent",
    "view_crudevent",
]

#
OTHERS = []

EXCLUDE_FOR_NON_ADMINS = OPERATIONAL_MODELS + SUPERUSER_MODELS + ADMIN_GROUP_MODELS
EXCLUDE_FOR_LICENSE = (
    OPERATIONAL_MODELS + SUPERUSER_MODELS + ADMIN_GROUP_MODELS + OTHERS
)


class AMSPermissions(BasePermission):
    """
    A base class from which all permission classes should inherit.
    """

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        user = request.user
        try:
            class_name = view.get_queryset().model.__name__
        except:
            try:
                class_name = str(view.__class__.queryset.model.__name__)
            except:
                class_name = None

        if user and class_name:
            if user.is_superuser and user.is_authenticated:
                return True

        return False

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        user = request.user
        try:
            class_name = view.get_queryset().model.__name__
        except:
            try:
                class_name = str(view.__class__.queryset.model.__name__)
            except:
                class_name = None

        if user and class_name != None:
            if user.is_superuser and user.is_authenticated:
                return True

            elif (
                user.is_authenticated
                and user.user_profile.organization.org_license.filter(status=True)
            ):
                return user.get_all_permissions(
                    permission_map[request.method].format(
                        model_class=str(class_name).lower()
                    )
                )
        return False


class AMSAuthenticatedPermissions(BasePermission):
    """
    A base class from which all permission classes should inherit.
    """

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        user = request.user

        if user:
            if user.is_superuser and user.is_authenticated:
                return True

            elif (
                user.is_authenticated
                and user.user_profile.organization.org_license.filter(status=True)
            ):
                return True

        return False

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        user = request.user

        if user:
            if user.is_superuser and user.is_authenticated:
                return True
        return False


class ReadOnlyPermission(BasePermission):
    # If the request method is in the SAFE_METHODS list, then return True. Otherwise, return False
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return request.method in SAFE_METHODS
