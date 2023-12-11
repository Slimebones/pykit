from collections.abc import Collection
from http import HTTPStatus
from typing import Any, Self

from pykit.errors._internals import InternalStringUtils


class NotFoundError(Exception):
    """
    Some entity was not found.
    """
    Code = "slimebones.pykit.errors.error.not-found"

    def __init__(
        self,
        title: str,
        value: Any | None = None,
        options: dict | None = None,
    ) -> None:
        message: str
        titled_value: str

        if value is None:
            titled_value = title
        else:
            titled_value = f"{title}={value}"

        if options is None:
            message = f"{titled_value} not found"
        else:
            message = \
                f"{titled_value} not found for" \
                f" options: {InternalStringUtils.stringify(options)}"
        super().__init__(message)


class PleaseDefineError(Exception):
    """
    Need to define some value before using an object.

    Usually such value is class attribute in confgurable classes.
    """
    Code = "slimebones.pykit.errors.error.please-define"

    def __init__(
        self,
        *,
        cannot_do: str,
        please_define: str,
    ) -> None:
        message: str = f"cannot do {cannot_do}: please define {please_define}"
        super().__init__(message)


class CannotBeNoneError(Exception):
    """
    Some value shouldn't be None.
    """
    Code = "slimebones.pykit.errors.error.cannot-be-none"
    def __init__(
        self,
        *,
        title: str,
    ):
        message: str = f"{title} cannot be None"
        super().__init__(message)


class UnsupportedError(Exception):
    """
    Some value is not recozniged/supported by the system.
    """
    Code = "slimebones.pykit.errors.error.unsupported"
    def __init__(
        self,
        *,
        title: str | None = None,
        value: Any,
    ) -> None:
        message: str

        pre_title: str = ""
        if title is not None:
            pre_title = f"{title}="

        message = f"unsupported value {pre_title}{value}"

        super().__init__(message)


class LogicError(Exception):
    """
    Something out of expected logic happened.
    """
    Code = "slimebones.pykit.errors.error.logic"
    def __init__(
        self,
        message: str,
    ):
        super().__init__(message)


class NoWebsocketConnectionError(Exception):
    """
    When some websocket connection is not found.
    """
    Code = "slimebones.pykit.errors.error.no-websocket-connection"


class StatusChangeError(Exception):
    """
    Wrong origin status on a new status set instruction.
    """
    Code = "slimebones.pykit.errors.error.status-change"

    def __init__(  # noqa: PLR0913
        self,
        *,
        title: str,
        expected_status: Any,
        value: Any | None = None,
        in_order_to_be: str | None = None,
        actual_status: Any | None = None,
    ):
        titled_value: str = InternalStringUtils.get_titled_value(title, value)

        formatted_in_order: str = ""
        if in_order_to_be:
            formatted_in_order = f" in order to be {in_order_to_be}"

        formatted_actual_status: str = ""
        if actual_status:
            formatted_actual_status = \
                f", got actual status={actual_status} instead"

        message: str = \
            f"{titled_value} should have status={expected_status}" \
            f"{formatted_in_order}{formatted_actual_status}"
        super().__init__(message)


class FinalStatusError(Exception):
    """
    Status if final and cannot be changed to anything else.
    """
    Code = "slimebones.pykit.errors.error.final-status"
    def __init__(
        self,
        *,
        final_status: Any,
    ) -> None:
        message: str = \
            f"status <{final_status}> is final and cannot be changed"
        super().__init__(message)


class DuplicateNameError(Exception):
    """
    Not unique constraint failed for name.
    """
    Code = "slimebones.pykit.errors.error.duplicate-name"

    def __init__(
        self,
        *,
        title: str,
        name: str,
    ) -> None:
        self._duplicated_name: str = name

        message: str = f"{title} with name={name} already exists"

        super().__init__(message)

    @property
    def duplicated_name(self) -> str:
        return self._duplicated_name


class IncorrectModelCompositionError(Exception):
    """
    When a model have an incorrect composition of fields for it's type.
    """
    Code = "slimebones.pykit.errors.error.incorrect-model-composition"
    def __init__(
        self,
        *,
        model: Any,
    ) -> None:
        message: str = \
            f"model={model} has an incorrect composition for it's type"
        super().__init__(message)


class RequiredClassAttributeError(Exception):
    """
    Required class attribute is not set.
    """
    Code = "slimebones.pykit.errors.error.required-class-attribute"
    def __init__(
        self,
        *,
        attribute_name: str,
        Class: type,
    ):
        message: str = \
            f"attribute={attribute_name} is required for class={Class}"
        super().__init__(message)


class ExpiredTokenError(Exception):
    Code =  "slimebones.pykit.errors.error.expired-token"

    def __init__(
        self,
        *,
        token_name: str,
    ):
        message: str = f"{token_name} has been expired"
        super().__init__(message)


class AuthError(Exception):
    """
    Authentication/Authorization base error.

    @abstract
    """


class UnauthorizedError(AuthError):
    Code = "slimebones.pykit.errors.error.unauthorized"

    def __init__(
        self,
    ) -> None:
        message: str = "no user is recognized for this request"
        super().__init__(message)


class MalformedHeaderAuthError(AuthError):
    Code =  "slimebones.pykit.errors.error.malformed-header-auth"
    def __init__(
        self,
        *,
        header: str,
    ):
        message: str = f"malformed auth header={header}"
        super().__init__(message)


class ModeFeatureError(Exception):
    """
    Feature is available only for specific application modes.
    """
    Code =  "slimebones.pykit.errors.error.mode-feature"
    def __init__(
        self,
        *,
        feature: str,
        available_modes: list[Any] | Any,
        this_mode: Any | None = None,
    ):
        available_modes_text: str
        if isinstance(available_modes, list):
            available_modes_text = ", ".join([str(m) for m in available_modes])
        else:
            available_modes_text = str(available_modes)

        this_mode_text: str = ""
        if this_mode:
            this_mode_text = f", but this mode={this_mode}"

        message: str = \
            f"feature {feature} is available only for" \
            f" modes={available_modes_text}{this_mode_text}"
        super().__init__(message)


class ForbiddenResourceError(AuthError):
    """
    Resource defined by method and route is forbidden for some user.
    """
    Code = "slimebones.pykit.errors.error.forbidden"

    def __init__(
        self,
        *,
        user: Any,
        method: str,
        route: str,
    ):
        message: str = \
            f"user={user} is not allowed for" \
            f" method={method} route={route}"
        super().__init__(message)


class DisabledAccessTokenError(AuthError):
    Code = "slimebones.pykit.errors.error.disabled-access-token"

    def __init__(
        self,
        *,
        access_token: Any,
        user: Any,
    ):
        message: str = \
            f"access token={access_token} provided by user=" \
            f"{user} is disabled"
        super().__init__(message)


class AbstractUsageError(Exception):
    """
    Attempted to use abstract things.
    """
    Code =  "slimebones.pykit.errors.error.abstract-usage"
    def __init__(
        self,
        *,
        explanation: str | None = None,
        Class: type,
    ) -> None:
        extra: str = ""
        if explanation is not None:
            extra = f"{explanation}: "
        message: str = f"{extra}abstract class={Class}"
        super().__init__(message)


class EmptyInputError(Exception):
    """
    An input data is empty.
    """
    Code =  "slimebones.pykit.errors.error.empty-input"
    def __init__(
        self,
        title: str,
    ):
        message: str = f"{title} input is empty"
        super().__init__(message)


class RequestError(Exception):
    """
    HTTP request failed.
    """
    Code =  "slimebones.pykit.errors.error.request"
    def __init__(
        self,
        *,
        url: str,
        status_code: HTTPStatus,
        error_data: Any | None = None,
    ) -> None:
        titled_value: str = ""
        if error_data:
            titled_value = f", data={error_data}"

        message: str = \
            f"request to url={url} resulted in" \
            f" code {status_code}{titled_value}"
        super().__init__(message)


class AlreadyEventError(Exception):
    """
    Something happened to an object already.
    """
    Code =  "slimebones.pykit.errors.error.already-event"
    def __init__(
        self,
        *,
        title: str,
        value: Any | None = None,
        event: str,
    ):
        titled_value: str = InternalStringUtils.get_titled_value(title, value)
        message: str = f"{titled_value} already {event}"
        super().__init__(message)


class LockError(Exception):
    """Object cannot be changed due to active lock."""
    Code =  "slimebones.pykit.errors.error.lock"
    def __init__(
        self,
        *,
        title: str,
        value: Any | None = None,
        explanation: str | None = None,
    ):
        titled_value: str = title
        if value:
            titled_value = f"{title} {value!s}"

        formatted_explanation: str = ""
        if explanation:
            formatted_explanation = f": {explanation}"

        message: str = f"{titled_value} locked{formatted_explanation}"
        super().__init__(message)


class WrongUsernameError(AuthError):
    Code = "slimebones.pykit.errors.error.wrong-username"

    def __init__(
        self,
        *,
        username: str,
    ):
        message: str = f"no user with such username {username}"
        super().__init__(message)


class WrongPasswordError(AuthError):
    Code = "slimebones.pykit.errors.error.wrong-password"

    def __init__(
        self,
        *,
        username: str,
    ):
        message: str = f"no username {username} with such password"
        super().__init__(message)


class TypeConversionError(Exception):
    """
    Cannot convert one type to another.
    """
    Code =  "slimebones.pykit.errors.error.type-conversion"
    def __init__(
        self,
        *,
        t1: type,
        t2: type | None = None,
        reason: str,
    ):
        second_type_message: str = ""
        if t2 is not None:
            second_type_message = f" to type {t2}"

        message: str = \
            f"cannot convert type {t1}{second_type_message}: {reason}"
        super().__init__(message)


class WrongGenericTypeError(Exception):
    """
    A generic method received a different type than one defined at the
    generic's initialization.
    """
    Code =  "slimebones.pykit.errors.error.wrong-generic-type"
    def __init__(
        self,
        *,
        GenericClass: type,
        ExpectedType: type,
        ReceivedType: type,
    ) -> None:
        message: str = \
            f"generic class {GenericClass} expected a type" \
            f"{ExpectedType}, but got type {ReceivedType} instead"
        super().__init__(message)


class UnsetValueError(Exception):
    """
    Some value is unset.
    """
    Code =  "slimebones.pykit.errors.error.unset-value"
    def __init__(
        self,
        *,
        explanation: str,
    ) -> None:
        message: str = f"{explanation}: has unset value"
        super().__init__(message)


class UnmatchedZipComposition(Exception):
    """
    One of zip() arguments has been exhausted earlier.
    """
    Code =  "slimebones.pykit.errors.composition.unmatched-zip"
    def __init__(
        self,
        *,
        exhausted_title: str,
        exhausted_value: Any,
        other_titles: list[str],
    ) -> None:
        exhausted: str = InternalStringUtils.get_titled_value(
            exhausted_title, exhausted_value,
        )
        other_titles_str: str = ",".join(other_titles)
        message: str = \
            f"iterable {exhausted} is exhausted" \
            f" earlier than {other_titles_str}"
        super().__init__(message)

    @classmethod
    def create_from_iterables(
        cls,
        # Collection is a Sized iterable (applied to len) - that's what we need
        iterables: list[Collection[Any]],
        titles: list[str],
    ) -> Self:
        """
        Creates this error instance out of iterables and their title.

        The iterable with the lowest length, or the last one with lowest length
        in the given list if there are several such iterables, will be
        considered as the exhausted.

        Args:
            iterables:
                List of iterables participated in zip().
            titles:
                List of title strings in corresponding to `iterables` order.

        Returns:
            This error instance created.
        """
        lowest_index: int | None = None
        lowest_len: int | None = None
        lowest_iterable: Collection[Any] | None = None

        iterables_len: int = len(iterables)
        titles_len: int = len(titles)

        if iterables_len == 0:
            raise EmptyInputError(title="iterables")
        elif titles_len == 0:
            raise EmptyInputError(title="titles")
        elif iterables_len > titles_len:
            raise cls(
                exhausted_title="titles",
                exhausted_value=titles,
                other_titles=["iterables"],
            )
        elif iterables_len < titles_len:
            raise cls(
                exhausted_title="iterables",
                exhausted_value=iterables,
                other_titles=["titles"],
            )

        for index, iterable in enumerate(iterables):
            iterable_len: int = len(iterable)
            if (
                lowest_len is None
                or iterable_len < lowest_len
            ):
                lowest_index = index
                lowest_len = iterable_len
                lowest_iterable = iterable

        if lowest_index is None:
            error_message: str = "after a loop lowest index is still None"
            raise LogicError(error_message)
        elif lowest_iterable is None:
            error_message: str = "after a loop lowest iterable is still None"
            raise LogicError(error_message)

        copied_titles: list[str] = titles.copy()
        copied_titles.pop(lowest_index)

        return cls(
            exhausted_title=titles[lowest_index],
            exhausted_value=lowest_iterable,
            other_titles=copied_titles,
        )
