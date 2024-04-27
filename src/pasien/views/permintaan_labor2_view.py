# myapp/views.py

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from config.permis import IsAuthenticated, IsAuthenticated
from config.report import GeneratePDF
from pasien.form.labor_form import PermintaanLabor2Form
from django.utils.timezone import localtime
from datetime import datetime
from config.documents import GoogleDocumentProvider
from pasien.models import  Pasien, PermintaanLabor2

class PermintaanLabor2ListView(IsAuthenticated, ListView):
    model = PermintaanLabor2
    template_name = 'labor/permintaan2/list.html'
    context_object_name = 'permintaan_labor_list'

    def get_pasien(self):
        return Pasien.objects.get(pk=self.kwargs['pasien_id'])
        
    
    def get_queryset(self):
        try:
            return super().get_queryset().filter(pasien=self.get_pasien())
        except Exception:
            return super().get_queryset()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Permintaan Laboratorium'
        context['header_title'] = 'Permintaan Laboratorium'
        context['btn_add'] = True
        context['pasien'] = self.get_pasien()
        context['create_url'] = reverse_lazy('permintaan-labor2-create', kwargs={'pasien_id': self.kwargs['pasien_id']})
        return context


class PermintaanLabor2CreateView(IsAuthenticated, CreateView):
    model = PermintaanLabor2
    template_name = 'labor/permintaan2/form.html'
    form_class = PermintaanLabor2Form
    success_url = reverse_lazy('permintaan-labor2-list')

    def get_success_url(self) -> str:
        return reverse_lazy('permintaan-labor2-list', kwargs={'pasien_id': self.kwargs['pasien_id']})

    def get_pasien(self):
        return Pasien.objects.get(pk=self.kwargs['pasien_id'])
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Permintaan Laboratorium'
        context['header_title'] = 'Permintaan Laboratorium'
        context['pasien'] = self.get_pasien()
        return context

    def form_valid(self, form):
        form.instance.pasien = self.get_pasien()
        form.save()
        return super().form_valid(form)

class PermintaanLabor2UpdateView(IsAuthenticated, UpdateView):
    model = PermintaanLabor2
    template_name = 'labor/permintaan2/form.html'
    form_class = PermintaanLabor2Form


    def get_success_url(self) -> str:
        return reverse_lazy('permintaan-labor2-list', kwargs={'pasien_id': self.get_object().pasien.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Permintaan Laboratorium'
        context['header_title'] = 'Edit Permintaan Laboratorium'
        context['pasien'] = self.get_object().pasien
        return context

    def form_valid(self, form):
        form.instance.pasien = self.get_object().pasien
        form.save()
        return super().form_valid(form)


class PermintaanLabor2DeleteView(IsAuthenticated, DeleteView):
    model = PermintaanLabor2
    template_name = 'component/delete.html'
    
    def get_success_url(self) -> str:
        return reverse_lazy('permintaan-labor2-list', kwargs={'pasien_id': self.get_object().pasien.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Permintaan Laboratorium'
        context['header_title'] = 'Delete Permintaan Laboratorium'
        return context


class DownloadPermintaanLabor2(IsAuthenticated, GeneratePDF, DetailView):
    model = PermintaanLabor2
    form_class = PermintaanLabor2Form
    template_name = 'labor/permintaan2/download.html'
    context_object_name = 'hasil_labor'


    
    def get(self, request, *args, **kwargs):
        document_id = '1tlu__vGuLD3uvw6I961tMkS-0OJuM5IdEiXEL9BsYqQ'
        created_at_local = localtime(self.get_object().created_at)
        file_name = f'FORMULIR PERMINTAAN PEMERIKSAAN LABORATORIUM - {self.get_object().pasien} ({datetime.now()})'
        params = {
            'created_at':created_at_local,
            'no_rm':self.get_object().pasien.no_rm,
            'nama':self.get_object().pasien.full_name,
            'tgl_lahir':self.get_object().pasien.tanggal_lahir, 
            'jnis_kelamin':self.get_object().pasien.jenis_kelamin,
            'alamat':self.get_object().pasien.alamat,
            'jenis_kelamin':self.get_object().pasien.jenis_kelamin,
            'no_rm':self.get_object().pasien.no_rm,


            'led':self.get_object().led,
            'hemo':self.get_object().hemoglobin,
            'leu':self.get_object().leukosit_hematologi,

            'bas':self.get_object().bas,
            'eos':self.get_object().eos,
            'stb':self.get_object().stb,
            'seg':self.get_object().seg,
            'lim':self.get_object().lim,
            'mon':self.get_object().mon,

            'trom':self.get_object().trombosit,
            'erit_hem':self.get_object().eritrosit_hematlogi,
            'hematokrit':self.get_object().hematokrit,
            'gol_darah':self.get_object().golongan_darah,
            'c_time':self.get_object().clotting_time,
            'b_time':self.get_object().bleeding_time,
            'mcv':self.get_object().mcv,
            'mch':self.get_object().mch,
            'mchc':self.get_object().mchc,

            'gd_p':self.get_object().gd_puasa,
            'gd_2_j':self.get_object().gd_2_j_pp,
            'gd_s':self.get_object().gd_sewaktu,
            'hba':self.get_object().hba1c,

            'kol_total':self.get_object().kolesterol_total,
            'hdl':self.get_object().hdl_kolesterol,
            'ldl':self.get_object().ldl_kolesterol,
            'trig':self.get_object().trigliserida,
            'bill_total':self.get_object().bilirubin_total,
            'bill_direk':self.get_object().bilirubin_direk,
            'bill_indirek':self.get_object().bilirubin_indirek,
            'sgot':self.get_object().sgot,
            'sgpt':self.get_object().sgpt,
            'alkasi_p':self.get_object().alkasi_phospatashe,
            'asam_urat':self.get_object().asam_urat,
            'ureum':self.get_object().ureum,
            'creatinin':self.get_object().creatinin,
            'bun':self.get_object().bun,
            'albumin':self.get_object().albumin,
            'total_pro':self.get_object().total_protein,
            'globulin':self.get_object().globulin,
            'ck_mb':self.get_object().ck_mb,

            # napaza
            'n_cocaine':self.get_object().napza_cocaine,
            'n_met':self.get_object().napza_metamphetamine,
            'n_can':self.get_object().napza_cannabis,
            'n_o':self.get_object().napza_o_morphine,

            # elektrolit
            'k':self.get_object().k,
            'na':self.get_object().na,
            'ci':self.get_object().ci,
            'ca':self.get_object().ca,
            'ph':self.get_object().ph,

            # wdal
            's_t':self.get_object().s_typhosa,
            's_ta':self.get_object().s_typhosa_a,
            's_tb':self.get_object().s_typhosa_b,
            's_tc':self.get_object().s_typhosa_c,

            # urine rutin
            'warna':self.get_object().warna_urin,
            'kekeruhan':self.get_object().kekeruhan,
            'k_ph':self.get_object().keasaman_ph,
            'bj':self.get_object().berat_jenis,
            'keton':self.get_object().keton,
            'darah_rutin':self.get_object().darah_rutin,
            'nitrit':self.get_object().nitrit,
            'p_al':self.get_object().protein_albumin,
            'glu_r':self.get_object().glukosa_reduksi,
            'bili':self.get_object().bilirubin,
            'urobil':self.get_object().urobilin,

            'leukosit_x':self.get_object().leukosit,
            'eritrosit_x':self.get_object().eritrosit,
            'ephitel_x':self.get_object().ephitel,
            'kristal_x':self.get_object().kristal,
            'silinder_x':self.get_object().silinder,
            'll_r':self.get_object().lain_lain_urin_rutin,

            # faces
            'konsistensi':self.get_object().konsistensi,
            'warna_f':self.get_object().warna_faces,
            'bau':self.get_object().bau,
            'nanah':self.get_object().nanah,
            'darah_f':self.get_object().darah_faces,
            'b_t':self.get_object().benzidine_test,
            't_c':self.get_object().telur_cacing,
            's_d':self.get_object().sel_darah,
            'amoeba':self.get_object().amoeba,
            'll_f':self.get_object().lain_lain_faces,
            's_b_c':self.get_object().sputum_bta_ct,
            'malaria':self.get_object().malaria,

            # serologi
            'pp_t':self.get_object().pp_test,
            'c_r_t':self.get_object().cek_rapid_test,
            'c_antigen':self.get_object().cek_antigen,
            'hcv':self.get_object().hcv,
            'hbs_ag':self.get_object().hbs_ag,
            'anti_hbs':self.get_object().anti_hbs,
            'hiv_aids':self.get_object().hiv_aids,
            'asto':self.get_object().asto,
            'dhf_test':self.get_object().dhf_test,
            'anti_malaria':self.get_object().anti_malaria_ict_test,
            'anti_igm':self.get_object().anti_dengue_igm,
            'anti_igg':self.get_object().anti_dengue_igg,
            'anti_sy':self.get_object().anti_syphilis_igg_igm,
            'igg_m':self.get_object().igg_m_anti_salmonella_typhi_tubex,
            'pemeriksa':self.get_object().pemeriksa,
            
        }
        document = GoogleDocumentProvider(document_id, params, file_name)
        proses_document = document.process_document()
        return document.download_google_docs_as_pdf(proses_document)
        # return self.render_to_pdf(
        #     {
        #         'title':'FORMULIR PERMINTAAN PEMERIKSAAN LABORATORIUM',
        #         'pasien':self.get_object().pasien,
        #         'created_at':self.get_object().created_at,
        #         'pemeriksa':self.get_object().pemeriksa,
        #         'form':self.form_class(instance=self.get_object()),
        #         'host' : f"{self.request.scheme}://{self.request.META['HTTP_HOST']}"
        #     },
        #     self.template_name,
        #     '/css/pdf.css',
        #     f'Permintaan Laboratorium Pasien {self.get_object().pasien.full_name}'
        # )

