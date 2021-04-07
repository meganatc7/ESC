from django import forms
from .models import Article, Photo, Comment

class ArticleForm(forms.ModelForm):
    title = forms.CharField(
        label='제목',
        widget=forms.TextInput(
            attrs={
                'class': 'my-title form-control',
                'placeholder': '제목을 입력해주세요.',
                'maxlength': 50,
            }
        )
    )
    content = forms.CharField(
        label='내용',
        widget=forms.Textarea(
            attrs={
                'class': 'my-content form-control',
                'placeholder': '내용을 입력해주세요.',
                'rows': 5,
                'cols': 30,
            }
        )
    )
    image = forms.ImageField(
        label='이미지',
    )

    class Meta:
        model = Photo
        fields = ('image',)
        model = Article
        fields = ('title', 'content',)        


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = '__all__'