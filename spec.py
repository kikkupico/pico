from pico import *

Anyone.can([list, create],'todos')
Anyone.can([retrieve, update, delete],'todos')
AuthenticatedUser.can([list, create],'teams')
