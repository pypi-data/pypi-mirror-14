Copyright (c) 2016 Matthew Wilkes

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Description: django-dob-widget
        =================
        
        |Build Status|
        
        A Django date widget optimised for usability in entering dates of birth.
        
        This is based on the guidelines put forward by the UK Government Digital
        Service at
        https://designnotes.blog.gov.uk/2013/12/05/asking-for-a-date-of-birth/
        
        Usage:
        
        ::
        
            from django import forms
            from dobwidget import DateOfBirthWidget
        
            class PersonModelForm(forms.ModelForm):
                """
                Model form for people.
                """
                
                class Meta(object):
                    model = Person
                    fields = ['name', 'date_of_birth']
                    widgets = {
                        'date_of_birth': DateOfBirthWidget(),
                    }
              
        
        The DateOfBirthWidget can take an optional order parameter, to make it
        useful in non-UK jurisdictions:
        
        ::
        
                class Meta(object):
                    model = Person
                    fields = ['name', 'date_of_birth']
                    widgets = {
                        'date_of_birth': DateOfBirthWidget(order='MDY'),
                    }
        
        Changes
        -------
        
        1.1.1
        ~~~~~
        
        -  Bug fix around character-based input
        
        1.1.0
        ~~~~~
        
        -  Allow attrs of the individual subwidgets to be set using day\_attrs,
           month\_attrs and year\_attrs.
        
        1.0.0
        ~~~~~
        
        -  Initial release
        
        Authors
        -------
        
        -  "Matthew Wilkes" matt@matthewwilkes.name
        
        .. |Build Status| image:: https://travis-ci.org/MatthewWilkes/django-dob-widget.svg?branch=master
           :target: https://travis-ci.org/MatthewWilkes/django-dob-widget
        
Keywords: django,widget,date
Platform: linux
Classifier: Development Status :: 3 - Alpha
Classifier: Environment :: Web Environment
Classifier: Framework :: Django
Classifier: Intended Audience :: Developers
Classifier: License :: OSI Approved :: BSD License
Classifier: Operating System :: Unix
Classifier: Programming Language :: Python
Classifier: Programming Language :: Python :: 2
Classifier: Programming Language :: Python :: 2.7
Classifier: Programming Language :: Python :: 3
Classifier: Programming Language :: Python :: 3.3
Classifier: Programming Language :: Python :: 3.4
Classifier: Topic :: Other/Nonlisted Topic
