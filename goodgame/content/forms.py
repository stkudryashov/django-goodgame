from django import forms
from .models import FullInfoUser, ClubInfo, CaseBody


class FullInfoUserForm(forms.ModelForm):
    class Meta:
        model = FullInfoUser
        fields = ('user_id', 'user_club', 'nickname', 'telegram_id')


class ClubInfoForm(forms.ModelForm):
    class Meta:
        model = ClubInfo
        fields = ('id_name', 'text_name', 'address', 'telegram_token')


class CaseBodyForm(forms.ModelForm):
    class Meta:
        model = CaseBody
        fields = ('club', 'date_start', 'date_end', 'how_open', 'about_text', 'image')
