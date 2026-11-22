# Week 7 glossary — lambdas and streams

Terms from [Week-07-notes.md](Week-07-notes.md). The exam words are English.

## Monday — lambdas and method references

| Term | Meaning |
|---|---|
| Lambda | A method body with no name. Its target type is a functional interface. |
| Functional interface | An interface with one abstract method. |
| Expression lambda | `s -> s.length()`. The value of the expression is the result. No `return` and no semicolon. |
| Block lambda | A body in braces. If the method returns a value, the block uses `return`. |
| `var` parameter | Allowed only inside parentheses. If one parameter uses `var`, every parameter does. The target type supplies the type. |
| Effectively final | A local assigned once and not assigned again. A lambda may use it. A field does not have this limit. |
| Static method reference | `Integer::parseInt`. The lambda argument becomes the method argument. |
| Bound method reference | `word::length`. The instance is already chosen. A `Supplier` can call it. |
| Unbound method reference | `String::length` or `String::isEmpty`. The instance arrives as the first argument. |
| Constructor reference | `ArrayList::new` or `StringBuilder::new`. The target method picks which constructor. |

## Wednesday — the common interfaces

| Term | Meaning |
|---|---|
| `Supplier<T>` | `T get()`. No arguments. |
| `Consumer<T>` | `void accept(T)`. |
| `Predicate<T>` | `boolean test(T)`. |
| `Function<T, R>` | `R apply(T)`. |
| `UnaryOperator<T>` | `T apply(T)`. A function whose input and output types match. |
| `BinaryOperator<T>` | `T apply(T, T)`. |
| `IntSupplier` | `int getAsInt()`. |
| `IntConsumer` | `void accept(int)`. |
| `IntPredicate` | `boolean test(int)`. |
| `IntFunction<R>` | `R apply(int)`. |
| `ToIntFunction<T>` | `int applyAsInt(T)`. |
| `BiFunction<T, U, R>` | `R apply(T, U)`. |
| `Runnable` | `void run()`. No result. Not in `java.util.function`, but the empty lambda `() -> {}` is one. |

## Friday — `Optional`

| Term | Meaning |
|---|---|
| `Optional.of` | Wraps a non-null value. `of(null)` throws `NullPointerException`. |
| `Optional.ofNullable` | Wraps a value, or returns an empty optional when the value is `null`. |
| `Optional.empty` | An optional with no value. |
| `map` | Applies a function when a value is present and wraps the result. On an empty optional, `map` stays empty and does not call the function. |
| `flatMap` | Like `map`, but the function already returns an `Optional`. One level is unwrapped, so you do not get `Optional<Optional<T>>`. |
| `orElse` | Always evaluates its argument, then returns the stored value if there is one. |
| `orElseGet` | Calls the supplier only when the optional is empty. |
| `orElseThrow()` | Throws `NoSuchElementException` when the optional is empty. |

## Saturday and Sunday — streams

| Term | Meaning |
|---|---|
| Intermediate operation | `filter`, `map`, `flatMap`, `sorted`, `distinct`, `limit`, `skip`, `peek`. Lazy. They do nothing until a terminal operation runs. |
| Terminal operation | `toList`, `reduce`, `count`, `collect`, `forEach`, `findFirst`, `anyMatch`, `allMatch`, `noneMatch`. It runs the pipeline. |
| Consumed stream | A stream after its terminal operation. Using it again throws `IllegalStateException`. |
| `Stream.toList()` | A list that refuses `add`. `add` throws `UnsupportedOperationException`. |
| `flatMap` | Turns each element into a stream and joins those streams. `map` would leave a stream of streams or a stream of lists. |
| `distinct` | Drops later duplicates. An ordered stream keeps the first occurrence. |
| `reduce` | Combines the elements. `reduce(0, Integer::sum)` starts from the identity `0`. |
| `anyMatch` | True when one element passes. |
| `allMatch` | True when every element passes. |
| `noneMatch` | True when every element fails the test. |
| `findFirst` | An `Optional` of the first element. An empty stream returns an empty optional. It does not throw. |
| `groupingBy` | Builds a `Map`. The classifier is the key. The default value is a `List` of the elements. `counting()` makes the value a `Long` count. |
| `partitioningBy` | A map with both keys, `true` and `false`, even when one side is empty. |
| `IntStream.range` | From the start, exclusive of the end. `range(1, 4)` is `1, 2, 3`. |
| `IntStream.rangeClosed` | Includes the end. |
| `IntStream.average` | Returns `OptionalDouble`, because an empty stream has no average. |
| `Stream.concat` | Joins two streams into one. The result is parallel if either input is parallel. |
| Parallel stream | `parallel()` or `parallelStream()`. A side-effect-free associative reduction matches the sequential result. `forEach` does not keep encounter order. `forEachOrdered` does. |
| `mapToInt` | Turns an object stream into an `IntStream`. `boxed` turns an `IntStream` back into `Stream<Integer>`. |
