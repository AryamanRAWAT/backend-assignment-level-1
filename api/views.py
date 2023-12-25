from django.http import JsonResponse
from django.shortcuts import HttpResponse
import json                                             #JavaScript Object Notation
from django.core.paginator import Paginator,EmptyPage
from api.models import user_details
from django.views.decorators.csrf import csrf_exempt
import traceback
from api.utils import db_check_save

class POST_user:                    
    @csrf_exempt                            # it is a Django decorator used to exempt a view or function from the requirement of including a CSRF token. 
    # to create a new user.
    def post_user(request): 

        if request.method == 'POST':        #if the method is POST then only will it work.
            try:
                data = json.loads(request.body)     #to convert JavaScript Object Notation format to python data structure dictionary.
                # print(data)
                if isinstance(data, list):          # if the datastructure of data is list then post_multi_users() is called to handle multiple entries.
                    taken_info = POST_user.post_multi_users(data)     
                    if taken_info:                  # this if statement check whether taken_info is none or not. If it is not none that means few entries already exists. It informs the user on taken entries
                        return JsonResponse({'status': 'These emails or ids are already taken rest are saved.', 'taken_emails': taken_info[0], 'id_taken': taken_info[1]}, status=400)
                    else:
                        return HttpResponse('All Users Created!', status=201)
                else:
                    taken_info = db_check_save(data) # this handles single entry
                    if taken_info:
                        return JsonResponse({'status': 'Email already taken', 'email_taken': taken_info[0], 'id_taken': taken_info[1]}, status=400)     #taken_info[0] contains the list of taken emails where as taken_info[1] contains taken ids.
                    else:
                        return HttpResponse('New User Created!', status=201)

                

            except:                                 #if any errors are encountered we cathc it using except
                print(traceback.format_exc())       # returns a string that contains the formatted traceback information leading to the error. 
                return HttpResponse('Server ERROR...', status=500)  # status 500 represents server side issue.


    # to create multiple users
    def post_multi_users(data):
        taken_emails = [[],[]] 

        for entry in data:                          #db_check_save method called for each entry.
            taken_info = db_check_save(entry)  
            if taken_info:
                taken_emails[0].extend(taken_info[0])   #taken_emails[0] holds all conflicting emails
                taken_emails[1].append(taken_info[1])   #taken_emails[1] holds all conflicting ids
        if len(taken_emails[0])>0 or len(taken_emails[1])>0:
            return taken_emails
        else:
            return None                             # none is returned as an indicator to post_user that signify that all entries were saved in db
    

class GET_user:
    # to return requested users.
    def get_users_all(request):
            try:
                if request.method == 'GET':            #if the method is GET then only will it work.
                    page_get = int(request.GET.get('page',1))   #retrieves the value of the 'page' parameter from the request's GET parameters, converting it to an integer with a default value of 1. This parameter tells the code which page of entries are to be shown.
                    limit = int(request.GET.get('limit',5))     #retrieves the value of the 'limit' parameter from the request's GET parameters, with this we can set the limit on entries shown per page.
                    name = request.GET.get('name','')           #variable used in searching of user by name as a substring in First Name or Last Name in database. Default value set to '', if nothing in sent 
                    sort = request.GET.get('sort','')           #variable used for sort the list of users according to user desired attribute (age,id,etc.). By default it is in ascending order but if '-' is at the front(eg:'-age') then the order is descending.
                    print(page_get,limit,name,sort)
                    users = user_details.objects.all()          #retrieves all entries from the table
                    user_lst = []                               #an empty list that will contain entries matching the query.
                    print('1>', users)
                    if name:
                        users = users.filter(first_name__icontains=name) | users.filter(last_name__icontains=name)   #the pipe operator '|' is used to combine results of filters. '__icontains' returns all names containing substring(name) and it is case insensitive.  

                    print('2>', sort)
                    if len(sort)>0:                  
                        users = users.order_by(sort)                #list of users according to user desired attribute (age,id,etc.).
                        # print('3>', users)
                    
                    print('4>', users)


                    for user in users:
                        user_dic = {                        
                        'id' : user.id,
                        'first_name' : user.first_name,
                        'last_name' : user.last_name,
                        'company_name' : user.company_name,
                        'city' : user.city,
                        'state' : user.state,
                        'zip' : user.zip,
                        'email' : user.email,
                        'web' : user.web,
                        'age' : user.age,
                        }                                   #creating a list of dictionaries (user_lst), where each dictionary represents a user's attributes extracted from the queryset fields. 
                        user_lst.append(user_dic)
                    p = Paginator(user_lst,limit)           #paginating the list of user dictionaries (user_lst) with a specified limit of items per page (limit). 
                    res_page = p.page(page_get)             #res_page holds the items at the specified page.
                    return JsonResponse(res_page.object_list, safe=False, status=200)  # safe=False argument is used when the data to be serialized is not a dictionary but a list.

            except(EmptyPage):                              # this exception is used if the user requests a page that does not hold any items.
                return HttpResponse('Empty Page.', status=500)    

            except:
                print(traceback.format_exc())
                return HttpResponse('Server Error', status=500)
            
    #method to return requested entry to the user.
    def get_user(request,uid):                              #this method requires 2 arguments http request and user id by which we find the requested user and return it to the user.
        if request.method == 'GET':
            try:
                user = user_details.objects.get(id=uid)
                user_dic = {
                        'id' : uid,
                        'first_name' : user.first_name,
                        'last_name' : user.last_name,
                        'company_name' : user.company_name,
                        'city' : user.city,
                        'state' : user.state,
                        'zip' : user.zip,
                        'email' : user.email,
                        'web' : user.web,
                        'age' : user.age,
                    }
                print(user_dic)
                return JsonResponse(user_dic,status=200)            #JsonResponse is used to send basic json data.
            
            except(user_details.DoesNotExist):                      #if the user does not exists this resposne will be sent.
                return HttpResponse('User Does Not Exsits.', status=500)
            except:
                print(traceback.format_exc())
                return HttpResponse('Server Error', status=500)  
            
class PUT_user:
    @csrf_exempt
    def update_user(request,uid):                              #This method updates exsisting user's attributes. This method requires 2 arguments http request and user id by which we find the requested user and update its attribute

        if request.method == 'PUT':                            #function works only if method is 'PUT' 
            try:
                data = json.loads(request.body)
                users = user_details.objects.filter(id=uid)
                print('1>',users)
                if users.exists():                             #checks if the user exists and if it does, it will update the entry with new attributes.
                    user = users.first()
                    user.first_name = data.get('first_name', user.first_name)
                    user.last_name = data.get('last_name', user.last_name)
                    user.company_name = data.get('company_name', user.company_name)
                    user.age = data.get('age', user.age)
                    user.city = data.get('city', user.city)
                    user.state = data.get('state', user.state)
                    user.zip = data.get('zip', user.zip)
                    user.email = data.get('email', user.email)
                    user.web = data.get('web', user.web)

                    user.save()

                    return HttpResponse('Entry Updated!', status=200)

            except(user_details.DoesNotExist):                              #if the user does not exists this resposne will be sent.
                return HttpResponse('User Does Not Exsits.', status=400)

            except:
                print(traceback.format_exc())
                return HttpResponse('Server Error', status=500)

class DELETE_user:        
    @csrf_exempt
    def delete_user(request,uid):                           #this method deletes a single entry from the table based on user id given by the user.
        if request.method == 'DELETE':                        
            try:
                user = user_details.objects.get(id=uid)     #to retrieve user based on 'id' attributegiven by the user. 
                user.delete()                               #this deletes the entry.
                return HttpResponse('Entry Deleted!', status=200)
            
            except(user_details.DoesNotExist):
                return HttpResponse('User Does Not Exsits.', status=500)

            except:
                print(traceback.format_exc())
                return HttpResponse('Server Error', status=500)


    @csrf_exempt     
    def delete_all(request):                                #this method deletes all user.
        if request.method == 'DELETE':
            try:
                first_name = request.GET.get('first_name','')
                last_name = request.GET.get('last_name','')
                age_start = int(request.GET.get('age_start', 0))  # Default value of 0 if not provided
                age_end = int(request.GET.get('age_end', 0))
                start_id = int(request.GET.get('start_id', 0))  
                end_id = int(request.GET.get('end_id', 0))  

                users = user_details.objects.all()

                # Filter based on provided parameters
                if first_name:
                    users = users.filter(first_name__iexact=first_name)     # case-insensitive matching for first_name.
                if last_name:
                    users = users.filter(last_name__iexact=last_name)       # case-insensitive matching for last_name.
                if age_start < age_end:
                    users = users.filter(age__gte=age_start, age__lte=age_end)      #__gte filters all ages greater than or eaqual to age_start.
                if start_id < end_id:
                    users = users.filter(id__gte=start_id, id__lte=end_id)          #__lte filterd all ids less than or eaqual to end_id.

                # Delete filtered entries
                
                user_list = []
                for user in users:
                    user_dic = {
                        'id' : user.id,
                        'first_name' : user.first_name,
                        'last_name' : user.last_name,
                        'email' : user.email,
                        'age' : user.age,
                    }
                    user_list.append(user_dic)
                print(user_list)
                users.delete()
                if user_list:
                    return HttpResponse('Entries Deleted!', status=200)
                else:
                    return HttpResponse('Users does not exists!', status=400)
                
            
            except:
                print(traceback.format_exc())
                return HttpResponse('Server Error', status=500)