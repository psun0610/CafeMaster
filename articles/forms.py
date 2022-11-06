from django import forms
from .models import Comment, Cafe



class CafeForm(forms.ModelForm):

    class Meta:
        model = Cafe
        fields = ['name', 'address', 'telephone', 'opening', 'picture1', 'picture2', 'picture3']

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = [ 'tag', 'content', 'picture',]