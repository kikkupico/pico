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



Anyone.can(create,read,update,delete todos)
PermittedUser.can(create, read, update, delete todos)



persona('PermittedUser').can([create,read,update,delete], 'todos')

User.subpersona('PermittedUser', check=...)) 



SUBPERSONA CREATION ALTERNATIVES
User.subpersona('Creator', check=lambda:current_user.id == item.creator))
User.subpersona('Creator', when=(current_user.id == item.creator for current_user, item in given_request()))
User.subpersona('Creator', condition=(info.current_user.id == info.item.creator for info in given_request()))


custom_actions['todo']={'mark_done':make(item.completed=True)}



spec('Anyone can [create, read, update, delete] todos')
spec('User can update completed in todos')
spec('User can update todos')
spec('default_properties_of todos [completed False]')




=====================================================
MOVIE TICKET BOOKING APP

Anyone can view shows
Users can book tickets

shows have a movie, a screen (and time/,date)
tickets have a user, a show, some ticket numbers


...

relationships['shows']=[one('movies'), one('screens')]
relationships['tickets']=[one('shows')]



relationships['shows']={'movie':one('movies'), 'screen':one('screens')}
relationships['tickets']{'show':one('shows')}



one('shows').to.one('movies')

relationships['item-tags']=[many('items'), many('tags')]




SHOPPING APP

Customers can create orders

relationships[orders]={items:many(order_items)}
relationships[order_items]={product:one(products)}
relationships[product_categories]={product:many(products), category:many(categories)}

each(orders).has_many(order_items)
each(order_items).has_one(products)

each['orders'] = has_many(order_items)
each[order_items] = has_

each order has many order_items

=====================================================
'''
