# Week 6 notes — collections and generics

**28 Dec 2026–3 Jan 2027. 15 hours.** Friday 1 Jan is off. This file follows Week 6 of the study plan. The gate is the collections and generics questions at **70%** (14 of the 20 questions in this file).

Monday and Wednesday are 3 hours each: 20 minutes on yesterday’s misses, 2 hours typing every listing, 40 minutes of questions and the notebook. Friday is a day off. Saturday is 6 hours. Sunday is 3 hours: generics, then the questions, then the score. Monday’s first 20 minutes are the Week 5 misses.

| Day | What the plan says | Where it is in this file |
|---|---|---|
| Mon | `List`, and the `remove` overload trap | Chapter 1, `Removes`, questions Q1–Q4 |
| Wed | `Set`, `Map`, null rules, and order | Chapter 2, `SameData`, questions Q1–Q4 |
| Fri 1 Jan | Off | — |
| Sat | `Deque`, sequenced methods, `Comparable`, and `Comparator` | Chapter 3, `Lines`, `Names`, questions Q1–Q6 |
| Sun | Generics, then the questions | Chapter 4, questions Q1–Q6, then score all 20 |

Same checklist as the study plan:

- [ ] Show `list.remove(1)` versus `list.remove(Integer.valueOf(1))`.
- [ ] The same data in a `List`, a `HashSet`, a `TreeSet`, and a `HashMap`. Write down what is ordered and what allows null.
- [ ] Use a `Deque` as a stack and as a queue. Call `getFirst`, `getLast`, `addFirst`, `addLast`, and `reversed`.
- [ ] Sort with `Comparable` and with `Comparator.comparing` followed by `thenComparing`.
- [ ] For `? extends` and for `? super`, say whether you can add and whether you can get. One example of each.
- [ ] Collections and generics questions at 70%.

Predict each listing before you run it. Each miss goes in the notebook as one rule and a five-line program.

The questions are practice in the exam’s style. They are not copied from the real exam or from a book. Try each one before its answer key.

---

# Chapter 1 — `List` and `remove`

> **必睇**　第 9 章 Collections and Generics，pp. 482–495：“Using Common Collection APIs” 同 “Using the List Interface”。
>
> **唔使睇**　“Working with Generics”（p. 526）留星期日。Review Questions 唔使做。

**Monday** is this chapter, `Removes`, and questions Q1–Q4.

## What you must know

`List` keeps insertion order and allows duplicates. `list.get(i)` and `list.remove(i)` use an index when the argument is an `int`.

`remove` is overloaded. `remove(int)` deletes by index. `remove(Object)` deletes the first element that `equals` the argument. For a `List<Integer>`, the literal `1` is an `int`, so `remove(1)` deletes index 1. `remove(Integer.valueOf(1))` deletes the value 1.

`List.of` returns an immutable list. It rejects `null` and it rejects `add` or `remove`. `Arrays.asList` is fixed-size and backed by the array: `set` works, `add` and `remove` throw `UnsupportedOperationException`.

### `Removes`

```java
import java.util.*;

public class Removes {
    public static void main(String[] args) {
        List<Integer> list = new ArrayList<>(List.of(1, 2, 3));
        list.remove(1);
        System.out.println(list);
        list.remove(Integer.valueOf(1));
        System.out.println(list);
    }
}
```

The run prints:

```text
[1, 3]
[3]
```

`remove(1)` deleted the element at index 1, which was `2`. The list was `[1, 3]`. `remove(Integer.valueOf(1))` then deleted the value `1`.

Monday’s questions are Q1–Q4.

## Chapter 1 questions

**Q1.** What is the list after `remove(1)` in `Removes`, before the second remove?

A. `[1, 2, 3]`
B. `[2, 3]`
C. `[1, 3]`
D. The code does not compile

**Q2.** `List<Integer> list = new ArrayList<>(List.of(1, 2, 3));` What does `list.remove(Integer.valueOf(2))` leave?

A. `[1, 3]`
B. `[1, 2]`
C. `[1, 2, 3]`
D. It throws `IndexOutOfBoundsException`

**Q3.** What is the result of `List.of(1, 2).add(3)`?

A. The list becomes `[1, 2, 3]`
B. The code does not compile
C. An `UnsupportedOperationException` is thrown
D. An `IndexOutOfBoundsException` is thrown

**Q4.** `String[] names = {"Ada"}; List<String> list = Arrays.asList(names);` Which call succeeds?

A. `list.add("Bea")`
B. `list.set(0, "Bea")`
C. `list.remove(0)`
D. None of them

### Chapter 1 answers

**Q1 — C.** The `int` overload deletes an index. Index 1 held `2`, so `[1, 2, 3]` becomes `[1, 3]`.

**Q2 — A.** `Integer.valueOf(2)` selects `remove(Object)`. The value `2` is deleted. Index 2 is not used.

**Q3 — C.** `List.of` returns a list that cannot be changed. `add` throws `UnsupportedOperationException`.

**Q4 — B.** `Arrays.asList` can replace an element with `set`. `add` and `remove` would change the size, and this list refuses that.

---

# Chapter 2 — `Set`, `Map`, null, and order

> **必睇**　第 9 章 “Using the Set Interface”，pp. 496–497。“Using the Map Interface”，pp. 502–508。
>
> **唔使睇**　Queue / Deque（pp. 498–501）係星期六。

**Wednesday** is this chapter, `SameData`, and questions Q1–Q4.

## What you must know

Write this table from memory before you run `SameData`.

| Type | Order | Null |
|---|---|---|
| `ArrayList` | Insertion order, duplicates allowed | Null elements allowed |
| `HashSet` | No order you can rely on | One null element |
| `TreeSet` | Sorted | No null when it uses natural order |
| `HashMap` | No key order you can rely on | One null key, and null values |
| `TreeMap` | Keys sorted | No null key when it uses natural order |

`HashSet` and `HashMap` use `hashCode` and `equals`. `TreeSet` and `TreeMap` use `Comparable` or a `Comparator`. A `TreeSet` of `String` prints in alphabetical order.

`Map` keys are unique by `equals`. Putting the same key again replaces the value. `get` on a missing key returns `null`. A null value that was stored also returns `null`, so `containsKey` is the test for a missing key.

### `SameData`

```java
import java.util.*;

public class SameData {
    public static void main(String[] args) {
        List<String> list = new ArrayList<>(List.of("b", "a", "c", "a"));
        Set<String> hash = new HashSet<>(list);
        Set<String> tree = new TreeSet<>(list);
        Map<String, Integer> map = new HashMap<>();
        map.put("b", 1);
        map.put("a", 2);
        map.put("c", 3);
        map.put("a", 9);
        System.out.println(list);
        System.out.println(hash.size());
        System.out.println(tree);
        System.out.println(map.get("a"));
    }
}
```

The run prints the list `[b, a, c, a]`, the hash size `3`, the tree `[a, b, c]`, and the map value `9`. The hash set’s own order is not part of the result. The size is. The second `put` of `"a"` replaced `2` with `9`.

Wednesday’s questions are Q1–Q4.

## Chapter 2 questions

**Q1.** What does `SameData` print for the `TreeSet`?

A. `[b, a, c, a]`
B. `[a, b, c]`
C. `[b, a, c]`
D. The code does not compile

**Q2.** What is `map.get("a")` after the two `put` calls for `"a"`?

A. `2`
B. `9`
C. `null`
D. An exception is thrown

**Q3.** Does `new TreeSet<String>().add(null)` succeed?

A. Yes. A set may hold one null
B. Yes. `TreeSet` sorts null first
C. No. Natural order has no place for null, and the call throws `NullPointerException`
D. The code does not compile

**Q4.** A `HashMap` already contains the key `null`. What is the result of a second `put(null, 1)`?

A. It throws `NullPointerException`
B. It stores a second null key
C. It replaces the value for the one null key
D. The code does not compile

### Chapter 2 answers

**Q1 — B.** `TreeSet` sorts the elements and drops the duplicate `"a"`. The print is `[a, b, c]`.

**Q2 — B.** One key has one value. The second `put` replaces `2` with `9`.

**Q3 — C.** `TreeSet` with natural ordering compares elements. Comparing to `null` throws `NullPointerException`. A `HashSet` can hold one `null`.

**Q4 — C.** `HashMap` allows one null key. Putting that key again replaces the value.

---

# Chapter 3 — `Deque`, sequenced collections, and sorting

> **必睇**　第 9 章 pp. 498–501（Queue 同 Deque）、pp. 509–525（sorting、sequenced collections、“Reviewing Collection Types”）。
>
> **唔使睇**　generics 仍然留星期日。

**Saturday** is 6 hours: this chapter, `Lines`, `Names`, and questions Q1–Q6.

## What you must know

`Deque` is a double-ended queue. As a stack, `push` and `pop` use the front. As a queue, `offer` adds at the back and `poll` removes from the front. `ArrayDeque` does not allow null elements.

Java 21 sequenced collections add `addFirst`, `addLast`, `getFirst`, `getLast`, `removeFirst`, `removeLast`, and `reversed`. `reversed` returns a reverse-ordered view. `List`, `Deque`, `SortedSet`, and `LinkedHashSet` are sequenced. `HashSet` is not.

`Comparable.compareTo` defines a class’s natural order. The sign is negative, zero, or positive, in the same style as Week 2’s `Arrays.compare`. `Comparator.comparing` builds an order from a method. `thenComparing` breaks ties with a second order. Sort a `List` with `list.sort(comparator)`.

### `Lines`

```java
import java.util.*;

public class Lines {
    public static void main(String[] args) {
        Deque<String> stack = new ArrayDeque<>();
        stack.push("a");
        stack.push("b");
        System.out.print(stack.pop());
        System.out.print(stack.pop());

        Deque<String> queue = new ArrayDeque<>();
        queue.offer("a");
        queue.offer("b");
        System.out.print(queue.poll());
        System.out.print(queue.poll());

        Deque<String> seq = new ArrayDeque<>();
        seq.addLast("a");
        seq.addFirst("b");
        System.out.print(seq.getFirst());
        System.out.print(seq.getLast());
        System.out.println(seq.reversed());
    }
}
```

The run prints:

```text
baabba[a, b]
```

Read it as `ba`, then `ab`, then `ba`, then `[a, b]`. The stack pops `b` then `a`. The queue polls `a` then `b`. After `addLast("a")` and `addFirst("b")`, the first element is `b` and the last is `a`. The reversed view prints `[a, b]`.

### `Names`

```java
import java.util.*;

public class Names {
    public static void main(String[] args) {
        List<String> names = new ArrayList<>(List.of("Ada", "Bea", "Cy"));
        names.sort(Comparator.comparing(String::length).thenComparing(Comparator.naturalOrder()));
        System.out.println(names);
    }
}
```

The run prints:

```text
[Cy, Ada, Bea]
```

`Cy` has length 2, so it comes first. `Ada` and `Bea` both have length 3, so natural alphabetical order puts `Ada` before `Bea`.

Saturday’s questions are Q1–Q6.

## Chapter 3 questions

**Q1.** A stack is pushed `"a"` then `"b"`. What does the first `pop` return?

A. `a`
B. `b`
C. `null`
D. The code does not compile

**Q2.** A queue is offered `"a"` then `"b"`. What does the first `poll` return?

A. `a`
B. `b`
C. `null`
D. It throws `NoSuchElementException`

**Q3.** `addLast("a")` then `addFirst("b")`. What are `getFirst` and `getLast`?

A. `a` then `b`
B. `b` then `a`
C. `a` then `a`
D. The code does not compile on a `Deque`

**Q4.** What does `seq.reversed()` print after those two adds?

A. `[b, a]`
B. `[a, b]`
C. `[a]`
D. The code does not compile

**Q5.** What does `Names` print?

A. `[Ada, Bea, Cy]`
B. `[Cy, Bea, Ada]`
C. `[Cy, Ada, Bea]`
D. `[Ada, Cy, Bea]`

**Q6.** `compareTo` returns a negative number. Where does this object belong relative to the argument?

A. After the argument
B. Before the argument
C. At the same position, and `equals` must be true
D. The sort throws `IllegalArgumentException`

### Chapter 3 answers

**Q1 — B.** `push` puts the element at the front. `pop` removes that front element. `b` was pushed last, so it comes off first.

**Q2 — A.** `offer` adds at the back. `poll` removes from the front. `a` was offered first. `poll` on an empty deque returns `null`. `pop` on an empty deque throws `NoSuchElementException`.

**Q3 — B.** `a` is at the back. `b` is then placed at the front. `getFirst` is `b` and `getLast` is `a`.

**Q4 — B.** The deque’s own order is `b`, `a`. The reversed view is `[a, b]`.

**Q5 — C.** Length is the first key, so `Cy` leads. Equal lengths use alphabetical order, so `Ada` precedes `Bea`.

**Q6 — B.** A negative `compareTo` means this object sorts before the argument. A zero result does not by itself prove `equals`.

---

# Chapter 4 — Generics

> **必睇**　“Working with Generics”，pp. 526–542，包括 Summary 同 Exam Essentials。
>
> **唔使睇**　Review Questions（p. 543 起）唔使做。

**Sunday** is 3 hours. The first 20 minutes are Saturday’s misses. Then this chapter, questions Q1–Q6, and the score.

## What you must know

A generic class stores a type parameter, such as `List<String>`. The compiler checks the type. At runtime the parameter is erased, so `List<String>` and `List<Integer>` are both just `List`. You cannot overload two methods that erase to the same signature.

`List<? extends Number>` is a producer. You can `get` a `Number`. You cannot `add` an `Integer` or a `Double`, because the list might be a `List<Integer>` or a `List<Double>`. `null` is the one reference you may add.

`List<? super Integer>` is a consumer. You can `add` an `Integer`. `get` returns `Object`, because the list might be a `List<Integer>`, a `List<Number>`, or a `List<Object>`.

Remember it as: `extends` lets you get, `super` lets you add. An unbounded `?` lets you get `Object` and lets you add only `null`.

```java
List<? extends Number> nums = new ArrayList<Integer>();
Number n = nums.size() == 0 ? null : nums.get(0);
List<? super Integer> sink = new ArrayList<Number>();
sink.add(1);
Object got = sink.get(0);
```

`got` is the `Integer` `1`, seen through an `Object` variable. `nums.add(1)` does not compile.

## Chapter 4 questions

**Q1.** `List<? extends Number> nums = new ArrayList<Integer>();` Does `nums.add(1)` compile?

A. Yes
B. Yes, but only because `1` is an `Integer`
C. No
D. It compiles and throws `ClassCastException`

**Q2.** `List<? super Integer> sink = new ArrayList<Number>();` What is the compile-time type of `sink.get(0)` after `sink.add(1)`?

A. `Integer`
B. `Number`
C. `Object`
D. The `get` does not compile

**Q3.** Does this compile?

```java
void show(List<String> a) {}
void show(List<Integer> a) {}
```

A. Yes
B. Yes, because the type arguments differ
C. No. Erasure gives both methods the same signature
D. No. A method cannot take a `List`

**Q4.** What can you add to a `List<?>` besides leaving it unchanged?

A. Any `Object`
B. Only `null`
C. Only `String`
D. Nothing, including `null`

**Q5.** Which assignment compiles?

```java
List<String> words = new ArrayList<>();
```

A. `List<Object> objs = words;`
B. `List<? extends CharSequence> objs = words;`
C. `List<CharSequence> objs = words;`
D. `List<? super Object> objs = words;`

**Q6.** `TreeSet<String>` natural order versus `HashSet`. Which statement is true?

A. Both print elements in insertion order
B. `TreeSet` is sorted. `HashSet` has no order you can rely on
C. Both reject duplicate `equals` matches and both allow one null
D. `HashSet` rejects null and `TreeSet` allows one

### Chapter 4 answers

**Q1 — C.** `? extends Number` might be a `List<Double>`. Adding an `Integer` is rejected at compile time.

**Q2 — C.** `? super Integer` might be a `List<Object>` or a `List<Number>`. `get` is typed as `Object`. The `add` of an `Integer` is legal.

**Q3 — C.** After erasure both methods are `show(List)`. The class does not compile.

**Q4 — B.** An unbounded wildcard hides the element type. `null` is the only reference that is safe to add. `get` returns `Object`.

**Q5 — B.** A `List<String>` is a `List<? extends CharSequence>`. It is not a `List<Object>`, a `List<CharSequence>`, or a `List<? super Object>`.

**Q6 — B.** `TreeSet` sorts. `HashSet` does not promise an order. `HashSet` allows one null. A naturally ordered `TreeSet` does not.

Score Chapter 1 (4), Chapter 2 (4), Chapter 3 (6), and Chapter 4 (6). **14 or more** of the 20 questions is the gate. Every miss becomes one rule and a five-line program before Monday of Week 7.

---

# Rules to copy onto one card

- `remove(int)` deletes an index. `remove(Object)` deletes a value. On `List<Integer>`, `remove(1)` is the index.
- `List.of` rejects null and rejects modification. `Arrays.asList` allows `set` and refuses `add` and `remove`.
- `HashSet` and `HashMap` have no reliable order. `TreeSet` and `TreeMap` are sorted. One null key is legal in `HashMap` and illegal in a naturally ordered `TreeMap`.
- A stack pops the last push. A queue polls the first offer. `getFirst` and `getLast` read the ends. `reversed` is a reverse view.
- `comparing` then `thenComparing` sorts by the first key and breaks ties with the second. A negative `compareTo` sorts first.
- `? extends` can get and cannot add. `? super` can add and `get` returns `Object`. Overloads that erase to the same signature do not compile.
