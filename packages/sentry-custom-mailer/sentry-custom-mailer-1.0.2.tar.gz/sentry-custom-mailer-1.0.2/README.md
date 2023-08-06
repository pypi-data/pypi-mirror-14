# Sentry Custom Mailer
The Sentry Mail plugin sends emails to users who have subscribed to certain project notifications. This plugin that allows a project administrator to specify certain recipients of notification for the given project. In the configuration, the administrator can view all the recipients who are currently set to receive emails from this plugin, as well as add or remove users. 

This plugin does not affect Sentry Mail; users will still receive notifications if they are subscribed to a project, regardless of this plugin. 

## Installation
The plugin will be enabled by default upon installation and resetting Sentry, and will just require configuration. 

From pip:  
`pip install sentry-custom-mailer`  
From source:  
`python setup.py install`  

## Configuration
In Sentry project settings, go to the configuration settings for "Custom Mailer" and enter all email addresses that should receive notifications for that project. 
