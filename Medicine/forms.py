from django import forms 
from .models import Medicine

class MedicineForm(forms.ModelForm):
    
    class Meta:
        
        model=Medicine
        fields ='__all__'
        
        widgets = {
            'Name':forms.TextInput(attrs={'class':'form-control'}),
            'Type':forms.TextInput(attrs={'class':'form-control'}),
            'Price':forms.TextInput(attrs={'class':'form-control'}),
            'Manufacturing_date':forms.DateInput(attrs={'class':'form-control'}),
            'Expiry_date':forms.DateInput(attrs={'class':'form-control'}),    
        }
    
        
            
        
        
    
      