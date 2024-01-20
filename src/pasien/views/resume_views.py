# myapp/views.py
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from config.permis import IsAuthenticated, IsAuthenticated
from config.report import GeneratePDF


from pasien.models import  Pasien, RawatInap, RawatJalan, Resume
from pasien.form.resume_form import ResumeForm

class ResumeListView(IsAuthenticated, ListView):
    model = Resume
    template_name = 'resume/list.html'
    context_object_name = 'list_resume'

    def get_pasien(self):
        try:
            title = 'Resume Perawatan Pasien Rawat Jalan'
            query_pasien =  RawatJalan.objects.get(pk=self.kwargs['pasien_id'])
            return title, query_pasien
        except Exception:
            title = 'Resume Perawatan Pasien Rawat Inap'
            query_pasien = RawatInap.objects.get(pk=self.kwargs['pasien_id'])
            return title , query_pasien
    
    def get_queryset(self):
        try:
            _, query_pasien = self.get_pasien()
            try:
                return super().get_queryset().filter(pasien_rawat_jalan=query_pasien)
            except Exception:
                return super().get_queryset().filter(pasien_rawat_inap=query_pasien)
        except Exception:
            return super().get_queryset()
    
    def get_context_data(self, **kwargs):
        title, query_pasien = self.get_pasien()
        context = super().get_context_data(**kwargs)
        context['header'] = title
        context['header_title'] = title
        context['btn_add'] = True
        context['pasien'] = query_pasien.pasien
        context['create_url'] = reverse_lazy('resume-create', kwargs={'pasien_id': self.kwargs['pasien_id']})
        context['download_url'] = reverse_lazy('resume-download', kwargs={'pasien_id': self.kwargs['pasien_id']})
        return context


class ResumeCreateView(IsAuthenticated, CreateView):
    model = Resume
    template_name = 'component/form.html'
    form_class = ResumeForm
    success_url = reverse_lazy('resume-list')

    def get_success_url(self) -> str:
        return reverse_lazy('resume-list', kwargs={'pasien_id': self.kwargs['pasien_id']})

    def get_pasien(self):
        try:
            title = 'Resume Perawatan Pasien Rawat Jalan'
            query_pasien = RawatJalan.objects.get(pk=self.kwargs['pasien_id'])
            return title, query_pasien
        except Exception:
            title = "Resume Perawatan Pasien Rawat Inap"
            query_pasien = RawatInap.objects.get(pk=self.kwargs['pasien_id'])
            return title, query_pasien

    def get_context_data(self, **kwargs):
        title, query_pasien = self.get_pasien()
        context = super().get_context_data(**kwargs)
        context['header'] = title
        context['header_title'] = title
        context['pasien'] = context['pasien'] = query_pasien.pasien
        return context

    def form_valid(self, form):
        title, query_pasien = self.get_pasien()
        try:
            form.instance.pasien_rawat_jalan = query_pasien
        except Exception:
            form.instance.pasien_rawat_inap = query_pasien
        form.save()
        return super().form_valid(form)

class ResumeUpdateView(IsAuthenticated, UpdateView):
    model = Resume
    template_name = 'component/form.html'
    form_class = ResumeForm


    def get_success_url(self) -> str:
        return reverse_lazy('resume-list', kwargs={'pasien_id': self.get_object().pasien_rawat_jalan.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Resume'
        context['header_title'] = 'Edit Resume'
        return context

    def form_valid(self, form):
        try:
            form.instance.pasien_rawat_jalan = self.get_object().pasien_rawat_jalan.id
        except Exception:
            form.instance.pasien_rawat_inap = self.get_object().pasien_rawat_inap.id
        form.save()
        return super().form_valid(form)


class ResumeDeleteView(IsAuthenticated, DeleteView):
    model = Resume
    template_name = 'component/delete.html'
    
    def get_success_url(self) -> str:
        return reverse_lazy('resume-list', kwargs={'pasien_id': self.get_object().pasien_rawat_jalan.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Resume'
        context['header_title'] = 'Delete Resume'
        return context


class DownloadResume(IsAuthenticated, GeneratePDF, ListView):
    model = Resume
    template_name = 'resume/download.html'
    context_object_name = 'list_resume'

    def get_pasien(self):
        try:
            title = 'Resume Perawatan Pasien Rawat Jalan'
            query_pasien =  RawatJalan.objects.get(pk=self.kwargs['pasien_id'])
            return title, query_pasien
        except Exception:
            title = 'Resume Perawatan Pasien Rawat Inap'
            query_pasien = RawatInap.objects.get(pk=self.kwargs['pasien_id'])
            return title , query_pasien
    
    def get_queryset(self):
        try:
            _, query_pasien = self.get_pasien()
            try:
                return super().get_queryset().filter(pasien_rawat_jalan=query_pasien)
            except Exception:
                return super().get_queryset().filter(pasien_rawat_inap=query_pasien)
        except Exception:
            return super().get_queryset()
    
    def get(self, request, *args, **kwargs):
        title, query_pasien = self.get_pasien()
        return self.render_to_pdf(
            {
                'list_resume': self.get_queryset(),
                'pasien':query_pasien,
                'title':title,
                'host' : f"{self.request.scheme}://{self.request.META['HTTP_HOST']}"
            },
            self.template_name,
            '/css/pdf.css',
            f'Resume Pasien {query_pasien.pasien.full_name}'
        )

