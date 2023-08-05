# -*- coding: utf-8 -*-

# This file is part of wger Workout Manager.
#
# wger Workout Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# wger Workout Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License

import logging

from django.core.urlresolvers import reverse
from django.http.response import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy, ugettext as _
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    ListView)

from wger.utils.generic_views import (
    WgerFormMixin,
    WgerDeleteMixin,
    WgerPermissionMixin
)
from wger.gym.models import ContractOption, Gym

logger = logging.getLogger(__name__)


class AddView(WgerFormMixin, CreateView):
    '''
    View to add a new contract option
    '''

    model = ContractOption
    fields = ('name', 'description')
    title = ugettext_lazy('Add option')
    permission_required = 'gym.add_contractoption'
    member = None

    def get_success_url(self):
        '''
        Redirect back to overview page
        '''
        return reverse('gym:contract-option:list', kwargs={'gym_pk': self.object.gym_id})

    def dispatch(self, request, *args, **kwargs):
        '''
        Can only add contract types in own gym
        '''
        if not request.user.is_authenticated():
            return HttpResponseForbidden()

        if request.user.userprofile.gym_id != int(self.kwargs['gym_pk']):
            return HttpResponseForbidden()

        return super(AddView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        '''
        Set the foreign key to the gym object
        '''
        form.instance.gym_id = self.kwargs['gym_pk']
        return super(AddView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        '''
        Send some additional data to the template
        '''
        context = super(AddView, self).get_context_data(**kwargs)
        context['form_action'] = reverse('gym:contract-option:add',
                                         kwargs={'gym_pk': self.kwargs['gym_pk']})
        return context


class UpdateView(WgerFormMixin, UpdateView):
    '''
    View to update an existing contract option
    '''

    model = ContractOption
    fields = ('name', 'description')
    permission_required = 'gym.change_contractoption'
    form_action_urlname = 'gym:contract-option:edit'

    def dispatch(self, request, *args, **kwargs):
        '''
        Can only add contract types in own gym
        '''
        if not request.user.is_authenticated():
            return HttpResponseForbidden()

        contract_type = self.get_object()
        if request.user.userprofile.gym_id != contract_type.gym_id:
            return HttpResponseForbidden()

        return super(UpdateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        '''
        Redirect back to overview page
        '''
        return reverse('gym:contract-option:list', kwargs={'gym_pk': self.object.gym_id})

    def get_context_data(self, **kwargs):
        '''
        Send some additional data to the template
        '''
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['title'] = _(u'Edit {0}').format(self.object)
        return context


class DeleteView(WgerDeleteMixin, DeleteView, WgerPermissionMixin):
    '''
    View to delete an existing contract option
    '''

    model = ContractOption
    permission_required = 'gym.delete_contractoption'
    form_action_urlname = 'gym:contract-option:delete'

    def dispatch(self, request, *args, **kwargs):
        '''
        Can only add contract option in own gym
        '''
        if not request.user.is_authenticated():
            return HttpResponseForbidden()

        contract_type = self.get_object()
        if request.user.userprofile.gym_id != contract_type.gym_id:
            return HttpResponseForbidden()

        return super(DeleteView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        '''
        Redirect back to overview page
        '''
        return reverse('gym:contract-option:list', kwargs={'gym_pk': self.object.gym_id})

    def get_context_data(self, **kwargs):
        '''
        Send some additional data to the template
        '''
        context = super(DeleteView, self).get_context_data(**kwargs)
        context['title'] = _(u'Delete {0}').format(self.object)
        return context


class ListView(WgerPermissionMixin, ListView):
    '''
    Overview of all available contract options
    '''
    model = ContractOption
    permission_required = 'gym.add_contractoption'
    template_name = 'contract_option/list.html'
    gym = None

    def get_queryset(self):
        '''
        Only documents for current user
        '''
        return ContractOption.objects.filter(gym=self.gym)

    def dispatch(self, request, *args, **kwargs):
        '''
        Can only list contract types in own gym
        '''
        if not request.user.is_authenticated():
            return HttpResponseForbidden()

        self.gym = get_object_or_404(Gym, id=self.kwargs['gym_pk'])
        if request.user.userprofile.gym_id != self.gym.id:
            return HttpResponseForbidden()

        return super(ListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        '''
        Send some additional data to the template
        '''
        context = super(ListView, self).get_context_data(**kwargs)
        context['gym'] = self.gym
        return context
