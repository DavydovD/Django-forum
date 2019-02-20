from django import forms
from .models import Category, SubCategory, Topic, Profile, Comment


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=255)


class CategoryCreationForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class SubcategoryCreationForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        exclude = ['category']


class TopicCreationForm(forms.ModelForm):
    class Meta:
        model = Topic
        exclude = ['subcategory']


class ProfileForm(forms.ModelForm):
    username = forms.CharField()

    class Meta:
        model = Profile
        exclude = ['user']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']






