from django import forms
from .models import Article, Photo, Comment

class ArticleForm(forms.ModelForm):
    CATEGORY_A = '1'
    CATEGORY_B = '2'
    CATEGORY_C = '3'
    CATEGORY_CHOICES = [
        (CATEGORY_A, '자유 게시판'),
        (CATEGORY_B, '질문 게시판'),
        (CATEGORY_C, '장터 게시판'),
    ]
    category = forms.ChoiceField(
        label='',
        choices=CATEGORY_CHOICES, 
    )
    
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

    class Meta:
        model = Article
        fields = ('category', 'title', 'content',)


class PhotoForm(forms.ModelForm):
    image = forms.ImageField(
        label='이미지',
        required=False,
    )
    class Meta:
        model = Photo
        fields = ('image',)        
# 이미지 폼을 갖고와 엮어서 폼셋으로 만들기
PhotoFormSet = forms.inlineformset_factory(Article, Photo, form=PhotoForm, extra=5)

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': '내용을 입력해주세요',
                'rows': 3,
                'cols': 150,
            }
        )
    )
    class Meta:
        model = Comment
        fields = ('content',)