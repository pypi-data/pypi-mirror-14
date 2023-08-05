# pylint-peewee

## Foreward

Do you use PeeWee? Do you also use PyLint? And the PeeWee flask_util?

Are you tired of getting PyLint errors like:

```
************* Module application.models.base
E: 32,15: Class 'BaseModel' has no 'get' member (no-member)
E: 45,16: Class 'BaseModel' has no 'select' member (no-member)
************* Module application.models.client_settings
E: 40,19: Class 'Settings' has no 'create' member (no-member)
E: 53,12: Class 'Settings' has no 'select' member (no-member)
E: 68,23: Class 'Settings' has no 'select' member (no-member)
E: 81,17: Class 'Settings' has no 'select' member (no-member)
```

Just because you're using flask_util?

If so, this is the plugin for you!

## How it Works

This plugin works very simply by hooking into ASTroid's Class Parser, seeing if 
the current class has a base of: db.Model (the standard for flask_util) and, if
so, it stubs out all the missing methods of: 'create', 'select', 'update', etc.

The methods are stubbed out by returning a class with the proper members, which
are all functions with a `pass` implementation.

## TODO

1. Make the base class configurable, so you can use Model, MyModel, peewee.Model, what have you.
