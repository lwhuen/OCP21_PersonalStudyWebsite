# Week 5 glossary — exceptions and the date-time API

Terms from [Week-05-notes.md](Week-05-notes.md). The exam words are English. Friday 25 Dec is off.

## Monday — `try`, `catch`, `finally`

| Term | Meaning |
|---|---|
| `Throwable` | The parent of `Error` and `Exception`. |
| `Error` | A serious JVM failure, such as `OutOfMemoryError` or `StackOverflowError`. Ordinary code does not catch it and does not declare it. |
| Checked exception | An `Exception` that is not a `RuntimeException`, such as `IOException`. The caller catches it or declares it. `Exception` itself is checked. |
| Unchecked exception | `RuntimeException` and its subclasses, such as `NullPointerException`, `IllegalArgumentException`, `ClassCastException`, and `ArithmeticException`. No `throws` clause is required. |
| `catch` order | Specific type first, then the parent type. A later catch of a child of an earlier catch does not compile. |
| Multi-catch | `catch (A \| B e)`. The alternatives cannot be related by inheritance. `e` is effectively final. |
| `finally` | Runs on the way out of `try` and `catch`, including when the `try` returns. If `finally` throws, that exception replaces the pending one. The pending one is not added as a suppressed exception. |

## Wednesday — resources and custom exceptions

| Term | Meaning |
|---|---|
| Try-with-resources | A `try` that declares resources in parentheses. Each type implements `AutoCloseable`. |
| Close order | After the body, resources close in reverse order of creation. The first one created is the last one closed. |
| Suppressed exception | When the body throws and `close` also throws, the body’s exception propagates and the close exception is added with `addSuppressed`. |
| Effectively final resource | A resource variable cannot be reassigned, including one declared outside and named in the parentheses. |
| Custom checked exception | A class that extends `Exception` and not `RuntimeException`. Callers must catch it or declare it. |

## Saturday — date and time

| Term | Meaning |
|---|---|
| `LocalDate` | A date, with no time and no zone. |
| `LocalTime` | A time, with no date and no zone. |
| `LocalDateTime` | A date and a time, with no zone. |
| `Instant` | A point on the UTC timeline. |
| `Period` | A date-based amount: years, months, and days. Printed as `P2D`. |
| `Duration` | A time-based amount: hours, minutes, seconds, and nanos. Printed as `PT2H30M`. |
| Immutable date | `plusDays` and the other `plus` methods return a new object. The original variable does not change until you assign the result. |
| `Period.between` | The period from the start date to the end date. |
| Date plus `Duration` | `LocalDate.plus(Duration)` throws `UnsupportedTemporalTypeException`. A date has no time fields. `LocalTime` accepts a `Duration`. An `Instant` accepts a `Duration` and rejects a `Period`. |

## Sunday — zones and formatters

| Term | Meaning |
|---|---|
| `ZonedDateTime` | A date, a time, and a zone. |
| Gap | A local time that does not exist, such as 02:30 in `America/New_York` on 8 March 2026. `ZonedDateTime.of` moves it forward. That call produces `2026-03-08T03:30-04:00`. |
| Overlap | A local time that happens twice, such as 01:30 in New York on 1 November 2026. `ZonedDateTime.of` picks the earlier offset, `-04:00`. `ofLocal` can pick `-05:00` when you pass that offset. |
| `DateTimeFormatter` | Turns a date or time into text from a pattern, or parses text. Use `Locale.US` when the pattern includes words. |
| `yyyy` | The year. `uuuu` is also the year. |
| `MM` | The month, with a leading zero. `MMM` is the short name (`Dec`). `MMMM` is the full name (`December`). |
| `dd` | The day of the month. |
| `HH` | The hour from 0 to 23. `h` is the hour on a 12-hour clock. `a` is the AM/PM marker. |
| `D` | The day of the year. 21 December 2026 is `355`. |
| `q` | The quarter. December is `4`. |
| `e` | The numeric day of the week for the locale. In `Locale.US` the week starts on Sunday, so Monday is `2`. |
| `EEE` | The short weekday name. 21 December 2026 is `Mon`. |
| Quoted pattern text | Characters in single quotes are literals. `yyyy-MM-dd'T'HH:mm` keeps the `T`. |
| `ISO_LOCAL_DATE` | The predefined formatter `yyyy-MM-dd`. |
