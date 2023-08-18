# Antievil 😈

Collection of Errors/Exceptions for different programming languages.

Due to different naming conventions in programming languages, the error objects
are suffixed with `Exception` or `Error`. For simplicity, the general
specification uses `Error` as a main suffix.

General Specification arguments' types are written in Python style, different
languages will have different *respective* types. For example for Python's
`Any` there might be C#'s `object` and TS's `any`.

## Error Specification


### 🔎 NotFoundError (ERROR.NOT_FOUND)

#### Arguments

##### title: string

Friendly name of an object that was not found.

##### value: Any | None = None

Which value an object has which had been obstructed the search. For example
for `title="person with name"`, value might be set to the name, which hadn't
been found.

There is no value mentioned by default.

##### options: dict | None = None

Map with extra options used during the searching.

Defaults to None.

#### Description

Some object was not found.


### 😠 PleaseDefineError

*...in writing*
