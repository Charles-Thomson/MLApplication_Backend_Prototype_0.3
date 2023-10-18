Running tests should be done from within the Django_main package

have to set the DJANGO_SETTINGS_MODULE at the root level
cmd -> 
set DJANGO_SETTINGS_MODULE=django_main.settings pytest
set DJANGO_SETTINGS_MODULE=django_main.settings