from django.http import HttpResponse
from api.models import user_details
from django.db.models import Q
import traceback

#to check wheter the email or id already exists in db. If not then it save data in db else skips and return a list containing the conflicting attributes.
def db_check_save(data):
                uid = int(data.get('id'))                    # get() builtin method for dictionary that returns the value of the key passed.
                first_name = data.get('first_name')
                last_name = data.get('last_name')
                company_name = data.get('company_name')
                age = int(data.get('age'))
                city = data.get('city')
                state = data.get('state')
                zip = int(data.get('zip'))
                email = data.get('email')
                web = data.get('web')                   
                existing_user = user_details.objects.filter(Q(email=email) | Q(id=uid)).first()  #the filter() method on a Django ORM to query the database and retrieve a user with a specific email or id.       

                print('db id>>>>',existing_user)
                if existing_user is not None:               # if existing_user is not none that means either user id or user mail already exists in db.
                    if existing_user.id == uid and existing_user.email == email:            #these if statements are used to find out which of the two already exsits in db. 
                        taken = [[email],uid]
                        return  taken
                    elif existing_user.id == uid:
                        taken = [[],uid]
                        return  taken
                    elif existing_user.email == email:
                        taken = [[email],'']
                        return  taken
                
                else:
                    try:  
                        user = user_details(
                                        id = uid,
                                        first_name = first_name,
                                        last_name = last_name,
                                        company_name = company_name,
                                        age = age,
                                        city = city,
                                        state = state,
                                        zip = zip,
                                        email = email,
                                        web = web
                                    )
                        user.save()     #to save attributes in table
                        print('saved')
                        return None      # none is returned as an indicator to post_user that the entry was saved in db
                    except:
                        print(traceback.format_exc())        
                        return HttpResponse('Server ERROR...', status=500)