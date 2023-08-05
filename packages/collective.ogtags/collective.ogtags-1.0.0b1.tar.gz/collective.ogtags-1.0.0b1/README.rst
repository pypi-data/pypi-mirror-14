Introduction
============

This packages provides Open Graph tags similar to those built in in plone 5.
Basically this is an attempt to backport the social media viewlet of
plone.app.layout in plone 5 to plone 4.

#### What is Open Graph
Open Graph is a specification developed by Facebook to provide information
about a webpage. This information is used by social media sites to get title,
author, description, url, images and more in order to create a marked up link.

Installation
============

 - add collective.ogtags to your eggs and run buildout
 - go to the add-ons page in the plone control panel and install
   collective.ogtags

Settings
========

Go to the ogtags settings in the plone control panel. Provide as much of the
following settings as possible:

 - Site name:
        Provide the name of your site here.
 - Facebook username:
        Provide your facebook username. You can find this by going to your
        facebook page. The format is:
        "https://www.facebook.com/<facebook_username>"
 - Facebook app id:
        Provide your facebook app id. Go to
        "https://developers.facebook.com/apps", choose your app and look for
        your app id in the description.
 - Twitter username:
        Provide your twitter name. The @-sign included, for example:
        @zestsoftware
 - Default image:
        Provide the URL to an image to be used in case no other image can be
        found. By default this will be /logo.png.
