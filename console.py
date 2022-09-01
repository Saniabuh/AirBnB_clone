#!/usr/bin/python3
"""
This module contains the command line interpreter
"""

import cmd
import models
from models.base_model import BaseModel
from models.user import User
import shlex

classes = {"BaseModel": BaseModel, "User": User}


class HBNBCommand(cmd.Cmd):
    """
    Implementation of the command line interpreter
    """

    prompt = '(hbnb) '

    def do_EOF(self, line):
        """Handling the EOF command"""
        return True

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def emptyline(self):
        """Called when an empty line is entered"""
        pass

    def do_create(self, line):
        """Creates a new instance and prints the id"""
        args = shlex.split(line)
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            instance = classes[args[0]]()
            print(instance.id)
            instance.save()
        else:
            print("** class doesn't exist **")
            return False

    def do_show(self, line):
        """Prints an instance based on the class name and id"""
        args = shlex.split(line)
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            if len(args) > 1:
                model = args[0] + "." + args[1]
                if model in models.storage.all():
                    print(models.storage.all()[model])
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id"""
        args = shlex.split(line)
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            if len(args) > 1:
                model = args[0] + "." + args[1]
                if model in models.storage.all():
                    models.storage.all().pop(model)
                    models.storage.save()
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_all(self, line):
        """Prints all string representation of all instances"""
        hold = []
        args = shlex.split(line)
        if len(args) < 1:
            for key in models.storage.all().keys():
                hold.append(str(models.storage.all()[key]))
        elif args[0] in classes:
            for key in models.storage.all().keys():
                if args[0] in key:
                    hold.append(str(models.storage.all()[key]))
        else:
            print("** class doesn't exist **")
            return False
        print(hold)

    def do_update(self, line):
        """Updates an instance based on the class name and id"""
        args = shlex.split(line)
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes and len(args) >= 4:
            model = args[0] + "." + args[1]
            if model in models.storage.all():
                setattr(models.storage.all()[model], args[2], args[3])
                models.storage.all()[model].save()
            else:
                print("** no instance found **")
        elif len(args) == 1 and args[0] in classes:
            print("** instance id missing **")
        elif len(args) == 2 and args[0] in classes:
            model = args[0] + "." + args[1]
            if model in models.storage.all():
                print("** attribute name missing **")
            else:
                print("** no instance found **")
        elif len(args) == 3 and args[0] == classes:
            model = args[0] + "." + args[1]
            if model in models.storage.all():
                print("** value missing **")
            else:
                print("** no instance found **")
        else:
            print("** class doesn't exist **")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
