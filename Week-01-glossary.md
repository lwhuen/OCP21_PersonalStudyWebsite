# Week 1 glossary — types, operators, and flow

Terms from [Week-01-notes.md](Week-01-notes.md). The exam words are English.

## Monday — a program

| Term | Meaning |
|---|---|
| `main` | The entry point. `public static void main(String[] args)`. `public` and `static` may be swapped. The parameter may be `String[]` or `String...`. |
| Compile | `javac Hello.java` checks the source and writes `Hello.class`. A file that fails to compile never runs. |
| Local variable | A variable declared inside a method. It has no default. Reading it before it is assigned does not compile. |

## Wednesday — primitives, literals, `var`, wrappers

| Term | Meaning |
|---|---|
| Primitive | One of eight types: `byte` 8-bit, `short` 16, `int` 32, `long` 64, `float` 32, `double` 64, `char` 16-bit unsigned, `boolean`. |
| `byte` range | −128 to 127. `byte b = 128` does not compile. |
| `char` | An unsigned number from 0 to 65,535. A negative literal such as `char c = -1` does not compile. A cast such as `(char) -1` does. |
| Field default | A field that is not assigned starts as `0`, `false`, `'\u0000'`, or `null`. Locals do not get these defaults. |
| Literal | A value written in source. A whole number is an `int` unless it ends in `L`. `1.0` is a `double`. A `float` literal ends in `f`. |
| Octal literal | A leading `0` means base 8. `011` is 9. `018` does not compile, because 8 is not an octal digit. |
| Underscore in a number | Allowed only between digits. `1_000` compiles. `10_L`, `0x_11`, and `1_000_` do not. |
| `var` | One local variable with an initializer the compiler can type. Not a field, a parameter, or a return type. `var x;` and `var y = null` do not compile. `var n = (String) null` does, because the cast supplies the type. |
| Scope | The block where a name can be used. An inner block cannot declare `int x` when the outer block already has `int x`. After the inner block ends, the name may be declared again. |
| Wrapper | An object for a primitive: `Integer`, `Long`, `Double`, and the others. On Java 21, `new Integer(1)` does not compile. Use `Integer n = 1` or `Integer.valueOf(1)`. |
| Boxing | Wrapping a primitive in its wrapper. `Integer n = 1` boxes. |
| Unboxing | Taking the primitive out of a wrapper. `int value = n` unboxes. Unboxing `null` throws `NullPointerException`. |
| `Integer` cache | `Integer` reuses one object for each value from −128 to 127. `==` on two wrappers compares references, so `127 == 127` is true and `128 == 128` is false. `equals` compares the number. `Byte`, `Short`, and `Long` use the same cache. `Character` caches 0 to 127. `Float` and `Double` do not cache. |
| Wrapper compared with a primitive | `Integer == int` unboxes the wrapper, so the cache does not matter. `Integer a = 200; int b = 200; a == b` is true. |

## Friday — operators

| Term | Meaning |
|---|---|
| Precedence | Which operator runs first. Postfix `++`, then `*`, then `+`, then `&&`, then `\|\|`, then `?:`. `?:` and assignment associate right to left. Most others associate left to right. |
| Numeric promotion | `byte`, `short`, and `char` arithmetic produces an `int`. A constant expression whose result fits may still be assigned: `byte d = 1 + 2` compiles, `byte c = a + b` does not. |
| Compound assignment | `+=`, `-=`, `*=`, and the rest. The operation includes a hidden cast back to the left-hand type, so `b += 1` compiles when `b = b + 1` does not. `n *= 2 + 3` means `n = n * (2 + 3)`. |
| Postfix and prefix | `x++` contributes the current value, then adds 1. `++x` adds 1, then contributes the new value. After `int x = 1; int y = x++ + ++x`, `x` is 3 and `y` is 4. |
| Short-circuit | `&&` and `\|\|` skip the right side when the result is already known. `&` and `\|` on a boolean always evaluate both sides. |
| Integer division | `5 / 2` is `2`. Truncation is toward zero. The sign of `%` follows the dividend, so `-5 % 2` is `-1`. An `int` divided by zero throws `ArithmeticException`. `1.0 / 0.0` is `Infinity`. |
| Cast | An explicit conversion, such as `(int) 5.0`. Casting a `double` toward zero drops the fraction: `(int) 9.9` is `9` and `(int) -9.9` is `-9`. `(boolean) 1` does not compile. A boolean cannot be cast to or from a number. |
| Shift | An `int` shift distance is taken mod 32, so `1 << 32` is `1 << 0`, which is `1`. `1 << 31` is `Integer.MIN_VALUE`. |
| Ternary | `condition ? a : b`. It associates to the right. Both branches share one type. `flag ? 1 : 2.0` has type `double`. |
| Assignment in `if` | `if (ready = true)` assigns, then tests the assigned boolean. `if (n = 5)` does not compile when `n` is an `int`, because `if` needs a boolean. |

## Saturday and Sunday — `Math` and flow

| Term | Meaning |
|---|---|
| `Math.round` | A tie rounds toward positive infinity. `Math.round(2.5)` is `3`. `Math.round(-1.5)` is `-1`. `round(double)` returns `long`. `round(float)` returns `int`. |
| `Math.floor` | Toward negative infinity. `floor(-1.1)` is `-2.0`. Returns `double`. |
| `Math.ceil` | Toward positive infinity. `ceil(-1.1)` is `-1.0`. Returns `double`. |
| `Math.abs` | The magnitude. `Math.abs(Integer.MIN_VALUE)` stays negative, because the positive value does not fit in an `int`. The same trap exists for `Long.MIN_VALUE`. |
| Dangling `else` | An `else` belongs to the nearest `if`. |
| Unreachable | `while (false)` does not compile. `if (false)` does compile, and the lines after the `if` still run. |
| Single statement | A local-variable declaration cannot be the only statement of an `if` or a loop. Use a block. |
| Classic `switch` | The selector may be `byte`, `short`, `char`, `int`, their wrappers, `String`, or an enum. Not `long`, `float`, `double`, or `boolean`. A case label is a compile-time constant. Duplicate labels do not compile. |
| Fall-through | In a colon `switch`, a case without `break` continues into the next case. `default` may sit anywhere. No match and no `default` means a switch statement does nothing. |
| Arrow `switch` | Cases use `->` and do not fall through. They do not use `break`. Mixing `->` and `:` in one switch does not compile. |
| Switch expression | Produces a value. On an `int` it must cover every remaining value, so it needs a `default` or enough cases. A block produces its value with `yield`. `break 10` is not Java. |
| `null` selector | A `switch` on a `null` `String` throws `NullPointerException` before any case or `default` runs. |
| `do` / `while` | The body runs at least once. The semicolon after `while (...)` is required. `int i = 0; do { print i; } while (i++ < 2);` prints `012`. |
| `break` | Leaves the nearest loop or switch. `break` with a label leaves the named enclosing loop or switch. |
| `continue` | Starts the next iteration of the nearest loop. `continue` with a label must name a loop. |
| Enhanced `for` | `for (int n : nums)` gives `n` a separate copy. Assigning to `n` does not write into the array. A `null` array throws `NullPointerException`. |
