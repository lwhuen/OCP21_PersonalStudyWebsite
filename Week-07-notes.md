# Week 7 notes — lambdas and streams

**4–10 Jan 2027. 25 hours.** Weekend days are 8 hours. This file follows Week 7 of the study plan. The gate is the 30 stream questions at **70%** (21 of 30). Under **60%** (under 18) means the first days of the mock month are streams, coded, before any other objective.

Weekdays are Monday, Wednesday, and Friday, 3 hours each: 20 minutes on yesterday’s misses, 2 hours typing every listing, 40 minutes of questions and the notebook. Saturday and Sunday are 8 hours each. The extra two hours are questions. Monday’s first 20 minutes are the Week 6 misses.

| Day | What the plan says | Where it is in this file |
|---|---|---|
| Mon | Lambda syntax and effectively final variables | Chapter 1, the eight rewrites, questions Q1–Q6 |
| Wed | The six functional interfaces and method references | Chapter 2, the 15 names, questions Q7–Q12 |
| Fri | `Optional`, including `orElse` versus `orElseGet` | Chapter 3, `Opts`, questions Q13–Q18 |
| Sat (8 h) | Pipelines, on paper first | Chapter 4, the 12 pipelines, questions Q19–Q24 |
| Sun (8 h) | `groupingBy`, primitive streams, 30 questions | Chapter 5, questions Q25–Q30, then score all 30 |

Same checklist as the study plan:

- [ ] Rewrite eight anonymous classes as lambdas, then as method references: static, bound, unbound, and constructor.
- [ ] Name the functional interface from a snippet, 15 out of 15. Include a primitive form such as `IntPredicate` or `ToIntFunction`.
- [ ] `Optional` `map`, `flatMap`, `orElse`, and `orElseGet`. Show that `orElse` evaluates its argument even when a value is present.
- [ ] On paper, 12 pipelines using `filter`, `map`, `flatMap`, `sorted`, `distinct`, `limit`, `reduce`, and `collect`. Then type them.
- [ ] `groupingBy` into a map of lists, and into a map of counts. `partitioningBy` into true and false. `IntStream.average` returns `OptionalDouble`. Reuse a consumed stream and read the exception.
- [ ] 30 stream questions at 70%. Under 60%: the first days of the mock month are streams, coded, before any other objective.

Predict each listing before you run it. Each miss goes in the notebook as one rule and a five-line program.

The questions are practice in the exam’s style. They are not copied from the real exam or from a book. Try each one before its answer key.

---

# Chapter 1 — Lambda syntax

> **必睇**　第 8 章 pp. 440–444（“Writing Simple Lambdas”）同 pp. 465–469（“Working with Variables in Lambdas”）。第 5 章 “Effectively Final Variables”，p. 244。
>
> **唔使睇**　functional interfaces 同 method references 係星期三。Review Questions 唔使做。

**Monday** is this chapter, eight rewrites, and questions Q1–Q6.

## What you must know

A lambda is a method body with no name. The target type is a functional interface: one abstract method. `var` is allowed for a parameter only inside parentheses, and if one parameter uses `var` then every parameter does.

```java
s -> s.isEmpty()
(s) -> s.isEmpty()
(String s) -> s.isEmpty()
(var s) -> s.isEmpty()
```

A body with braces uses `return` when the abstract method returns a value. A body without braces returns the expression and does not use `return` or a semicolon.

A lambda may use a local variable only when that variable is final or effectively final. One assignment, and no assignment after that, makes it effectively final. A field does not have this limit. The lambda reads the field when it runs.

## Eight rewrites

Type each anonymous class, then replace it with the lambda, then with the method reference. Two of each kind is enough for the checklist.

Static:

```java
Function<String, Integer> a = new Function<>() {
    public Integer apply(String s) { return Integer.parseInt(s); }
};
Function<String, Integer> b = s -> Integer.parseInt(s);
Function<String, Integer> c = Integer::parseInt;
```

```java
Function<String, String> a = s -> s.trim();
Function<String, String> c = String::trim;
```

`String::trim` is an unbound instance method. The instance arrives as the argument. `Integer::parseInt` is static. The argument is the parameter.

Bound. The instance is already chosen:

```java
String word = "hi";
Supplier<Integer> a = new Supplier<>() {
    public Integer get() { return word.length(); }
};
Supplier<Integer> b = () -> word.length();
Supplier<Integer> c = word::length;
```

Unbound again, with the instance as the first argument:

```java
Function<String, Integer> len = String::length;
BiFunction<String, String, String> cat = String::concat;
```

Constructor:

```java
Supplier<List<String>> lists = ArrayList::new;
Function<String, StringBuilder> builders = StringBuilder::new;
```

`ArrayList::new` matches `get()` with the empty constructor. `StringBuilder::new` matches `apply(String)` with `new StringBuilder(String)`.

Monday’s questions are Q1–Q6.

## Chapter 1 questions

**Q1.** Does this compile?

```java
int n = 1;
Runnable r = () -> System.out.println(n);
n = 2;
```

A. Yes, and `r.run()` prints `2`
B. Yes, and `r.run()` prints `1`
C. No
D. It compiles and throws when `r.run()` is called

**Q2.** Which lambda assigns to `Supplier<String>`?

A. `s -> "ok"`
B. `() -> "ok"`
C. `(String s) -> s`
D. `() -> {}`

**Q3.** Does this compile as a `Function<String, Integer>`?

```java
s -> { s.length(); }
```

A. Yes
B. Yes, and the result is the length
C. No. A brace body that produces a value needs `return`
D. No. A lambda cannot use braces

**Q4.** Does `(var s) -> s.length()` compile as a `Function<String, Integer>`?

A. Yes
B. No. `var` is illegal in a lambda
C. No. `var` cannot sit inside parentheses
D. No. `length` returns `int`, not `Integer`

**Q5.** `String word = "hi"; Supplier<Integer> len = word::length;` What does `len.get()` return?

A. `0`
B. `2`
C. `"hi"`
D. The code does not compile

**Q6.** What does `Function<String, Integer> f = Integer::parseInt; f.apply("10")` return?

A. `"10"`
B. `10`
C. `2`
D. The code does not compile

### Chapter 1 answers

**Q1 — C.** `n` is assigned after the lambda captures it, so `n` is not effectively final.

**Q2 — B.** `Supplier.get` takes no arguments and returns a value. `() -> "ok"` matches. `() -> {}` returns nothing, so it is a `Runnable`.

**Q3 — C.** Braces make a statement body. `s.length();` throws the length away. `return s.length();` is the body that matches `Function`.

**Q4 — A.** A parenthesized `var` parameter takes its type from the target. `int` returned from `length` is boxed to `Integer`.

**Q5 — B.** `word::length` is a bound reference. The supplier calls `length` on `"hi"`.

**Q6 — B.** `Integer::parseInt` is a static method reference. `apply` passes `"10"` to `parseInt`.

---

# Chapter 2 — Functional interfaces

> **必睇**　第 8 章 pp. 445–464：“Coding Functional Interfaces”、“Using Method References”、“Working with Built-in Functional Interfaces”。
>
> **唔使睇**　`Optional` 在第 10 章，星期五先睇。

**Wednesday** is this chapter, 15 names, and questions Q7–Q12.

## What you must know

| Interface | Abstract method |
|---|---|
| `Supplier<T>` | `T get()` |
| `Consumer<T>` | `void accept(T)` |
| `Predicate<T>` | `boolean test(T)` |
| `Function<T, R>` | `R apply(T)` |
| `UnaryOperator<T>` | `T apply(T)` |
| `BinaryOperator<T>` | `T apply(T, T)` |
| `IntSupplier` | `int getAsInt()` |
| `IntConsumer` | `void accept(int)` |
| `IntPredicate` | `boolean test(int)` |
| `IntFunction<R>` | `R apply(int)` |
| `ToIntFunction<T>` | `int applyAsInt(T)` |

`UnaryOperator<T>` is a `Function<T, T>`. Use the primitive interface when the snippet takes or returns a primitive and the target type says so. Boxing still lets `Function<String, Integer>` accept `String::length`.

## Name these 15

Write the interface, including type arguments, before you look at the key.

| # | Snippet |
|---|---|
| 1 | `() -> "a"` |
| 2 | `s -> s.isEmpty()` for a `String` argument and a `boolean` result |
| 3 | `s -> System.out.println(s)` for a `String` |
| 4 | `s -> s.trim()` for `String` in and `String` out |
| 5 | `(a, b) -> a + b` for two `Integer`s |
| 6 | `() -> 1` as a primitive `int` |
| 7 | `n -> n > 0` for a primitive `int` |
| 8 | `s -> s.length()` as a primitive `int` result from a `String` |
| 9 | `n -> "n" + n` from a primitive `int` to a `String` |
| 10 | `n -> System.out.println(n)` for a primitive `int` |
| 11 | `(s, n) -> s.substring(n)` for `String` and `int` |
| 12 | `() -> {}` |
| 13 | `x -> x` for one `String` |
| 14 | `list -> list.add("a")` for a `List<String>`, result ignored |
| 15 | `() -> new ArrayList<String>()` |

The names are: 1 `Supplier<String>`. 2 `Predicate<String>`. 3 `Consumer<String>`. 4 `UnaryOperator<String>`. 5 `BinaryOperator<Integer>`. 6 `IntSupplier`. 7 `IntPredicate`. 8 `ToIntFunction<String>`. 9 `IntFunction<String>`. 10 `IntConsumer`. 11 `BiFunction<String, Integer, String>`. 12 `Runnable`. 13 `UnaryOperator<String>`. 14 `Consumer<List<String>>`. 15 `Supplier<List<String>>`.

15 of 15 is the checklist item. A miss here is a notebook line even if the later questions go well.

## Chapter 2 questions

**Q7.** `Predicate<String> p = String::isEmpty;` What is `p.test("")`?

A. `true`
B. `false`
C. `""`
D. The code does not compile

**Q8.** What is the target of `n -> n + 1` when `n` is an `Integer` and the result is an `Integer`?

A. `Predicate<Integer>`
B. `Consumer<Integer>`
C. `UnaryOperator<Integer>`
D. `IntSupplier`

**Q9.** `ToIntFunction<String> f = String::length;` What is `f.applyAsInt("java")`?

A. `4`
B. `"java"`
C. `Integer.valueOf(4)` as the only legal return
D. The code does not compile

**Q10.** `Supplier<List<String>> lists = ArrayList::new;` What is `lists.get().size()`?

A. `null`
B. `0`
C. The code does not compile
D. An exception is thrown at runtime

**Q11.** Does `IntPredicate p = n -> n > 0; p.test(1)` compile and return `true`?

A. It does not compile. `IntPredicate` has no `test`
B. It compiles and returns `true`
C. It compiles and returns `false`
D. It compiles and throws, because `1` is boxed

**Q12.** Which reference is bound?

A. `String::length`
B. `Integer::parseInt`
C. `word::length`, where `word` is a `String` variable
D. `ArrayList::new`

### Chapter 2 answers

**Q7 — A.** `String::isEmpty` is an unbound reference and matches `test(String)`. The empty string is empty.

**Q8 — C.** The same type goes in and comes out. That is `UnaryOperator<Integer>`. `IntUnaryOperator` would be the primitive form.

**Q9 — A.** `applyAsInt` returns the primitive `4`. `String::length` matches `ToIntFunction<String>`.

**Q10 — B.** `ArrayList::new` calls the empty constructor. The new list has size 0.

**Q11 — B.** `IntPredicate.test` takes an `int`. `1` passes the `n > 0` test.

**Q12 — C.** A bound reference fixes the instance. `String::length` is unbound. `Integer::parseInt` is static. `ArrayList::new` is a constructor.

---

# Chapter 3 — `Optional`

> **必睇**　第 10 章 “Returning an Optional”，pp. 554–557。同後面 “Chaining Optionals”，p. 587。
>
> **唔使睇**　中間嘅 stream pipeline 留星期六。唔好順住讀完整章。

**Friday** is this chapter, `Opts`, and questions Q13–Q18.

## What you must know

`Optional.of(value)` rejects null. `Optional.ofNullable(value)` turns null into an empty optional. `Optional.empty()` is empty.

`map` applies a function when a value is present and wraps the result. On an empty optional, `map` stays empty. `flatMap` is the same idea when the function already returns an `Optional`. Use `flatMap` so you do not end up with `Optional<Optional<T>>`.

`orElse(other)` always evaluates `other`, then returns the stored value if there is one. `orElseGet(supplier)` calls the supplier only when the optional is empty. `orElseThrow` with no supplier throws `NoSuchElementException` when the optional is empty.

### `Opts`

```java
import java.util.*;

public class Opts {
    static int calls;
    static String mark() { calls++; return "x"; }
    public static void main(String[] args) {
        Optional.of("a").orElse(mark());
        System.out.print(calls);
        Optional.of("a").orElseGet(Opts::mark);
        System.out.println(calls);
        System.out.println(Optional.<String>empty().map(String::length));
        System.out.println(Optional.of("hi").flatMap(s -> Optional.of(s.length())));
    }
}
```

The run prints:

```text
11
Optional.empty
Optional[2]
```

`orElse` called `mark` even though `"a"` was present, so `calls` became 1. `orElseGet` did not call `mark`, so `calls` stayed 1. The two digits are stuck together: `11`.

Friday’s questions are Q13–Q18.

## Chapter 3 questions

**Q13.** `Optional.of("a").orElse(mark())` calls `mark`, and `mark` increments a counter that started at 0. What is the counter afterward?

A. `0`
B. `1`
C. The code does not compile
D. A `NullPointerException` is thrown

**Q14.** After that call, `Optional.of("a").orElseGet(Opts::mark)` runs. What is the counter if it was already `1`?

A. `1`
B. `2`
C. `0`
D. The code does not compile

**Q15.** What is `Optional.<String>empty().map(String::length)`?

A. `0`
B. `Optional.empty`
C. `Optional[0]`
D. A `NullPointerException` is thrown

**Q16.** What does `Optional.of("hi").flatMap(s -> Optional.of(s.length()))` print?

A. `2`
B. `Optional[2]`
C. `Optional[Optional[2]]`
D. The code does not compile

**Q17.** What is the result of `Optional.of(null)`?

A. An empty optional
B. `Optional[null]`
C. A `NullPointerException` is thrown
D. The code does not compile

**Q18.** What does `Optional.empty().orElseThrow()` throw?

A. `NullPointerException`
B. `IllegalStateException`
C. `NoSuchElementException`
D. Nothing. It returns `null`

### Chapter 3 answers

**Q13 — B.** `orElse` evaluates its argument before it looks at the optional. The value `"a"` is returned, and `mark` has already run.

**Q14 — A.** `orElseGet` calls the supplier only when the optional is empty. This optional holds `"a"`, so the counter stays `1`.

**Q15 — B.** `map` on an empty optional does not call the function. The result is still empty. It is not `Optional[0]`.

**Q16 — B.** `flatMap` expects an `Optional` and unwraps one level. The length of `"hi"` is `2`.

**Q17 — C.** `Optional.of` requires a non-null value. `Optional.ofNullable(null)` is the call that returns an empty optional.

**Q18 — C.** `orElseThrow()` with no argument throws `NoSuchElementException` when the optional is empty.

---

# Chapter 4 — Pipelines

> **必睇**　第 10 章 “Using Streams”，pp. 558–578。
>
> **唔使睇**　primitive streams（p. 579 起）同 “Collecting Results”（p. 590）留星期日。

**Saturday** is 8 hours. Write the result of each pipeline on paper, then type it. Questions Q19–Q24 are after the 12 lines.

A pipeline is lazy. Intermediate operations (`filter`, `map`, `flatMap`, `sorted`, `distinct`, `limit`, `skip`, `peek`) do nothing until a terminal operation runs (`toList`, `reduce`, `count`, `collect`, `forEach`, `findFirst`, `anyMatch`, `allMatch`, `noneMatch`). A stream can be consumed once. `Stream.toList()` returns a list that refuses `add`.

## Twelve pipelines

| # | Pipeline | Result |
|---|---|---|
| 1 | `List.of(1, 2, 2, 3).stream().filter(x -> x > 1).distinct().map(x -> x * 10).toList()` | `[20, 30]` |
| 2 | `Stream.of(List.of(1, 2), List.of(3)).flatMap(List::stream).toList()` | `[1, 2, 3]` |
| 3 | `Stream.of(1, 2, 3).reduce(0, Integer::sum)` | `6` |
| 4 | `Stream.of(3, 1, 2).sorted().limit(2).toList()` | `[1, 2]` |
| 5 | `Stream.of("a", "b", "a").distinct().toList()` | `[a, b]` |
| 6 | `Stream.of("a", "b", "c").skip(1).limit(1).toList()` | `[b]` |
| 7 | `Stream.of("hi", "a").map(String::length).toList()` | `[2, 1]` |
| 8 | `Stream.of(1, 2, 3).anyMatch(n -> n > 2)` | `true` |
| 9 | `Stream.of(1, 2).allMatch(n -> n > 0)` | `true` |
| 10 | `Stream.of(1, 2).noneMatch(n -> n < 0)` | `true` |
| 11 | `Stream.of("a", "a").distinct().count()` | `1` |
| 12 | `Stream.of("a", "b").collect(Collectors.joining(","))` | `a,b` |

Lines 1, 2, and 3 were run on JDK 21. Run the other nine yourself and keep any miss.

## Chapter 4 questions

**Q19.** What is pipeline 1?

A. `[20, 20, 30]`
B. `[20, 30]`
C. `[10, 20, 30]`
D. `[2, 3]`

**Q20.** What is pipeline 2?

A. `[[1, 2], [3]]`
B. `[1, 2, 3]`
C. `[1, 2]`
D. The code does not compile

**Q21.** What is pipeline 4?

A. `[3, 1]`
B. `[1, 2]`
C. `[1, 2, 3]`
D. `[2, 3]`

**Q22.** A stream is built and `peek` prints each element. No terminal operation is called. What prints?

A. Every element
B. Nothing
C. The first element
D. An `IllegalStateException` is thrown

**Q23.** `Stream.of("a").count()` has already run. A second `count` on that same stream does what?

A. It returns `1`
B. It returns `0`
C. It throws `IllegalStateException`
D. It throws `NullPointerException`

**Q24.** What does `Stream.of(1, 2, 3).filter(n -> n > 1).toList().add(9)` do?

A. The list becomes `[2, 3, 9]`
B. It throws `UnsupportedOperationException`
C. It throws `IllegalStateException`
D. The code does not compile

### Chapter 4 answers

**Q19 — B.** `filter` keeps `2, 2, 3`. `distinct` keeps `2, 3`. `map` multiplies by 10.

**Q20 — B.** `flatMap` turns each inner list into a stream of its elements and joins those streams. `map` would have left a stream of lists.

**Q21 — B.** `sorted` produces `1, 2, 3`. `limit(2)` keeps the first two of that sorted stream.

**Q22 — B.** `peek` is intermediate. Without a terminal operation the pipeline does not run.

**Q23 — C.** A stream is consumed by the first terminal operation. Using it again throws `IllegalStateException`.

**Q24 — B.** `Stream.toList()` returns a list that cannot be modified. `add` throws `UnsupportedOperationException`.

---

# Chapter 5 — `groupingBy` and primitive streams

> **必睇**　第 10 章 pp. 579–586（primitive streams）同 pp. 590–603（“Collecting Results”、Summary、Exam Essentials）。第 13 章 “Working with Parallel Streams”，pp. 786–794。
>
> **略讀**　p. 587：“Linking Streams to the Underlying Data”。“Chaining Optionals” 星期五讀過就跳過。“Using a Spliterator”（p. 599）知道個名就得，唔使記 API。
>
> **唔使睇**　第 13 章其餘 threads 留第 8 週。Review Questions 唔使做。

**Sunday** is 8 hours. The first 20 minutes are Saturday’s misses. Then this chapter, questions Q25–Q30, and the score of all 30.

## What you must know

`Collectors.groupingBy` builds a `Map`. The classifier is the key. The default downstream value is a `List` of the elements. `Collectors.counting()` makes the value a `Long` count instead.

`Collectors.partitioningBy` always produces both keys, `true` and `false`.

`IntStream.average` returns `OptionalDouble`, because an empty stream has no average. `OptionalDouble[2.0]` is the print for the average of `1, 2, 3`. `IntStream.range(1, 4)` is `1, 2, 3`. `rangeClosed(1, 4)` includes `4`. `mapToInt` turns an object stream into an `IntStream`. `boxed` turns an `IntStream` back into `Stream<Integer>`.

```java
Map<Integer, List<String>> grouped = Stream.of("a", "bb", "a")
    .collect(Collectors.groupingBy(String::length));
Map<Integer, Long> counts = Stream.of("a", "bb", "a")
    .collect(Collectors.groupingBy(String::length, Collectors.counting()));
Map<Boolean, List<String>> parts = Stream.of("a", "bb", "ccc")
    .collect(Collectors.partitioningBy(s -> s.length() > 1));
```

The run produces `{1=[a, a], 2=[bb]}`, `{1=2, 2=1}`, and `{false=[a], true=[bb, ccc]}`. Map print order can vary. The keys and the members are the result that matters.

`Stream.concat(Stream.of(1), Stream.of(2, 3))` is one stream of `1, 2, 3`. That is concatenation. The joined stream is parallel when either input is parallel. `flatMap` is decomposition: one element becomes its own stream, and those streams are joined. `reduce` is reduction.

`stream.parallel()` and `list.parallelStream()` run the pipeline on more than one thread. `sequential()` switches that stream back. A parallel stream is still consumed once. `forEach` on a parallel stream does not promise encounter order. `forEachOrdered` does. A sum, or any `reduce` whose operator is associative and has no side effects, has the same result as the sequential stream. Do not store into an ordinary `ArrayList` from `forEach` on a parallel stream. That list is not safe for concurrent adds.

## Chapter 5 questions

**Q25.** `Stream.of("a", "bb", "a")` grouped by `String::length`. Which list sits under key `1`?

A. `[a]`
B. `[a, a]`
C. `[bb]`
D. `[a, bb]`

**Q26.** The same strings, grouped with `Collectors.counting()`. What is the value for key `2`?

A. `1`
B. `2`
C. `[bb]`
D. The code does not compile

**Q27.** `Stream.of("a", "bb", "ccc")` partitioned by `length > 1`. Which list is under `false`?

A. `[a]`
B. `[bb, ccc]`
C. The key `false` is absent
D. `[a, bb, ccc]`

**Q28.** What does `IntStream.of(1, 2, 3).average()` return?

A. `2.0` as a `double`
B. `OptionalDouble[2.0]`
C. `Optional[2.0]`
D. `2`

**Q29.** What does `IntStream.range(1, 4).sum()` return?

A. `6`
B. `10`
C. `4`
D. An empty optional

**Q30.** `Stream.of("b", "a").sorted().findFirst()` returns what?

A. `"b"`
B. `Optional[a]`
C. `Optional.empty`
D. An exception, because `findFirst` requires a present value

### Chapter 5 answers

**Q25 — B.** `"a"` and `"a"` both have length 1. `"bb"` has length 2.

**Q26 — A.** Counting replaces the list. One string has length 2, so the `Long` value is `1`. The two strings of length 1 produce `2`.

**Q27 — A.** `"a"` fails the test. `partitioningBy` still creates the `false` key. `"bb"` and `"ccc"` are under `true`.

**Q28 — B.** `average` returns `OptionalDouble`. An empty `IntStream` returns an empty `OptionalDouble`, not a number.

**Q29 — A.** `range(1, 4)` is `1, 2, 3`. The end is exclusive. The sum is `6`. `rangeClosed(1, 4)` would include `4` and sum to `10`.

**Q30 — B.** `sorted` on an ordered stream of strings yields `"a"` then `"b"`. `findFirst` wraps that first element. It returns an empty optional when the stream has no element. It does not throw.

Score all 30. **21 or more** is the gate. Under 18, the mock month opens with streams. Every miss becomes one rule and a five-line program before Monday of Week 8.

---

# Rules to copy onto one card

- A lambda’s locals are final or effectively final. A brace body that returns a value uses `return`.
- `Supplier` gets, `Consumer` accepts, `Predicate` tests, `Function` applies. `UnaryOperator` is a function with one type. Primitive forms avoid boxing: `IntPredicate`, `ToIntFunction`, `IntFunction`.
- Static reference: `Integer::parseInt`. Bound: `word::length`. Unbound: `String::length`. Constructor: `ArrayList::new`.
- `orElse` always evaluates its argument. `orElseGet` evaluates the supplier only when the optional is empty. `of(null)` throws. `ofNullable(null)` is empty.
- Intermediate operations run when a terminal operation runs. A stream is consumed once.
- `flatMap` flattens a stream of streams. `Stream.concat` joins two streams. `groupingBy` builds a map of lists, or a map of counts with `counting`. `partitioningBy` always has `true` and `false`.
- `parallel()` and `parallelStream()` do not change an associative sum. `forEach` on a parallel stream has no encounter order. `forEachOrdered` keeps it.
- `IntStream.average` returns `OptionalDouble`. `range` excludes the end. `rangeClosed` includes it.
