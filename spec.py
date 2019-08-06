from pico import *

Anyone.can([create, read, update, delete, delete_all],'todos')
AuthenticatedUser.can([read, create],'teams')
Creator.can([update, delete], 'teams')

default_props['todos']={'completed':False}

end()


'''
wishlist

Anyone.can([create, read, update, delete, delete_all], 'todos')
User.can(update, 'todos', props=['completed'] )
default_props['todos']={'completed':False})


spec('Anyone can [create, read, update, delete] todos')
spec('User can update completed in todos')
spec('User can update todos')
spec('default_properties_of todos [completed False]')

'''