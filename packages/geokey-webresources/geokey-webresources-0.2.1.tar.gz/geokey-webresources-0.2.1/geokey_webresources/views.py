"""All views for the extension."""

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.views.generic import CreateView, FormView, TemplateView
from django.shortcuts import redirect
from django.db.models import BooleanField, Q, Case, When
from django.utils.safestring import mark_safe
from django.contrib import messages

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from braces.views import LoginRequiredMixin

from geokey.core.decorators import handle_exceptions_for_ajax
from geokey.projects.models import Project
from geokey.projects.views import ProjectContext

from .helpers.context_helpers import does_not_exist_msg
from .helpers.url_helpers import check_url
from .base import STATUS
from .exceptions import URLError
from .models import WebResource
from .forms import WebResourceForm
from .serializers import WebResourceSerializer


# ###########################
# ADMIN PAGES
# ###########################

class IndexPage(LoginRequiredMixin, TemplateView):
    """Main index page."""

    template_name = 'wr_index.html'

    def get_context_data(self, *args, **kwargs):
        """
        GET method for the template.

        Return the context to render the view. Overwrite the method by adding
        all projects (where user is an administrator) and available filters to
        the context. It optionally filters projects by the filter provided on
        the URL.

        Returns
        -------
        dict
            Context.
        """
        projects = Project.objects.filter(admins=self.request.user).annotate(
            with_webresources=Case(
                When(
                    ~Q(webresources__status='deleted') &
                    Q(webresources__isnull=False),
                    then=True
                ),
                default=False,
                output_field=BooleanField()
            )
        ).distinct()

        filters = {}
        filter_for_projects = self.request.GET.get('filter')

        filter_to_add = 'without-web-resources-only'
        if filter_for_projects == filter_to_add:
            projects = projects.filter(with_webresources=False)
        filters[filter_to_add] = 'Without web resources'

        filter_to_add = 'with-web-resources-only'
        if filter_for_projects == filter_to_add:
            projects = projects.filter(with_webresources=True)
        filters[filter_to_add] = 'With web resources'

        return super(IndexPage, self).get_context_data(
            projects=projects,
            filters=filters,
            *args,
            **kwargs
        )


class AllWebResourcesPage(LoginRequiredMixin, ProjectContext, TemplateView):
    """All web resources page."""

    template_name = 'wr_all_webresources.html'


class AddWebResourcePage(LoginRequiredMixin, ProjectContext, CreateView):
    """Add new web resource page."""

    template_name = 'wr_add_webresource.html'
    form_class = WebResourceForm

    def get_context_data(self, *args, **kwargs):
        """
        GET method for the template.

        Return the context to render the view. Overwrite the method by adding
        project ID to the context.

        Returns
        -------
        dict
            Context.
        """
        project_id = self.kwargs['project_id']

        return super(AddWebResourcePage, self).get_context_data(
            project_id,
            *args,
            **kwargs
        )

    def form_valid(self, form):
        """
        Add web resource when form data is valid.

        Parameters
        ----------
        form : geokey_webresource.forms.WebResourceForm
            Represents the user input.

        Returns
        -------
        django.http.HttpResponse
            Rendered template.
        """
        context = self.get_context_data(form=form)
        project = context.get('project')

        if project:
            if project.islocked:
                messages.error(
                    self.request,
                    'The project is locked. New web resources cannot be added.'
                )
            else:
                form.instance.project = project
                form.instance.creator = self.request.user

                try:
                    form.instance.dataformat = check_url(form.instance.url)

                    add_another_url = reverse(
                        'geokey_webresources:webresource_add',
                        kwargs={
                            'project_id': project.id
                        }
                    )
                    messages.success(
                        self.request,
                        mark_safe(
                            'The web resource has been added. <a href="%s">'
                            'Add another web resource.</a>' % add_another_url
                        )
                    )
                    return super(AddWebResourcePage, self).form_valid(form)
                except URLError, error:
                    messages.error(self.request, error.to_html())

        return self.render_to_response(context)

    def form_invalid(self, form):
        """
        Display an error message when form data is invalid.

        Parameters
        ----------
        form : geokey_webresource.forms.WebResourceForm
            Represents the user input.

        Returns
        -------
        dict
            Context.
        """
        messages.error(self.request, 'An error occurred.')
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        """
        Set URL redirection when web resource created successfully.

        Returns
        -------
        str
            URL for redirection.
        """
        return reverse(
            'geokey_webresources:all_webresources',
            kwargs={
                'project_id': self.kwargs['project_id']
            }
        )


class WebResourceContext(LoginRequiredMixin, ProjectContext):
    """Get web resource mixin."""

    def get_context_data(self, project_id, webresource_id, *args, **kwargs):
        """
        GET method for the template.

        Return the context to render the view. Overwrite the method by adding
        a web resource and available status types to the context.

        Parameters
        ----------
        project_id : int
            Identifies the project in the database.
        webresource_id : int
            Identifies the web resource in the database.

        Returns
        -------
        dict
            Context.
        """
        context = super(WebResourceContext, self).get_context_data(
            project_id,
            *args,
            **kwargs
        )

        context['status_types'] = STATUS

        try:
            context['webresource'] = WebResource.objects.get(
                pk=webresource_id,
                project=context.get('project')
            )

            return context
        except WebResource.DoesNotExist:
            return {
                'error': 'Not found.',
                'error_description': does_not_exist_msg('Web resource')
            }


class SingleWebResourcePage(WebResourceContext, FormView):
    """Single web resource page."""

    template_name = 'wr_single_webresource.html'

    def get_object(self):
        """
        Get and return web resource object.

        Returns
        -------
        geokey_webresource.models.WebResource
            Web resource object.
        """
        try:
            return WebResource.objects.get(
                pk=self.kwargs['webresource_id']
            )
        except WebResource.DoesNotExist:
            return None

    def get_context_data(self, *args, **kwargs):
        """
        GET method for the template.

        Return the context to render the view. Overwrite the method by adding
        project ID and web resource ID to the context.

        Returns
        -------
        dict
            Context.
        """
        project_id = self.kwargs['project_id']
        webresource_id = self.kwargs['webresource_id']

        return super(SingleWebResourcePage, self).get_context_data(
            project_id,
            webresource_id,
            *args,
            **kwargs
        )

    def get_form(self, form_class=WebResourceForm):
        """Attach instance object to form data."""
        return form_class(instance=self.get_object(), **self.get_form_kwargs())

    def form_valid(self, form):
        """
        Update web resource when form data is valid.

        Parameters
        ----------
        form : geokey_webresource.forms.WebResourceForm
            Represents the user input.

        Returns
        -------
        django.http.HttpResponse
            Rendered template.
        """
        context = self.get_context_data(form=form)
        project = context.get('project')

        if project:
            if project.islocked:
                messages.error(
                    self.request,
                    'The project is locked. Web resources cannot be updated.'
                )
            else:
                try:
                    form.instance.dataformat = check_url(form.instance.url)

                    if self.request.POST.get('symbol_clear') == 'true':
                        form.instance.symbol = None
                    form.save()

                    messages.success(
                        self.request,
                        mark_safe('The web resource has been updated.')
                    )
                    return super(SingleWebResourcePage, self).form_valid(form)
                except URLError, error:
                    messages.error(self.request, error.to_html())

        return self.render_to_response(context)

    def form_invalid(self, form):
        """
        Display an error message when form data is invalid.

        Parameters
        ----------
        form : geokey_webresource.forms.WebResourceForm
            Represents the user input.

        Returns
        -------
        dict
            Context.
        """
        messages.error(self.request, 'An error occurred.')
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        """
        Set URL redirection when web resource updated successfully.

        Returns
        -------
        str
            URL for redirection.
        """
        return reverse(
            'geokey_webresources:all_webresources',
            kwargs={
                'project_id': self.kwargs['project_id']
            }
        )


class RemoveWebResourcePage(WebResourceContext, TemplateView):
    """Remove web resource page."""

    template_name = 'base.html'

    def get(self, request, project_id, webresource_id):
        """
        GET method for removing web resource.

        Parameters
        ----------
        request : django.http.HttpRequest
            Object representing the request.
        project_id : int
            Identifies the project in the database.
        webresource_id : int
            Identifies the web resource in the database.

        Returns
        -------
        django.http.HttpResponseRedirect
            Redirects to all web resources if web resource is removed, single
            web resource page if project is locked.
        django.http.HttpResponse
            Rendered template if project or web resource does not exist.
        """
        context = self.get_context_data(project_id, webresource_id)
        webresource = context.get('webresource')

        if webresource:
            if webresource.project.islocked:
                messages.error(
                    request,
                    'The project is locked. Web resource cannot be removed.'
                )
                return redirect(
                    'geokey_webresources:single_webresource',
                    project_id=project_id,
                    webresource_id=webresource_id
                )
            else:
                webresource.delete()
                messages.success(
                    request,
                    'The web resource has been removed.'
                )
                return redirect(
                    'geokey_webresources:all_webresources',
                    project_id=project_id
                )

        return self.render_to_response(context)


# ###########################
# ADMIN AJAX
# ###########################

class ReorderWebResourcesAjax(APIView):
    """Reorder web resources via Ajax."""

    @handle_exceptions_for_ajax
    def post(self, request, project_id):
        """
        POST method for reordering web resources.

        Parameters
        ----------
        request : rest_framework.request.Request
            Object representing the request.
        project_id : int
            Identifies the project in the database.

        Returns
        -------
        rest_framework.response.Response
            Response to the request.
        """
        project = Project.objects.as_admin(request.user, project_id)

        if project.islocked:
            return Response(
                {'error': 'Project is locked.'},
                status=status.HTTP_403_FORBIDDEN
            )
        elif not project.webresources.exists():
            return Response(
                {'error': 'Project has no web resources.'},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            webresources = []

            for order, webresource_id in enumerate(request.data.get('order')):
                webresource = project.webresources.get(pk=webresource_id)
                webresource.order = order
                webresources.append(webresource)

            for webresource in webresources:
                webresource.save()

            serializer = WebResourceSerializer(
                project.webresources,
                many=True
            )
            return Response(serializer.data)
        except WebResource.DoesNotExist:
            return Response(
                {'error': 'One or more web resources were not found.'},
                status=status.HTTP_400_BAD_REQUEST
            )


class UpdateWebResourceAjax(APIView):
    """Update web resource via Ajax."""

    @handle_exceptions_for_ajax
    def put(self, request, project_id, webresource_id):
        """
        PUT method for updating web resource.

        Parameters
        ----------
        request : rest_framework.request.Request
            Object representing the request.
        project_id : int
            Identifies the project in the database.
        webresource_id : int
            Identifies the web resource in the database.

        Returns
        -------
        rest_framework.response.Response
            Response to the request.
        """
        project = Project.objects.as_admin(request.user, project_id)

        if project.islocked:
            return Response(
                {'error': 'Project is locked.'},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            webresource = project.webresources.get(pk=webresource_id)
            serializer = WebResourceSerializer(
                webresource,
                data=request.data,
                partial=True,
                fields=('id', 'status')
            )

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
        except WebResource.DoesNotExist, error:
            return Response(
                {'error': str(error)},
                status=status.HTTP_404_NOT_FOUND
            )


# ###########################
# PUBLIC API
# ###########################

class AllWebResourcesAPI(APIView):
    """All web resources via API."""

    @handle_exceptions_for_ajax
    def get(self, request, project_id):
        """
        GET method for all web resources of a project.

        Parameters
        ----------
        request : rest_framework.request.Request
            Object representing the request.
        project_id : int
            Identifies the project in the database.

        Returns
        -------
        rest_framework.response.Response
            Response to the request.
        """
        project = Project.objects.get_single(request.user, project_id)
        serializer = WebResourceSerializer(
            project.webresources.filter(status=STATUS.active),
            many=True
        )
        return Response(serializer.data)


class SingleWebResourceAPI(APIView):
    """Single web resource via API."""

    @handle_exceptions_for_ajax
    def get(self, request, project_id, webresource_id):
        """
        GET method for a single web resource of a project.

        Only active web resources are returned to anyone who has access to the
        project.

        Parameters
        ----------
        request : rest_framework.request.Request
            Object representing the request.
        project_id : int
            Identifies the project in the database.
        webresource_id : int
            Identifies the web resource in the database.

        Returns
        -------
        rest_framework.response.Response
            Response to the request.
        """
        project = Project.objects.get_single(request.user, project_id)

        try:
            webresource = project.webresources.get(
                pk=webresource_id,
                status=STATUS.active
            )
            serializer = WebResourceSerializer(webresource)
            return Response(serializer.data)
        except WebResource.DoesNotExist:
            return Response(
                {'error': 'Web resource not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
