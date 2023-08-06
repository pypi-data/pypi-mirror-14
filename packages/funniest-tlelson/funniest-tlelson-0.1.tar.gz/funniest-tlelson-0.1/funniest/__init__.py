## Putting the method in the __init__.py like this is equivilent to
## the import below. Note that the package name is used.

## Both methods allow importing the package (funniest) as a module and using
## the functions like:
##  >>> import funniest
##  >>> funniest.joke()

## N.B that because we don't import main() here to use it we must import
## it from the module it belongs to (command_line)
##  >>> from funniest.command_line import main

#from markdown import markdown
#
#
#def joke():
#    return markdown(u'Wenn ist das Nunst\u00fcck git und Slotermeyer?'
#                    u'Ja! ... **Beiherhund** das Oder die Flipperwaldt '
#                    u'gersput.')


from funniest.joke_file import joke

##
