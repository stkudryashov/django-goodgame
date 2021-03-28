from django.contrib import admin
from .forms import FullInfoUserForm, ClubInfoForm, CaseBodyForm, CaseGradesForm, CaseRewardForm
from .models import FullInfoUser, ClubInfo, CaseBody, CaseGrades, CaseReward, Mainlog


@admin.register(FullInfoUser)
class FullInfoUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'user_club', 'nickname', 'telegram_id')
    list_display_links = ('id', 'user_id', 'nickname')
    form = FullInfoUserForm


@admin.register(ClubInfo)
class ClubInfoAdmin(admin.ModelAdmin):
    list_display = ('id_name', 'text_name', 'address', 'telegram_token')
    list_display_links = ('id_name', 'text_name')
    form = ClubInfoForm


@admin.register(CaseBody)
class CaseBodyAdmin(admin.ModelAdmin):
    list_display = ('club', 'date_start', 'date_end')
    list_display_links = ('club',)
    form = CaseBodyForm


@admin.register(CaseGrades)
class CaseGradesAdmin(admin.ModelAdmin):
    list_display = ('club', 'cost', 'text', 'rewards')
    list_display_links = ('club', 'cost')
    form = CaseGradesForm


@admin.register(CaseReward)
class CaseRewardAdmin(admin.ModelAdmin):
    list_display = ('club', 'user_id', 'text', 'created_at', 'is_received')
    list_display_links = ('club', 'user_id')
    form = CaseRewardForm


@admin.register(Mainlog)
class MainlogAdmin(admin.ModelAdmin):
    list_display = ('recorddtime', 'cashadd', 'clientid')
    list_display_links = ('recorddtime',)
