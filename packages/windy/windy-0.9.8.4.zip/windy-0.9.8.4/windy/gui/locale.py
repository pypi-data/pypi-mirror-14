# -*- coding: utf-8 -*-
'''
Created on Feb 26, 2016

@author: zeljko.gavrilovic
'''
import enum


class Locale(enum.Enum):
    windy_title = "Windy - Editor for Windows environment variables"
    scope = "Scope"
    name = "Name"
    value = "Value"
    system_permission_title = "System environment variables permission"
    system_permission_desc = r"You have started the application with NO ADMIN RIGHTS. In order to change the system environment variables you need to open the application in the admin mode. Otherwise you are allowed to edit only user environment variables..."
    env_variables = "Environment variables"
    remove = "Remove"
    edit = "Edit"
    add_new = "Add new"
    env_var_selection = "Environment variable selection" 
    env_var_selection_edit = "Please select a row to be edited"
    env_var_selection_remove = "Please select a row to be removed"
    env_var_delete_title = "Delete"
    env_var_delete_desc = "Are you sure you want to remove the environment variable {name}?"
    content_import = "Content to be imported"
    system="System"
    from_file="From file..."
    clear_content="Clear content"
    save="Save"
    close="Close"
    cancel="Cancel"
    new="New"
    importThreeDots = "Import..."
    empty_content_title="Empty content not allowed"
    empty_content_desc="Empty content for the import is not allowed. Please add some environment variables."
    bad_format_title="Bad format or empty value", 
    bad_format_desc="Bad format or empty entries for the line {line}. Please use name=value format."
    import_file_title="Import environment variables"
    import_file_desc="Cannot persist changes. You need to open the application in the admin mode in order to change system environment variables..."
    
    env_var_title="Enter the new environment variable"
    empty_entry_not_allowed_title="Empty entry not allowed"
    empty_entry_not_allowed_desc="Please fill both the name and the value of the environment variable"
    admin_role_title="Add/update Environment variable"
    admin_role_desc="Cannot persist changes. You need to open the application in the admin mode in order to change the system environment variables..."
    file="File"
    exit="Exit"
    help="Help"
    about_title="About"
    about_desc="""
Windy
=====

Short description
----
Windy is an application for managing Windows user/system environment variables. 

Features
--------
* Add/update/remove of the environment variables
* Batch import of the environment variables from a file or a clipboard
* Resizable GUI with the examined views
* Absolutely free and open source

Homepage
--------
git [link](https://github.com/zeljko-m-gavrilovic/windy)
pyPI [link](https://pypi.python.org/pypi/windy)

Notes
----
Tested on Windows 7 and Windows 8

Credits
-------
Icon Author Website [link](http://www.iconsmind.com)
    """
    about="About"
    
    
if __name__ == "__main__":
    print("dddd")
    print(Locale.scope.value)
    print(Locale.importThreeDots.value)
