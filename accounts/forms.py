from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django import forms

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label = '아이디',
        widget = forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '아이디를 입력하세요',
                'autofocus': 'True',
            }
        )
    )

    password1 = forms.CharField(
        label = '비밀번호',
        widget = forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '비밀번호를 입력하세요',
            }
        )
    )
    
    password2 = forms.CharField(
        label = '비밀번호 확인',
        widget = forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '비밀번호를 입력하세요',
            }
        )
    )

    email = forms.CharField(
        label = '이메일',
        widget = forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '이메일을 입력하세요',
            }
        )
    )

    address = forms.CharField(
        label = '주소',
        widget = forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'address',
                'placeholder': '주소',
                'readonly': True,
            }
        )
    )

    nickname = forms.CharField(
        label = '닉네임',
        widget = forms.TextInput(
            attrs={
                'class': 'form-control',
                'style': 'width: 200px;',
            }
        )
    )

    image = forms.ImageField(
        label = '프로필',
        required = False,
        widget = forms.FileInput(
            attrs={
                'class': 'form-control',
                'name': 'image',
                'accept': 'image/*',
            }
        )
    )

    introduction = forms.CharField(
        label = '자기소개',
        widget = forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 3,
                'maxlength': 300,
                'placeholder': '나에 대해 작성해주세요. (300자 이내)'
            }
        )
    )
    class Meta(UserCreationForm):
        model = get_user_model()
        fields = ('username', 'password1', 'password2', 'email', 'address', 'nickname', 'image', 'introduction',)
        # fields = UserCreationForm.Meta.fields + ('image', 'email', 'introduction', 'address', 'nickname',)

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label = '아이디',
        widget = forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '아이디를 입력해주세요',
                'autofocus': 'True',
            }
        )
    )
    password = forms.CharField(
        label = '비밀번호',
        widget = forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '비밀번호를 입력해주세요',
            }
        )
    )
    class Meta(AuthenticationForm):
        fields = '__all__'

class CustomUserChangeForm(UserChangeForm):
    
    email = forms.CharField(
        label = '이메일',
        widget = forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '이메일을 입력하세요',
            }
        )
    )

    address = forms.CharField(
        label = '주소',
        widget = forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    nickname = forms.CharField(
        label = '닉네임',
        widget = forms.TextInput(
            attrs={
                'class': 'form-control',
                'style': 'width: 200px;',
            }
        )
    )

    introduction = forms.CharField(
        label = '자기소개',
        widget = forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 3,
                'maxlength': 300,
            }
        )
    )

    class Meta(UserChangeForm):
        model = get_user_model()
        fields = ('email', 'address', 'nickname', 'introduction',)