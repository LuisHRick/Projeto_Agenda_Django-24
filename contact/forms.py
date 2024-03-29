from contact.models import Contact
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from django.contrib.auth.models import User

class ContactForms(forms.ModelForm):

    picture = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'accept': 'image/*',
            }
        ),
        required=False,
        label='Foto'
    )

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                    'class': 'classe-a classe-b',
                    'placeholder': 'Escreva aqui',
            }
        ),
        label='Nome',
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                    'class': 'classe-a classe-b',
                    'placeholder': 'Escreva aqui',
            }
        ),
        label='Sobrenome',
    )

    phone = forms.IntegerField(
        widget=forms.TextInput(
            attrs={
                    'class': 'classe-a classe-b',
                    'placeholder': '(99) 9999-9999',
            }
        ),
        label='Número de Telefone',
        help_text= 'Coloque seu número com o DDD e sem espaços.\nMínimo 10 números, máximo 11.'
    )

    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                    'placeholder': 'email@dominio.com'
            }
        ),
        label='E-mail'
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                    'placeholder': '...'
            }
        ),
        label='Descrição'
    )


    class Meta:
        model = Contact
        fields = (
            'first_name',
            'last_name',
            'phone',
            'email',
            'description',
            'category',
            'picture'
        )

    def clean(self):
        cleaned_data = self.cleaned_data
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        phone = cleaned_data.get('phone')

        if first_name == last_name:
            self.add_error(
                'last_name',
                ValidationError(
                    'O sobrenome não pode ser igual ao nome',
                    code='invalid'
                )
            )

        return super().clean()



    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')

        if not first_name.isalpha():
            self.add_error(
                'first_name',
                ValidationError(
                    'O nome não pode incluir números (0-9) ou caracteres especiais (!#%&?).',
                    code='invalid'
                )
            )
        return first_name


    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')

        if not last_name.isalpha():
            self.add_error(
                'last_name',
                ValidationError(
                    'O sobrenome não pode incluir números (0-9) ou caracteres especiais (!#%&?).',
                    code='invalid'
                )
            )
        
        return last_name


    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if len(str(phone)) < 10 or len(str(phone)) > 11:
            self.add_error(
                'phone',
                ValidationError(
                    'O número de telefone não pode ter menos que 10 digitos ou mais que' \
                        ' 11. Utilize o formato ddd + numero de telefone.',
                        code='invalid'
                )
            )

        return phone

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='E-mail'
    )

    first_name = forms.CharField(
        required=True,
        min_length=3,
        label='Nome'
    )

    last_name = forms.CharField(
        required=False,
        min_length=3,
        label='Sobrenome'
    )

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email',
            'username', 'password1', 'password2'
        )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            self.add_error(
                'email',
                ValidationError('Esse E-mail já existe', code='invalid')
            )
        
        return email
    
class RegisterUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        label='Nome',
        min_length=2,
        max_length=30,
        required=True,
        help_text='Obrigatório.',
        error_messages={
            'min_length': 'Por favor, adicione mais 2 letras.'
        }
    )
    last_name = forms.CharField(
        label='Sobrenome',
        min_length=2,
        max_length=30,
        required=True,
        help_text='Obrigatório.'
    )

    password1 = forms.CharField(
        label="Senha",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
    )

    password2 = forms.CharField(
        label="Confirmação de senha",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text='Use a mesma senha que antes.',
        required=False,
    )

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email',
            'username',
        )

    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        user = super().save(commit=False)
        password = cleaned_data.get('password1')

        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                self.add_error(
                    'password2',
                    ValidationError('Senhas não batem')
                )

        return super().clean()

    def clean_email(self):
        email = self.cleaned_data['email']
        current_email = self.instance.email

        if User.objects.filter(email=email).exists() and current_email.lower() != email.lower():
            self.add_error(
               'email',
               ValidationError('Já existe este e-mail', code='invalid')
            )

        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if password1:
            try:
                password_validation.validate_password(password1)
            except ValidationError as errors:
                self.add_error(
                    'password1',
                    ValidationError(errors)
                )

        return password1