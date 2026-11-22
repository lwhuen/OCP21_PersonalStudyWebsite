# Week 5 notes — exceptions and the date-time API

**21–27 Dec 2026. 15 hours.** Friday 25 Dec is off. This file follows Week 5 of the study plan. The gate is the exceptions and date-time questions at **70%** (14 of the 20 questions in this file).

Monday and Wednesday are 3 hours each: 20 minutes on yesterday’s misses, 2 hours typing every listing, 40 minutes of questions and the notebook. Friday is a day off. Saturday is 6 hours. Sunday is 3 hours: the daylight-saving listing, 15 formatter predictions, and the questions. Monday’s first 20 minutes are the Week 4 misses.

| Day | What the plan says | Where it is in this file |
|---|---|---|
| Mon | `try` / `catch` / `finally`, multi-catch, checked versus unchecked | Chapter 1, questions Q1–Q6 |
| Wed | Try-with-resources and a custom checked exception | Chapter 2, `Doors`, `Pay`, questions Q1–Q4 |
| Fri 25 Dec | Off | — |
| Sat | `LocalDate`, `LocalTime`, `LocalDateTime`, `Period`, `Duration`, `Instant` | Chapter 3, `Dates`, questions Q1–Q5 |
| Sun | One daylight-saving example, 15 formatter predictions, then questions | `Dst`, the 15 patterns, questions Q1–Q5, then score all 20 |

Same checklist as the study plan:

- [ ] From memory: checked versus unchecked versus `Error`, and what `finally` does when the catch block throws.
- [ ] A custom checked exception, and a try-with-resources class whose close messages print in reverse order of creation.
- [ ] `LocalDate`, `LocalTime`, `LocalDateTime`, `Instant`, `Period`, and `Duration`. `Period` is date-based. `Duration` is time-based. `plusDays` returns a new object.
- [ ] On a real daylight-saving date, show a local time that is skipped or repeated, and what `ZonedDateTime` does.
- [ ] Predict 15 `DateTimeFormatter` patterns, then run them.
- [ ] Exceptions and date-time questions at 70%.

Predict each listing before you run it. Each miss goes in the notebook as one rule and a five-line program.

The questions are practice in the exam’s style. They are not copied from the real exam or from a book. Try each one before its answer key.

---

# Chapter 1 — `try`, `catch`, `finally`

> **必睇**　第 11 章 Exceptions and Localization，pp. 614–636：由 “Understanding Exceptions” 到 “Adding a finally Block”。
>
> **唔使睇**　“Automating Resource Management”（p. 637）係星期三。p. 646 起嘅格式同 locale 留星期日同第 8 週。Review Questions 唔使做。

**Monday** is this chapter and questions Q1–Q6.

## What you must know

`Throwable` has two branches. `Error` means the JVM is in trouble (`OutOfMemoryError`, `StackOverflowError`). You do not catch `Error` in ordinary code, and you do not declare it. `Exception` splits again:

- Unchecked: `RuntimeException` and its subclasses, such as `NullPointerException`, `IllegalArgumentException`, `ClassCastException`, and `ArithmeticException`. A method may throw them without a `throws` clause.
- Checked: other `Exception` subclasses, such as `IOException` and `FileNotFoundException`. The caller catches them or declares them. `Exception` itself is checked. `RuntimeException` is not.

`catch` clauses are tried in order. A later catch cannot use a parent of an earlier catch, or the earlier one would have taken everything. `catch (FileNotFoundException | IOException e)` does not compile, because the alternatives are related by inheritance. The parameter of a multi-catch is effectively final.

`finally` runs after `try` and after `catch`, on the way out, including when the `try` returns. A `System.exit` call is the case that skips it. If `finally` throws, that exception replaces the one that was pending from `try` or `catch`. The pending one is not added as a suppressed exception. Suppressed exceptions belong to try-with-resources, which is Wednesday.

This method prints `catch finally-ran` when `finally` does not throw, because `finally` runs and then the catch exception continues:

```java
try {
    throw new RuntimeException("try");
} catch (RuntimeException e) {
    throw new RuntimeException("catch");
} finally {
    System.out.print("finally-ran ");
}
```

When `finally` itself throws `new RuntimeException("finally")`, the caller sees the message `finally`, and `getSuppressed()` is empty.

Monday’s questions are Q1–Q6.

## Chapter 1 questions

**Q1.** Which type is checked?

A. `IllegalArgumentException`
B. `IOException`
C. `NullPointerException`
D. `StackOverflowError`

**Q2.** What reaches the caller?

```java
try {
    throw new RuntimeException("try");
} catch (RuntimeException e) {
    throw new RuntimeException("catch");
} finally {
    throw new RuntimeException("finally");
}
```

A. The message `try`, with `catch` suppressed
B. The message `catch`, with `finally` suppressed
C. The message `finally`, and `getSuppressed()` is empty
D. The code does not compile

**Q3.** Does this compile?

```java
try {
    throw new java.io.FileNotFoundException();
} catch (java.io.FileNotFoundException | java.io.IOException e) {
}
```

A. Yes
B. Yes, and `e` can be assigned a new exception
C. No. The two types are related by inheritance
D. No. `FileNotFoundException` is unchecked

**Q4.** This method returns a `String`. The caller does not print the returned value. What does the method print?

```java
static String go() {
    String s = "go";
    try {
        s = s + " try";
        return s;
    } finally {
        s = s + " finally";
        System.out.print(s);
    }
}
```

A. `go try`
B. `go try finally`
C. `go finally`
D. The code does not compile

**Q5.** Which catch order compiles?

```java
catch (Exception e) { }
catch (RuntimeException e) { }
```

A. This order
B. The same catches swapped, with `RuntimeException` first
C. Both orders
D. Neither. `RuntimeException` cannot be caught

**Q6.** A method calls `Files.readString` and does not catch `IOException` or declare it. What is the result?

A. It compiles. `IOException` is unchecked
B. It compiles. `finally` is implied
C. It does not compile
D. It compiles and throws `Error` if the file is missing

### Chapter 1 answers

**Q1 — B.** `IOException` is a checked `Exception`. The two runtime exceptions are unchecked. `StackOverflowError` is an `Error`.

**Q2 — C.** A `finally` that throws becomes the exception that leaves the statement. On this JDK the pending `catch` exception is not in `getSuppressed()`.

**Q3 — C.** Multi-catch alternatives cannot be subclasses of each other. Catch `FileNotFoundException` in its own clause before `IOException`, or catch only `IOException`.

**Q4 — B.** `finally` runs before the `return` completes. The print sees `go try finally`. The returned string is still `go try`, because `return` already captured that value. This question asks for the print.

**Q5 — B.** The specific type comes first. A later `RuntimeException` catch is unreachable once `Exception` has been caught.

**Q6 — C.** `IOException` is checked. The method must catch it or add `throws IOException`.

---

# Chapter 2 — Try-with-resources and a custom checked exception

> **必睇**　第 11 章 “Automating Resource Management”，pp. 637–645。自訂 checked exception 在 “Throwing an Exception”（p. 618）；星期一未讀完就補呢一節。
>
> **唔使睇**　p. 646 之後今日唔好睇。

**Wednesday** is this chapter, `Doors`, `Pay`, and questions Q1–Q4.

## What you must know

A try-with-resources declares resources in parentheses. Each resource’s type implements `AutoCloseable`. The resources close automatically, after the body, in reverse order of creation. The first one created is the last one closed.

If the body throws and `close` also throws, the body’s exception is the one that propagates. Each exception from `close` is added with `addSuppressed`. This is different from a `finally` that throws.

The resource variable is effectively final. Assigning it inside the body does not compile.

A custom checked exception extends `Exception` and not `RuntimeException`. Callers must catch it or declare it.

### `Doors`

```java
class Door implements AutoCloseable {
    private final String name;
    Door(String name) {
        this.name = name;
        System.out.print(name);
    }
    public void close() {
        System.out.print(name.toLowerCase());
    }
}
public class Doors {
    public static void main(String[] args) {
        try (Door a = new Door("A"); Door b = new Door("B")) {
            System.out.print("-");
        }
    }
}
```

The run prints:

```text
AB-ba
```

`A` and `B` are constructed, the body prints `-`, then `B` closes, then `A` closes.

### `Pay`

```java
class BadAmount extends Exception {
    BadAmount(String message) { super(message); }
}
public class Pay {
    static void charge(int cents) throws BadAmount {
        if (cents <= 0) {
            throw new BadAmount("cents");
        }
    }
    public static void main(String[] args) throws BadAmount {
        charge(50);
        System.out.println("charged");
    }
}
```

The run prints:

```text
charged
```

Remove `throws BadAmount` from `main` and `main` does not compile. `charge(-1)` throws `BadAmount` before `charged`.

Wednesday’s questions are Q1–Q4.

## Chapter 2 questions

**Q1.** What does `Doors` print?

A. `AB-ab`
B. `AB-ba`
C. `baAB-`
D. `AB-AB`

**Q2.** The body throws `IllegalStateException("body")` and `close` throws `IllegalStateException("close")`. What does the caller observe?

A. Message `close`, and `body` is suppressed
B. Message `body`, and `close` is suppressed
C. Message `finally`
D. The code does not compile

**Q3.** Does this compile?

```java
Door d = new Door("A");
try (d) {
    d = new Door("B");
}
```

A. Yes, and the close order is `ba`
B. Yes, and only `A` is closed
C. No. The resource variable is effectively final
D. No. A resource must be `Closeable`, not `AutoCloseable`

**Q4.** `charge` throws `BadAmount`. `main` calls `charge(50)` and does not catch or declare `BadAmount`. What is the result?

A. It compiles and prints `charged`
B. It compiles and throws `BadAmount` at runtime
C. It does not compile
D. It compiles because `BadAmount` extends `RuntimeException`

### Chapter 2 answers

**Q1 — B.** Creation prints `AB`. The body prints `-`. Close runs last-created first, so `b` then `a`.

**Q2 — B.** The exception from the body propagates. The exception from `close` is suppressed on it. A throwing `finally` does not work this way. That was Monday’s rule.

**Q3 — C.** A resource declared outside and used in the parentheses still cannot be reassigned. It is effectively final.

**Q4 — C.** `BadAmount` extends `Exception` and not `RuntimeException`, so it is checked. `main` must handle it or declare it.

---

# Chapter 3 — Date and time

> **必睇**　第 4 章 “Working with Dates and Times”，pp. 205–219：由 “Creating Dates and Times” 到 “Working with Instants”。
>
> **唔使睇**　“Accounting for Daylight Saving Time”（p. 220）同第 11 章嘅 formatter 係星期日。locale（第 11 章 p. 651 起）留第 8 週。

**Saturday** is 6 hours: this chapter, `Dates`, and questions Q1–Q5.

## What you must know

These types are immutable. A `plus` method returns a new object. The original variable does not change until you assign the result.

| Type | What it stores |
|---|---|
| `LocalDate` | A date, with no time and no zone |
| `LocalTime` | A time, with no date and no zone |
| `LocalDateTime` | A date and a time, with no zone |
| `Instant` | A point on the UTC timeline |
| `Period` | Years, months, and days. Date-based |
| `Duration` | Hours, minutes, seconds, and nanos. Time-based |
| `ZonedDateTime` | A date, a time, and a zone. Sunday uses it |

`Period.of(1, 2, 3)` is one year, two months, and three days. `Period.between(start, end)` counts from the start date to the end date. `Duration.ofHours(2).plusMinutes(30)` prints `PT2H30M`. `LocalDate.plus(Duration.ofDays(1))` throws `UnsupportedTemporalTypeException`, because a date has no time fields for a `Duration` to change. `LocalDate.plus(Period.ofDays(1))` works.

`LocalDateTime` can take a `Period` or a `Duration`. `Instant` takes a `Duration`. Adding a `Period` to an `Instant` does not fit: an instant has no calendar fields.

### `Dates`

```java
import java.time.*;

public class Dates {
    public static void main(String[] args) {
        LocalDate d = LocalDate.of(2026, 12, 21);
        d.plusDays(1);
        System.out.println(d);
        System.out.println(d.plusDays(1));
        LocalDate later = d.plus(Period.ofDays(2));
        System.out.println(later);
        System.out.println(Period.between(d, later));
        System.out.println(Duration.ofHours(2).plusMinutes(30));
    }
}
```

The run prints:

```text
2026-12-21
2026-12-22
2026-12-23
P2D
PT2H30M
```

The first line is still 21 December. `plusDays` returned a new date and the code ignored it.

Saturday’s questions are Q1–Q5.

## Chapter 3 questions

**Q1.** `LocalDate d = LocalDate.of(2026, 12, 21); d.plusDays(1);` What is `d`?

A. `2026-12-21`
B. `2026-12-22`
C. The code does not compile
D. An exception is thrown at runtime

**Q2.** What is `Period.between(LocalDate.of(2026, 12, 21), LocalDate.of(2026, 12, 23))`?

A. `PT48H`
B. `P2D`
C. `P0Y2M`
D. The code does not compile

**Q3.** What happens on `LocalDate.of(2026, 12, 21).plus(Duration.ofDays(1))`?

A. It returns `2026-12-22`
B. It returns a `LocalDateTime`
C. It throws `UnsupportedTemporalTypeException`
D. The code does not compile

**Q4.** Which addition fits the type?

A. `Instant.now().plus(Period.ofDays(1))`
B. `LocalDate.now().plus(Duration.ofHours(1))`
C. `LocalTime.now().plus(Duration.ofHours(1))`
D. `LocalDate.now().plus(Duration.ofDays(1))`

**Q5.** What does `Duration.ofHours(2).plusMinutes(30)` print?

A. `2:30`
B. `PT2H30M`
C. `P2H30M`
D. `150`

### Chapter 3 answers

**Q1 — A.** `plusDays` returns a new `LocalDate`. `d` still points at 21 December.

**Q2 — B.** `Period.between` is date-based. Two days is `P2D`. A `Duration` would use the `PT` form.

**Q3 — C.** `LocalDate` has no time-of-day fields. A `Duration` cannot be applied to it.

**Q4 — C.** `LocalTime` has hour fields, so a `Duration` applies. An `Instant` does not accept a `Period`. A `LocalDate` does not accept a `Duration`.

**Q5 — B.** `Duration` prints with a `PT` prefix. `Period` prints with a `P` prefix and calendar units.

---

# Sunday — daylight saving, 15 patterns, then the score

> **必睇**　第 4 章 “Accounting for Daylight Saving Time”，p. 220。第 11 章 “Formatting Dates and Times” 同 “Customizing the Date/Time Format”，pp. 647–650。15 條 pattern 用呢兩節。
>
> **唔使睇**　p. 651 起嘅 locale、貨幣、resource bundle 留第 8 週。

Sunday is 3 hours. The first 20 minutes are Saturday’s misses.

## `Dst`

8 March 2026 is the New York spring-forward. Local time 02:30 does not exist. 1 November 2026 is the fall-back. Local time 01:30 happens twice.

```java
import java.time.*;

public class Dst {
    public static void main(String[] args) {
        ZoneId ny = ZoneId.of("America/New_York");
        LocalDateTime gap = LocalDateTime.of(2026, 3, 8, 2, 30);
        System.out.println(ZonedDateTime.of(gap, ny));
        LocalDateTime overlap = LocalDateTime.of(2026, 11, 1, 1, 30);
        System.out.println(ZonedDateTime.of(overlap, ny));
        System.out.println(ZonedDateTime.ofLocal(overlap, ny, ZoneOffset.ofHours(-5)));
    }
}
```

The run prints:

```text
2026-03-08T03:30-04:00[America/New_York]
2026-11-01T01:30-04:00[America/New_York]
2026-11-01T01:30-05:00[America/New_York]
```

`ZonedDateTime.of` moves the missing 02:30 forward to 03:30. On the overlap, `of` picks the earlier offset, which is still `-04:00`. `ofLocal` with the preferred offset `-05:00` picks the later, standard-time occurrence.

## Fifteen patterns

Use `LocalDateTime.of(2026, 12, 21, 15, 4, 5)` and `Locale.US`. That date is a Monday. Write the fifteen results before you run them. Then run a loop of `DateTimeFormatter.ofPattern(pattern, Locale.US)`, and use `DateTimeFormatter.ISO_LOCAL_DATE` for the last one.

| # | Pattern | Result |
|---|---|---|
| 1 | `yyyy-MM-dd` | `2026-12-21` |
| 2 | `dd/MM/yyyy` | `21/12/2026` |
| 3 | `MMM d, yyyy` | `Dec 21, 2026` |
| 4 | `MMMM` | `December` |
| 5 | `EEE` | `Mon` |
| 6 | `HH:mm:ss` | `15:04:05` |
| 7 | `h:mm a` | `3:04 PM` |
| 8 | `yyyy-MM-dd'T'HH:mm` | `2026-12-21T15:04` |
| 9 | `D` | `355` |
| 10 | `uuuu` | `2026` |
| 11 | `q` | `4` |
| 12 | `e` | `2` |
| 13 | `a` | `PM` |
| 14 | `ss` | `05` |
| 15 | `ISO_LOCAL_DATE` | `2026-12-21` |

`D` is the day of the year. `q` is the quarter. `e` is the numeric day of the week for this locale, and Monday is 2 because the US week starts on Sunday. A single `M` would print `12` without a leading zero. `MM` prints `12`. `MMM` prints `Dec`.

## Sunday questions

**Q1.** What does `ZonedDateTime.of(LocalDateTime.of(2026, 3, 8, 2, 30), ZoneId.of("America/New_York"))` use as the local time?

A. `02:30`
B. `03:30`
C. `01:30`
D. The code does not compile

**Q2.** On 1 November 2026 in `America/New_York`, which offset does `ZonedDateTime.of` choose for local time 01:30?

A. `-04:00`
B. `-05:00`
C. `Z`
D. The call throws `DateTimeException`

**Q3.** What is pattern `yyyy-MM-dd'T'HH:mm` for 21 Dec 2026 at 15:04:05?

A. `2026-12-21 15:04:05`
B. `2026-12-21T15:04`
C. `21/12/2026T3:04 PM`
D. The pattern does not compile

**Q4.** What does pattern `D` print for 21 Dec 2026?

A. `21`
B. `12`
C. `355`
D. `Monday`

**Q5.** `LocalDate` and `LocalDateTime` are created with `of`. You call `plusDays(1)` and do not assign the result. Which statement is true?

A. Both variables move forward one day
B. Both variables stay on the original date
C. Only `LocalDate` stays. `LocalDateTime` changes
D. The calls do not compile

### Sunday answers

**Q1 — B.** 02:30 does not exist on the spring-forward morning. `ZonedDateTime.of` resolves it to 03:30 at offset `-04:00`.

**Q2 — A.** The local time happens twice. `ZonedDateTime.of` selects the earlier offset, `-04:00`. The later offset is `-05:00`, and `ofLocal` can select it when you pass that offset.

**Q3 — B.** The quoted `T` is a literal. `HH:mm` stops at minutes, so the seconds are not in the text.

**Q4 — C.** `D` is the day of the year. 21 December is day 355 in 2026.

**Q5 — B.** Both types are immutable. `plusDays` returns a new value and leaves the receiver unchanged.

Score Chapter 1 (6), Chapter 2 (4), Chapter 3 (5), and Sunday (5). **14 or more** of the 20 questions is the gate. Every miss becomes one rule and a five-line program before Monday of Week 6.

---

# Rules to copy onto one card

- Checked exceptions must be caught or declared. `RuntimeException` is unchecked. `Error` is a separate branch.
- `catch` goes from the specific type to the general type. Multi-catch alternatives cannot be related by inheritance.
- `finally` runs on the way out. If `finally` throws, that exception replaces the pending one.
- Try-with-resources closes in reverse order of creation. An exception from `close` is suppressed when the body also threw.
- A custom checked exception extends `Exception`, not `RuntimeException`.
- `Period` is date-based (`P2D`). `Duration` is time-based (`PT2H30M`). `plus` returns a new object.
- `LocalDate` accepts a `Period` and rejects a `Duration`. A missing local time in a zone is moved. A repeated local time has two offsets.
- `yyyy` is the year, `MM` the month, `dd` the day, `HH` the hour 0–23, `D` the day of the year.
