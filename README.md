# All_Mighty_Reserve
https://model-ripple-167901.appspot.com

Author: Tianhui Zhu
Email: tz406@nyu.edu

This app is a Google App Engine based website designed to create resource and make reservations.

Language and Template:
Written in Python2.7 and Jinja2.
Google Cloud Datastore is used to store date.
All required features are implemented. A git brunch with no RSS was made. 

Details:
1. Both resource and reservation start/end time input is checked at front end in 'checkInput.js'. 
2. When any page presents resources, resources are ordered by the last reservation time if there 
are any reservations made, or they will be ordered by the resource modDate. 
3. All expired reservations will be deleted from the Cloud Datastore before presenting to the front end. 
Expiration of reservation is defined as 'when the end time of a reservation is already passed', 
so user can reserve a resource even when the resource has started, as long as it is still before end.
4. All expired resources will be highlighted and disabled from making reservations but not deleted.
5. To edit or delete a resource, all reservations made for this resource will be deleted.
6. By clicking the the title of the resource, it can lead to the resource content page. 
7. Although the requirement was just resource within a day, this app made it capable of spanning days, 
which is harder and more convenient to use as a real everyday app.


Additional Features:
1.Search Resource: User can search resource by resource name.
2.Upload Image: User can upload a image to a resource and the image will be presented in resource content page. 
3. Send Confirmation Email: When a resource is created or when a reservation is made, 
a confirmation email will be sent to the user.
4.Max of Attendee: The number of max attendee is required for creating a resource.
5.Num of Attendee: The front end only shows the number of available attendee.
If there is no spot available, no reservations can be made.


Requirements:
To run the app on local, the following python libraries are required to enable the image feature.
pillow and PIL.
To install pillow: sudo pip install pillow
To install PIL: sudo easy_install --find-links http://www.pythonware.com/products/pil/ Imaging

Front end:
A bootstrap-datetimepicker is used for the datetime input:
http://www.bootcss.com/p/bootstrap-datetimepicker/

