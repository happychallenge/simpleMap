from django import forms


from .models import Post, Content, Theme

class PostForm(forms.ModelForm):
    pictures = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}))
    is_published = forms.BooleanField(initial=True, widget=forms.CheckboxInput(attrs={'class': 'js-switch'}))

    class Meta:
        model = Post
        fields = ['theme', 'text', 'pictures', 'is_published']

    # def __init__(self, user, *args, **kwargs):
    #     super(PostForm, self).__init__(*args, **kwargs)
    #     self.fields['theme'].queryset = Theme.objects.filter(create_user=user)
