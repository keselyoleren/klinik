# myapp/views.py
from config.choice import KATEGORI_SKRINING, AsupanMakanTerakhir, CategoryNorton, GejalaChoice, Kesadaran, KondisiPasien, KondisiUmum, OnsetChoice, TypeNyeri, WaktuChoice, YesOrNo
from config.documents import GoogleDocumentProvider
from datetime import datetime
from django.utils.timezone import localtime

from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404


from django.contrib import messages
from config.permis import IsAuthenticated, IsAuthenticated
from config.report import GeneratePDF
from pasien.form.assesment_rawatinap import AssesmentRawatInapForm, PemerikasanPenunjangForm, RiwayatOperasiForm

from pasien.models import AssessmentRawatInap, PemerikasanPenunjang, RawatInap, RiwayatOperasi


class AssessmentRawatInapCreateView(IsAuthenticated, CreateView):
    model = AssessmentRawatInap
    template_name = 'rawat_inap/form_assesment.html'
    form_class = AssesmentRawatInapForm
    
    def get_pasien_fisioterapi(self):
        return get_object_or_404(RawatInap, pk=self.kwargs['pasien_id'])

    def get_success_url(self) -> str:
        return reverse_lazy('rawat_inap-update', kwargs={'pk': self.get_pasien_fisioterapi().id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Assesmen Pasien Rawat Inap'
        context['header_title'] = 'Assesmen Pasien Rawat Inap'
        context['pasien'] = RawatInap.objects.get(pk=self.kwargs['pasien_id']).pasien
        riwayat_operasi_formset = inlineformset_factory(AssessmentRawatInap, RiwayatOperasi, form=RiwayatOperasiForm, extra=1, can_delete=True)
        pemeriksaan_penunjang_formset = inlineformset_factory(AssessmentRawatInap, PemerikasanPenunjang, form=PemerikasanPenunjangForm, extra=1, can_delete=True)
        if self.request.POST:
            context['riwayat_operasi_formset'] = riwayat_operasi_formset(self.request.POST, self.request.FILES, instance=self.object)
            context['pemeriksaan_penunjang_formset'] = pemeriksaan_penunjang_formset(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['riwayat_operasi_formset'] = riwayat_operasi_formset()
            context['pemeriksaan_penunjang_formset'] = pemeriksaan_penunjang_formset()
        return context
    
    def form_valid(self, form):
        form.instance.pasien_rawat_inap = RawatInap.objects.get(pk=self.kwargs['pasien_id'])
        response = super().form_valid(form)
        riwayat_operasi_formset = inlineformset_factory(AssessmentRawatInap, RiwayatOperasi, form=RiwayatOperasiForm, extra=1, can_delete=True)
        pemeriksaan_penunjang_formset = inlineformset_factory(AssessmentRawatInap, PemerikasanPenunjang, form=PemerikasanPenunjangForm, extra=1, can_delete=True)
        operasi = riwayat_operasi_formset(self.request.POST, instance=self.object)
        pemeriksaan_penunjang = pemeriksaan_penunjang_formset(self.request.POST, instance=self.object)
        if operasi.is_valid():
            operasi.save()
        if pemeriksaan_penunjang.is_valid():
            pemeriksaan_penunjang.save()
        messages.success(self.request, 'Create success')
        return response

class AssessmentRawatInapUpdateView(IsAuthenticated, UpdateView):
    model = AssessmentRawatInap
    template_name = 'rawat_inap/form_assesment.html'
    form_class = AssesmentRawatInapForm
    context_object_name = 'assesment'

    def get_success_url(self) -> str:
        return reverse_lazy('rawat_inap-update', kwargs={'pk': self.get_object().pasien_rawat_inap.id})
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Assesmen Pasien Rawat Inap'
        context['header_title'] = 'Edit Assesmen Pasien Rawat Inap'
        context['pasien'] = self.get_object().pasien_rawat_inap.pasien
        context['btn_delete'] = True
        riwayat_operasi_formset = inlineformset_factory(AssessmentRawatInap, RiwayatOperasi, form=RiwayatOperasiForm, extra=1, can_delete=True)
        pemeriksaan_penunjang_formset = inlineformset_factory(AssessmentRawatInap, PemerikasanPenunjang, form=PemerikasanPenunjangForm, extra=1, can_delete=True)
        context['pemeriksaan_penunjang_formset'] = pemeriksaan_penunjang_formset(instance=self.get_object())
        context['riwayat_operasi_formset'] = riwayat_operasi_formset(instance=self.get_object())
        return context

    def form_valid(self, form):
        form.instance.pasien_rawat_inap = self.get_object().pasien_rawat_inap
        response = super().form_valid(form)
        riwayat_operasi_formset = inlineformset_factory(AssessmentRawatInap, RiwayatOperasi, form=RiwayatOperasiForm, extra=1, can_delete=True)
        pemeriksaan_penunjang_formset = inlineformset_factory(AssessmentRawatInap, PemerikasanPenunjang, form=PemerikasanPenunjangForm, extra=1, can_delete=True)
        pemeriksaan_penunjang = pemeriksaan_penunjang_formset(self.request.POST, instance=self.get_object())
        operasi = riwayat_operasi_formset(self.request.POST, instance=self.get_object())
        if operasi.is_valid():
            operasi.save()
        if pemeriksaan_penunjang.is_valid():
            pemeriksaan_penunjang.save()

        messages.success(self.request, 'Create success')
        return response

class AssessmentRawatInapDeleteView(IsAuthenticated, DeleteView):
    model = AssessmentRawatInap
    template_name = 'component/delete.html'

    def get_success_url(self) -> str:
        return reverse_lazy('rawat_inap-update', kwargs={'pk': self.get_object().pasien_fisioterapi.id})


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Assesmen Pasien Rawat Inap'
        context['header_title'] = 'Delete Assesmen Pasien Rawat Inap'
        return context


class DownloadAssesmentRawatInapView(IsAuthenticated, GeneratePDF,  UpdateView):
    model = AssessmentRawatInap
    template_name = 'rawat_inap/export/assesment.html'
    context_object_name = 'assesment'
    form_class = AssesmentRawatInapForm

    # def get(self, request, *args, **kwargs):
    #     return self.render_to_pdf(
    #         {
    #             'assesment': self.get_object(),
    #             'pasien':self.get_object().pasien_rawat_inap.pasien,
    #             'host' : f"{self.request.scheme}://{self.request.META['HTTP_HOST']}"
    #         },
    #         self.template_name,
    #         '/css/pdf.css',
    #         f'Assesment Pasien Fisioterapi {self.get_object().pasien_rawat_inap.pasien.full_name}'
    #     )

    def get(self, request, *args, **kwargs):
        document_id = '1mcFpyvqEvn02aNg_UGVed5gXntgb4O1yiJwuz0_tRXo'
        created_at_local = localtime(self.get_object().created_at)
        try:
            tgl_terakhir_bab = localtime(self.get_object().tgl_terakhir).strftime('%Y-%m-%d')
        except:
            tgl_terakhir_bab = ""
        screening = self.get_object()


        def check_condition(value, choices):
            return ["(√)" if value == choice else "()" for choice in choices]

        choices = [GejalaChoice.TIDAK_ADA, GejalaChoice.ADA_RINGAN, GejalaChoice.ADA_BERAT]
        a_1, b_1, c_1 = check_condition(screening.perubahan_berat_badan, choices)
        a_3, b_3, c_3 = check_condition(screening.gejala_gastrointestinal, choices)
        a_4, b_4, c_4 = check_condition(screening.faktor_pemberat, choices)
        a_5, b_5, c_5 = check_condition(screening.penurun_kapasitas, choices)

        asupan_choices = [AsupanMakanTerakhir.CUKUP, AsupanMakanTerakhir.MENURUN, AsupanMakanTerakhir.NGT]
        a_2, b_2, c_2 = check_condition(screening.asupan_makanan, asupan_choices)

        onset_choice = [OnsetChoice.AKUN, OnsetChoice.KRONIK]
        o_1, o_2 = check_condition(screening.onset, onset_choice)
        
        waktu_nyeri_choice = [WaktuChoice.INTERMITEN, WaktuChoice.TERUS_MENERUS]
        w_1, w_2 = check_condition(screening.waktu_nyeri, waktu_nyeri_choice)

        type_nyeri_choice = [TypeNyeri.TEKANAN, TypeNyeri.TERBAKAR, TypeNyeri.TAJAM_TUSUKAN, TypeNyeri.TAJAM_DIRIS, TypeNyeri.MENCENGKRAM, TypeNyeri.MELILIT]
        t_1, t_2, t_3, t_4, t_5, t_6 = check_condition(screening.type_nyeri, type_nyeri_choice)

        kat_1, kat_2, kat_3, kat_4, kat_5 = check_condition(screening.kategori_skrining, KATEGORI_SKRINING)

        kesadaran_choice = [Kesadaran.COMPOSMENTIS, Kesadaran.APATIS, Kesadaran.SOMMOLEN, Kesadaran.SOPOROCOMA, Kesadaran.LAINNYA]
        k_1, k_2, k_3, k_4, k_5 = check_condition(screening.kesadaran, kesadaran_choice)

        k_umum_choice = [KondisiUmum.BAIK, KondisiUmum.TAMPAK_SAKIT, KondisiUmum.SESAK, KondisiUmum.PUCAT, KondisiUmum.LEMAH, KondisiUmum.KEJANG, KondisiUmum.LAINNYA]
        k_u_1, k_u_2, k_u_3, k_u_4, k_u_5, k_u_6, k_u_7 = check_condition(screening.kondisi_umum_perawat, k_umum_choice)

        norton_choice = [CategoryNorton.RESIKO_BESAR, CategoryNorton.RESIKO_KECIL]
        nor_1, nor_2 = check_condition(screening.kategori_norton, norton_choice)

        # kontraktur_nyeri_choice = [YesOrNo.YA, YesOrNo.TIADK]
        # kon_1, kon_2 = check_condition(screening.kontraktur_nyeri, kontraktur_nyeri_choice)

        params = {            
            "alergi":self.get_object().alergi,
            "jenis_alergi": self.get_object().jenis_alergi,

            'created_at': created_at_local.strftime('%Y-%m-%d'), #created_at_local.strftime('%d %B %Y')
            'nama-pasien': self.get_object().pasien_rawat_inap.pasien.full_name,
            'no-rm': self.get_object().pasien_rawat_inap.pasien.no_rm,
            'jnis-kelamin': self.get_object().pasien_rawat_inap.pasien.jenis_kelamin,
            'tgl-lahir': self.get_object().pasien_rawat_inap.pasien.tanggal_lahir,

            "a_1": a_1, "b_1": b_1, "c_1": c_1,
            "a_2": a_2, "b_2": b_2, "c_2": c_2,
            "a_3": a_3, "b_3": b_3, "c_3": c_3,
            "a_4": a_4, "b_4": b_4, "c_4": c_4,
            "a_5": a_5, "b_5": b_5, "c_5": c_5,
       
            'kategori':self.get_object().kategori,
            'catatan_skrining_gizi': self.get_object().catatan_skrining_gizi,

            # sekrining nyeri
            "merasakan_nyeri": self.get_object().merasakan_nyeri,
            "lokasi": self.get_object().lokasi,
            'o_1': o_1, 'o_2': o_2,
            'w_1': w_1, 'w_2': w_2,
            "pencetus_nyeri": self.get_object().pencetus_nyeri,
            "t_1": t_1, "t_2": t_2, "t_3":t_3, "t_4": t_4, "t_5": t_5, "t_6": t_6,
            "nyeri_lainnya": self.get_object().nyeri_lainnya,
            "skor_nyeri": self.get_object().skor_nyeri,

            # skrining functional 
            "hygiene": self.get_object().personal_hygiene,
            "nadi": self.get_object().nadi,
            "makan": self.get_object().makan,
            "toileting": self.get_object().toileting,
            "tangga":self.get_object().menaiki_tangga,
            "pakaian":self.get_object().memekai_pakaian,
            "bab":self.get_object().kontrol_bab,
            "bak":self.get_object().kontrol_bak,
            "ambulasi":self.get_object().ambulasi,
            "kursi":self.get_object().transfer_kursi,
            "skor_skrining":self.get_object().total_skor_skrining,
            # "kat_skrining":self.get_object().kategori_skrining,
            "kat_1": kat_1, "kat_2": kat_2, "kat_3": kat_3, "kat_4": kat_4, "kat_5": kat_5,
            "total_sek":self.get_object().total_skor_skrining,

            # psiokologis dan sosial ekonomi
            "kondisi_pasien": self.get_object().kodisi_pasien,
            "hubungan_pasien": self.get_object().hubungan_pasien,
            "kusus_pasien": self.get_object().keinginan_kusus_pasien,
            "hambatan_sosial": self.get_object().hambatan_sosial,
            
            # kebutuhan cairan
            "minum": self.get_object().minum,
            "mukosa_mulut": self.get_object().mukosa_mulut,
            "edema": self.get_object().edema,
            "haus_berlebihan": self.get_object().haus_berlebihan,
            "turgor_kulit": self.get_object().turgor_kulit,

            # kebutuhan eliminasi
            "f_bak": self.get_object().fekuensi_bak,
            "j_bak": self.get_object().jumblah_bak,
            "fi_bab": self.get_object().fekuensi_bab,
            "warna": self.get_object().warna,
            "bau": self.get_object().bau,
            "konsistensi": self.get_object().konsistensi,
            "tgl_terakhir": tgl_terakhir_bab,

            # kebutuhan persepsi / sensori
            "penglihatan": self.get_object().pengelihatan,
            "pengecapan":self.get_object().pengecapan,
            "pendengaran":self.get_object().pendengaran,
            "perabaan":self.get_object().perabaan,
            "penciuman":self.get_object().penciuman,

            # kebutuhan komunikasi
            "berbicara":self.get_object().berbicara,
            "penyebab":self.get_object().penyebab_tdk_berbicara,
            "disorentasi":self.get_object().disorentasi,
            "penyebab_dis":self.get_object().penyebaba_disorentasi,
            "pembicaraan":self.get_object().pembicaraan,
            "menarik_diri":self.get_object().menarik_diri,
            "apatis":self.get_object().apatis,

            # kesadaran
            "k_1": k_1, "k_2": k_2, "k_3": k_3, "k_4": k_4, "k_5": k_5,
            "kesadaran_lainnya": self.get_object().val_kesadaran_lainya,

            # kondisi umum
            "k_u_1": k_u_1, "k_u_2": k_u_2, "k_u_3": k_u_3, "k_u_4": k_u_4, "k_u_5": k_u_5, "k_u_6": k_u_6, "k_u_7": k_u_7,
            "val_kon_lainnya":self.get_object().val_kon_laiinya,

            # tanda vital
            "td": self.get_object().tekanan_darah,
            "nadi": self.get_object().nadi,
            "pernapasan": self.get_object().pernapasan,
            "suhu": self.get_object().suhu,

            # kondisi fisik dan mental
            "dekubitus":self.get_object().dekubitus,
            "ket_dekubitus":self.get_object().keterangan_dekubitus,

            # kondisi fisik umum
            "s_fisik":self.get_object().skor_kondisi_fisik_umum,
            "s_kesadaran":self.get_object().skor_kesadaran,
            "s_aktifitas":self.get_object().skor_aktifitas,
            "s_inkentinensia":self.get_object().skor_inkentinensia,

            "nor_1":nor_1, "nor_2":nor_2,
            "kon":self.get_object().kontraktur_nyeri,
            "ket_nyeri":self.get_object().keterangan_nyeri,

        }
        file_name = f'Assesment Awal Rawat Inap - {self.get_object()} ({datetime.now()})'
        document = GoogleDocumentProvider(document_id, params, file_name)
        proses_document = document.process_document()
        return document.download_google_docs_as_pdf(proses_document)