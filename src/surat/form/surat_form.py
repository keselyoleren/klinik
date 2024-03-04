from config.form import AbstractForm
from config.form import AbstractForm, Select2Widget
from django import forms
from master_data.models import TenagaMedis
from pasien.models import Pasien
from surat.models import *

class KetarangaSakitForm(AbstractForm):
    pasien = forms.ModelChoiceField(widget=Select2Widget(), queryset=Pasien.objects.all())
    class Meta:
        model = KeteraganSakit
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super(KetarangaSakitForm, self).__init__(*args, **kwargs)
        choices_pasien = [(p.id, p.full_name) for p in Pasien.objects.all()]
        self.fields['pasien'].choices = choices_pasien

class GenerateKetarangaSakitForm(AbstractForm):
    class Meta:
        model = KeteraganSakit
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super(GenerateKetarangaSakitForm, self).__init__(*args, **kwargs)
        self.fields['pasien'].widget = forms.HiddenInput()


class KetarangaSehatForm(AbstractForm):
    pasien = forms.ModelChoiceField(widget=Select2Widget(), queryset=Pasien.objects.all())
    class Meta:
        model = KeteranganSehat
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(KetarangaSehatForm, self).__init__(*args, **kwargs)
        choices_pasien = [(p.id, p.full_name) for p in Pasien.objects.all()]
        self.fields['pasien'].choices = choices_pasien

class GenerateKetarangaSehatForm(AbstractForm):
    class Meta:
        model = KeteranganSehat
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(GenerateKetarangaSehatForm, self).__init__(*args, **kwargs)
        self.fields['pasien'].widget = forms.HiddenInput()


class SuratRujukanForm(AbstractForm):
    pasien = forms.ModelChoiceField(widget=Select2Widget(), queryset=Pasien.objects.all())
    tenaga_medis = forms.ModelChoiceField(widget=Select2Widget(), queryset=TenagaMedis.objects.all())
    class Meta:
        model = SuratRujukan
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(SuratRujukanForm, self).__init__(*args, **kwargs)
        choices_pasien = [(p.id, p.full_name) for p in Pasien.objects.all()]
        choices_tenaga_medis = [(p.id, p.nama) for p in TenagaMedis.objects.all()]
        self.fields['tenaga_medis'].choices = choices_tenaga_medis
        self.fields['pasien'].choices = choices_pasien

class GenerateSuratRujukanForm(AbstractForm):
    tenaga_medis = forms.ModelChoiceField(widget=Select2Widget(), queryset=TenagaMedis.objects.all())
    class Meta:
        model = SuratRujukan
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(GenerateSuratRujukanForm, self).__init__(*args, **kwargs)
        choices_tenaga_medis = [(p.id, p.nama) for p in TenagaMedis.objects.all()]
        self.fields['tenaga_medis'].choices = choices_tenaga_medis
        self.fields['pasien'].widget = forms.HiddenInput()

class SuratKelahiranForm(AbstractForm):
    pasien = forms.ModelChoiceField(widget=Select2Widget(), queryset=Pasien.objects.all())
    class Meta:
        model = SuratKelahiran
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(SuratKelahiranForm, self).__init__(*args, **kwargs)
        choices_pasien = [(p.id, p.full_name) for p in Pasien.objects.all()]
        self.fields['pasien'].choices = choices_pasien



class SuratKematianForm(AbstractForm):
    pasien = forms.ModelChoiceField(widget=Select2Widget(), queryset=Pasien.objects.all())
    class Meta:
        model = SuratKematian
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SuratKematianForm, self).__init__(*args, **kwargs)
        choices_pasien = [(p.id, p.full_name) for p in Pasien.objects.all()]
        self.fields['pasien'].choices = choices_pasien

class SuratRapidAntigenForm(AbstractForm):
    pasien = forms.ModelChoiceField(widget=Select2Widget(), queryset=Pasien.objects.all())
    class Meta:
        model = SuratRapidAntigen
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SuratRapidAntigenForm, self).__init__(*args, **kwargs)
        choices_pasien = [(p.id, p.full_name) for p in Pasien.objects.all()]
        self.fields['pasien'].choices = choices_pasien

class SuratPerintahTugasForm(AbstractForm):
    tenaga_medis = forms.ModelChoiceField(widget=Select2Widget(), queryset=TenagaMedis.objects.all())
    class Meta:
        model = SuratPerintahTugas
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SuratPerintahTugasForm, self).__init__(*args, **kwargs)
        tenaga_medis = [(p.id, p.nama) for p in TenagaMedis.objects.all()]
        self.fields['tenaga_medis'].choices = tenaga_medis

    
class SuratBebasNarkobaForm(AbstractForm):
    pasien = forms.ModelChoiceField(widget=Select2Widget(), queryset=Pasien.objects.all())
    tenaga_medis = forms.ModelChoiceField(widget=Select2Widget(), queryset=TenagaMedis.objects.all())
    class Meta:
        model = SuratBebasNarkoba
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SuratBebasNarkobaForm, self).__init__(*args, **kwargs)
        choices_pasien = [(p.id, p.full_name) for p in Pasien.objects.all()]
        choices_tenaga_medis = [(p.id, p.nama) for p in TenagaMedis.objects.all()]
        self.fields['tenaga_medis'].choices = choices_tenaga_medis
        self.fields['pasien'].choices = choices_pasien

class GenerateSuratBebasNarkobaForm(AbstractForm):
    
    tenaga_medis = forms.ModelChoiceField(widget=Select2Widget(), queryset=TenagaMedis.objects.all())
    class Meta:
        model = SuratBebasNarkoba
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(GenerateSuratBebasNarkobaForm, self).__init__(*args, **kwargs)
        choices_tenaga_medis = [(p.id, p.nama) for p in TenagaMedis.objects.all()]
        self.fields['tenaga_medis'].choices = choices_tenaga_medis
        self.fields['pasien'].widget = forms.HiddenInput()

class SuratPersetujuanForm(AbstractForm):
    pasien = forms.ModelChoiceField(widget=Select2Widget(), queryset=Pasien.objects.all())
    tenaga_medis = forms.ModelChoiceField(widget=Select2Widget(), queryset=TenagaMedis.objects.all())
    class Meta:
        model = SuratPersetujuan
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SuratPersetujuanForm, self).__init__(*args, **kwargs)
        choices_pasien = [(p.id, p.full_name) for p in Pasien.objects.all()]
        choices_tenaga_medis = [(p.id, p.nama) for p in TenagaMedis.objects.all()]
        self.fields['tenaga_medis'].choices = choices_tenaga_medis
        self.fields['pasien'].choices = choices_pasien

class GenerateSuratPersetujuanForm(AbstractForm):
    tenaga_medis = forms.ModelChoiceField(widget=Select2Widget(), queryset=TenagaMedis.objects.all())
    class Meta:
        model = SuratPersetujuan
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(GenerateSuratPersetujuanForm, self).__init__(*args, **kwargs)
        self.fields['pasien'].widget = forms.HiddenInput()


class SuratPenolakanForm(AbstractForm):
    pasien = forms.ModelChoiceField(widget=Select2Widget(), queryset=Pasien.objects.all())
    class Meta:
        model = SuratPenolakan
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SuratPenolakanForm, self).__init__(*args, **kwargs)
        choices_pasien = [(p.id, p.full_name) for p in Pasien.objects.all()]
        self.fields['pasien'].choices = choices_pasien

class GenerateSuratPenolakanForm(AbstractForm):
    class Meta:
        model = SuratPenolakan
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(GenerateSuratPenolakanForm, self).__init__(*args, **kwargs)
        self.fields['pasien'].widget = forms.HiddenInput()