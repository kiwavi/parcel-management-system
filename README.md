# parcel-management-system
This project automates the process of registering, reporting, and discharging parcels in a way that makes analogue record keeping obsolete.     
Many Matatu Saccos usually use analogue methods to manage parcels    
This project currently uses email to inform customers about their parcels.    
Get Started    
Clone this repository into a folder     
`git clone https://github.com/Kiwavi/parcel-management-system.git .`    
Create a virtual environment    
`python -m venv venv`    
Activate the virtual environment    
`source venv/bin/activate`    


This project uses email to communicate to customers by informing them about parcel arrival, departure, and status. Therefore, it uses gmail credentials to send out emails    
These environment variables are best kept in a .env file    
Create a .env file in the root directory and add the following variables:    

SECRET_KEY = 'secret_key'                                                                
DEBUG = True                                                                                                                                     
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'                                                                                    
EMAIL_HOST = 'smtp.gmail.com'                                                                                                                    
EMAIL_USE_TLS = True                                                                                                                             
EMAIL_PORT = 587                                                                                                                                 
EMAIL_HOST_USER = 'email'                                                                                                          
EMAIL_HOST_PASSWORD = 'app_access_password'    

Enter your own secret_key, email-host-user and email-host-password. The password should be an app password provided for such apps.     
You can generate a secret key using the following url: https://djecrety.ir/    

Run migrations    
python manage.py migrate    
Once you're done, run the server.     
`python manage.py runserver`     
Navigate to 127:0.0.0.1/8000 on your browser and start testing    
