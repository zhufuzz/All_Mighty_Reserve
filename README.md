# All_Mighty_Reserve
https://model-ripple-167901.appspot.com

This app engine app is designed to create resource and make reservations.
A Google App Engine based website for reserving, written in Python2.7 and Jinja2.
Google Cloud Datastore is used to store date.
A git brunch with no RSS was made.

All required features are implements. 

All expired reservations will be deleted from the Cloud Datastore before presenting to the front end. 
All expired resource will be highlighted and disabled from making reservations.
To edit or delete a resource, all reservations made for this resource will be deleted.
By clicking the the title of the resource, it can lead to the resource content page. 
Although the requirement was just resource within a day, this app made it spanning days, 
which is harder and more convenient to use as a real app.


Additional Features:
1.Search Resource: User can search resource by resource name.
2.Upload Image: User can upload a image to a resource and the image will be presented when 
3.Send Confirmation Email: When a resource is created and when a reservation is made, 
a confirmation email will be sent to the user.
4.Max of Attendee: The number of max attendee is required for creating a resource.
5.Num of Attendee: The front end only shows the number of available attendee.
If there is no spot available, no further reservations can be made.


Requirements:
To run the app on local, the following python libraries are required to enable the image feature.
pillow and PIL

To install pillow: sudo pip install pillow
To install PIL: sudo easy_install --find-links http://www.pythonware.com/products/pil/ Imaging
