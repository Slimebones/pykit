# CHANGELOG

## 0.4.9

- Added StrExpectError, NameExpectError now inherits this class.
- Made error strings less polluted with symbols.

## 0.4.8

- Refactored FuncSpec, fn -> func.

## 0.4.7

### Refactor

- New keycode format

## 0.4.6

### Fixes

- Fixed MapUtils location search bug.


## 0.4.5

### Fixes

- Fixed YML type checking.

## 0.4.4

### Refactor

- Renamed mp module to map.

## 0.4.3

### Fixes

- Corrected by tests.
- API fixes.

## 0.4.2

### Features

- Added StringUtils.
- Codes added to all active errors.

### Fixes

- Installed bcrypt to support `crypto.py`
- Codes are renamed to proper KeyCode format.

### Refactor

- Renamed inner package to `pykit` (instead of old `sbpykit`).

## 0.4.1

### Fixes

- Move pytest-asyncio to dev deps

## 0.4.0

### Features

- Integrate Orwynn utils.

## 0.3.0

### Refactor

- Merged to pykit.

## 0.2.0

### Features

- TypeExpectError now accepts multiple expectations.

### Refactor

- Restructured project to the normal python-project view.
- Removed enum codes, replaced to string ones.
