# Week 2 notes — methods, text, and arrays

**21 hours.** This file follows Week 2 of the study plan. Calendar dates are only in the [15-week plan](OCP-Java-SE-21-study-plan.md). The gate is two parts: methods, text, and arrays questions at **70%** (21 of the 30 questions in this file), and **one hour with autocomplete off**.

Weekdays are Monday, Wednesday, and Friday, 3 hours each: 20 minutes on yesterday’s misses, 2 hours typing every listing, 40 minutes of questions and the notebook. Saturday and Sunday are 6 hours each. Monday’s first 20 minutes are the Week 1 misses.

The exam topic this week is text, `String`, `StringBuilder`, and arrays. Methods are the tool you use to write that code.

| Day | What the plan says | Where it is in this file |
|---|---|---|
| Mon | Methods, return, overloading | Chapter 1 through overloading, the `Adder` lab, questions Q1–Q4 |
| Wed | Varargs and pass-by-value | The varargs overload, `PassByValue`, questions Q5–Q8 |
| Fri | `String`, `StringBuilder`, and a text block | Chapter 2, `TextCalls`, the copy loop, questions Q1–Q8 |
| Sat | Arrays, sort, `binarySearch` | Chapter 3, `ArrayLab`, questions Q1–Q8 |
| Sun | Autocomplete off for one hour, then the questions | The hour, the mixed set, then score all 30 |

Same checklist as the study plan:

- [ ] Overload one method three ways, including varargs. Varargs is the last parameter, and there is only one.
- [ ] Prove pass-by-value: reassigning the parameter does not change the caller; mutating the object does.
- [ ] One call each for `substring`, `indexOf`, `equals`, `strip`, `isBlank`, `indent`, `formatted`, and a text block. The end index of `substring` is exclusive.
- [ ] Show, in a loop, why `String` concatenation copies and `StringBuilder` does not. One sentence in the notebook.
- [ ] Reverse an array in place, sort it, and `binarySearch` it. A negative result encodes the insertion point. Make one jagged two-dimensional array.
- [ ] Autocomplete off for one hour. Methods, text, and arrays questions at 70%.

Classes, encapsulation, and constructors are Week 3. These listings use `static` methods so `main` can call them.

The questions are practice in the exam’s style. They are not copied from the real exam or from a book. Try each one before its answer key.

---

# Chapter 1 — Methods

> **必睇**　參考書第 5 章 Methods：pp. 234–242（“Designing Methods”）、pp. 246–248（varargs）、pp. 266–279（“Passing Data among Methods”、“Overloading Methods”、Summary、Exam Essentials）。
>
> **唔使睇**　“Applying Access Modifiers”（pp. 249–256）同 “Accessing Static Data”（pp. 257–265）留第 3 週。“Effectively Final Variables”（p. 244）留第 7 週。Review Questions（p. 280 起）唔使做。

**Monday** is return and overloading. **Wednesday** adds varargs and pass-by-value. The three overloads of `add` are one checklist item, finished on Wednesday.

## What you must know

A method has a name, a parameter list, and a return type. The **signature** is the name plus the parameter types. Parameter names are not part of the signature. The return type is not part of the signature.

```java
static int add(int a, int b) {
    return a + b;
}
```

`void` returns nothing. A bare `return;` is legal in a `void` method. A method whose type is not `void` must return a value on every path that can finish. The compiler checks this.

```java
static int value(boolean flag) {
    if (flag) {
        return 1;
    }
    return 0;          // without this line the method does not compile
}
```

### Monday — overloading

Two methods overload each other when they share a name and their parameter lists differ. A different return type alone does not overload. It does not compile.

When more than one method could accept the call, Java picks in this order:

1. Exact parameter types.
2. Widen a primitive (`int` to `long`) .
3. Box (`int` to `Integer`). After boxing, the value may widen to a supertype (`Integer` to `Object`).
4. Varargs.

Widening beats boxing. Boxing beats varargs. An `int` does not become a `Long`: that would widen and then box, and Java does not do that for a method call. `int` can box to `Integer` and then widen to `Object`.

```java
static void pick(int x) { System.out.println("int"); }
static void pick(long x) { System.out.println("long"); }

pick(1);               // int, exact match
```

If the `int` method is removed, `pick(1)` prints `long`. Widening is used before a method that takes `Integer`.

Type the two-argument overloads on Monday. The varargs overload is Wednesday.

```java
public class Adder {
    static int add(int a, int b) {
        return a + b;
    }

    static double add(double a, double b) {
        return a + b;
    }

    public static void main(String[] args) {
        System.out.println(add(1, 2));
        System.out.println(add(1.5, 2.5));
    }
}
```

`add(1, 2)` prints `3`. `add(1.5, 2.5)` prints `4.0`. Monday’s questions are Q1–Q4.

### Wednesday — varargs

A varargs parameter is zero or more arguments, and inside the method it is an array. It is the last parameter. A method has only one varargs parameter.

```java
static int add(int... nums) {
    int sum = 0;
    for (int n : nums) {
        sum += n;
    }
    return sum;
}
```

Add that method to `Adder`. Then call it.

```java
System.out.println(add(1, 2, 3));   // 6
System.out.println(add());          // 0, the array is empty, not null
```

`add(1, 2)` still uses `add(int, int)`. The exact two-parameter method beats varargs.

These do not compile:

```java
static void bad(int... nums, int extra) {}   // varargs is not last
static void same(int[] nums) {}
static void same(int... nums) {}             // int... and int[] are the same signature
```

A call that matches two methods equally does not compile. `show(1, 2)` is ambiguous for `show(int, long)` and `show(long, int)`, because each needs one widening. `pick(null)` is ambiguous for `pick(Integer)` and `pick(String)`.

### Wednesday — pass-by-value

Java copies the value of each argument into the parameter. For a primitive, the copy is the number. For an object, the copy is the reference. Reassigning the parameter changes the copy. Mutating the object changes the object the caller still points at.

Type this and run it.

```java
public class PassByValue {
    static void reassign(String s) {
        s = "changed";
    }

    static void mutate(StringBuilder sb) {
        sb.append("!");
    }

    public static void main(String[] args) {
        String name = "Ada";
        reassign(name);
        System.out.println(name);

        StringBuilder word = new StringBuilder("cat");
        mutate(word);
        System.out.println(word);
    }
}
```

The run prints:

```text
Ada
cat!
```

`name` is still `"Ada"` because `s = "changed"` points the copy at a different object. `word` prints `cat!` because `append` changes the same `StringBuilder` the caller holds.

Wednesday’s questions are Q5–Q8.

## Chapter 1 questions

Q1–Q4 are Monday. Q5–Q8 are Wednesday.

**Q1.** What is the result?

```java
public class Q1 {
    static int pick(int x) { return x; }
    static long pick(int x) { return x; }
    public static void main(String[] args) {
        System.out.println(pick(1));
    }
}
```

A. `1`
B. `1` printed as a `long`
C. The code does not compile
D. An exception is thrown at runtime

**Q2.** What is the output?

```java
public class Q2 {
    static void pick(int x) { System.out.print("int"); }
    static void pick(long x) { System.out.print("long"); }
    static void pick(Integer x) { System.out.print("Integer"); }
    public static void main(String[] args) {
        pick(1);
    }
}
```

A. `int`
B. `long`
C. `Integer`
D. The code does not compile

**Q3.** What is the output?

```java
public class Q3 {
    static void pick(long x) { System.out.print("long"); }
    static void pick(Integer x) { System.out.print("Integer"); }
    public static void main(String[] args) {
        pick(1);
    }
}
```

A. `long`
B. `Integer`
C. `longInteger`
D. The code does not compile

**Q4.** What is the result of compiling this method?

```java
static int value(boolean flag) {
    if (flag) {
        return 1;
    }
}
```

A. It compiles and returns `0` when `flag` is false
B. It compiles and returns `1` when `flag` is false
C. The code does not compile
D. A `NullPointerException` is thrown when `flag` is false

**Q5.** Which method compiles?

A. `static void m(int... a, int b) {}`
B. `static void m(int b, int... a) {}`
C. Both
D. Neither

**Q6.** What is the output?

```java
public class Q6 {
    static void m(int... a) { System.out.print(a.length); }
    public static void main(String[] args) {
        m();
        m(1, 2);
    }
}
```

A. `02`
B. `12`
C. `null2`
D. The code does not compile

**Q7.** What is the output?

```java
public class Q7 {
    static void reassign(int[] a) { a = new int[] {9}; }
    static void mutate(int[] a) { a[0] = 9; }
    public static void main(String[] args) {
        int[] nums = {1, 2};
        reassign(nums);
        System.out.print(nums[0]);
        mutate(nums);
        System.out.print(nums[0]);
    }
}
```

A. `11`
B. `19`
C. `99`
D. The code does not compile

**Q8.** What is the result?

```java
public class Q8 {
    static void pick(Integer a) { System.out.print("I"); }
    static void pick(String a) { System.out.print("S"); }
    public static void main(String[] args) {
        pick(null);
    }
}
```

A. `I`
B. `S`
C. The code does not compile
D. A `NullPointerException` is thrown

### Chapter 1 answers

**Q1 — C.** Both methods have the signature `pick(int)`. The return type is not part of the signature, so this is a duplicate method and does not compile.

**Q2 — A.** `1` is an `int`. The exact `int` method is chosen. The `long` and `Integer` methods are legal overloads, and they are not used.

**Q3 — A.** There is no `int` method. Widening `int` to `long` is tried before boxing `int` to `Integer`, so the call prints `long`.

**Q4 — C.** When `flag` is false the method ends without returning an `int`. Every path must return a value.

**Q5 — B.** The varargs parameter is last, and it is the only one. Option A puts a parameter after the varargs, so it does not compile.

**Q6 — A.** `m()` passes an empty array, so the length is `0`. `m(1, 2)` passes an array of length `2`. The print is `02`. The array is not `null`.

**Q7 — B.** `reassign` points its own copy at a new array. `nums` is still `{1, 2}`, so the first print is `1`. `mutate` writes into the same array, so the second print is `9`.

**Q8 — C.** `null` matches `Integer` and `String` equally. The call is ambiguous and does not compile. No method runs, so nothing throws.

---

# Chapter 2 — Text

> **必睇**　第 1 章 “Defining Text Blocks”（pp. 31–33，第 1 週跳過嘅）。第 4 章 pp. 166–188：“Creating and Manipulating Strings”、“Using the StringBuilder Class”、“Understanding Equality”。
>
> **唔使睇**　“Working with Dates and Times”（p. 205 起）係第 5 週。Review Questions 唔使做。

**Friday** is this chapter, `TextCalls`, the concatenation loop, and questions Q1–Q8.

## What you must know

A `String` cannot be changed. Every method that looks like it edits a string returns a new `String`. The variable still points at the old one until you assign the result.

```java
String s = "animal";
s.substring(0, 3);
System.out.println(s);          // animal
s = s.substring(0, 3);
System.out.println(s);          // ani
```

String literals with the same characters share one pooled object. `new String("hi")` is a different object with the same characters. `==` compares references. `equals` compares characters.

```java
String a = "hi";
String b = "hi";
String c = new String("hi");
System.out.println(a == b);         // true
System.out.println(a == c);         // false
System.out.println(a.equals(c));    // true
```

### The methods on the checklist

| Call | Result to remember |
|---|---|
| `"animal".substring(1, 4)` | `"nim"`. The end index is exclusive. `substring(3, 3)` is `""`. A begin past the end, or a begin after the end, throws `StringIndexOutOfBoundsException` |
| `"animal".substring(3)` | `"mal"`. From that index to the end. `substring(6)` on a length-6 string is `""` |
| `"animals".indexOf('a')` | `0`. The first match. A missing character or string returns `-1` |
| `"animals".indexOf("al")` | `4` |
| `"hi".equals("hi")` | `true`. `"hi".equals(null)` is `false`. Calling `equals` on a `null` reference throws `NullPointerException` |
| `"  hi  ".strip()` | `"hi"`. Also removes Unicode whitespace. `trim` only removes characters at or below U+0020 |
| `" ".isBlank()` | `true`. Blank means empty or only whitespace |
| `" ".isEmpty()` | `false`. Empty means length 0 |
| `"a".indent(1)` | `" a\n"`. Each line is indented, line endings become `\n`, and the result ends with `\n` |
| `"Hi %s".formatted("Java")` | `"Hi Java"`. Same idea as `String.format` |

`charAt` is the other index method. `"cat".charAt(0)` is `'c'`. An index that does not exist throws `StringIndexOutOfBoundsException`. `length()` is a method on a string. On an array, `length` is a field. The exam uses that difference.

### Friday lab — one call each

Type this class. Predict each line, then run it.

```java
public class TextCalls {
    public static void main(String[] args) {
        String word = "animal";
        System.out.println(word.substring(1, 4));
        System.out.println(word.indexOf('a', 1));
        System.out.println(word.equals("animal"));
        System.out.println("  hi  ".strip());
        System.out.println(" ".isBlank());
        System.out.println("a".indent(1).equals(" a\n"));
        System.out.println("Hi %s".formatted("Java"));

        String block = """
        cat
        """;
        System.out.println(block.equals("cat\n"));
    }
}
```

In that text block, `cat` and the closing `"""` start in the same column, so the spaces in the source are incidental and are removed. A text block is a `String`. The line breaks in the source become `\n`, including the break before the closing quotes. `"cat\n"` is the value.

A text block cannot sit on one line. `"""cat"""` does not compile. The opening `"""` is the end of its line.

The position of the closing `"""` sets how much shared indent is removed. Content that sticks out farther to the right keeps the extra spaces.

### `StringBuilder`

`StringBuilder` is a changeable buffer. `append`, `insert`, `delete`, `deleteCharAt`, `reverse`, and `replace` change that buffer and return the same builder, so calls can chain. `substring` on a builder returns a `String`, so the chain cannot continue with `append`.

`StringBuilder` does not override `equals`. `sb.equals("hi")` is false even when the characters are `hi`. Compare `sb.toString().equals("hi")`.

```java
var sb = new StringBuilder("animals");
String start = sb.substring(0, 3);   // "ani", and sb is still "animals"
sb.append("!");                       // legal, sb is a builder
// sb.substring(0, 3).append("x");    // does not compile
```

### Friday — the copy loop

Type this. Both variables end as `"012"`. Then write one sentence in the notebook: each `+=` builds a new `String` and copies the characters so far; `StringBuilder` appends into one buffer.

```java
public class Copies {
    public static void main(String[] args) {
        String s = "";
        for (int i = 0; i < 3; i++) {
            s += i;
        }
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < 3; i++) {
            sb.append(i);
        }
        System.out.println(s.equals(sb.toString()));
    }
}
```

The print is `true`. The sentence is about the copies, not about the final characters.

## Chapter 2 questions

**Q1.** What is the output?

```java
public class Q1 {
    public static void main(String[] args) {
        System.out.println("animal".substring(1, 4));
    }
}
```

A. `ani`
B. `nim`
C. `nima`
D. An exception is thrown at runtime

**Q2.** What is the output?

```java
public class Q2 {
    public static void main(String[] args) {
        String a = "hi";
        String b = "hi";
        String c = new String("hi");
        System.out.print(a == b);
        System.out.print(a == c);
        System.out.print(a.equals(c));
    }
}
```

A. `truetruetrue`
B. `truefalsetrue`
C. `falsefalsetrue`
D. `truefalsefalse`

**Q3.** What is the output?

```java
public class Q3 {
    public static void main(String[] args) {
        System.out.print(" ".isEmpty());
        System.out.print(" ".isBlank());
        System.out.print("".isBlank());
    }
}
```

A. `falsetruetrue`
B. `falsefalsefalse`
C. `truetruetrue`
D. `falsetruefalse`

**Q4.** What is the output?

```java
public class Q4 {
    public static void main(String[] args) {
        var sb = new StringBuilder("hi");
        System.out.print(sb.equals("hi"));
        System.out.print(sb.toString().equals("hi"));
    }
}
```

A. `truetrue`
B. `falsetrue`
C. `falsefalse`
D. The code does not compile

**Q5.** What is the result?

```java
public class Q5 {
    public static void main(String[] args) {
        var sb = new StringBuilder("animals");
        sb.substring(0, 3).append("x");
        System.out.println(sb);
    }
}
```

A. `animals`
B. `anixals`
C. `xanimals`
D. The code does not compile

**Q6.** What is the output?

```java
public class Q6 {
    public static void main(String[] args) {
        String s = "animal";
        s.substring(0, 3);
        System.out.println(s);
    }
}
```

A. `ani`
B. `animal`
C. `mal`
D. The code does not compile

**Q7.** What is the output?

```java
public class Q7 {
    public static void main(String[] args) {
        System.out.print("a".indent(1).equals(" a\n"));
    }
}
```

A. `true`
B. `false`
C. ` a`
D. The code does not compile

**Q8.** What is the output?

```java
public class Q8 {
    public static void main(String[] args) {
        System.out.print("animals".indexOf('z'));
        System.out.print(" ");
        System.out.print("animals".indexOf("al"));
    }
}
```

A. `-1 4`
B. `0 4`
C. `-1 -1`
D. An exception is thrown at runtime

### Chapter 2 answers

**Q1 — B.** Indexes are 0 `a`, 1 `n`, 2 `i`, 3 `m`, 4 `a`, 5 `l`. `substring(1, 4)` takes indexes 1, 2, and 3: `nim`. The end index is not included.

**Q2 — B.** `a` and `b` are the same pooled literal, so `==` is true. `new String` is a different object, so `==` is false. `equals` compares the characters, so the last value is true.

**Q3 — A.** A single space has length 1, so `isEmpty` is false. It is only whitespace, so `isBlank` is true. The empty string is also blank.

**Q4 — B.** `StringBuilder` uses reference equality from `Object`. The characters match only after `toString()`.

**Q5 — D.** `substring` on a `StringBuilder` returns a `String`. `String` has no `append` method, so the chain does not compile. `sb` itself is never printed.

**Q6 — B.** `substring` returns a new string and does not assign it. `s` still refers to `"animal"`.

**Q7 — A.** `indent(1)` puts one space at the start of the line and ends the result with `\n`. The strings are equal, so the print is `true`.

**Q8 — A.** `z` is not in the string, so `indexOf` returns `-1`. `"al"` starts at index 4 (`a` at 4, `l` at 5).

---

# Chapter 3 — Arrays

> **必睇**　參考書第 4 章 “Understanding Arrays”，pp. 189–201。
>
> **唔使睇**　Math 已在第 1 週。日期（p. 205 起）留第 5 週。Review Questions 唔使做。

**Saturday** is this chapter, `ArrayLab`, and questions Q1–Q8.

## What you must know

An array is an object. The size is fixed when it is created. `length` is a field.

```java
int[] nums = new int[3];     // 0, 0, 0
String[] names = new String[2]; // null, null
System.out.println(nums.length);
```

`nums.length()` does not compile. A string uses `length()` with parentheses. An index from `0` through `length - 1` is legal. Any other index throws `ArrayIndexOutOfBoundsException` at runtime.

These create an array with values:

```java
int[] a = {1, 2, 3};
int[] b = new int[] {1, 2, 3};
```

The brace form without `new` is allowed only in the declaration. This does not compile:

```java
int[] c;
c = {1, 2};
```

This does:

```java
c = new int[] {1, 2};
```

A field of array type defaults to `null`. Reading `null.length` throws `NullPointerException`.

### Sort, search, and a negative result

`Arrays.sort` orders the array in place. `Arrays.binarySearch` is defined for a sorted array. On an unsorted array the result is undefined. The exam’s answer for that case is that the result is undefined, not a particular index.

If the value is present, `binarySearch` returns its index. If it is absent, the result is negative: `-(insertion point) - 1`. The insertion point is the index where the value would go to keep the array sorted.

```java
int[] sorted = {1, 3, 5, 7};
Arrays.binarySearch(sorted, 5);    // 2
Arrays.binarySearch(sorted, 4);    // -3, insertion point 2
Arrays.binarySearch(sorted, 0);    // -1, insertion point 0
```

For `-3`, the insertion point is `-(-3) - 1`, which is `2`.

`Arrays.equals` compares elements one level deep. `==` compares the two array references. `Arrays.mismatch` returns the first index that differs, or `-1` when the arrays match. `Arrays.compare` returns a negative number, zero, or a positive number, in the same style as `compareTo`.

An array’s component type is checked at runtime. This compiles and throws `ArrayStoreException`:

```java
Object[] objects = new String[1];
objects[0] = 1;
```

### Saturday lab — reverse, sort, search, jagged

Type this. Predict the prints, then run it.

```java
import java.util.Arrays;

public class ArrayLab {
    public static void main(String[] args) {
        int[] nums = {3, 1, 4, 2};
        for (int i = 0; i < nums.length / 2; i++) {
            int tmp = nums[i];
            nums[i] = nums[nums.length - 1 - i];
            nums[nums.length - 1 - i] = tmp;
        }
        System.out.println(Arrays.toString(nums));

        Arrays.sort(nums);
        System.out.println(Arrays.toString(nums));
        System.out.println(Arrays.binarySearch(nums, 3));
        System.out.println(Arrays.binarySearch(nums, 0));

        int[][] jagged = {{1, 2}, {3}};
        System.out.println(jagged.length);
        System.out.println(jagged[0].length);
        System.out.println(jagged[1].length);
    }
}
```

The run prints:

```text
[2, 4, 1, 3]
[1, 2, 3, 4]
2
-1
2
2
1
```

The reverse swaps the ends and moves inward. After the sort, `3` is at index `2`. `0` would be inserted at index `0`, so the search returns `-1`.

`jagged` is an array of two arrays. The first inner array has length 2. The second has length 1. This also compiles, and the inner arrays are different lengths:

```java
int[][] rows = new int[2][];
rows[0] = new int[1];
rows[1] = new int[3];
```

`rows[0]` is `null` until you assign an array. `rows[0][0]` before that assignment throws `NullPointerException`.

## Chapter 3 questions

**Q1.** What is the result?

```java
public class Q1 {
    public static void main(String[] args) {
        int[] nums = new int[3];
        System.out.println(nums.length());
    }
}
```

A. `3`
B. `0`
C. The code does not compile
D. An `ArrayIndexOutOfBoundsException` is thrown

**Q2.** What is the result?

```java
public class Q2 {
    public static void main(String[] args) {
        int[] nums;
        nums = {1, 2};
        System.out.println(nums[0]);
    }
}
```

A. `1`
B. `0`
C. The code does not compile
D. A `NullPointerException` is thrown

**Q3.** What is the output?

```java
import java.util.Arrays;

public class Q3 {
    public static void main(String[] args) {
        int[] nums = {1, 3, 5, 7};
        System.out.println(Arrays.binarySearch(nums, 4));
    }
}
```

A. `2`
B. `-2`
C. `-3`
D. An exception is thrown at runtime

**Q4.** What is the result?

```java
import java.util.Arrays;

public class Q4 {
    public static void main(String[] args) {
        int[] nums = {5, 1, 3};
        System.out.println(Arrays.binarySearch(nums, 1));
    }
}
```

A. `1`
B. `0`
C. `-1`
D. The result is undefined

**Q5.** What is the result?

```java
public class Q5 {
    public static void main(String[] args) {
        int[] nums = new int[2];
        System.out.println(nums[0]);
        System.out.println(nums[2]);
    }
}
```

A. `0` then `0`
B. `0` is printed, then an `ArrayIndexOutOfBoundsException` is thrown
C. The code does not compile
D. A `NullPointerException` is thrown

**Q6.** What is the result?

```java
public class Q6 {
    public static void main(String[] args) {
        int[][] rows = new int[2][];
        System.out.println(rows[0] == null);
        System.out.println(rows[1].length);
    }
}
```

A. `true` then `0`
B. `false` then `0`
C. `true` is printed, then a `NullPointerException` is thrown
D. The code does not compile

**Q7.** What is the output?

```java
import java.util.Arrays;

public class Q7 {
    public static void main(String[] args) {
        int[] nums = {3, 1, 2};
        Arrays.sort(nums);
        System.out.println(Arrays.binarySearch(nums, 2));
    }
}
```

A. `0`
B. `1`
C. `2`
D. `-1`

**Q8.** What is the result?

```java
public class Q8 {
    public static void main(String[] args) {
        Object[] objects = new String[1];
        objects[0] = 1;
        System.out.println(objects[0]);
    }
}
```

A. `1`
B. `null`
C. The code does not compile
D. An `ArrayStoreException` is thrown

### Chapter 3 answers

**Q1 — C.** An array stores its size in the field `length`. The parentheses make the compiler look for a method, and there is not one. A `String` would use `length()`.

**Q2 — C.** `{1, 2}` without `new` is allowed in a declaration. A later assignment needs `new int[] {1, 2}`.

**Q3 — C.** The array is sorted. `4` would be inserted at index `2`, before `5`. The result is `-(2) - 1`, which is `-3`.

**Q4 — D.** `{5, 1, 3}` is not sorted. `binarySearch` does not promise an index for an unsorted array. The result is undefined.

**Q5 — B.** A new `int` array is filled with `0`, so the first print is `0`. Index `2` is past the end of a length-2 array, so the second line throws `ArrayIndexOutOfBoundsException`.

**Q6 — C.** `new int[2][]` creates two slots and leaves them `null`. The first print is `true`. Calling `.length` on `rows[1]` throws `NullPointerException`.

**Q7 — B.** After sorting, the array is `{1, 2, 3}`. `2` is at index `1`.

**Q8 — D.** The variable’s type is `Object[]`, so the assignment compiles. The array’s runtime type is `String[]`. Storing an `Integer` throws `ArrayStoreException`.

---

# Sunday — autocomplete off, then the questions

> **唔使睇**　呢一小時關掉自動完成，然後做筆記嘅題。

Turn suggestions off for one hour: Settings, Editor, General, Code Completion, and clear “Show suggestions as you type”. Turn it back on when the hour ends.

In that hour, write one program from a blank file. Use no checklist code copied from above. The program needs all three of these:

- an overloaded method, and one of the overloads is varargs
- a `String` or `StringBuilder` call that you predict before you run it
- a jagged `int` array, plus `Arrays.sort` and `Arrays.binarySearch` on a one-dimensional array

About 40 lines is enough. If it compiles and the search result matches the insertion-point rule, the hour counts.

Then do the mixed set. After that, score Chapter 1 (8), Chapter 2 (8), Chapter 3 (8), and the mixed set (6). **21 or more** of the 30 questions is the gate. Every miss becomes one rule and a five-line program before Monday of Week 3.

## Mixed set

**M1.** What is the output?

```java
public class M1 {
    public static void main(String[] args) {
        System.out.print("animal".charAt(0));
        System.out.print("animal".substring(6));
    }
}
```

A. `a`
B. `al`
C. `a` followed by nothing else
D. An exception is thrown at runtime

**M2.** What is the output?

```java
public class M2 {
    static void grow(StringBuilder sb) { sb.append("s"); }
    public static void main(String[] args) {
        StringBuilder sb = new StringBuilder("cat");
        grow(sb);
        System.out.println(sb);
    }
}
```

A. `cat`
B. `cats`
C. `s`
D. The code does not compile

**M3.** What is the output?

```java
import java.util.Arrays;

public class M3 {
    public static void main(String[] args) {
        int[] a = {1, 2, 3};
        int[] b = {1, 2, 4};
        System.out.print(Arrays.mismatch(a, b));
        System.out.print(Arrays.mismatch(a, a));
    }
}
```

A. `2-1`
B. `1-1`
C. `20`
D. The code does not compile

**M4.** Which of these compile?

```java
String a = """cat""";
String b = """
        cat
        """;
```

A. `a` only
B. `b` only
C. Both
D. Neither

**M5.** What is the output?

```java
public class M5 {
    public static void main(String[] args) {
        var sb = new StringBuilder("abc");
        sb.append("de").delete(1, 3).reverse();
        System.out.println(sb);
    }
}
```

A. `abcde`
B. `eda`
C. `ade`
D. The code does not compile

**M6.** What is the output?

```java
public class M6 {
    static void add(int a, int b) { System.out.print("two"); }
    static void add(int... nums) { System.out.print(nums.length); }
    public static void main(String[] args) {
        add(1, 2);
        add(1, 2, 3);
    }
}
```

A. `two3`
B. `23`
C. `two2`
D. The code does not compile

### Mixed answers

**M1 — C.** `charAt(0)` prints `a`. `"animal"` has length 6, so `substring(6)` is the empty string from the end index. Nothing more is printed, and no exception is thrown. `substring(7)` would throw.

**M2 — B.** `grow` receives a copy of the reference and calls `append` on that same builder. The caller’s variable sees `cats`.

**M3 — A.** The arrays first differ at index `2`. `mismatch` of an array with itself is `-1`, because there is no differing index. The print is `2-1`.

**M4 — B.** A text block’s opening `"""` ends its line. `"""cat"""` is one line and does not compile. The second value is a text block.

**M5 — B.** `"abc"` plus `"de"` is `"abcde"`. `delete(1, 3)` removes indexes 1 and 2 (`b` and `c`), leaving `"ade"`. `reverse` leaves `"eda"`.

**M6 — A.** `add(1, 2)` matches `add(int, int)` exactly, so varargs is not used. `add(1, 2, 3)` matches only the varargs method, and that array’s length is `3`.

---

# Rules to copy onto one card

- The signature is the name and the parameter types. A different return type does not overload.
- Call resolution: exact, then primitive widening, then boxing, then varargs. An `int` does not match a `Long` parameter.
- Varargs is the last parameter, and there is only one. Inside the method it is an array. A call with no extra arguments passes an empty array.
- Reassigning a parameter does not change the caller. Mutating the object the reference points at does.
- `substring`’s end index is exclusive. `indexOf` returns `-1` when there is no match. `String` methods do not change the original string.
- `isBlank` is true for empty or whitespace-only text. `isEmpty` is true only for length 0.
- `StringBuilder.equals` does not compare characters. `substring` on a builder returns a `String`.
- `"a".indent(1)` is `" a\n"`. A text block’s closing `"""` decides the indent that is removed.
- Each `+=` in a loop builds a new `String`. `StringBuilder.append` updates one buffer.
- `length` on an array is a field. `binarySearch` needs a sorted array. A missing value returns `-(insertion point) - 1`.
