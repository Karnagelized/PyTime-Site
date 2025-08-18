
from django import forms
from apps.comments.models import Comment
from better_profanity import profanity


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


    def clean_content(self):
        content = self.cleaned_data['content']
        clean_content = profanity.censor(content, '*')

        return clean_content


    class Meta:
        model = Comment
        fields = ('content',)
