# 0.11.1

- renamed tb.py -> traceback.py
- traceback: added create_traceback()

# 0.11.0

- log: track now writes obvious err data if traceback is unavailable
- log: track now accepts Res::Err and extracts formatted stacktrace
- res: added traceback to errors initialized with Err()
- added tb.py for working with traceback

# 0.10.0

- renamed pointer -> ptr
- fixed Lock incorrect behaviour
- integrated "reg" abbreviation
- added Code.get_regd_codeid_by_type()
- removed io.py
- added log.track and log.atrack
- added res.track and res.atrack

# 0.9.2

- renamed Res._ignore -> Res.ignore

# 0.9.1

- removed `cls` from create_err_dto

# 0.9.0

- removed fcode; added lightweight analog code.py
- removed ValueErr, use ValErr instead
- removed benedict; removed map.py
- forked rustedpy/result into res.py; updated result API
- added lock.py to support async locking mechanisms
- deprecated RandomUtils; added uuid::uuid4()

# 0.8.0

- added d.py - tools for working with dicts
- added t.py - tools for working with time
- deprecated map.py::MapUtils, use d.py instead
- deprecated dt.py::DtUtils, use t.py instead

- query: fixed call without arguments error (like Query())
- query: added CreateQuery
- query: added SearchQuery.check, support for $sort and $limit operators
- query: implemented Query.get_recursive()
- removed search.py

- res: ensured re-exports Ok and Err
- res: added eject() - alternative to unwrap if you want to raise the original error from Res object

- env: deprecated EnvUtils, added module-level improved alternatives

- proc: added ProcGroup.proc_dereg_method which defines how processes will be ended (kill or terminate)
- proc: fixed reg(proc_kwargs) no default state

# 0.7.1

- fixed mark.py quieries

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
