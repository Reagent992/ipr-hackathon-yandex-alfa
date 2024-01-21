from django_filters import SearchFilter

from tasks.models import Skill

class SkillsFilter(filters.FilterSet):
    название = SearchFilter(field_name='skill_name')

    class Meta:
        model = Skill
        fields = ['skill_name']