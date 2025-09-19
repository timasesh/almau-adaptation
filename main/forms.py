from django import forms
from django.forms import ModelForm
from .models import History, Mission, Values, Leader, Document, DocumentCategory, Editor



class DocumentForm(ModelForm):
    """Форма для документов"""
    class Meta:
        model = Document
        fields = [
            'title', 'description', 'file',
            'title_en', 'description_en', 'file_en',
            'title_kk', 'description_kk', 'file_kk',
            'category', 'is_active'
        ]


class DocumentCategoryForm(ModelForm):
    """Форма для категорий документов"""
    class Meta:
        model = DocumentCategory
        fields = ['name', 'description', 'order_index', 'is_active']


class EditorRegistrationForm(forms.Form):
    """Форма регистрации редактора"""
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите email'
        })
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        }),
        min_length=8
    )
    password_confirm = forms.CharField(
        label='Подтвердите пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Подтвердите пароль'
        }),
        min_length=8
    )
    full_name = forms.CharField(
        label='Полное имя',
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите полное имя'
        })
    )
    department = forms.CharField(
        label='Кафедра/Отдел',
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите кафедру или отдел'
        })
    )
    position = forms.CharField(
        label='Должность',
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите должность'
        })
    )
    phone = forms.CharField(
        label='Телефон',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите номер телефона'
        })
    )
    bio = forms.CharField(
        label='Биография',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Краткая биография (необязательно)'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        email = cleaned_data.get('email')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают')

        if email:
            # Проверяем, не существует ли уже пользователь с таким email
            from django.contrib.auth.models import User
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('Пользователь с таким email уже существует')

        return cleaned_data


class EditorLoginForm(forms.Form):
    """Форма входа для редакторов"""
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите email'
        })
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )


class EditorProfileForm(forms.ModelForm):
    """Форма редактирования профиля редактора"""
    class Meta:
        model = Editor
        fields = ['full_name', 'department', 'position', 'phone', 'bio']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
