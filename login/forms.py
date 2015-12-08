from django import forms

class UploadReportForm(forms.Form):
	report_title = forms.CharField(max_length=100)
	report_body = forms.CharField(max_length=5000, widget=forms.Textarea)
	report_private = forms.BooleanField(required=False)
	#report_files = forms.FileField(required=False, label='Select a file') 
