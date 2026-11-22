# OCP Java SE 21 study plan

Exam **1Z0-830** (Oracle Certified Professional: Java SE 21 Developer) on **Sunday 7 March 2027**.

You start from no Java on **Monday 23 November 2026**. The first eight weeks cover the whole syllabus. The next month is mock exams. The last three weeks stay on mocks so the score is still there on exam morning.

| | |
|---|---|
| Questions | 50, multiple choice |
| Time | 120 minutes |
| Pass mark | 68% = **34 of 50** |
| Sit the exam when | The last two timed mocks are both **75% or higher** (38 of 50) |

Weekdays are Monday, Wednesday, and Friday, 3 hours each. Swap the names if your free days differ. A normal weekend day is 6 hours. Weeks 4, 7, and 8 use the full 8 hours each weekend day.

## Hours

| Phase | Dates | Hours | What you do |
|---|---|---|---|
| Syllabus | 23 Nov 2026 – 17 Jan 2027 | 168 h | Every exam topic, once |
| Mock month | 18 Jan – 14 Feb 2027 | 84 h | Drills, then timed mocks 1–5 |
| Hold the score | 15 Feb – 6 Mar 2027 | about 48 h | Mocks 6–7 and the notebook |
| Exam | Sunday 7 Mar 2027 | — | 50 questions, 120 minutes |

About 300 hours in total. Friday 25 December and Friday 1 January are already days off, so those two weeks inside the sprint are 15 hours, not 21.

| Block | Hours |
|---|---|
| Foundations (weeks 1–2) | 42 |
| OOP (weeks 3–4) | 46 |
| Exceptions and dates (week 5) | 15 |
| Collections (week 6) | 15 |
| Lambdas and streams (week 7) | 25 |
| I/O, modules, threads (week 8) | 25 |
| Mock month (weeks 9–12) | 84 |
| Last three weeks (weeks 13–15) | 48 |

If a chapter is still open on Sunday 17 January, it becomes the first repair in the mock month. After that Sunday the book is a reference. You study the questions you missed.

## How a session is split

**Knowledge week, 3 hours on a weekday**

- 20 min: review yesterday’s misses
- 2 h: the chapter, every listing typed by you
- 40 min: questions, then the notebook

**Mock week, 3 hours on a weekday**

- 20 min: review yesterday’s misses
- 2 h 20 min: code the traps you missed
- 20 min: notebook

A full mock is 120 minutes. It belongs on a weekend day, or on the Wednesday slots in February. The next session reviews it. On a heavy weekend day the extra two hours go into questions.

Predict the output before you run the code. Each miss goes in the notebook as one rule and a five-line program. A chapter you scored 80% on does not get a second full reading during the sprint. It comes back as questions in January.

You work about 80 to 100 book pages in each of the first eight weeks, because the pages are listings and questions.

## Where each exam topic sits

Oracle publishes the topic list and does not publish how many questions each topic gets.

| Exam topic | Week |
|---|---|
| Numeric types, boolean logic, operators | 1 |
| Program flow | 1 |
| Text, String, StringBuilder, arrays | 2 |
| Classes, encapsulation, immutability | 3 |
| Inheritance, interfaces, records, sealed types, patterns | 4 |
| Exceptions | 5 |
| Date, time, duration, period, time zones | 5 |
| Collections, sequenced collections, generics | 6 |
| Lambdas and streams | 7 |
| I/O and NIO.2 | 8 |
| Localization, plus logging and annotations | 8 |
| Modules | 8 |
| Concurrency and virtual threads | 8 |

Generics are week 6. Annotations and the logging API are week 8, at recognition level. The published 1Z0-830 topics do not include JDBC.

---

# Part 1 — Eight-week syllabus (23 Nov – 17 Jan)

## Week 1 · 23–29 Nov 2026 · Types, operators, and flow

**21 h.** Gate: chapter questions at 70%.

- Mon: JDK, IntelliJ, one `main` line
- Wed: primitives, literals, `var`
- Fri: operators, precedence, casts
- Sat: `Math`, `if` / `else`, both switches
- Sun: loops, `break`, `continue`, review

- [ ] Install JDK 21 and IntelliJ IDEA Community. `java -version` prints 21. A class with `main` prints your name.
- [ ] Write the eight primitives, their sizes, and their default values from memory.
- [ ] Fifteen expressions on precedence, promotion, and casts. Write the answer first, then run. Keep the misses.
- [ ] One program that uses if / else, a switch expression, `for`, `while`, `break`, and `continue`.
- [ ] Call `Math.abs`, `min`, `max`, `round`, `ceil`, `floor`, and `pow`. `Math.round` on a double returns a long.
- [ ] Building-blocks, operators, and decisions review questions at 70%. Each miss: one rule and a five-line program in the notebook.

## Week 2 · 30 Nov–6 Dec 2026 · Methods, text, and arrays

**21 h.** Gate: 70%, plus one hour with autocomplete off.

- Mon: methods, return, overloading
- Wed: varargs, pass-by-value
- Fri: `String`, `StringBuilder`, text blocks
- Sat: arrays, sort, `binarySearch`
- Sun: autocomplete off, then questions

- [ ] Overload one method three ways, including varargs. Varargs is the last parameter, and there is only one.
- [ ] Prove pass-by-value: reassigning the parameter does not change the caller; mutating the object does.
- [ ] One call each for `substring`, `indexOf`, `equals`, `strip`, `isBlank`, `indent`, `formatted`, and a text block. The end index of `substring` is exclusive.
- [ ] Show, in a loop, why `String` concatenation copies and `StringBuilder` does not. One sentence in the notebook.
- [ ] Reverse an array in place, sort it, and `binarySearch` it. A negative result encodes the insertion point. Make one jagged two-dimensional array.
- [ ] Autocomplete off for one hour. Methods, text, and arrays questions at 70%.

## Week 3 · 7–13 Dec 2026 · Classes and memory

**21 h.** Gate: you can hand-trace initializer order, and score 70%.

- Mon: classes, fields, constructors, `this`
- Wed: statics, initializer order
- Fri: encapsulation
- Sat: immutable class, GC diagrams
- Sun: chapter questions

- [ ] A class with fields, a constructor, and `this`. No public fields.
- [ ] Hand-write static-then-instance initializer order for a superclass and a subclass. Run code that prints the order and compare.
- [ ] An encapsulated `BankAccount`: private fields, constructor, methods.
- [ ] An immutable `Money` class: private final fields, no setters, class is final.
- [ ] Five memory diagrams. A box is an object, an arrow is a reference. Mark what is eligible for collection.
- [ ] Class-design questions at 70%, including one you can explain about garbage collection.

## Week 4 · 14–20 Dec 2026 · Inheritance through pattern matching

**25 h. Weekend days are 8 h.** Gate: mixed OOP questions at 70%. This is the heavy week before the holidays.

- Mon: `extends`, `super`, override rules
- Wed: reference vs object type, field hiding
- Fri: `equals`, `hashCode`, interfaces, enums
- Sat (8 h): records, sealed types, patterns
- Sun (8 h): nested classes, mixed OOP set

- [ ] `Animal`, `Dog`, and `Cat`. Overriding rules on one card: signature, covariant return, access, checked exceptions.
- [ ] One example where a field is hidden, not overridden. The reference type decides what compiles; the object type decides which override runs.
- [ ] A correct `equals` and `hashCode`, and one broken `equals`. If `equals` is true, the hash codes match.
- [ ] An interface with a default method and a static method, two implementers, and an enum with a field and a method.
- [ ] A sealed interface with an exhaustive switch, a record with a compact constructor, a record pattern, and a `when` guard. A general pattern above a specific one does not compile.
- [ ] Mixed questions on inheritance, interfaces, records, and patterns at 70%. Nested classes: one notebook page on what each kind can see.

## Week 5 · 21–27 Dec 2026 · Exceptions and the date-time API

**15 h. Holiday week.** Gate: exceptions and dates at 70%. Friday 25 Dec is off.

- Mon: `try` / `catch` / `finally`, multi-catch
- Wed: try-with-resources, custom exception
- Fri: off
- Sat: `LocalDate`, `LocalTime`, `Period`, `Duration`
- Sun: DST example, 15 formatters, questions

- [ ] From memory: checked versus unchecked versus `Error`, and what `finally` does when the catch block throws.
- [ ] A custom checked exception, and a try-with-resources class whose close messages print in reverse order of creation.
- [ ] `LocalDate`, `LocalTime`, `LocalDateTime`, `Instant`, `Period`, and `Duration`. `Period` is date-based. `Duration` is time-based. `plusDays` returns a new object.
- [ ] On a real daylight-saving date, show a local time that is skipped or repeated, and what `ZonedDateTime` does.
- [ ] Predict 15 `DateTimeFormatter` patterns, then run them.
- [ ] Exceptions and date-time questions at 70%.

## Week 6 · 28 Dec 2026–3 Jan 2027 · Collections and generics

**15 h. Holiday week.** Gate: collections questions at 70%. Friday 1 Jan is off.

- Mon: `List`, `remove` overload trap
- Wed: `Set`, `Map`, null rules, order
- Fri: off
- Sat: `Deque`, sequenced APIs, sorting
- Sun: generics, then questions

- [ ] Show `list.remove(1)` versus `list.remove(Integer.valueOf(1))`.
- [ ] The same data in a `List`, a `HashSet`, a `TreeSet`, and a `HashMap`. Write down what is ordered and what allows null.
- [ ] Use a `Deque` as a stack and as a queue. Call `getFirst`, `getLast`, `addFirst`, `addLast`, and `reversed`.
- [ ] Sort with `Comparable` and with `Comparator.comparing` followed by `thenComparing`.
- [ ] For `? extends` and for `? super`, say whether you can add and whether you can get. One example of each.
- [ ] Collections and generics questions at 70%.

## Week 7 · 4–10 Jan 2027 · Lambdas and streams

**25 h. Weekend days are 8 h.** Gate: 30 stream questions at 70%. Under 60% means mock week 1 opens with streams.

- Mon: lambdas, effectively final
- Wed: functional interfaces, method refs
- Fri: `Optional`, `orElse` vs `orElseGet`
- Sat (8 h): stream pipelines on paper
- Sun (8 h): `groupingBy`, primitives, 30 Qs

- [ ] Rewrite eight anonymous classes as lambdas, then as method references: static, bound, unbound, and constructor.
- [ ] Name the functional interface from a snippet, 15 out of 15. Include a primitive form such as `IntPredicate` or `ToIntFunction`.
- [ ] `Optional` `map`, `flatMap`, `orElse`, and `orElseGet`. Show that `orElse` evaluates its argument even when a value is present.
- [ ] On paper, 12 pipelines using `filter`, `map`, `flatMap`, `sorted`, `distinct`, `limit`, `reduce`, and `collect`. Then type them.
- [ ] `groupingBy` into a map of lists, and into a map of counts. `partitioningBy` into true and false. `IntStream.average` returns `OptionalDouble`. Reuse a consumed stream and read the exception.
- [ ] 30 stream questions at 70%. Under 60%: the first days of the mock month are streams, coded, before any other objective.

## Week 8 · 11–17 Jan 2027 · I/O, modules, and threads

**25 h. Weekend days are 8 h.** Gate: mixed quiz at 65%. Sunday 17 Jan the syllabus is closed.

- Mon: streams, `Path`, `Files`
- Wed: serialization, locales, bundles
- Fri: modules in the terminal
- Sat (8 h): threads, executors, races
- Sun (8 h): mixed quiz, weak-topic list

- [ ] With `Path` and try-with-resources, read a file, count words, and write a report. One notebook example each for `resolve`, `relativize`, and `normalize`.
- [ ] State what `transient` and `serialVersionUID` do. A resource bundle in two locales, printing a date and a currency. Search order is full locale, then language, then the base bundle.
- [ ] Two modules, one `exports` and one `requires`, run with `java -p` and `-m`. Then a service with `provides`, `with`, and `uses`. Break a missing `exports` once and save the error.
- [ ] A counter that loses updates, then the same counter fixed with `synchronized` or `AtomicInteger`. Run tasks on a fixed pool and on `newVirtualThreadPerTaskExecutor`.
- [ ] From memory: thread states, `Runnable` versus `Callable`, `start` versus `run`, `shutdown` versus `shutdownNow`. Calling `run` does not start a thread. `Future.get` blocks.
- [ ] Mixed quiz on I/O, locale, modules, and threads at 65%. Write your three weakest topics at the top of the notebook. The book is now a reference, not a reading plan.

---

# Part 2 — Mock month (18 Jan – 14 Feb)

Five timed mocks. Review is part of the mock: a score with no notebook lines does not count.

| When | What you sit | Target |
|---|---|---|
| 18–24 Jan | Objective drills, untimed | A ranked weak list |
| 31 Jan, Sunday review | Timed mock 1 | 65% |
| 3 Feb, Wednesday | Timed mock 2 | 70% |
| 6 Feb, Saturday | Timed mock 3 | 75% |
| 10 Feb, Wednesday | Timed mock 4 | 75% |
| 13 Feb, Saturday | Timed mock 5 | 80% (40 of 50) |

## Week 9 · 18–24 Jan 2027 · Find the weak objectives

**21 h.** Gate: a ranked list of objectives. No full mock yet.

- Mon: 40 Qs — OOP and exceptions
- Wed: 40 Qs — collections and streams
- Fri: 30 Qs — dates, I/O, locales
- Sat: 30 Qs — modules and threads
- Sun: one-page rule sheet, ranked weak list

- [ ] 40 Enthuware questions on OOP and exceptions. Review each miss before Wednesday.
- [ ] 40 questions on collections and streams. If streams were under 60% in week 7, this day is streams only.
- [ ] 30 questions on dates, I/O, and localization.
- [ ] 30 questions on modules and concurrency. Code every miss, including the ones you guessed.
- [ ] One page: objectives ranked from weakest to strongest, with the rule you keep breaking.
- [ ] No timed mock this week. The rank list is the gate.

## Week 10 · 25–31 Jan 2027 · Mock 1

**21 h.** Gate: timed mock 1 at 65% after a full review.

- Mon: code weakest-objective traps
- Wed: code weakest-objective traps
- Fri: 20 Qs on that objective
- Sat: timed mock 1, start review
- Sun: finish review before next mock

- [ ] Two weekday sessions on the single weakest objective. Small programs.
- [ ] Friday: 20 questions on that same objective.
- [ ] Saturday: Enthuware timed mock 1. 50 questions, 120 minutes, no book, no pause.
- [ ] Sunday: every miss becomes a rule plus a five-line program. Guessed answers count as misses.
- [ ] Record the score. 65% is the target. Under 55% means next week repairs two objectives and still takes mock 2.
- [ ] The review is finished before any new mock is opened.

## Week 11 · 1–7 Feb 2027 · Mocks 2 and 3

**21 h.** Gate: mock 2 at 70%. Mock 3 at 75%.

- Mon: code new weakest objective
- Wed: timed mock 2, then mark
- Fri: review mock 2
- Sat: timed mock 3
- Sun: review mock 3

- [ ] Monday: code the traps from whichever objective mock 1 scored lowest.
- [ ] Wednesday: timed mock 2. Target 70%.
- [ ] Friday: review mock 2 completely.
- [ ] Saturday: timed mock 3. Target 75% (38 of 50).
- [ ] Sunday: review mock 3. Update the ranked list.
- [ ] Both reviews are in the notebook. The lower of the two scores decides next Monday’s topic.

## Week 12 · 8–14 Feb 2027 · Mocks 4 and 5

**21 h.** Gate: mock 5 at 80% (40 of 50). This Sunday closes the mock month.

- Mon: one weak objective, coded
- Wed: timed mock 4
- Fri: review mock 4
- Sat: timed mock 5
- Sun: review, record carry score

- [ ] Monday: the objective that is still under 70% across the mocks so far.
- [ ] Wednesday: timed mock 4. Target 75%.
- [ ] Friday: review mock 4.
- [ ] Saturday: timed mock 5. Target 80%, 40 of 50.
- [ ] Sunday: review mock 5. Circle the rules that appeared in more than one mock.
- [ ] Mock month ends. Later weeks repeat mocks and the notebook.

---

# Part 3 — Hold the score (15 Feb – 6 Mar)

The exam is three weeks after the mock month ends. These weeks repeat mocks and the notebook.

| When | What you sit | Target |
|---|---|---|
| 20 Feb, Saturday | Timed mock 6 | 80% |
| 27 Feb, if needed | Timed mock 7 | 80% |
| Before 7 Mar | Last two timed mocks | Both 75% or higher |

## Week 13 · 15–21 Feb 2027 · Mock 6

**21 h.** Gate: mock 6 at 80%, or a written list of what is still under 75%.

- Mon: re-code repeated mock traps
- Wed: re-code repeated mock traps
- Fri: 30 Qs at exam pace, review
- Sat: timed mock 6
- Sun: review mock 6

- [ ] Re-code the repeated traps from the notebook. Two weekday sessions.
- [ ] Friday: 30 mixed questions at two minutes each, then review.
- [ ] Saturday: timed mock 6. Target 80%.
- [ ] Sunday: review mock 6 the same day. A miss with no notebook line is unfinished.
- [ ] Practice the exam habit: first pass for what you know, flag the rest, answer every question.
- [ ] If mock 6 is under 75%, next week is another full mock. If it is 80% or higher, next week is the notebook.

## Week 14 · 22–28 Feb 2027 · Mock 7 only if the score moved

**15 h if mock 6 was 80% or higher, otherwise 21 h.** Gate: two recent mocks at 75% or higher.

If mock 6 was under 75%: Mon and Wed repair, Sat timed mock 7, Sun review.

If mock 6 was 80% or higher: Mon, Wed, and Sat are notebook and flashcards only, about 3 hours each. Friday stays light either way.

- [ ] Choose from mock 6: another timed mock, or notebook only. Write the choice down before Monday.
- [ ] Two sessions on the objective that still costs the most points.
- [ ] Timed mock 7 if the last mock was under 80%. Target 80%. Skip it if you are already there twice.
- [ ] Review that mock the next day, or spend the same hours rereading the one-page rule sheet.
- [ ] The last two timed mocks are both 75% or higher (38 of 50). That is the line for sitting on 7 Mar.
- [ ] The rule sheet is one page. If it has grown, cut it back to the rules you still miss.

## Week 15 · 1–7 Mar 2027 · Taper, then the exam

**About 12 h, then stop.** Saturday is two hours. Sunday 7 Mar is the exam.

- Mon: mock if under 75%, else flashcards
- Wed: rule sheet, 3 hours
- Fri: flashcards, stop by 18:00
- Sat: short review, confirm exam setup
- Sun: exam

- [ ] Monday: timed mock 8 only if the last two mocks are not both at 75%. Otherwise the notebook.
- [ ] Wednesday: one-page rule sheet, out loud.
- [ ] Friday: three hours of flashcards. No mock after 18:00.
- [ ] Saturday: at most two hours. Confirm the start time, the ID, and the test center or OnVUE setup.
- [ ] Exam pace: about two minutes a question, flag and move, answer every question.
- [ ] Sunday 7 Mar: 1Z0-830. 50 questions, 120 minutes, pass at 34.

---

# Books and tools

| Material | Role |
|---|---|
| Jeanne Boyarsky and Scott Selikoff, *OCP Oracle Certified Professional Java SE 21 Developer Study Guide*, exam 1Z0-830 | The only book during the 8 weeks. One pass. Errata: [selikoff.net/ocp21](https://www.selikoff.net/ocp21/) |
| [Enthuware 1Z0-830](https://enthuware.com/mock-exams/oracle-certified-professional/java-se-21-1z0-830) | Objective drills from 18 Jan, then the timed mocks. This is the score you trust. |
| JDK 21 and IntelliJ IDEA Community | Daily coding. Turn autocomplete off for the hour named in week 2. |
| [Oracle exam page for 1Z0-830](https://education.oracle.com/oracle-certified-professional-java-se-21-developer/pexam_1Z0-830) | Topic list. Read it again in the first mock week. Schedule the seat by mid-January. |

# Exam morning

50 questions, 120 minutes, pass at 34.

About two minutes each. First pass for the ones you can answer, flag the rest, then return. A wrong answer costs the same as a blank one, so every question gets an answer. If it says choose two, choose two. Look for the line that does not compile, or the line that throws, before you compute a result.

# Mistake notebook

One entry per miss: the rule in a sentence, then a five-line program. From 18 January this is what you study.

```
Date:
Question / snippet:
What I answered:
The rule:
Five-line program:
```
