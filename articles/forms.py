from django import forms
from .models import Comment, Cafe



class CafeForm(forms.ModelForm):

    class Meta:
        model = Cafe
        fields = ['name', 'address', 'telephone', 'opening', 'lastorder','picture1',]

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content', 'picture', 'tag',]