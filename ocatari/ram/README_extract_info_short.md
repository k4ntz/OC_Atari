The script 'extract_ram_info_short' is a try to generalize the methods of the games so that in 'extract_ram_info'
doesn't need to be added a case for every new game.
When you want to use it, you have to change all the method names of every game that
is currently implemented. This is the same for its equivalent 'extract_vision_info_short'

Another way was to use importlib with import_module and then getattr, which we didn't get to work or exec,
which would be time consuming for every call or didn't handle exceptions rightly.
