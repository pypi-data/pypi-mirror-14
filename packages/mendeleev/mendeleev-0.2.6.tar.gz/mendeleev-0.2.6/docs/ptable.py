
from mendeleev import periodic_plot, get_table

ptable = get_table('elements')

periodic_plot(ptable, output='ptable.html', width=700)

