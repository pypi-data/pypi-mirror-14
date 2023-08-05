# django-simple-email-verification
A view decorator for verifying e-mail addresses

## Example
Let's say that you have the following view:

    def some_view(request):
        return render(request, 'sometemplate.html')
        
... and for whatever reason, you want to make sure that visitors have
verified their e-mail addresses before seeing the view's output:

    from simple_email_verification.decorators import require_verification_token
    @require_verification_token
    def some_view(request):
        return render(request, 'sometemplate.html')
        
By using the ``require_verification_token`` decorator, visitors will be
redirected to a form where they'll be prompted for their e-mail address
before continuing. A verification link will be sent to the address they
entered on the form. Upon clicking the link, they will be "verified"
and redirected to URL they originally attempted to visit.

## Installation & configuration
Standard python installation:

    python setup.py install
    
Then, in ``settings.py``:

    INSTALLED_APPS = [
        ...
        simple_email_verification,
    ]
    
    # Don't forget to configure a valid mail server!
    EMAIL_HOST = 'your.mailserver.tld'
    
    SIMPLE_EMAIL_VERIFICATION = {
        'EMAIL_FROM_ADDRESS': 'donotreply@domain.tld'
    }


### Configuration Options
All options reside in a dictionary, ``SIMPLE_EMAIL_VERIFICATION`` within your project's ``settings.py``. The options are as follows:

    VERIFICATION_FORM_TEMPLATE      Used for overriding the default verification form
    VERIFICATION_EMAIL_SUBJECT      Configures the Subject of the verification e-mail
    VERIFICATION_EMAIL_PLAINTEXT    Used for overriding the default plaintext e-mail template
    VERIFICATION_EMAIL_HTML         Used for overriding the default HTML e-mail template
    GET_TOKEN_PARAM_NAME            Name of the verification token when passed as a GET parameter
    SESSION_TOKEN_PARAM_NAME        Name of the verification token residing in the session
    EMAIL_ADDRESS_PARAM_NAME        Parameter name that contains the e-mail address when posted from the verification form
    EMAIL_FROM_ADDRESS              "From" e-mail address of verification e-mails

To configure any or all of these options, you simply need to define them in ``settings.py``:

    SIMPLE_EMAIL_VERIFICATION = {
        'VERIFICATION_FORM_TEMPLATE': 'myapp/templates/my_custom_form.html',
        'EMAIL_ADDRESS_PARAM_NAME': 'my_custom_email_field',
        'EMAIL_FROM_ADDRESS': 'myaddress@mydomain.tld',
        ...
    }
    
## Tests
To run tests, simply run the ``runtests.py`` script:

    ./runtests.py
    
## Demonstration
To run a demonstration using the included templates and default settings, first configure the necessary items:

    INSTALLED_APPS = [
        simple_email_verification,
    ]
    
    # Configure a valid mail server here!
    EMAIL_HOST = 'your.mailserver.tld'
    
    # Configure an e-mail address will be successfully relayed 
    # by the mail server specified by 'EMAIL_HOST'
    SIMPLE_EMAIL_VERIFICATION = {
        'EMAIL_FROM_ADDRESS': 'donotreply@domain.tld'
    }
    
Next, using the included ``manage.py``, execute the following command:

      ./manage.py migrate --run-syncdb; ./manage.py runserver
      
Finally, open a web browser to http://127.0.0.1/test/ ... you should see
the e-mail verification form. Fill out and submit the form, then check
your e-mail. You should have an e-mail with a link that looks something 
like this:

    http://localhost:8000/test/?get_verification=A7RvITNH_8seAWrZ4I3sZv3_AQzrYE6CoEYz8hXYTVk=
    
Click the link, and you should receive the following JSON response:

    {"response_data": "email address verified"}


        

