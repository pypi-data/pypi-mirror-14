"""This is the "nestor.py" module, and it provides one function
called print_lol() which prints lists that may or may not include nested lists."""
def print_lol(the_list, doIndent = False, level = 0):
  """This function takes a positional agrument called "the_list", which is any
  Python list (of, possibly, nested lists).  Each data item in the provided list 
  is (recursively) printed to the screen on its own line. The level parameter
  specifies how many tabs to indent the list elements with when printing."""
  for each_item in the_list:
    if isinstance(each_item, list):
      print_lol(each_item, doIndent, level + 1)
    else:
      if doIndent:
        for tab_stop in range(level):
          print('\t', end='')
      print(each_item)
