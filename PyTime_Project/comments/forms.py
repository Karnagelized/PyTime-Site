
from django import forms
from comments.models import Comment


# Форма для блока с написанием комментария
class WriteCommentForm(forms.ModelForm):
    content = forms.CharField(
        max_length=1500,
        min_length=3,
        label='',
        strip=True,
        widget=forms.Textarea(
            attrs={
                'class': 'feedback_input w-100',
                'placeholder': 'Комментарий',
            }
        )
    )


    class Meta:
        model = Comment
        fields = ('content',)
