
from django import forms
from apps.comments.models import Comment
from better_profanity import profanity
from re import match



class WriteCommentForm(forms.ModelForm):
    """
        Форма для блока с написанием комментария
    """

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

        # Валидация символов
        if not match(r'^[a-zA-Zа-яА-ЯёЁ0-9\s\.,!?;:()\-+@#$%&*"\']+$', clean_content):
            raise forms.ValidationError(
                'Комментарий содержит запрещенные символы. ' +
                'Разрешены только буквы, цифры и основные знаки препинания.'
            )

        return clean_content


    class Meta:
        model = Comment
        fields = ('content',)
