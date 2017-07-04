from django import forms
class ArticleForm(forms.Form):
    title=forms.CharField(widget=forms.TextInput(),max_length=200)
    context=forms.CharField(widget=forms.Textarea())
    create_at=forms.DateTimeField(widget=forms.SelectDateWidget())