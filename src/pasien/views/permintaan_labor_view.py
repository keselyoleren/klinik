# myapp/views.py

from gc import get_objects
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.utils.timezone import localtime
from datetime import datetime
from config.documents import GoogleDocumentProvider

from config.permis import IsAuthenticated, IsAuthenticated
from config.report import GeneratePDF
from pasien.form.labor_form import PermintaanLaborForm

from pasien.models import  Pasien, PermintaanLabor

class PermintaanLaborListView(IsAuthenticated, ListView):
    model = PermintaanLabor
    template_name = 'labor/permintaan/list.html'
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
        context['create_url'] = reverse_lazy('permintaan-labor-create', kwargs={'pasien_id': self.kwargs['pasien_id']})
        return context


class PermintaanLaborCreateView(IsAuthenticated, CreateView):
    model = PermintaanLabor
    template_name = 'labor/permintaan/form.html'
    form_class = PermintaanLaborForm
    success_url = reverse_lazy('permintaan-labor-list')

    def get_success_url(self) -> str:
        return reverse_lazy('permintaan-labor-list', kwargs={'pasien_id': self.kwargs['pasien_id']})

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

class PermintaanLaborUpdateView(IsAuthenticated, UpdateView):
    model = PermintaanLabor
    template_name = 'labor/permintaan/form.html'
    form_class = PermintaanLaborForm


    def get_success_url(self) -> str:
        return reverse_lazy('permintaan-labor-list', kwargs={'pasien_id': self.get_object().pasien.id})

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


class PermintaanLaborDeleteView(IsAuthenticated, DeleteView):
    model = PermintaanLabor
    template_name = 'component/delete.html'
    
    def get_success_url(self) -> str:
        return reverse_lazy('permintaan-labor-list', kwargs={'pasien_id': self.get_object().pasien.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Permintaan Laboratorium'
        context['header_title'] = 'Delete Permintaan Laboratorium'
        return context


class DownloadPermintaanLabor(IsAuthenticated, GeneratePDF, DetailView):
    model = PermintaanLabor
    template_name = 'labor/permintaan/download.html'
    context_object_name = 'hasil_labor'
    form_class = PermintaanLaborForm

    
    def get(self, request, *args, **kwargs):
        # document_id = '1q7V1wYTGRjr6PnCLFssaQaIH2h9baIwDguXgj9q5Wv8'
        # document_id = '1K3l0UYGrSh4G_xpPW3hlqtW6xqvJlTZ8pawtr0pLuts'
        document_id = '1K3l0UYGrSh4G_xpPW3hlqtW6xqvJlTZ8pawtr0pLuts'
        created_at_local = localtime(self.get_object().created_at)
        print(self.get_object())
        params = {            
            'created_at': created_at_local, #created_at_local.strftime('%d %B %Y')
            'hb': "[ √ ]" if self.get_object().hemoglobin else "[  ]",
            'led': "[ √ ]" if self.get_object().led else "[  ]",
            'leu': "[ √ ]" if self.get_object().leukosit else "[  ]",
            'dif': "[ √ ]" if self.get_object().diff else "[  ]",
            'bas': "[ √ ]" if self.get_object().bas else "[  ]",
            'eos': "[ √ ]" if self.get_object().eos else "[  ]",
            'stb': "[ √ ]" if self.get_object().stb else "[  ]",
            'seg': "[ √ ]" if self.get_object().seg else "[  ]",
            'lim': "[ √ ]" if self.get_object().lim else "[  ]",
            'mon': "[ √ ]" if self.get_object().mon else "[  ]",
            'trom': "[ √ ]" if self.get_object().trombosit else "[  ]",
            'erit': "[ √ ]" if self.get_object().eritrosit else "[  ]",
            'hemat': "[ √ ]" if self.get_object().hematokrit else "[  ]",
            'gol-d': "[ √ ]" if self.get_object().golongan_darah else "[  ]",
            'clot-t': "[ √ ]" if self.get_object().clotting_time else "[  ]",
            'bled-t': "[ √ ]" if self.get_object().bleeding_time else "[  ]",
            'mcv': "[ √ ]" if self.get_object().mcv else "[  ]",
            'mch': "[ √ ]" if self.get_object().mch else "[  ]",
            'mchc': "[ √ ]" if self.get_object().mchc else "[  ]",
            'prf-dab': "[ √ ]" if self.get_object().profil_diabetik else "[  ]",
            'gd_p': "[ √ ]" if self.get_object().gd_puasa else "[  ]",
            'gd2': "[ √ ]" if self.get_object().gd_2_j_pp else "[  ]",
            'gd_sew': "[ √ ]" if self.get_object().gd_sewaktu else "[  ]",
            'hba': "[ √ ]" if self.get_object().hba1c else "[  ]",
            'koles': "[ √ ]" if self.get_object().kolesterol_total else "[  ]",
            'hdl-k': "[ √ ]" if self.get_object().hdl_kolesterol else "[  ]",
            'ldl-k': "[ √ ]" if self.get_object().ldl_kolesterol else "[  ]",
            'trig': "[ √ ]" if self.get_object().trigliserida else "[  ]",
            'bil-ttl': "[ √ ]" if self.get_object().bilirubin_total else "[  ]",
            'bil-drk': "[ √ ]" if self.get_object().bilirubin_direk else "[  ]",
            'bil-idrk': "[ √ ]" if self.get_object().bilirubin_indirek else "[  ]",
            'sgot': "[ √ ]" if self.get_object().sgot else "[  ]",
            'sgpt': "[ √ ]" if self.get_object().sgpt else "[  ]",
            'alk-ph': "[ √ ]" if self.get_object().alkasi_phospatashe else "[  ]",
            'asm-u': "[ √ ]" if self.get_object().asam_urat else "[  ]",
            'urm': "[ √ ]" if self.get_object().ureum else "[  ]",
            'crtn': "[ √ ]" if self.get_object().creatinin else "[  ]",
            'bun': "[ √ ]" if self.get_object().bun else "[  ]",
            'alb': "[ √ ]" if self.get_object().albumin else "[  ]",
            'ttl-p': "[ √ ]" if self.get_object().total_protein else "[  ]",
            'glb': "[ √ ]" if self.get_object().globulin else "[  ]",
            'ck-mb': "[ √ ]" if self.get_object().ck_mb else "[  ]",
            # napza
            'npz-c': "[ √ ]" if self.get_object().napza_cocaine else "[  ]",
            'npz-m': "[ √ ]" if self.get_object().napza_metamphetamine else "[  ]",
            'npz-ca': "[ √ ]" if self.get_object().napza_cannabis else "[  ]",
            'npz-o': "[ √ ]" if self.get_object().napza_o_morphine else "[  ]",
            
            # ELEKTROLIT\
            'e-c': "[ √ ]" if self.get_object().elektrolit_cocaine else "[  ]",
            'e-m': "[ √ ]" if self.get_object().elektrolit_metamphetamine else "[  ]",
            'e-ca': "[ √ ]" if self.get_object().elektrolit_cannabis else "[  ]",
            'e-o': "[ √ ]" if self.get_object().elektrolit_o_morphine else "[  ]",

            # ELEKTROLIT
            'e-c': "[ √ ]" if self.get_object().elektrolit_cocaine else "[  ]",
            'e-m': "[ √ ]" if self.get_object().elektrolit_metamphetamine else "[  ]",
            'ec-2': "[ √ ]" if self.get_object().elektrolit_cannabis else "[  ]",
            'e-o-m': "[ √ ]" if self.get_object().elektrolit_o_morphine else "[  ]",

            # wdal
            's-': "[ √ ]" if self.get_object().s_typhosa else "[  ]",
            's-a': "[ √ ]" if self.get_object().s_typhosa_a else "[  ]",
            's-b': "[ √ ]" if self.get_object().s_typhosa_b else "[  ]",
            's-c': "[ √ ]" if self.get_object().s_typhosa_c else "[  ]",

            # urin rutiin
            'wrna': "[ √ ]" if self.get_object().warna_urin else "[  ]",
            'kkrhn': "[ √ ]" if self.get_object().kekeruhan else "[  ]",
            'ph': "[ √ ]" if self.get_object().keasaman_ph else "[  ]",
            'bj': "[ √ ]" if self.get_object().berat_jenis else "[  ]",
            'kton': "[ √ ]" if self.get_object().keton else "[  ]",
            'd-r': "[ √ ]" if self.get_object().darah_rutin else "[  ]",
            'ntrit': "[ √ ]" if self.get_object().nitrit else "[  ]",
            'k-u': "[ √ ]" if self.get_object().kimiawi_urin else "[  ]",
            'p-a': "[ √ ]" if self.get_object().protein_albumin else "[  ]",
            'g-r': "[ √ ]" if self.get_object().glukosa_reduksi else "[  ]",
            'blbrn': "[ √ ]" if self.get_object().bilirubin else "[  ]",
            'urlbn': "[ √ ]" if self.get_object().urobilin else "[  ]",
            'm-r': "[ √ ]" if self.get_object().mikroskopis_urin else "[  ]",
            'leu': "[ √ ]" if self.get_object().leukosit else "[  ]",
            'erit': "[ √ ]" if self.get_object().eritrosit else "[  ]",
            'ephi': "[ √ ]" if self.get_object().ephitel else "[  ]",
            'krstl': "[ √ ]" if self.get_object().kristal else "[  ]",
            'slndr': "[ √ ]" if self.get_object().silinder else "[  ]",
            'lln-urn': "[ √ ]" if self.get_object().lain_lain_urin_rutin else "[  ]",

            # faces
            'm-f': "[ √ ]" if self.get_object().makroskopis_faces else "[  ]",
            'k-s': "[ √ ]" if self.get_object().konsistensi else "[  ]",
            'w-f': "[ √ ]" if self.get_object().warna_faces else "[  ]",
            'bau': "[ √ ]" if self.get_object().bau else "[  ]",
            'nnh': "[ √ ]" if self.get_object().nanah else "[  ]",
            'd-f': "[ √ ]" if self.get_object().darah_faces else "[  ]",
            'k-f': "[ √ ]" if self.get_object().kimiawi_faces else "[  ]",
            'b-t': "[ √ ]" if self.get_object().benzidine_test else "[  ]",
            'm-f': "[ √ ]" if self.get_object().mikroskopis_faces else "[  ]",
            't-c': "[ √ ]" if self.get_object().telur_cacing else "[  ]",
            's-d': "[ √ ]" if self.get_object().sel_darah else "[  ]",
            'amb': "[ √ ]" if self.get_object().amoeba else "[  ]",
            'lln-f': "[ √ ]" if self.get_object().lain_lain_faces else "[  ]",
            
            # sputum
            's-b-c': "[ √ ]" if self.get_object().sputum_bta_ct else "[  ]",

            # mikrobiologi_parasitologi
            'mlra': "[ √ ]" if self.get_object().malaria else "[  ]",

            # serologi
            'pp-t': "[ √ ]" if self.get_object().pp_test else "[  ]",
            'c-r-t': "[ √ ]" if self.get_object().cek_rapid_test else "[  ]",
            'c-a': "[ √ ]" if self.get_object().cek_antigen else "[  ]",
            'hcv': "[ √ ]" if self.get_object().hcv else "[  ]",
            'h-a': "[ √ ]" if self.get_object().hbs_ag else "[  ]",
            'hiv': "[ √ ]" if self.get_object().hiv_aids else "[  ]",
            'ast': "[ √ ]" if self.get_object().asto else "[  ]",
            'd-t': "[ √ ]" if self.get_object().dhf_test else "[  ]",
            'a-mt': "[ √ ]" if self.get_object().anti_malaria_ict_test else "[  ]",
            'a-di': "[ √ ]" if self.get_object().anti_dengue_igm else "[  ]",
            'a-dg': "[ √ ]" if self.get_object().anti_dengue_igg else "[  ]",
            'n-d': "[ √ ]" if self.get_object().ns1ag_dengue else "[  ]",
            'a-s-i': "[ √ ]" if self.get_object().anti_syphilis_igg_igm else "[  ]",
            'i-m-a': "[ √ ]" if self.get_object().igg_m_anti_salmonella_typhi_tubex else "[  ]",

            'catatan':self.get_object().catatan,
            'ket_faces':self.get_object().ket_lain_lain_faces,
            'ket_urin':self.get_object().ket_lain_lain_urinte,
            'krm_tgl':localtime(self.get_object().kirim_tanggal),
            'ruangan':self.get_object().ruangan,
            'phone':self.get_object().phone,
            'ket_klinis':self.get_object().ket_klinis,
            'diterima_at':self.get_object().spes_lab_diterima,
            'leukosit_hematologi':self.get_object().leukosit_hematologi,

            # pasien
            'no_rm':self.get_object().pasien.no_rm,
            'nama':self.get_object().pasien.full_name,
            'tgl_lahir':self.get_object().pasien.tanggal_lahir, 
            'jnis_kelamin':self.get_object().pasien.jenis_kelamin,
            'alamat':self.get_object().pasien.alamat,
            

        }
        file_name = f'FORMULIR PERMINTAAN PEMERIKSAAN LABORATORIUM - {self.get_object().pasien} ({datetime.now()})'
        document = GoogleDocumentProvider(document_id, params, file_name=file_name)
        proses_document = document.process_document()
        return document.download_google_docs_as_pdf(proses_document)
        # return self.render_to_pdf(
        #     {
        #         'title':'FORMULIR PERMINTAAN PEMERIKSAAN LABORATORIUM',
        #         'form':self.form_class(instance=self.get_object()),
        #         'pasien':self.get_object().pasien,
        #         'host' : f"{self.request.scheme}://{self.request.META['HTTP_HOST']}"
        #     },
        #     self.template_name,
        #     '/css/pdf.css',
        #     f'Permintaan Laboratorium Pasien {self.get_object().pasien.full_name}'
        # )

