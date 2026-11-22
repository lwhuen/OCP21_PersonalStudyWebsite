# Week 6 glossary — collections and generics

Terms from [Week-06-notes.md](Week-06-notes.md). The exam words are English. Friday 1 Jan is off.

## Monday — `List`

| Term | Meaning |
|---|---|
| `List` | An ordered collection that allows duplicates. `get` and the `int` form of `remove` use an index. |
| `remove(int)` | Deletes by index. On a `List<Integer>`, `remove(1)` deletes index 1. |
| `remove(Object)` | Deletes the first element that `equals` the argument. `remove(Integer.valueOf(1))` deletes the value 1. |
| `List.of` | An immutable list. It rejects `null`. `add` and `remove` throw `UnsupportedOperationException`. |
| `Arrays.asList` | A fixed-size list backed by the array. `set` works. `add` and `remove` throw `UnsupportedOperationException`. |

## Wednesday — `Set` and `Map`

| Term | Meaning |
|---|---|
| `HashSet` | A set with no order you can rely on. Allows one `null`. Uses `hashCode` and `equals`. |
| `TreeSet` | A sorted set. Natural order rejects `null` with `NullPointerException`. Uses `Comparable` or a `Comparator`. |
| `HashMap` | A map with no key order you can rely on. One null key, and null values. Putting the same key again replaces the value. |
| `TreeMap` | A map with sorted keys. Natural order rejects a null key. |
| `get` | Returns the value, or `null` when the key is missing. A stored null value also returns `null`. |
| `containsKey` | Tells a missing key from a key whose stored value is `null`. |

## Saturday — `Deque`, sequenced collections, sorting

| Term | Meaning |
|---|---|
| `Deque` | A double-ended queue. `ArrayDeque` does not allow null elements. |
| Stack methods | `push` and `pop` use the front. The first `pop` returns the last `push`. `pop` on an empty deque throws `NoSuchElementException`. |
| Queue methods | `offer` adds at the back. `poll` removes from the front. `poll` on an empty deque returns `null`. |
| Sequenced collection | Has `addFirst`, `addLast`, `getFirst`, `getLast`, `removeFirst`, `removeLast`, and `reversed`. `List`, `Deque`, `SortedSet`, and `LinkedHashSet` are sequenced. `HashSet` is not. |
| `reversed` | A reverse-ordered view of the same collection, not a new copy of the elements. |
| `Comparable` | A class’s natural order, through `compareTo`. A negative result sorts this object before the argument. Zero does not by itself prove `equals`. |
| `Comparator` | An order supplied from outside the class. |
| `comparing` | Builds a comparator from a method, such as `String::length`. |
| `thenComparing` | A second comparator used only when the first comparison is a tie. |

## Sunday — generics

| Term | Meaning |
|---|---|
| Generic type | A type with a parameter, such as `List<String>`. The compiler checks it. At runtime the parameter is erased. |
| Erasure | `List<String>` and `List<Integer>` are both `List` at runtime. Two methods that erase to the same signature do not compile. |
| Invariant | `List<String>` is not a `List<Object>` and not a `List<CharSequence>`. |
| `? extends` | A producer. `get` returns the upper bound. You cannot add an element, except `null`, because the list might be a more specific type. |
| `? super` | A consumer. You can add the lower bound. `get` returns `Object`. |
| Unbounded `?` | `get` returns `Object`. The only reference you may add is `null`. |
