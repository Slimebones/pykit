# 0.7.0

- query: Query.disallow() now rejects disallowed upd operators, also fixed modifies of the
    origin query (copy is made)
- query: added subclasses for each query type
- query: Query.as_search_sid -> SearchQuery.create_sid
- query: Query.as_upd -> UpdQuery.create
- query: added AggQuery to handle aggregation pipelines
- added proc.py::ProcGroup to manage multiprocessing
- removed yml.py for good (using pyyaml directly is enough straightforward)
- added range.py::Range
- added keeper.py to manage smart data containers
- restructured FnSpec into FuncSpec, with generic addition
- added ArbitraryFunc(Protocol), accepting arbitrary number of args and kwargs
- res: added raise_err_val(), try_or_res() helper functions
- query: Query.copy now automatically does deepcopy

# 0.6.0

- add Result and res.py with helpers
- add ref.py - value storage

# 0.5.1

- import fix

# 0.5.0

- many things happened since our last met... who knows what are they...

# 0.4.14

- Add Log.

# 0.4.13

- Rename package to slimebones-pykit.

# 0.4.12

- Added env.py.

# 0.4.11

- Removed ObjectInfo in favor of simple strings.

# 0.4.10

- Added missing imports.

# 0.4.9

- Added StrExpectError, NameExpectError now inherits this class.
- Made error strings less polluted with symbols.

# 0.4.8

- Refactored FuncSpec, fn -> func.

# 0.4.7

## Refactor

- New keycode format

# 0.4.6

## Fixes

- Fixed MapUtils location search bug.


# 0.4.5

## Fixes

- Fixed YML type checking.

# 0.4.4

## Refactor

- Renamed mp module to map.

# 0.4.3

## Fixes

- Corrected by tests.
- API fixes.

# 0.4.2

## Features

- Added StringUtils.
- Codes added to all active errors.

## Fixes

- Installed bcrypt to support `crypto.py`
- Codes are renamed to proper KeyCode format.

## Refactor

- Renamed inner package to `pykit` (instead of old `sbpykit`).

# 0.4.1

## Fixes

- Move pytest-asyncio to dev deps

# 0.4.0

## Features

- Integrate Orwynn utils.

# 0.3.0

## Refactor

- Merged to pykit.

# 0.2.0

## Features

- TypeExpectError now accepts multiple expectations.

## Refactor

- Restructured project to the normal python-project view.
- Removed enum codes, replaced to string ones.
