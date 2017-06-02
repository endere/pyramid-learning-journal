# pyramid-learning-journal

#Author: Erik Enderlein
##(with assistance from Chris Hudson)

##site: https://endere-learning-journal.herokuapp.com/

### Routes and Views: 


###Routes
    -Routes the home page to /
    -routes the detail page for entrieds to /journal(entry id)
    -routes the new entry page(create) to /journal/new-entry
    -routes the edit page to /journal/(entry id)/edit-entry

###Views:
    -List view for the home page(s) to main.html
    -detail view for each entry page to entry.html
    -create view for making a new entry to new-entry.html
    -edit view for editing an entry to edit_entry.html
    
    
  ```
----------- coverage: platform linux, python 3.6.1-final-0 -----------
Name                                           Stmts   Miss  Cover
------------------------------------------------------------------
pyramid_learning_journal/data/__init__.py          0      0   100%
pyramid_learning_journal/data/data.py              1      0   100%
pyramid_learning_journal/scripts/__init__.py       0      0   100%
pyramid_learning_journal/views/default.py         27      0   100%
------------------------------------------------------------------
TOTAL                                             28      0   100%
```
