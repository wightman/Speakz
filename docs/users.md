
# Description

Originally defined in the retwis pakage, a User is a representation of a physical human who will make use of the site.  This user may sign in and out of the site, post messages (Posts) within the site, see recent activity of other users, and update their personal information.

# Attributes


####id:
a unique number that identifies a single user.

####username:
a unique string that identifies a single user. Chosen by user when signing up.  The user is required to enter their username when logging into the website.

####password _(removed in Speakz)_:
secret string that the user will use to authenticate themselves when logging in.


**note**: when password is retrieved, it will be "salted" (i.e. it will contain the salt string)

####firstName:
the first name of the user to be displayed on their profile.

####lastName:
the last name of the user to be displayed on their profile.

####greeting:
a greeting message to be displayed on the users profile.

####followers:
a list of Users (User[]) that are currently following the user.

####followers_count:
the number of Users currently following the user.

####followees:
a list of Users (User[]) that the user is currently following.

####followees_count:
the number of Users that the user is currently following.

####speakz_count:
the number of speakz (Posts) that the user has made.

# Capabilities

####Static User User.find_by_id(int user_id):
retrieves the User with corresponding id from the database.

####Static User User.find_by_username(String username):
retrieves the User with corresponding username from the database.

####Static User User.create(String username, String password, Dict attributes):
creates a new User with the specified username and password.  Attributes are key value pairs where the key is the attribute to be set, value is what that attribute should be set to.

####Speakzs[] speakzs():
returns all posts made by user.

####Post[] timeline(int page=1):
TODO

####Post[] mentions(int page=1):
TODO - list of mentions?

####Post[] recent():
TODO

####None follow(User user):
add a User to the current list of followers.

####None stop_following(User user):
remove a User from the current list of followers.

####None updateAttributes(Dict attributes):
Will write all specified updates to database.

attributes: key value pairs where
* key - name of attribute to update
* value - new value to be saved

####Boolean following(User user):
returns whether User is in current list of followees.
___
# Edit History
* Rick Wightman (wightman@unb.ca) - 2016/11/28 (Converted to markdown, modified for Speakz)
* Aaron Tabor (aarontabor50@gmail.com) - 2013/05/29/ (Created)
