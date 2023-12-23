# myapp/views.py

from urllib import request
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from config.choice import RoleUser
from config.permis import IsAuthenticated, IsPuskeswan
from manage_users.form.user_form import AccountUserForm, UserForm
from manage_users.models import AccountUser


class AccountUserListView(IsPuskeswan, ListView):
    model = AccountUser
    template_name = 'users/list.html'
    context_object_name = 'list_users'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'User'
        context['header_title'] = 'List User'
        context['btn_add'] = True
        context['create_url'] = reverse_lazy('user-create')
        return context

class AccountUserCreateView(IsPuskeswan, CreateView):
    model = AccountUser
    template_name = 'component/form.html'
    form_class = AccountUserForm
    success_url = reverse_lazy('user-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'User'
        context['header_title'] = 'Tambah User'
        return context

    def form_valid(self, form):
        return super().form_valid(form)

class AccountUserUpdateView(IsPuskeswan, UpdateView):
    model = AccountUser
    template_name = 'component/form.html'
    form_class = UserForm
    success_url = reverse_lazy('user-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'User'
        context['header_title'] = 'Edit User'
        return context

class AccountUserDeleteView(IsPuskeswan, DeleteView):
    model = AccountUser
    template_name = 'component/delete.html'
    success_url = reverse_lazy('user-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'User'
        context['header_title'] = 'Delete User'
        return context
