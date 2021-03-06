from django import forms
from .models import FullInfoUser, ClubInfo, CaseBody, CaseGrades, CaseReward


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
        fields = ('club', 'date_start', 'date_end', 'how_open', 'about_text', 'message_text', 'limit', 'image')


class CaseGradesForm(forms.ModelForm):
    class Meta:
        model = CaseGrades
        fields = ('club', 'cost', 'text', 'rewards', 'rewards_cost', 'weights')


class CaseRewardForm(forms.ModelForm):
    class Meta:
        model = CaseReward
        fields = ('club', 'user_id', 'text', 'case_cost', 'reward_cost')
