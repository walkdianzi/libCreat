import tw2.core as twc
import tw2.forms as twf

class StudentForm(twf.Form):
   class child(twf.TableLayout):
      name = twf.TextField(size = 20)
      city = twf.TextField()
      address = twf.TextArea("",rows = 5, cols = 30)
      pincode = twf.NumberField()

   action = '/save_record'
   submit = twf.SubmitButton(value = 'Submit')