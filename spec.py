from pico import *

Anyone.can([create, read, update, delete],'todos')
AuthenticatedUser.can([read, create],'teams')
Creator.can([update, delete], 'teams')

end()