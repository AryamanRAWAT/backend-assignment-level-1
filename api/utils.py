# from local
from api.serializers import User_detailsSerializer

# python modules
import traceback


#to check wheter the email or id already exists in db. If not then it save data in db else skips and return a list containing the conflicting attributes.
def user_details_save(data):
    serializer = User_detailsSerializer(data=data)
    if serializer.is_valid():
        try:
            serializer.save()
            return None
        except:
            print(traceback.format_exc())
            return 'Error'
    else:
        return serializer.errors