# from rest_framework
from rest_framework import serializers

# from 'api' app
from .models import user_details

class User_detailsSerializer(serializers.ModelSerializer):
	class Meta:
		model = user_details
		fields = '__all__'