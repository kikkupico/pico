from pico import *

Anyone.can([create, read, update, delete, delete_all],'todos')
AuthenticatedUser.can([read, create],'teams')
Creator.can([update, delete], 'teams')

default_props['todos']={'completed':False}

end()



'''

New style spec based on refined understanding

spec(
Anyone-can-[get]-movies,
Users-can-[post]-tickets,
many-shows-to-one-movies,
many-tickets-to-one-shows,
tickets-validation-
    (given.seats not in flattened /shows/given.show/tickets/seats)
)

'''



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
subactions['todos']={{'mark_done':(update(item.completed, True) for item in given_request())}



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


subaction('shows', read) = ()


one('shows').to.one('movies')

one_to_one('shows', 'movies', as='movie')
relationship('shows', one_to_one, 'movies', as='movie')

rel('shows', have_a, 'movie', from, 'movies')

relationships['item-tags']=[many('items'), many('tags')]
rel('item_tags', have_many, 'items', 'tags')
rel('item_tags', have_one, 'item', from, items')...
rel(many, items, have, many, tags)
rel('movies', have_many, 'shows')

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




STYLES

(movies, shows, tickets) = ('movies'...)

spec(
(Anyone, can, view, shows),
(Users, can, book, tickets),
)

spec(
Anyone.can.view.shows,
Users.can.book.tickets,
)


spec(
Anyone-can-view-shows,
Users-can-book-tickets
)


config(CORS=True,DB=sqllite,logging_level='debug')

spec(
Anyone can view shows
User can book tickets
shows have a 'movie' from movies
tickets have a 'show' from shows
)

spec(
(anyone can view shows)
(user can book tickets)
(shows have one 'movie' from movies)
)

=====================================================
'''
