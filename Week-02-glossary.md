# Week 2 glossary — methods, text, and arrays

Terms from [Week-02-notes.md](Week-02-notes.md). The exam words are English.

## Monday — methods and overloading

| Term | Meaning |
|---|---|
| Signature | The method name plus the parameter types. Parameter names are not part of it. The return type is not part of it. |
| Overload | Two methods with the same name and different parameter lists. A different return type alone is not an overload. It does not compile. |
| Return path | A non-`void` method must return a value on every path that can finish. A `void` method may use a bare `return;`. |
| Overload resolution | The order Java picks a method: exact match, then primitive widening, then boxing, then varargs. Widening beats boxing. Boxing beats varargs. |
| Widening | A primitive becomes a wider primitive, such as `int` to `long`. An `int` argument does not match a `Long` parameter, because that would widen and then box. |
| Boxing in a call | `int` can box to `Integer`, and that `Integer` can then widen to `Object`. Widening a primitive is tried before this boxing. |
| Ambiguous call | A call that matches two methods equally does not compile. `show(1, 2)` is ambiguous for `show(int, long)` and `show(long, int)`. `pick(null)` is ambiguous for `pick(Integer)` and `pick(String)`. |

## Wednesday — varargs and pass-by-value

| Term | Meaning |
|---|---|
| Varargs | A last parameter written `int... nums`. A method has only one. Inside the method it is an array. A call with no extra arguments passes an empty array, not `null`. |
| `int...` and `int[]` | The same signature. Declaring both does not compile. A parameter after the varargs does not compile. |
| Exact match beats varargs | `add(int, int)` is chosen for `add(1, 2)` when `add(int...)` also exists. `add(1, 2, 3)` can use only the varargs method. |
| Pass-by-value | Java copies each argument into the parameter. Reassigning the parameter changes the copy. Mutating the object the copy points at changes the object the caller still holds. |

## Friday — `String`, `StringBuilder`, text blocks

| Term | Meaning |
|---|---|
| `String` immutability | A `String` cannot be changed. Methods such as `substring` return a new `String`. The variable still points at the old one until you assign the result. |
| String pool | The same literal shares one object. `new String("hi")` is a different object with the same characters. |
| `==` and `equals` | `==` compares references. `equals` compares characters. `"hi".equals(null)` is `false`. Calling `equals` on a `null` reference throws `NullPointerException`. |
| `substring` | The end index is exclusive. `"animal".substring(1, 4)` is `nim`. `substring(3, 3)` and `substring(6)` on a length-6 string are `""`. A start past the length throws `StringIndexOutOfBoundsException`. |
| `indexOf` | The index of the first match, or `-1` when the character or string is missing. The search can start at a from-index. |
| `charAt` | The `char` at one index. A missing index throws `StringIndexOutOfBoundsException`. |
| `length()` | A method on a `String`. An array uses the field `length`, with no parentheses. |
| `strip` | Removes leading and trailing whitespace, including Unicode whitespace. `trim` only removes characters at or below U+0020. |
| `isBlank` | True for empty text or text that is only whitespace. `" ".isBlank()` is true. |
| `isEmpty` | True only when the length is 0. `" ".isEmpty()` is false. The empty string is blank. |
| `indent` | Indents each line, turns line endings into `\n`, and the result ends with `\n`. `"a".indent(1)` equals `" a\n"`. |
| `formatted` | Fills a format string. `"Hi %s".formatted("Java")` is `Hi Java`. The same idea as `String.format`. |
| Text block | A `String` opened with `"""` at the end of a line. `"""cat"""` does not compile. The closing `"""` sets the indent that is removed. Content farther right keeps its extra spaces. A text block includes the newline before the closing quotes. |
| `StringBuilder` | A changeable buffer. `append`, `insert`, `delete`, `deleteCharAt`, `reverse`, and `replace` change that buffer and return it, so they can chain. |
| `delete` | The end index is exclusive. `"abcde"` after `delete(1, 3)` is `ade`. |
| `StringBuilder.substring` | Returns a `String`. The chain cannot continue with `append`. The builder itself is unchanged by that call. |
| `StringBuilder.equals` | Does not compare characters. It uses reference equality. Compare with `toString().equals`. |
| `+=` on a `String` | Each `+=` builds a new `String` and copies the characters so far. `StringBuilder.append` updates one buffer. |

## Saturday — arrays

| Term | Meaning |
|---|---|
| Array | An object with a fixed size. `new int[3]` holds `0, 0, 0`. `new String[2]` holds `null, null`. |
| `length` | A field. `nums.length()` does not compile. Legal indexes are `0` through `length - 1`. Any other index throws `ArrayIndexOutOfBoundsException`. |
| Brace initializer | `{1, 2}` without `new` is allowed only in the declaration. A later assignment needs `new int[] {1, 2}`. |
| Array field | Defaults to `null`. Reading `null.length` throws `NullPointerException`. |
| `Arrays.sort` | Sorts the array in place. |
| `Arrays.binarySearch` | Defined for a sorted array. A present value returns its index. A missing value returns `-(insertion point) - 1`. On an unsorted array the result is undefined. |
| Insertion point | The index where a missing value would go to keep the array sorted. For a negative search result, the insertion point is `-result - 1`. |
| `Arrays.equals` | Compares elements one level deep. `==` compares the two array references. |
| `Arrays.mismatch` | The first index that differs, or `-1` when the arrays match. |
| `Arrays.compare` | A negative number, zero, or a positive number, in the same style as `compareTo`. |
| `ArrayStoreException` | Thrown when the variable type allows an assignment that the array’s runtime type rejects. `Object[] objects = new String[1]; objects[0] = 1` throws it. |
| Jagged array | An array of arrays whose inner arrays may have different lengths. `new int[2][]` creates two slots and leaves them `null`. Using a null inner array throws `NullPointerException`. |
