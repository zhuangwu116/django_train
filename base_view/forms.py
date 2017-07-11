from django import forms
class ArticleForm(forms.Form):
    title=forms.CharField(required=False,widget=forms.TextInput(),max_length=200)
    context=forms.CharField(required=False,widget=forms.Textarea())
    create_at=forms.DateTimeField(required=False,widget=forms.SelectDateWidget())

class AuthorInterestForm(forms.Form):
    message=forms.CharField()


