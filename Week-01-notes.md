# Week 1 notes — types, operators, and flow

**23–29 Nov 2026. 21 hours.** This file follows Week 1 of the study plan. The gate is the building-blocks, operators, and decisions questions at **70%** (24 of the 34 questions in this file).

參考書係 Boyarsky 同 Selikoff 嘅 *OCP Oracle Certified Professional Java SE 21 Developer Study Guide*。每章下面嘅頁碼係紙本書。**必睇**先至翻開。**略讀**只核對標題同筆記未寫過嘅一句。**唔使睇**留到標明嗰一週，或者唔使做。每章末嘅 Review Questions 都唔使做，計分用呢份筆記嘅題。書前面嘅 Assessment Test 同網上題庫留到 1 月 18 日。勘誤在 [selikoff.net/ocp21](https://www.selikoff.net/ocp21/)。

Weekdays are Monday, Wednesday, and Friday, 3 hours each: 20 minutes on yesterday’s misses, 2 hours typing every listing, 40 minutes of questions and the notebook. Saturday and Sunday are 6 hours each. Monday has nothing to review yet, so those 20 minutes are the JDK check.

These are the two exam objectives the plan puts in this week:

- Numeric types and boolean logic: primitives, wrapper classes, precedence, promotion, casts, and `Math`.
- Program flow: `if` / `else`, `switch` statements and expressions, loops, `break`, and `continue`.

String methods, arrays, and methods you write yourself are Week 2. Leave them until 30 Nov.

| Day | What the plan says | Where it is in this file |
|---|---|---|
| Mon | Install JDK 21 and IntelliJ. Print one line from `main`. | Monday lab, then Chapter 1 question Q7 |
| Wed | Eight primitives, literals, and `var`. | Primitives through wrappers, then the rest of the Chapter 1 questions |
| Fri | Operators, precedence, and casts. Write the answer before you run it. | Chapter 2 through the operator traps, then the fifteen expressions, then Chapter 2 questions Q1–Q6, Q9, and Q10 |
| Sat | `Math`, `if` / `else`, and both kinds of `switch`. | `Math` lab, Chapter 2 questions Q7 and Q8, then `if` and both switches |
| Sun | Loops, `break`, `continue`, then the review questions. | Loops, the one program, Chapter 3 loop questions, the mixed set, then score all 34 |

Same checklist as the study plan:

- [ ] Install JDK 21 and IntelliJ IDEA Community. `java -version` prints 21. A class with `main` prints your name.
- [ ] Write the eight primitives, their sizes, and their default values from memory.
- [ ] Fifteen expressions on precedence, promotion, and casts. Write the answer first, then run. Keep the misses.
- [ ] One program that uses `if` / `else`, a `switch` expression, `for`, `while`, `break`, and `continue`.
- [ ] Call `Math.abs`, `min`, `max`, `round`, `ceil`, `floor`, and `pow`. `Math.round` on a double returns a `long`.
- [ ] Building-blocks, operators, and decisions review questions at 70%. Each miss: one rule and a five-line program in the notebook.

JDK 21 is already installed on this PC at `C:\Program Files\Java\jdk-21` (version 21.0.9). `JAVA_HOME` points there. Monday still confirms `java -version`, then IntelliJ.

The questions are practice in the exam’s style. They are not copied from the real exam or from a book. Try each one before its answer key.

---

# Chapter 1 — Building blocks

> **必睇**　參考書第 1 章 Building Blocks，pp. 2–30 同 pp. 34–52：由 “Learning About the Environment” 到 “Managing Variable Scope”，再加 Summary 同 Exam Essentials。
>
> **唔使睇**　“Defining Text Blocks”（pp. 31–33，第 2 週）、“Destroying Objects”（第 3 週，就在本章 Summary 前面）、Review Questions（p. 53 起）。

## What you must know

A Java file holds one or more classes. The file name matches the `public` class. `javac Hello.java` compiles it to `Hello.class`. `java Hello` runs it. The exam uses snippets, so you have to imagine that wrapping class yourself.

### A valid `main`

The program starts at:

```java
public static void main(String[] args) {}
```

These also work:

```java
static public void main(String[] args) {}
public static void main(String... args) {}
public static void main(String args[]) {}
```

`public` and `static` may be swapped. The parameter may be a `String` array or `String` varargs. The name is `main`, the return type is `void`. Anything else (`Main`, a return of `int`, a parameter of `int[]`) compiles as an ordinary method and is not the entry point. On Java 21 the exam still uses this classic `main`.

### Monday lab — JDK, IntelliJ, one line from `main`

1. Open a new terminal and run `java -version`. The first line should contain `21`. PowerShell often shows that line in red because Java writes it to the error stream. The version text is the result.
2. Install IntelliJ IDEA Community if it is not installed yet. In the new project dialog, set the JDK to **21** and the folder `C:\Program Files\Java\jdk-21`.
3. Type this class. The printed line is your name.

```java
public class Hello {
    public static void main(String[] args) {
        System.out.println("Your Name");
    }
}
```

4. Run it from IntelliJ. Then answer Chapter 1 question Q7. That is Monday’s question time.

### Wednesday — eight primitives, literals, and `var`

Close this file and write the eight primitives, their sizes, and their default field values from memory. Then check the table. After the table, read literals and `var`, and type every listing. Wrappers are the same day’s reading: the week’s exam topic is numeric types, and the Chapter 1 questions use them. End Wednesday with Chapter 1 questions Q1–Q6 and Q8 (40 minutes). Each miss goes in the notebook.

### The eight primitives

| Type | Size | Default on a field | Range to remember |
|---|---|---|---|
| `byte` | 8-bit | `0` | -128 to 127 |
| `short` | 16-bit | `0` | -32,768 to 32,767 |
| `int` | 32-bit | `0` | about ±2.1 billion |
| `long` | 64-bit | `0` | needs an `L` suffix on big literals |
| `float` | 32-bit | `0.0f` | literal needs `f` |
| `double` | 64-bit | `0.0` | default for `1.0` |
| `char` | 16-bit unsigned | `'\u0000'` | 0 to 65,535 |
| `boolean` | — | `false` | only `true` or `false` |

Fields (instance or `static`) get those defaults. **Local variables do not.** Reading a local variable before it has been assigned is a compile error.

```java
public class Defaults {
    static int count;          // 0
    static boolean ready;      // false
    static String name;        // null, a reference, not a primitive

    public static void main(String[] args) {
        int local;
        // System.out.println(local); // does not compile
        local = 1;
        System.out.println(local);    // 1
    }
}
```

`String` is a class. Its default on a field is `null`. A local `String` still must be assigned before you read it.

### Literals

```java
int n = 1_000_000;     // underscores sit between digits
long big = 3_000_000_000L;
float f = 1.0f;
double d = 1.0;        // 1.0 is a double
char c = 'A';
char c2 = 65;          // 65 fits in a char, so this compiles
boolean b = true;
int hex = 0x1F;        // 31
int bin = 0b1010;      // 10
int oct = 011;         // octal: 9, not 11
```

Rules the exam uses:

- `1.0` is a `double`. `float f = 1.0;` does not compile. `float f = 1;` does, because an `int` widens to `float`.
- A whole number is an `int`. `long x = 3000000000;` does not compile. Write `3000000000L`.
- `byte b = 128;` does not compile. 128 does not fit. `byte b = 127;` does.
- `char c = -1;` does not compile. A `char` cannot be negative. `char c = (char) -1;` compiles.
- A leading zero means octal. `011` is 9. `018` does not compile, because 8 is not an octal digit.
- Underscores must sit between digits. `_1`, `1_`, `1_.0`, and `1_L` do not compile. `1_000` and `1__000` do.

### `var` is for local variables only

```java
var count = 1;                 // int
var price = 1.0;               // double
var name = "ocp";              // String
var nums = new int[] {1, 2};   // int[]
```

These do not compile:

```java
var x;                  // no initializer, so no type to infer
var y = null;           // null has no type
var z = {1, 2};         // an array initializer needs a type on the left, or new
var a = 1, b = 2;       // only one variable
```

`var` cannot be a field, a parameter, or a return type. `var` is a type name, so `int var = 1;` is legal. `var n = (String) null;` compiles, because the cast tells the compiler the type.

### Scope

A local variable lives from its declaration to the end of the block. A nested block cannot declare the same name again.

```java
public static void main(String[] args) {
    int x = 1;
    {
        // int x = 2;   // does not compile: x is already in scope
        int y = 2;
    }
    // y is gone here
    int y = 3;          // legal, the previous y is out of scope
}
```

### Wrapper classes

Each primitive has a class: `Byte`, `Short`, `Integer`, `Long`, `Float`, `Double`, `Character`, `Boolean`.

Assigning a primitive to a wrapper is **boxing**. The other direction is **unboxing**.

```java
Integer count = 10;     // boxing
int n = count;          // unboxing
```

On Java 21 the constructors are gone. `new Integer(1)` does not compile. Use assignment or `Integer.valueOf(1)`.

`Integer.parseInt("10")` returns an `int` and throws `NumberFormatException` on `"ten"`. `Integer.valueOf("10")` returns an `Integer`.

Unboxing `null` throws `NullPointerException`:

```java
Integer empty = null;
int n = empty;          // NullPointerException
```

`Integer.valueOf` caches **-128 to 127**. `==` on two wrappers compares references. Inside the cache they are often the same object. Outside it, two equal values can be different objects. Use `equals` to compare values.

```java
Integer a = 127;
Integer b = 127;
System.out.println(a == b);       // true, cached

Integer c = 128;
Integer d = 128;
System.out.println(c == d);       // false, different objects
System.out.println(c.equals(d));  // true

Integer e = 1000;
int f = 1000;
System.out.println(e == f);       // true, the wrapper is unboxed
```

`Byte`, `Short`, and `Long` use the same -128 to 127 cache. `Character` caches 0 to 127. `Float` and `Double` do not cache, so `==` on two `Float` objects is a reference check even for small values.

## Chapter 1 questions

**Q1.** What is the output?

```java
public class Q1 {
    static int count;
    static boolean ready;
    public static void main(String[] args) {
        System.out.print(count);
        System.out.print(ready);
    }
}
```

A. `0false`
B. `0true`
C. The code does not compile
D. A `NullPointerException` is thrown

**Q2.** Which of the following compile? (Choose all that apply.)

```java
byte a = 127;
byte b = 128;
long c = 3_000_000_000;
long d = 3_000_000_000L;
float e = 1.0;
char f = 65;
int g = 018;
int h = 011;
```

A. `a`
B. `b`
C. `c`
D. `d`
E. `e`
F. `f`
G. `g`
H. `h`

**Q3.** What is the result?

```java
public class Q3 {
    public static void main(String[] args) {
        int local;
        System.out.println(local);
    }
}
```

A. `0`
B. `null`
C. The code does not compile
D. A `NullPointerException` is thrown

**Q4.** Which lines compile? (Choose all that apply.)

```java
var a = 10;
var b = null;
var c = (String) null;
var d = {1, 2};
var e = new int[] {1, 2};
var f = 1, g = 2;
```

A. The line with `a`
B. The line with `b`
C. The line with `c`
D. The line with `d`
E. The line with `e`
F. The line with `f` and `g`

**Q5.** What is the output?

```java
public class Q5 {
    public static void main(String[] args) {
        Integer a = 128;
        Integer b = 128;
        Integer c = 100;
        Integer d = 100;
        System.out.print(a == b);
        System.out.print(" ");
        System.out.print(c == d);
        System.out.print(" ");
        System.out.print(a.equals(b));
    }
}
```

A. `true true true`
B. `false true true`
C. `false false true`
D. `true false true`

**Q6.** What is the result?

```java
public class Q6 {
    public static void main(String[] args) {
        Integer n = null;
        int value = n;
        System.out.println(value);
    }
}
```

A. `0`
B. `null`
C. The code does not compile
D. A `NullPointerException` is thrown

**Q7.** What is the output of this legal entry-point class? If it does not run, choose the reason.

```java
public class Q7 {
    static public void main(String args[]) {
        System.out.println("go");
    }
}
```

A. `go`
B. The code does not compile
C. It compiles, but there is no valid `main`, so it does not start
D. A `NullPointerException` is thrown

**Q8.** Which snippet compiles?

A.

```java
{
    int x = 1;
}
int x = 2;
```

B.

```java
int x = 1;
{
    int x = 2;
}
```

C.

```java
int value = 1_000_;
```

D.

```java
Integer n = new Integer(5);
```

### Chapter 1 answers

**Q1 — A.** A missing `int` field is `0`. A missing `boolean` field is `false`. Printing them produces `0false` with no space.

**Q2 — A, D, F, H.** `127` fits in a `byte`. `128` does not. `3_000_000_000` is an `int` literal that is too big; the `L` makes it a `long`. `1.0` is a `double` and does not fit in a `float` variable without a cast or an `f`. `65` fits in a `char`. `018` is illegal octal. `011` is octal for 9, and it compiles.

**Q3 — C.** `local` is a local variable. Locals have no default. Reading it before assignment does not compile. The same name as a field would have printed `0`.

**Q4 — A, C, E.** `var` needs an initializer with a clear type. `null` alone has no type. A cast supplies one. `{1, 2}` is not a standalone expression. `new int[] {1, 2}` is. `var` declares one variable, so the comma form does not compile.

**Q5 — B.** `128` is outside the `Integer` cache, so `a == b` is `false`. `100` is inside -128 to 127, so `c == d` is `true`. `equals` compares the numeric value, so the last print is `true`.

**Q6 — D.** The assignment unboxes `n`. Unboxing `null` throws `NullPointerException`. The code does compile.

**Q7 — A.** `static` and `public` may appear in either order. `String args[]` is a `String` array. This is a valid `main`, and it prints `go`.

**Q8 — A.** After the inner block ends, `x` can be declared again. A nested block cannot reuse a name that is already in scope, so B fails. An underscore cannot be the last character of a literal, so C fails. `new Integer(5)` does not compile on Java 21, so D fails.

---

# Chapter 2 — Operators

> **必睇**　參考書第 2 章 Operators，pp. 64–92：由 “Understanding Java Operators” 到 Exam Essentials。同第 4 章 “Calculating with Math APIs” pp. 202–203（`min`、`max`、`round`、`ceil`、`floor`、`pow`）。
>
> **唔使睇**　bitwise operators（p. 86。筆記 “Shifts” 一段就夠）、`BigInteger`（p. 204）、第 4 章其餘部分、Review Questions（p. 93 起）。

**Friday** is this chapter through the operator traps, then the fifteen expressions. Skip `Math` until Saturday. The shift section is part of Friday only after the fifteen expressions are done; Chapter 2 question Q10 uses one shift.

**Saturday part 1** is the `Math` section, the `Math` lab, and Chapter 2 questions Q7 and Q8.

## What you must know

The exam asks you to evaluate an expression by hand. Precedence decides what happens first. When two operators share a precedence, most of them associate left to right. Assignment and the ternary operator associate right to left.

### Precedence, highest first

1. Postfix `x++` `x--`
2. Prefix `++x` `--x` `+` `-` `!`
3. Cast `(int)`
4. `*` `/` `%`
5. `+` `-` (and string concatenation, which is the same `+`)
6. Shifts `<<` `>>` `>>>`
7. Relational `<` `>` `<=` `>=` `instanceof`
8. Equality `==` `!=`
9. `&`
10. `^`
11. `|`
12. `&&`
13. `||`
14. Ternary `?:`
15. Assignment `=` `+=` `-=` `*=` and the rest

`instanceof` returns in week 4 with classes. For this week, remember that it sits with the relational operators.

### Numeric promotion

Smaller integer types are promoted to `int` before arithmetic. `byte`, `short`, and `char` arithmetic produces an `int`.

```java
byte a = 1;
byte b = 2;
byte c = a + b;     // does not compile: a + b is an int
byte d = 1 + 2;     // compiles: 1 + 2 is a constant that fits in a byte
```

Binary promotion for an operator with two numbers:

- if either side is `double`, the other becomes `double`
- else if either is `float`, the other becomes `float`
- else if either is `long`, the other becomes `long`
- else both become `int`

A widening assignment is free: `int` to `long`, `float` to `double`. A narrowing assignment needs a cast: `long` to `int`, `double` to `int`. The cast truncates toward zero. `(int) 9.9` is `9`. `(int) -9.9` is `-9`.

A `boolean` cannot be cast to a number, and a number cannot be cast to a `boolean`.

### The operators that generate traps

Integer division truncates toward zero. `5 / 2` is `2`. `5 % 2` is `1`. The sign of `%` follows the dividend: `-5 % 2` is `-1`.

Dividing an integer by zero throws `ArithmeticException`. Dividing a floating-point value by zero does not: `1.0 / 0.0` is `Infinity`, and `0.0 / 0.0` is `NaN`.

`+` is left to right. Once a `String` appears, the rest is concatenation.

```java
System.out.println(1 + 2 + "3" + 4 + 5);   // 3345
System.out.println("3" + 1 + 2);           // 312
```

`&&` and `||` stop early. `&` and `|` on booleans always evaluate both sides. On numbers, `&` `|` `^` are bitwise.

```java
int x = 0;
boolean left = false && ++x > 0;   // x stays 0
boolean both = false & ++x > 0;    // x becomes 1
```

`^` on booleans is exclusive or: `true ^ false` is `true`, `true ^ true` is `false`.

A compound assignment includes a hidden cast, and the right-hand side is evaluated as a whole:

```java
byte b = 1;
b += 1;            // compiles: b = (byte) (b + 1)
b = b + 1;         // does not compile

int n = 5;
n *= 2 + 3;        // n = 5 * (2 + 3) = 25
```

`x++` returns the old value, then adds one. `++x` adds one, then returns the new value.

```java
int x = 1;
int y = x++ + ++x;   // 1 + 3, and x is now 3
```

The ternary operator associates to the right. Both branches must end up as one type. `flag ? 1 : 2.0` has type `double`. Assigning that to an `int` does not compile.

An assignment is an expression. `if (ready = true)` assigns `true` and then tests it, when `ready` is a `boolean`. `if (n = 5)` does not compile when `n` is an `int`, because the value of the assignment is an `int`, and `if` requires a `boolean`.

### Shifts

Read this on Friday after the fifteen expressions. `<<` shifts left. `>>` shifts right and keeps the sign. `>>>` shifts right and fills with zeros. For an `int`, the distance is taken mod 32. `1 << 32` is `1`, because the distance is 0. `1 << 31` is `Integer.MIN_VALUE`.

### Friday task — fifteen expressions

Write the value, and the type when it matters, before you compile anything. Then type each line into `main` and run it. Keep every miss.

1. `1 + 2 * 3`
2. `(1 + 2) * 3`
3. `5 / 2`
4. `5 / 2.0`
5. `(int) (5 / 2.0)`
6. `(int) 5 / 2.0`
7. `(double) (5 / 2)`
8. `(double) 5 / 2`
9. `10 % 3`
10. `-5 % 2`
11. `(int) 9.9`
12. `(int) -9.9`
13. `1 + 2 + "3" + 4`
14. `true || false && false`
15. `(byte) 200`

The answer key is after the Chapter 2 answers. Do not scroll to it yet.

Friday’s question time, after the expressions: Chapter 2 questions Q1–Q6, Q9, and Q10.

### Saturday part 1 — `Math`

Call each method below by typing the lab. `Math.round` on a double returns a `long`. That is the checklist item.

| Call | Returns | Rule |
|---|---|---|
| `Math.abs` | same type as the argument | `Math.abs(Integer.MIN_VALUE)` stays negative, because the positive value does not fit in an `int` |
| `Math.min` / `Math.max` | the type of the overload you called | |
| `Math.round(double)` | `long` | ties go toward positive infinity |
| `Math.round(float)` | `int` | same tie rule |
| `Math.ceil` | `double` | toward positive infinity |
| `Math.floor` | `double` | toward negative infinity |
| `Math.pow` | `double` | |
| `Math.random` | `double` | from 0.0 inclusive to 1.0 exclusive |

`Math.round(2.5)` is `3`. `Math.round(-1.5)` is `-1`, because the tie rounds toward positive infinity. `Math.ceil(-1.1)` is `-1.0`. `Math.floor(-1.1)` is `-2.0`.

`int i = Math.round(2.5);` does not compile, because that overload returns a `long`. `int i = Math.round(2.5f);` compiles.

Type this class and run it. Leave the commented line commented, then uncomment it once and confirm the compile error.

```java
public class MathCalls {
    public static void main(String[] args) {
        System.out.println(Math.abs(-7));
        System.out.println(Math.min(3, 8));
        System.out.println(Math.max(3, 8));
        long rounded = Math.round(2.5);
        System.out.println(rounded);
        System.out.println(Math.ceil(1.2));
        System.out.println(Math.floor(1.2));
        System.out.println(Math.pow(2, 3));
        // int bad = Math.round(2.5);
    }
}
```

Saturday’s question time for this half: Chapter 2 questions Q7 and Q8. Then go to Chapter 3 for `if` / `else` and both kinds of `switch`.

## Chapter 2 questions

Q1–Q6, Q9, and Q10 are Friday. Q7 and Q8 are Saturday.

**Q1.** What is the output?

```java
public class Q1 {
    public static void main(String[] args) {
        System.out.println(1 + 2 + "3" + 4 + 5);
    }
}
```

A. `15`
B. `3345`
C. `12345`
D. The code does not compile

**Q2.** Which lines compile? (Choose all that apply.)

```java
byte a = 1;
byte b = 2;
byte c = a + b;
byte d = 1 + 2;
byte e = (byte) (a + b);
int f = a + b;
```

A. The declaration of `a`
B. The declaration of `c`
C. The declaration of `d`
D. The declaration of `e`
E. The declaration of `f`

**Q3.** What is the output?

```java
public class Q3 {
    public static void main(String[] args) {
        int x = 1;
        int y = x++ + ++x;
        System.out.print(x);
        System.out.print(y);
    }
}
```

A. `23`
B. `33`
C. `34`
D. `24`

**Q4.** What is the output?

```java
public class Q4 {
    public static void main(String[] args) {
        int x = 0;
        if (false && ++x == 1) {}
        System.out.print(x);
        if (false & ++x == 1) {}
        System.out.print(x);
    }
}
```

A. `00`
B. `01`
C. `11`
D. An `ArithmeticException` is thrown

**Q5.** What is the result?

```java
public class Q5 {
    public static void main(String[] args) {
        byte b = 1;
        b += 1;
        System.out.println(b);
    }
}
```

A. `1`
B. `2`
C. The code does not compile
D. A `NullPointerException` is thrown

**Q6.** What is the output?

```java
public class Q6 {
    public static void main(String[] args) {
        int n = 5;
        n *= 2 + 3;
        System.out.println(n);
    }
}
```

A. `13`
B. `25`
C. `10`
D. The code does not compile

**Q7.** What is the output?

```java
public class Q7 {
    public static void main(String[] args) {
        System.out.print(Math.round(2.5));
        System.out.print(" ");
        System.out.print(Math.round(-1.5));
        System.out.print(" ");
        System.out.print(Math.floor(-1.1));
    }
}
```

A. `2 -1 -1.0`
B. `3 -1 -2.0`
C. `3 -2 -1.0`
D. `2 -2 -2.0`

**Q8.** Which of the following compile? (Choose all that apply.)

```java
int a = Math.round(2.5);
int b = Math.round(2.5f);
long c = Math.round(2.5);
int d = (int) Math.ceil(1.2);
int e = Math.abs(Integer.MIN_VALUE);
boolean f = (boolean) 1;
```

A. `a`
B. `b`
C. `c`
D. `d`
E. The line that calls `Math.abs` compiles, and the value is negative
F. `f`

**Q9.** What is the output?

```java
public class Q9 {
    public static void main(String[] args) {
        int x = 10;
        int y = 20;
        System.out.println(x > 5 ? y > 15 ? 1 : 2 : 3);
    }
}
```

A. `1`
B. `2`
C. `3`
D. The code does not compile

**Q10.** What is the result?

```java
public class Q10 {
    public static void main(String[] args) {
        System.out.println(1 << 32);
    }
}
```

A. `0`
B. `1`
C. `32`
D. The code does not compile

### Chapter 2 answers

**Q1 — B.** `1 + 2` happens first and is `3`. Then `"3"` turns the expression into a `String`, so `4` and `5` are concatenated. The print is `3345`.

**Q2 — A, C, D, E.** `a` is a constant that fits. `a + b` has type `int`, so storing it in a `byte` needs a cast. `1 + 2` is a constant expression whose result fits in a `byte`. The explicit cast compiles. Assigning the `int` sum to an `int` compiles.

**Q3 — C.** `x` starts at 1. `x++` contributes 1 and leaves `x` at 2. `++x` raises `x` to 3 and contributes 3. `y` is 4. The print is `x` then `y`: `34`.

**Q4 — B.** `&&` does not evaluate `++x`, so the first print is `0`. `&` on a `boolean` evaluates both sides, so `x` becomes 1 and the second print is `1`.

**Q5 — B.** `b += 1` is `b = (byte) (b + 1)`. It compiles and prints `2`. The line `b = b + 1` would not compile. That line is not in this question.

**Q6 — B.** `n *= 2 + 3` is `n = n * (2 + 3)`. `5 * 5` is `25`.

**Q7 — B.** A tie rounds toward positive infinity, so `2.5` rounds to `3` and `-1.5` rounds to `-1`. `floor` goes toward negative infinity, so `-1.1` becomes `-2.0`.

**Q8 — B, C, D, E.** `Math.round(double)` returns a `long`, so A does not compile and C does. `Math.round(float)` returns an `int`. `ceil` returns a `double`; the cast makes an `int` of `2`. `Math.abs(Integer.MIN_VALUE)` compiles and returns `Integer.MIN_VALUE`, which is negative. A `boolean` cast of `1` does not compile.

**Q9 — A.** `?:` associates to the right, so this is `x > 5 ? (y > 15 ? 1 : 2) : 3`. `x > 5` is true and `y > 15` is true, so the result is `1`.

**Q10 — B.** An `int` shift distance is taken mod 32. `32 % 32` is `0`, so this is `1 << 0`, which is `1`.

### Friday expression answers

1. `7`. Multiplication happens before addition.
2. `9`. The parentheses run first.
3. `2`. Integer division truncates toward zero.
4. `2.5`. The `double` promotes the division.
5. `2`. The division is a `double`, then the cast truncates.
6. `2.5`. The cast applies only to `5`, then `5 / 2.0` is a `double` division.
7. `2.0`. `5 / 2` is already `2` before the cast widens it.
8. `2.5`. The cast makes `5` a `double` before the division.
9. `1`.
10. `-1`. The sign of `%` follows the dividend.
11. `9`. A cast toward zero drops the fraction.
12. `-9`. Same rule for a negative value.
13. `"334"`. `1 + 2` is `3`, then the `String` turns the rest into concatenation.
14. `true`. `&&` runs before `||`, so this is `true || (false && false)`.
15. `-56`. `200` does not fit in a `byte`. The low 8 bits are kept.

---

# Chapter 3 — Making decisions

> **必睇**　參考書第 3 章 Making Decisions：pp. 102–105（`if` / `else`）、pp. 111–123（`switch` 語句同表達式）、pp. 130–149（迴圈、`break`、`continue`、Summary、Exam Essentials）。
>
> **唔使睇**　“Shortening Code with Pattern Matching”（pp. 106–110）同 “Using Pattern Matching with switch”（pp. 124–129）。呢兩節係第 4 週。Review Questions（p. 150 起）唔使做。

**Saturday part 2** is `if` / `else`, the `switch` statement, and the `switch` expression. Stop before “Loops”.

**Sunday** is loops, `break`, `continue`, the one program, and then every review question in this file.

## What you must know

`if` requires a `boolean`. An `int` is not a condition. Braces are optional around one statement, and a declaration cannot be that one statement.

```java
if (true)
    int x = 1;     // does not compile
```

`else` binds to the nearest `if`.

### `switch` statement

A classic `switch` accepts `byte`, `short`, `char`, `int`, the matching wrappers, `String`, and (from week 4) an enum. It does not accept `long`, `float`, `double`, or `boolean`.

A `case` label is a compile-time constant. Duplicate labels do not compile. Without `break`, execution falls into the next case. `default` may sit anywhere. A `switch` statement with no matching case and no `default` does nothing.

```java
int n = 1;
switch (n) {
    case 1:
        System.out.print("A");
    case 2:
        System.out.print("B");
        break;
    default:
        System.out.print("C");
}
// AB
```

Arrow form is also a statement. Arrows do not fall through, so `break` is not used:

```java
switch (n) {
    case 1 -> System.out.print("A");
    case 2, 3 -> System.out.print("B");
    default -> System.out.print("C");
}
```

You cannot mix `->` and `:` in one `switch`. A `null` selector throws `NullPointerException` before any case runs.

### `switch` expression

A `switch` expression produces a value. It must be exhaustive, so an `int` or a `String` needs a `default` (or enough cases for the compiler to see that every value is covered). It ends with a semicolon when you assign it.

```java
int result = switch (n) {
    case 1 -> 10;
    case 2 -> 20;
    default -> 0;
};
```

A block on the right of `->` uses `yield` to produce the value:

```java
int result = switch (n) {
    case 1 -> {
        System.out.print("A");
        yield 10;
    }
    default -> 0;
};
```

Colon form inside an expression uses `yield` as well. Falling out of a case without `yield` does not compile. `yield` belongs to a `switch` expression. `break 10;` is not Java.

When every constant of an enum is listed, a `switch` expression on that enum can omit `default`. Enums are week 4. Pattern matching in `switch` is week 4 as well.

### Sunday — loops, `break`, `continue`, then the review

`while` tests first. The body can be skipped. `do` / `while` runs the body once, then tests. The semicolon after `while (...)` is required.

```java
int i = 0;
do {
    System.out.print(i);
} while (i++ < 2);     // prints 012
```

`for` has init, condition, and update. The init variable’s scope is the loop. All three parts are optional. `for (;;)` is an infinite loop.

The enhanced `for` walks an array or an `Iterable`. The loop variable is a new variable each time. Assigning to it does not change the array. A `null` array throws `NullPointerException`.

```java
int[] nums = {1, 2, 3};
for (int n : nums) {
    n = 0;             // changes the copy, not the array
}
```

A declaration cannot be the single statement of a loop:

```java
for (int i = 0; i < 3; i++)
    int x = i;         // does not compile
```

### Unreachable code

`while (false)` does not compile. `if (false) { ... }` does compile, and the lines after the `if` still run. This special case is only for `if`. An infinite `while (true)` makes the lines after the loop unreachable, unless a `break` makes them reachable.

### `break` and `continue`

`break` leaves the nearest loop or `switch`. `continue` starts the next iteration of the nearest loop. A label sits in front of a statement:

```java
outer:
for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
        if (j == 1) break outer;
    }
}
```

`break` with a label must be inside that labeled loop or `switch`. `continue` with a label must be inside that labeled loop. The label name is an identifier, not a `String`.

### Sunday task — the one program

Type this after the loop section. It is the checklist program: `if` / `else`, a `switch` expression, `for`, `while`, `break`, and `continue`. Write the output on paper, then run it.

```java
public class Week1Flow {
    public static void main(String[] args) {
        int n = 2;
        if (n > 0) {
            System.out.println("positive");
        } else {
            System.out.println("not positive");
        }

        String label = switch (n) {
            case 1 -> "one";
            case 2 -> "two";
            default -> "other";
        };
        System.out.println(label);

        for (int i = 0; i < 3; i++) {
            if (i == 1) {
                continue;
            }
            System.out.println("for " + i);
        }

        int j = 0;
        while (j < 3) {
            if (j == 2) {
                break;
            }
            System.out.println("while " + j);
            j++;
        }
    }
}
```

The run prints:

```text
positive
two
for 0
for 2
while 0
while 1
```

Sunday’s question time is Chapter 3 questions Q6–Q10, then the mixed set. Q1–Q5 are the Saturday `if` and `switch` questions; do them on Saturday if you have not already. After that, score all 34 questions. **24 or more** meets the gate. Every miss becomes one rule and a five-line program before Monday of Week 2.

## Chapter 3 questions

Q1–Q5 are Saturday. Q6–Q10 are Sunday.

**Q1.** What is the output?

```java
public class Q1 {
    public static void main(String[] args) {
        if (false)
            if (true)
                System.out.print("A");
            else
                System.out.print("B");
        System.out.print("C");
    }
}
```

A. `AC`
B. `BC`
C. `C`
D. The code does not compile

**Q2.** What is the output?

```java
public class Q2 {
    public static void main(String[] args) {
        int n = 1;
        switch (n) {
            case 1:
                System.out.print("A");
            case 2:
                System.out.print("B");
                break;
            default:
                System.out.print("C");
        }
    }
}
```

A. `A`
B. `AB`
C. `ABC`
D. `AC`

**Q3.** What is the result?

```java
public class Q3 {
    public static void main(String[] args) {
        int n = 2;
        int result = switch (n) {
            case 1 -> 10;
            case 2 -> 20;
        };
        System.out.println(result);
    }
}
```

A. `20`
B. `0`
C. The code does not compile
D. A `NullPointerException` is thrown

**Q4.** What is the output?

```java
public class Q4 {
    public static void main(String[] args) {
        int n = 1;
        int result = switch (n) {
            case 1 -> {
                System.out.print("A");
                yield 10;
            }
            case 2 -> 20;
            default -> 0;
        };
        System.out.print(result);
    }
}
```

A. `A10`
B. `10`
C. `A`
D. The code does not compile

**Q5.** What is the output?

```java
public class Q5 {
    public static void main(String[] args) {
        String s = null;
        switch (s) {
            default -> System.out.print("X");
        }
    }
}
```

A. `X`
B. No output
C. The code does not compile
D. A `NullPointerException` is thrown

**Q6.** What is the output?

```java
public class Q6 {
    public static void main(String[] args) {
        int i = 0;
        do {
            System.out.print(i);
        } while (i++ < 2);
    }
}
```

A. `01`
B. `012`
C. `0123`
D. The code does not compile

**Q7.** What is the output?

```java
public class Q7 {
    public static void main(String[] args) {
        int count = 0;
        outer:
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                count++;
                if (i == 1) break outer;
            }
        }
        System.out.println(count);
    }
}
```

A. `3`
B. `4`
C. `6`
D. `9`

**Q8.** Which snippets compile? (Choose all that apply.)

A.

```java
while (false) {
    System.out.print("A");
}
```

B.

```java
if (false) {
    System.out.print("A");
}
System.out.print("B");
```

C.

```java
for (int i = 0; i < 2; i++)
    int x = i;
```

D.

```java
int n = 1;
switch (n) {
    case 1 -> System.out.print("A");
    case 1 -> System.out.print("B");
}
```

**Q9.** What is the output?

```java
public class Q9 {
    public static void main(String[] args) {
        int[] nums = {1, 2, 3};
        for (int n : nums) {
            n = 9;
        }
        System.out.print(nums[0]);
    }
}
```

A. `9`
B. `1`
C. `123`
D. A `NullPointerException` is thrown

**Q10.** What is the result?

```java
public class Q10 {
    public static void main(String[] args) {
        boolean ready = false;
        if (ready = true)
            System.out.print("yes");
        else
            System.out.print("no");
    }
}
```

A. `yes`
B. `no`
C. The code does not compile
D. No output

### Chapter 3 answers

**Q1 — C.** The `else` belongs to the inner `if`. The outer condition is `false`, so the inner `if` never runs and neither branch prints. The statement after the whole `if` prints `C`.

**Q2 — B.** Case `1` has no `break`, so execution falls into case `2`, prints `B`, and then `break` leaves the `switch`. `default` does not run. The output is `AB`.

**Q3 — C.** A `switch` expression on an `int` must cover every remaining value. There is no `default`, so the code does not compile. The same cases in a `switch` statement would compile and do nothing for an unmatched value.

**Q4 — A.** The arrow block runs, prints `A`, and `yield 10` becomes the value of the expression. The following print adds `10`. Output is `A10`.

**Q5 — D.** The selector is evaluated first. A `null` `String` throws `NullPointerException`. `default` does not get a chance to run.

**Q6 — B.** The body prints, then the condition uses the current `i` and increments it. Prints happen at `i` equal to 0, 1, and 2. When `i` is 2 the test `2 < 2` fails after that print. Output is `012`.

**Q7 — B.** `i` is 0 for a full inner loop: `count` becomes 3. `i` becomes 1, the inner loop increments `count` to 4, and `break outer` leaves both loops. The print is `4`.

**Q8 — B.** `while (false)` is unreachable code and does not compile. `if (false)` is allowed, and the print of `B` is reachable. A local-variable declaration cannot be the single statement of a `for`. Duplicate case labels do not compile.

**Q9 — B.** The enhanced-for variable is a separate `int`. Assigning `9` to it does not write into the array. `nums[0]` is still `1`.

**Q10 — A.** `ready = true` assigns `true` and the assignment’s value is `true`, so the `if` body runs and prints `yes`. The same pattern with an `int` would not compile.

---

# Sunday mixed set

> **唔使睇**　呢個混合題用筆記計分。唔好翻第 3 章嘅 Review Questions。

Do this set after `Week1Flow` and Chapter 3 questions Q6–Q10. Then score Chapter 1 (8), Chapter 2 (10), Chapter 3 (10), and this set (6) together. There are 34 questions. **24 or more** is the Week 1 gate from the study plan. Redo every miss before Monday of Week 2.

**M1.** What is the output?

```java
public class M1 {
    static char letter;
    public static void main(String[] args) {
        System.out.println((int) letter);
    }
}
```

A. A blank line
B. `0`
C. `null`
D. The code does not compile

**M2.** What is the output?

```java
public class M2 {
    public static void main(String[] args) {
        System.out.print(5 / 2);
        System.out.print(" ");
        System.out.print(-5 % 2);
    }
}
```

A. `2.5 -1`
B. `2 -1`
C. `2 1`
D. An `ArithmeticException` is thrown

**M3.** What is the result?

```java
public class M3 {
    public static void main(String[] args) {
        int n = 0;
        switch (n) {
            case 1 -> System.out.print("A");
            default -> System.out.print("B");
        }
    }
}
```

A. `A`
B. `B`
C. `AB`
D. The code does not compile

**M4.** What is the output?

```java
public class M4 {
    public static void main(String[] args) {
        int x = 0;
        for (int i = 0; i < 3; i++) {
            if (i == 1) continue;
            x++;
        }
        System.out.println(x);
    }
}
```

A. `1`
B. `2`
C. `3`
D. The code does not compile

**M5.** Which line does not compile?

```java
int a = 1_000;
double b = 1_000.00;
float c = 10.0_0F;
long d = 10_L;
int e = 0x_11;
```

A. `a`
B. `b`
C. `c`
D. `d`
E. `e`
F. More than one of these

**M6.** What is the output?

```java
public class M6 {
    public static void main(String[] args) {
        Integer a = 200;
        int b = 200;
        System.out.print(a == b);
        System.out.print(Math.ceil(1.0));
    }
}
```

A. `true1.0`
B. `false1.0`
C. `true2.0`
D. A `NullPointerException` is thrown

### Mixed answers

**M1 — B.** A `char` field defaults to `'\u0000'`, whose numeric value is 0. The cast prints `0`.

**M2 — B.** Integer division truncates toward zero, so `5 / 2` is `2`. The remainder keeps the sign of the dividend, so `-5 % 2` is `-1`.

**M3 — B.** This is a `switch` statement in arrow form. `n` is `0`, so only `default` runs. Arrows do not fall through.

**M4 — B.** `continue` skips the rest of the body when `i` is 1. `x` is incremented for `i` equal to 0 and `i` equal to 2. The print is `2`.

**M5 — F.** `10_L` puts an underscore next to the suffix, and `0x_11` puts an underscore at the start of the digits. Both fail. The other three are legal.

**M6 — A.** Comparing a wrapper to a primitive unboxes the wrapper, so `200 == 200` is `true` even though 200 is outside the cache. `ceil(1.0)` is already an integer value, so it stays `1.0`.

---

# Rules to copy onto one card

- Fields get defaults. Local variables must be assigned before they are read.
- `byte`, `short`, and `char` arithmetic produces an `int`. A constant that fits may still be assigned.
- `+=` casts back to the left-hand type. `b = b + 1` does not.
- `&&` and `||` can skip the right side. `&` and `|` do not.
- `Integer` `==` is a reference compare, except when one side is a primitive and gets unboxed. The cache is -128 to 127. `equals` compares values.
- `Math.round(double)` returns a `long`. Ties go toward positive infinity, so `round(-1.5)` is `-1`.
- A `switch` statement can fall through when it uses colons. A `switch` expression must cover every value and uses `yield` inside a block.
- `else` binds to the nearest `if`. `while (false)` does not compile. `if (false)` does.
- `break` leaves a loop or a `switch`. `continue` goes to the next iteration. A label is how you name the outer one.
