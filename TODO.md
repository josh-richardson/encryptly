# wad2-teamproject: to do
#### This file is a work in progress and will definitely grow as the project does. 
Web pages:
- [x] Index
- [x] About us
- [x] FAQ
- [x] Contact
- [x] Login (+2FA) - GUI for the user logging in to the webiste. Requires their username, password, decryption key and potentially their 2FA key
- [x] Sign up - lets the user sign up to the website. During this process the user must choose a username and password, and a decryption key, they also may potentially enable 2FA and enter a mobile number. A key-pair must also be generated for the user
- [ ] Messaging interface - This should be implemented to a very basic level before the messaging capability is implemented on the backend, then the basics of the messaging capability should be implemented on the backend, and then the two should be developed iteratively in tandem with each other. The messaging interface should let users type messages, send files, and interact with friends
- [ ] Themes - Low priority, probably just a user profile based variable which dictates which custom CSS we load into the messaging interface
- [x] Logo & Favicon - Low priority, just adds eye-candy, doesn't affect functionality
- [ ] Chrome manifest for app - Low priority, adds better support for mobile apps.

Frontend JavaScript:
- [x] Keypair generation - Allows the browser to generate a key pair for the user so they can sign up and message others securely - specific to the signup interface
- [x] Login form logic - Logic for the login form in terms of validation and client side javascript, making sure that the browser sends the correct JSON to the server in order for the user to log in, and responding correctly if the user has 2FA enabled. For details on how I approached and am implementing this, take a look at doc/implementation notes/login_spec.txt
- [x] Sign up form logic - Logic for the sign up form in terms of validation and client side javascript, making sure that all fields are entered properly, and that the username doesn't already exist before keypair generation is allowed to take place
- [ ] Implementation of websockets for messaging and messaging ecosystem - the main backbone of the funtionality of the application. Allows for fast and efficient transferral of information between the client and the server in realtime. A prototype of this will probably be implemented without the encryption element in advance of the actual implementation. On the client side this means the ability to render messages when they are received, and send the correct websocket requests to the server when the user wants to send a message.
- [ ] AES Encryption & Decryption of messages - when messages are received on the clientside they must be decrypted before they can be viewed - this should be developed in tandem with the clientside websocket implemtnation, but after the prototype messaging app
- [ ] Friend requests - Developed after the ability to send and receive messages, in terms of client side implementation this includes rendering a notification when the user receives a friend request, and sending the correct data to the server when the user sends a friend request
- [ ] Online status - A websocket signal that fires every x amount of time in order to show the online status of a particular user, developed last in terms of javascript functionality. Should be trivial to implement though.



Backend development:
- [x] Database models started (MySQL as driver)
- [x] Login & 2FA capability (Twilio) - The server side component of letting users log in, has to verify that the user's username, password and decryption key without the decryption key being sent to the server. For details on how I approached and am implementing this, take a look at doc/implementation notes/login_spec.txt
- [ ] Database models for messaging completed - The database models in which we store data about messages which have been sent between users or in a group. These models will be difficult to implement and will require significant thought
- [ ] Friend request capability - Backend functionality for a user to be able to send a friend request to another user - this involves handling the request from user a, and sending the correct data to user b, as well as storing the request in the DB until it is replied to
- [ ] One-to-one messaging - Backend functionality for a user to be able to send a message to another user - this involves handling the message from user a, and sending the correct data to user b, as well as storing the message in a DB until it is deleted
- [ ] Image/other media handling - Backend functionality for a user to be able to send generic data to another user - unsure of the implementation as of yet, likely won't be simply storing the data in the DB as that will lead to provocative file sizes, only storage of media metadata in DB; media itself in the django uploads directory
- [ ] Online statuses - When a user is online, a value representing their online status will be added to a memcached database. Low priority
- [ ] Database models completed - Indicates that all database models have been completed - essentially the product works correctly and is ready to be shipped in terms of messaging infrastructure.
- [ ] Chrome push notifications - Push notifications to Chrome browsers on Android and Desktop could potentially be implemented for notifications when a user is contacted.


### Contributing & Relevant links/tutorials/etc:
##### These are relevant videos to how some of the functionality in this app will work:
Frontend development:
- Beginner's jQuery tutorial (we do all DOM manipulation with jQuery if it's not handled by the template): https://www.youtube.com/watch?v=hMxGhHNOkCU
- Communicating with the server via AJAX (login request and some form validation both use with AJAX): https://www.youtube.com/watch?v=fEYx8dQr_cQ

Sending & receiving messages with websockets (relevant to frontend and backend):
- Understanding websockets and how they differ from HTTP (we'll be sending and receiving messages this way): https://www.youtube.com/watch?v=Y0g3M4VG6Ns
- Great tutorial on Django channels which will likely inspire our implementation, although our implementation is likely to be significantly more complex: https://www.sourcelair.com/blog/articles/115/django-channels-chat

Encryption: 
- Basic explanation of asymmetric encryption (great video that shows the concepts): https://www.youtube.com/watch?v=GSIDS_lvRv4
- Explanation of key exchange using asymmetric encryption (we'll only be using asymmetric crypto for key exchange, not for sending messages): https://www.youtube.com/watch?v=ERp8420ucGs
- JSEncrypt demo: http://travistidwell.com/jsencrypt/demo/index.html

Relevant to two-factor implementation and rate limiting:
- What is memcached and how does it work: https://www.youtube.com/watch?v=-h9q2FmX4eo
- It should be noted that what we're using memcached for at the moment is pretty hacky and not really the usual use-case.

Chrome app manifest and chrome push notifications:
- Chrome manifest details: https://developers.google.com/web/updates/2014/11/Support-for-installable-web-apps-with-webapp-manifest-in-chrome-38-for-Android
- Web push demo: https://goroost.com/try-web-push
- Web push implementation: https://developers.google.com/web/fundamentals/getting-started/codelabs/push-notifications/
