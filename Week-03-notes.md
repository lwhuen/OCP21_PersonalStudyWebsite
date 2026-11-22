# Week 3 notes — classes and memory

**7–13 Dec 2026. 21 hours.** This file follows Week 3 of the study plan. The gate is two parts: you can hand-trace superclass-then-subclass initializer order, and the class-design questions in this file at **70%** (23 of the 32 questions).

Weekdays are Monday, Wednesday, and Friday, 3 hours each: 20 minutes on yesterday’s misses, 2 hours typing every listing, 40 minutes of questions and the notebook. Saturday and Sunday are 6 hours each. Monday’s first 20 minutes are the Week 2 misses.

The exam topic this week is classes, encapsulation, and immutability, plus the garbage-collection diagrams on the checklist. Wednesday uses `extends` only so you can watch a superclass finish before the subclass. Overriding, interfaces, records, and sealed types are Week 4. Leave them until 14 Dec.

| Day | What the plan says | Where it is in this file |
|---|---|---|
| Mon | Classes, fields, constructors, `this` | Chapter 1, `Person`, questions Q1–Q6 |
| Wed | Static members and initializer order | `Counter`, `Once`, `OrderLab`, questions Q1–Q8 |
| Fri | Encapsulation | `OpenBox`, `BankAccount`, questions Q1–Q6 |
| Sat | An immutable class and five garbage-collection diagrams | `Money`, `CopyLab`, the five diagrams, questions Q1–Q6 |
| Sun | Chapter questions | Hand-trace M1, the mixed set, then score all 32 |

Same checklist as the study plan:

- [ ] A class with fields, a constructor, and `this`. No public fields.
- [ ] Hand-write static-then-instance initializer order for a superclass and a subclass. Run code that prints the order and compare.
- [ ] An encapsulated `BankAccount`: private fields, constructor, methods.
- [ ] An immutable `Money` class: private final fields, no setters, class is final.
- [ ] Five memory diagrams. A box is an object, an arrow is a reference. Mark what is eligible for collection.
- [ ] Class-design questions at 70%, including one you can explain about garbage collection.

Predict each listing before you run it. Each miss goes in the notebook as one rule and a five-line program.

The questions are practice in the exam’s style. They are not copied from the real exam or from a book. Try each one before its answer key.

---

# Chapter 1 — Classes, fields, constructors, `this`

> **必睇**　參考書第 6 章 Class Design，pp. 297–311：“Creating Classes” 同 “Declaring Constructors”（`this`、`super()`）。
>
> **唔使睇**　“Inheriting Members” 同 “Creating Abstract Classes” 留第 4 週。Review Questions 唔使做。

**Monday** is this chapter, the `Person` lab, and questions Q1–Q6.

## What you must know

A class groups fields and methods. `new Person("Ada", 36)` allocates an object and runs a constructor. The fields receive their defaults first: `0` for a number, `false` for a boolean, `'\u0000'` for a char, and `null` for a reference. Those are the same defaults as Week 1. A local variable still has no default.

A file has at most one `public` top-level class, and the file name matches that class. A top-level class is `public` or package-private (no modifier). `private` and `protected` are not modifiers for a top-level class.

A constructor’s name is the class name, and it has no return type.

```java
public Person(String name) {
    this.name = name;
}
```

`void Person(String name)` is an ordinary method that happens to share the class name. `new` does not call it. If you write no constructor, the compiler adds a no-arg constructor with the same access as the class. The moment you write any constructor, that default constructor is gone. `new Person()` then fails unless one of your constructors takes no arguments.

A parameter with the same name as a field hides the field. `this.field` is the field. `n = n` assigns the parameter to itself and leaves the field at its default.

`this(...)` calls another constructor of the same class. It is the first statement of the constructor. The arguments cannot be instance fields or instance methods, because this object is not ready yet. A cycle, where two constructors call each other, does not compile.

Instance initializers run in the constructor that actually builds the object. A constructor that starts with `this(...)` waits, and the body after `this(...)` runs when the other constructor returns. Type this.

```java
public class Chain {
    { System.out.print("I"); }
    Chain() { this(1); System.out.print("A"); }
    Chain(int n) { System.out.print("B"); }
    public static void main(String[] args) {
        new Chain();
    }
}
```

`new Chain()` prints `IBA`. The `{ }` block and the `Chain(int)` body run inside the delegated constructor. `A` prints after that constructor returns.

## Monday lab — `Person`

Type this. The fields are private. The constructor stores both parameters with `this`.

```java
public class Person {
    private String name;
    private int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public String describe() {
        return name + " " + age;
    }

    public static void main(String[] args) {
        Person p = new Person("Ada", 36);
        System.out.println(p.describe());
    }
}
```

The run prints:

```text
Ada 36
```

Monday’s questions are Q1–Q6.

## Chapter 1 questions

**Q1.** What is the output?

```java
public class Q1 {
    boolean ok = true;
    void Q1() { ok = false; }
    public static void main(String[] args) {
        System.out.println(new Q1().ok);
    }
}
```

A. `true`
B. `false`
C. The code does not compile
D. An exception is thrown at runtime

**Q2.** What is the output?

```java
public class Q2 {
    int n = 5;
    void set(int n) { n = 10; }
    public static void main(String[] args) {
        Q2 q = new Q2();
        q.set(10);
        System.out.println(q.n);
    }
}
```

A. `5`
B. `10`
C. `0`
D. The code does not compile

**Q3.** What is the result?

```java
public class Q3 {
    int n;
    Q3() {
        n = 1;
        this(2);
    }
    Q3(int n) { this.n = n; }
    public static void main(String[] args) {
        System.out.println(new Q3().n);
    }
}
```

A. `1`
B. `2`
C. The code does not compile
D. An exception is thrown at runtime

**Q4.** What is the result?

```java
public class Q4 {
    Q4(int n) {}
    public static void main(String[] args) {
        new Q4();
    }
}
```

A. It runs and prints nothing
B. `0`
C. The code does not compile
D. An exception is thrown at runtime

**Q5.** What is the result?

```java
public class Q5 {
    Q5() { this(1); }
    Q5(int n) { this(); }
    public static void main(String[] args) {
        new Q5();
    }
}
```

A. It runs and prints nothing
B. A `StackOverflowError` is thrown
C. The code does not compile
D. A `NullPointerException` is thrown

**Q6.** What is the result?

```java
public class Q6 {
    int n = 1;
    Q6() { this(n); }
    Q6(int n) {}
    public static void main(String[] args) {
        new Q6();
    }
}
```

A. It runs and prints nothing
B. `1`
C. The code does not compile
D. An exception is thrown at runtime

### Chapter 1 answers

**Q1 — A.** `void Q1()` has a return type, so it is a method. `new` uses the no-arg constructor the compiler added. That constructor leaves `ok` as `true`.

**Q2 — A.** The parameter `n` hides the field. `n = 10` changes the parameter. The field stays `5`. `this.n = n` would store `10`.

**Q3 — C.** `this(...)` is the first statement of a constructor. Here `n = 1` comes first, so the class does not compile.

**Q4 — C.** `Q4(int)` is a constructor, so the compiler does not add a no-arg constructor. `new Q4()` has nothing to call.

**Q5 — C.** The two constructors call each other. The compiler rejects that cycle. It does not become a `StackOverflowError` at runtime.

**Q6 — C.** `this(n)` reads the instance field `n` before the object is built. That reference is illegal. A constant such as `this(1)` would compile.

---

# Chapter 2 — Static members and initializer order

> **必睇**　第 5 章 “Accessing Static Data”，pp. 257–265。第 6 章 “Initializing Objects”，pp. 312–319。
>
> **唔使睇**　p. 320 起嘅 overriding 留第 4 週。

**Wednesday** is this chapter, three listings, and questions Q1–Q8. The hand-written order is a gate item. Write it on paper before you run `OrderLab`.

## What you must know

A `static` member belongs to the class. There is one copy, shared by every object. An instance field belongs to one object.

A `static` method can use `static` members. It cannot use `this` or an instance member, because it has no object. An instance method can use `static` members.

A subclass `extends` one superclass. Constructors are not inherited. The child constructor calls a parent constructor first. If you write neither `this(...)` nor `super(...)`, the compiler inserts `super()`. That inserted call needs a no-arg constructor on the superclass. If the superclass only has `Parent(int n)`, the child must start with `super(n)`. Overriding is Week 4.

Initialization of one class, the first time it is used:

1. `static` fields and `static` blocks, top to bottom, once.
2. For each `new`: instance fields and instance blocks, top to bottom, then the constructor body.

A constructor that starts with `this(...)` does not repeat step 2. Step 2 runs in the constructor that calls the superclass. You already saw that as `IBA` in Chapter 1.

The first time a subclass is used, the superclass goes first:

1. Superclass `static` fields and blocks.
2. Subclass `static` fields and blocks.
3. Superclass instance fields and blocks.
4. Superclass constructor body.
5. Subclass instance fields and blocks.
6. Subclass constructor body.

The second `new` of that subclass skips steps 1 and 2. Both classes are already loaded. If `main` is inside the class you are loading, the `static` steps run before the first line of `main`.

A blank `final` field is assigned exactly once on every constructor path. The assignment can be the declaration, an instance block, or the constructor body. Two assignments do not compile. Zero assignments do not compile.

An initializer may call a method. It may not use a field that is declared later by its simple name.

```java
int a = b;       // does not compile: illegal forward reference
int b = 7;
```

```java
int a = read();  // compiles
int b = 7;
int read() { return b; }
```

`new` of that second class prints `0` for `a`. The field `b` still holds its default when `read()` runs. `b = 7` has not run yet.

### `Counter`

Type this. Two objects share one `static` field.

```java
public class Counter {
    static int made;
    Counter() { made++; }
    public static void main(String[] args) {
        new Counter();
        new Counter();
        System.out.println(made);
    }
}
```

The run prints:

```text
2
```

### `Once`

Predict the line, then type this. `main` is inside the class, so the `static` work runs before `main` prints the space.

```java
public class Once {
    static int s = mark("S1");
    static { mark("S2"); }
    int i = mark("I1");
    { mark("I2"); }
    Once() { mark("C"); }

    static int mark(String label) {
        System.out.print(label);
        return 0;
    }

    public static void main(String[] args) {
        new Once();
        System.out.print(" ");
        new Once();
        System.out.println();
    }
}
```

The run prints:

```text
S1S2I1I2C I1I2C
```

`S1S2` is stuck to the first object because those two marks happen before `main` starts. The second object prints `I1I2C` only.

### `OrderLab`

On paper, list the six steps from the section above and write the output. Then type this and compare. The file name is `OrderLab.java`.

```java
class Parent {
    static { System.out.print("1"); }
    int p = mark("3");
    { System.out.print("4"); }
    Parent() { System.out.print("5"); }
    static int mark(String s) { System.out.print(s); return 0; }
}

class Child extends Parent {
    static { System.out.print("2"); }
    int c = mark("6");
    { System.out.print("7"); }
    Child() { System.out.print("8"); }
}

public class OrderLab {
    public static void main(String[] args) {
        new Child();
        System.out.print(" ");
        new Child();
        System.out.println();
    }
}
```

The run prints:

```text
12345678 345678
```

| Digit | What ran |
|---|---|
| `1` | `Parent` static block |
| `2` | `Child` static block |
| `3` | `Parent` instance field |
| `4` | `Parent` instance block |
| `5` | `Parent` constructor |
| `6` | `Child` instance field |
| `7` | `Child` instance block |
| `8` | `Child` constructor |

The second object starts at `3`. The static steps have already run.

Wednesday’s questions are Q1–Q8.

## Chapter 2 questions

**Q1.** What is the output?

```java
public class Q1 {
    static { System.out.print("S"); }
    { System.out.print("I"); }
    Q1() { System.out.print("C"); }
    public static void main(String[] args) {
        new Q1();
    }
}
```

A. `SIC`
B. `ISC`
C. `CIS`
D. The code does not compile

**Q2.** What is the output?

```java
public class Q2 {
    static { System.out.print("S"); }
    { System.out.print("I"); }
    Q2() { System.out.print("C"); }
    public static void main(String[] args) {
        new Q2();
        new Q2();
    }
}
```

A. `SICIC`
B. `SICSIC`
C. `ICIC`
D. The code does not compile

**Q3.** What is the output? The file name is `Q3.java`.

```java
class Base {
    static { System.out.print("1"); }
    { System.out.print("3"); }
    Base() { System.out.print("4"); }
}
public class Q3 extends Base {
    static { System.out.print("2"); }
    { System.out.print("5"); }
    Q3() { System.out.print("6"); }
    public static void main(String[] args) {
        new Q3();
    }
}
```

A. `123456`
B. `123456123456`
C. `125634`
D. The code does not compile

**Q4.** What is the result of compiling this class?

```java
public class Q4 {
    int n = 1;
    static void show() {
        System.out.println(n);
    }
}
```

A. It compiles
B. It compiles, and `show()` prints `1`
C. The code does not compile
D. A `NullPointerException` is thrown when the class loads

**Q5.** What is the output?

```java
public class Q5 {
    int a = read();
    int b = 7;
    int read() { return b; }
    public static void main(String[] args) {
        System.out.println(new Q5().a);
    }
}
```

A. `0`
B. `7`
C. The code does not compile
D. An exception is thrown at runtime

**Q6.** What is the result of compiling this class?

```java
public class Q6 {
    final int n;
    Q6() {}
}
```

A. It compiles, and `n` is `0`
B. It compiles, and `n` is `null`
C. The code does not compile
D. An exception is thrown when `new Q6()` runs

**Q7.** What is the result? The file name is `Q7.java`.

```java
class Parent {
    Parent(int n) {}
}
public class Q7 extends Parent {
    Q7() {}
}
```

A. It compiles
B. It compiles, and `new Q7()` prints nothing
C. The code does not compile
D. A `StackOverflowError` is thrown

**Q8.** What is the output?

```java
public class Q8 {
    { System.out.print("X"); }
    Q8() { this(1); System.out.print("Y"); }
    Q8(int n) { System.out.print("Z"); }
    public static void main(String[] args) {
        new Q8();
    }
}
```

A. `XYZ`
B. `XZY`
C. `ZXY`
D. The code does not compile

### Chapter 2 answers

**Q1 — A.** The class loads before `main`, so `S` prints first. `new` then runs the instance block `I` and the constructor `C`.

**Q2 — A.** `S` runs once. Each `new` adds `IC`. The print is `SICIC`.

**Q3 — A.** Parent static `1`, child static `2`, parent instance `3`, parent constructor `4`, child instance `5`, child constructor `6`.

**Q4 — C.** `show` is `static`, so it has no object. The instance field `n` cannot be used there.

**Q5 — A.** `read()` runs while `b` still has the default `0`. The assignment `b = 7` comes later. Writing `int a = b` above the declaration of `b` would not compile.

**Q6 — C.** `n` is a blank `final` and this constructor never assigns it.

**Q7 — C.** `Parent` has no no-arg constructor. `Q7()` does not start with `super(...)`, so the compiler inserts `super()`, and that call matches nothing. Constructors are not inherited.

**Q8 — B.** `Q8()` delegates with `this(1)`. The instance block and `Z` run in `Q8(int)`. Control then returns and prints `Y`. The print is `XZY`.

---

# Chapter 3 — Encapsulation

> **必睇**　第 5 章 “Applying Access Modifiers”，pp. 249–256。
>
> **唔使睇**　第 7 章 “Understanding Encapsulation”（p. 387）係 record，留第 4 週。

**Friday** is this chapter, `OpenBox`, `BankAccount`, and questions Q1–Q6.

## What you must know

Encapsulation means the data is private and every change goes through a method. Another class cannot assign a bad value to the field, because it cannot name the field.

| Modifier | Who can use the member |
|---|---|
| `private` | The declaring class only |
| no modifier | Classes in the same package |
| `protected` | The same package, and subclasses |
| `public` | Every class |

Week 4 practices a subclass that lives in another package. This week, fields of a bank account are `private`.

`private` still allows the class’s own `main` to read the field. The ban applies to other classes. A package-private member, the one with no modifier, is visible to another class in the same file, because that file is the same package.

A getter that returns a `String` is safe. A `String` cannot be changed. A getter that returns a `StringBuilder`, an array, or a list hands the caller the object you stored. The caller can append or replace elements, and your field sees the change. Return a copy when the stored object is mutable.

### `OpenBox`

Type this. The file name is `OpenBox.java`.

```java
class Box {
    int size = 2;
    private int secret = 9;
}

public class OpenBox {
    public static void main(String[] args) {
        Box box = new Box();
        System.out.println(box.size);
        // box.secret = 1;
    }
}
```

The run prints:

```text
2
```

`size` has no modifier, and `OpenBox` is in the same package, so the read is legal. Remove the comment from `box.secret` and the file does not compile. `secret` is `private` to `Box`.

### `BankAccount`

Type this. Both fields are private. `deposit` and `withdraw` change `cents` only when the amount is one the account can accept. A non-positive deposit is ignored. A withdrawal larger than the balance is ignored. Week 5 replaces that quiet ignore with an exception.

```java
public class BankAccount {
    private String owner;
    private int cents;

    public BankAccount(String owner, int cents) {
        this.owner = owner;
        this.cents = cents;
    }

    public String owner() {
        return owner;
    }

    public int cents() {
        return cents;
    }

    public void deposit(int amount) {
        if (amount > 0) {
            cents += amount;
        }
    }

    public void withdraw(int amount) {
        if (amount > 0 && amount <= cents) {
            cents -= amount;
        }
    }

    public static void main(String[] args) {
        BankAccount account = new BankAccount("Ada", 100);
        account.deposit(40);
        account.withdraw(25);
        account.withdraw(1000);
        System.out.println(account.cents());
    }
}
```

Predict the balance, then run. The print is:

```text
115
```

`100 + 40` is `140`, then `25` leaves `115`. The withdrawal of `1000` does not run, because `1000` is greater than `115`.

Friday’s questions are Q1–Q6.

## Chapter 3 questions

**Q1.** Which class is encapsulated?

```java
class A {
    public int cents;
}
class B {
    private int cents;
    public int cents() { return cents; }
}
```

A. `A` only
B. `B` only
C. Both
D. Neither

**Q2.** What is the output?

```java
public class Q2 {
    private int cents;
    public void setCents(int cents) { cents = cents; }
    public int cents() { return cents; }
    public static void main(String[] args) {
        Q2 q = new Q2();
        q.setCents(50);
        System.out.println(q.cents());
    }
}
```

A. `50`
B. `0`
C. The code does not compile
D. An exception is thrown at runtime

**Q3.** What is the result? The file name is `Q3.java`.

```java
class Secret {
    private int n = 1;
    int size = 2;
}
public class Q3 {
    public static void main(String[] args) {
        Secret s = new Secret();
        System.out.println(s.n);
    }
}
```

A. `1`
B. `2`
C. The code does not compile
D. An exception is thrown at runtime

**Q4.** What is the output?

```java
public class Q4 {
    private final StringBuilder name = new StringBuilder("a");
    public StringBuilder name() { return name; }
    public static void main(String[] args) {
        Q4 q = new Q4();
        q.name().append("b");
        System.out.println(q.name());
    }
}
```

A. `a`
B. `ab`
C. The code does not compile
D. An exception is thrown at runtime

**Q5.** What is the output?

```java
public class Q5 {
    private int cents = 100;
    public void deposit(int amount) {
        if (amount > 0) {
            cents += amount;
        }
    }
    public static void main(String[] args) {
        Q5 q = new Q5();
        q.deposit(-40);
        System.out.println(q.cents);
    }
}
```

A. `60`
B. `100`
C. The code does not compile
D. An exception is thrown at runtime

**Q6.** Which assignment compiles, when the assignment is written in a third class?

```java
class Account { public int cents; }
class Safe { private int cents; }
```

A. `new Account().cents = -1` only
B. `new Safe().cents = -1` only
C. Both
D. Neither

### Chapter 3 answers

**Q1 — B.** `A` exposes the field, so any class can set it. `B` keeps `cents` private and offers a method to read it.

**Q2 — B.** `cents = cents` assigns the parameter to itself. The field stays at the default `0`. The method is inside the class, so the `private` field is visible to `cents()`. The bug is the missing `this`.

**Q3 — C.** `Q3` is another class. `n` is `private` to `Secret`. `s.size` would print `2`, because `size` is package-private and the classes share a package. The printed expression is `s.n`.

**Q4 — B.** The field is `private` and `final`, and `name()` returns that same builder. `append("b")` changes the object the field points at. The print is `ab`.

**Q5 — B.** `-40` fails the `amount > 0` test, so `cents` stays `100`. `main` is inside the class, so reading the `private` field is legal.

**Q6 — A.** `Account.cents` is `public`. `Safe.cents` is `private`, so a third class cannot assign it.

---

# Chapter 4 — Immutability and garbage collection

> **必睇**　第 6 章 “Creating Immutable Objects”（在 “Creating Abstract Classes” 之後、Summary 之前，包括 defensive copy）。第 1 章 “Destroying Objects”（在該章 Summary 之前）。
>
> **唔使睇**　“Creating Abstract Classes” 本身留第 4 週，呢個星期跳過。

**Saturday** is this chapter, `Money`, `CopyLab`, five diagrams, and questions Q1–Q6. Drawing the diagrams is a checklist item. Draw each one before you read its mark.

## What you must know

An immutable object does not change after the constructor finishes. The usual shape is:

- the class is `final`, so a subclass cannot add mutable behavior
- every field is `private` and `final`
- there is no setter
- a method that looks like a change returns a new object
- a field that points at a mutable object is a copy, both in the constructor and in the getter

`final` fixes the reference stored in the field. It does not freeze the `StringBuilder`, array, or list that the reference points at. A `String` or an `int` has nothing further to change, so a `final` field of that kind is safe to share.

An object is eligible for collection when no live reference can reach it. Eligible means the collector is allowed to reclaim it. The exam asks about eligibility. It does not ask you to name the moment the collector actually runs.

These references keep an object alive:

- a local variable that still holds it
- a field of a reachable object
- a `static` field

Setting that variable to `null`, pointing it at a different object, or leaving the block where it was declared drops that one reference. The object becomes eligible only when the last reference is gone. Two objects that point at each other, with no reference from outside, are both eligible. That is an island.

`System.gc()` asks for a collection. A reachable object stays. The call returns without a promise that anything was collected.

### `Money`

Type this. The class is `final`. Both fields are `private final`. `plus` returns a new `Money` and leaves `price` alone. This lab uses the currency of the object you called `plus` on.

```java
public final class Money {
    private final int cents;
    private final String currency;

    public Money(int cents, String currency) {
        this.cents = cents;
        this.currency = currency;
    }

    public int cents() {
        return cents;
    }

    public String currency() {
        return currency;
    }

    public Money plus(Money other) {
        return new Money(this.cents + other.cents, this.currency);
    }

    public static void main(String[] args) {
        Money price = new Money(100, "USD");
        Money total = price.plus(new Money(50, "USD"));
        System.out.println(price.cents());
        System.out.println(total.cents());
    }
}
```

The run prints:

```text
100
150
```

### `CopyLab`

Predict the line, then type this. The file name is `CopyLab.java`. `Shared` stores the caller’s builder. `Copied` stores a new builder with the same characters.

```java
final class Shared {
    private final StringBuilder name;
    Shared(StringBuilder name) { this.name = name; }
    public String toString() { return name.toString(); }
}

final class Copied {
    private final StringBuilder name;
    Copied(StringBuilder name) { this.name = new StringBuilder(name); }
    public String toString() { return name.toString(); }
}

public class CopyLab {
    public static void main(String[] args) {
        StringBuilder raw = new StringBuilder("a");
        Shared shared = new Shared(raw);
        raw.append("b");
        System.out.print(shared);
        System.out.print(" ");

        StringBuilder raw2 = new StringBuilder("a");
        Copied copied = new Copied(raw2);
        raw2.append("b");
        System.out.println(copied);
    }
}
```

The run prints:

```text
ab a
```

`Shared` changed because `raw` and the field are the same object. `Copied` still prints `a`.

### Five diagrams

A box is an object. An arrow is a reference. Draw all five on paper and mark which boxes are eligible. Then read the marks.

**Diagram 1.** A local variable.

```java
static void run() {
    Object obj = new Object();
}
```

**Diagram 2.** Two names, then one is cleared.

```java
Object a = new Object();
Object b = a;
a = null;
```

**Diagram 3.** One name is pointed at a new object.

```java
Object a = new Object();
a = new Object();
```

**Diagram 4.** An island.

```java
class Node { Node next; }
Node a = new Node();
Node b = new Node();
a.next = b;
b.next = a;
a = null;
b = null;
```

**Diagram 5.** A `static` field.

```java
class Hold {
    static Object kept;
    static void run() {
        kept = new Object();
        Object local = kept;
        local = null;
    }
}
```

Draw before the marks below.

**Diagram 1 mark.** Inside `run`, `obj` points at the box, so it is not eligible. After `run` returns, that local variable is gone. Nothing else was stored. The box is eligible.

**Diagram 2 mark.** After `a = null`, `b` still points at the box. The box is not eligible.

**Diagram 3 mark.** The first box has no arrow left. It is eligible. `a` points at the second box, so the second box is not eligible.

**Diagram 4 mark.** After `a = null` and `b = null`, the two boxes point at each other and nothing outside points in. Both are eligible.

**Diagram 5 mark.** After `run` returns, `local` is gone and `kept` still points at the box. The box is not eligible. It stays reachable until `kept` is changed.

Saturday’s questions are Q1–Q6.

## Chapter 4 questions

**Q1.** What is the output? The file name is `Q1.java`.

```java
final class Bag {
    private final StringBuilder items;
    Bag(StringBuilder items) { this.items = items; }
    public String toString() { return items.toString(); }
}
public class Q1 {
    public static void main(String[] args) {
        StringBuilder items = new StringBuilder("a");
        Bag bag = new Bag(items);
        items.append("b");
        System.out.println(bag);
    }
}
```

A. `a`
B. `ab`
C. The code does not compile
D. An exception is thrown at runtime

**Q2.** What is the output? The file name is `Q2.java`.

```java
final class Coin {
    private final int cents;
    Coin(int cents) { this.cents = cents; }
    int cents() { return cents; }
    Coin plus(Coin other) { return new Coin(cents + other.cents); }
}
public class Q2 {
    public static void main(String[] args) {
        Coin a = new Coin(100);
        Coin b = a.plus(new Coin(50));
        System.out.println(a.cents());
        System.out.println(b.cents());
    }
}
```

A. `100` then `150`
B. `150` then `150`
C. `100` then `100`
D. The code does not compile

**Q3.** Which class is immutable?

```java
final class A {
    private final int cents;
    A(int cents) { this.cents = cents; }
    A plus(int more) { return new A(cents + more); }
}
final class B {
    private final StringBuilder name;
    B(StringBuilder name) { this.name = name; }
    StringBuilder name() { return name; }
}
```

A. `A` only
B. `B` only
C. Both
D. Neither

**Q4.** After `a = null`, and before `main` returns, is the object eligible?

```java
public class Q4 {
    public static void main(String[] args) {
        Object a = new Object();
        Object b = a;
        a = null;
    }
}
```

A. Yes, because `a` was set to `null`
B. No, because `b` still points at it
C. Yes, but only if the method calls `System.gc()`
D. The code does not compile

**Q5.** After both assignments to `null`, which objects are eligible? The file name is `Q5.java`.

```java
class Node { Node next; }
public class Q5 {
    public static void main(String[] args) {
        Node a = new Node();
        Node b = new Node();
        a.next = b;
        b.next = a;
        a = null;
        b = null;
    }
}
```

A. Neither, because each `next` still points at a node
B. Both
C. Only the node that `a` used to reference
D. The code does not compile

**Q6.** What is true after `System.gc()` returns?

```java
public class Q6 {
    static Object kept;
    public static void main(String[] args) {
        kept = new Object();
        System.gc();
    }
}
```

A. The object has been collected
B. The object is still reachable through `kept`
C. `System.gc()` does not compile
D. The call makes the object eligible

### Chapter 4 answers

**Q1 — B.** `Bag` stores the same builder the caller still holds. `items.append("b")` changes that builder. `final` stopped the field from being pointed somewhere else. It did not stop `append`.

**Q2 — A.** `plus` returns a new `Coin`. `a` is still `100`. `b` is `150`.

**Q3 — A.** `A` is `final`, the field is a `private final int`, and `plus` returns a new object. `B` returns the `StringBuilder` it stored, so a caller can change the characters.

**Q4 — B.** `a` and `b` were two arrows to one box. Clearing `a` leaves the arrow from `b`. The box is not eligible while that arrow exists.

**Q5 — B.** The two nodes point at each other, and `a` and `b` no longer point in from outside. Both are eligible.

**Q6 — B.** `kept` is a `static` field and it still holds the object, so the object is reachable. `System.gc()` is a request. It does not make a reachable object eligible, and it does not promise a collection.

---

# Sunday — chapter questions

> **唔使睇**　用手追溯 initializer 順序，然後用筆記計分。

The first 20 minutes are Saturday’s misses.

Then write the output of M1 on paper before you read the mixed answers. That tracing is the other half of the gate. Use the six steps from Chapter 2. The second `new` skips the static steps.

Then do M2–M6. After that, score Chapter 1 (6), Chapter 2 (8), Chapter 3 (6), Chapter 4 (6), and the mixed set (6). **23 or more** of the 32 questions is the score half of the gate. The trace half is a correct M1, written before you check it.

Every miss becomes one rule and a five-line program before Monday of Week 4.

Say M4 out loud before you check it. Name the two objects, say which arrows remain after `first = second`, and say which object is eligible. A correct letter with no explanation does not finish the checklist item.

## Mixed set

**M1.** What is the output? Write it before you look at the answer. The file name is `M1.java`.

```java
class Base {
    static { System.out.print("A"); }
    { System.out.print("C"); }
    Base() { System.out.print("D"); }
}
public class M1 extends Base {
    static { System.out.print("B"); }
    { System.out.print("E"); }
    M1() { System.out.print("F"); }
    public static void main(String[] args) {
        new M1();
        new M1();
    }
}
```

A. `ABCDEFCDEF`
B. `ABCDEFABCDEF`
C. `CDEFCDEF`
D. The code does not compile

**M2.** What is the output?

```java
public class M2 {
    static int made;
    int n;
    M2(int n) { this.n = n; made++; }
    public static void main(String[] args) {
        M2 a = new M2(1);
        M2 b = new M2(2);
        System.out.print(a.n);
        System.out.print(made);
    }
}
```

A. `12`
B. `22`
C. `11`
D. The code does not compile

**M3.** What is the output? The file name is `M3.java`.

```java
final class Tag {
    private final StringBuilder text;
    Tag(StringBuilder text) { this.text = new StringBuilder(text); }
    public String toString() { return text.toString(); }
}
public class M3 {
    public static void main(String[] args) {
        StringBuilder text = new StringBuilder("a");
        Tag tag = new Tag(text);
        text.append("b");
        System.out.println(tag);
    }
}
```

A. `a`
B. `ab`
C. The code does not compile
D. An exception is thrown at runtime

**M4.** What is true after `first = second`? Explain this one out loud.

```java
public class M4 {
    public static void main(String[] args) {
        Object first = new Object();
        Object second = new Object();
        first = second;
    }
}
```

A. Both objects are eligible
B. The first object is eligible, and the second is not
C. The second object is eligible, and the first is not
D. Neither object is eligible

**M5.** What is the output?

```java
public class M5 {
    private int cents = 80;
    public void withdraw(int amount) {
        if (amount > 0 && amount <= cents) {
            cents -= amount;
        }
    }
    public int cents() { return cents; }
    public static void main(String[] args) {
        M5 m = new M5();
        m.withdraw(80);
        m.withdraw(1);
        System.out.println(m.cents());
    }
}
```

A. `80`
B. `0`
C. `-1`
D. The code does not compile

**M6.** What is the output?

```java
public class M6 {
    final int n;
    { n = 3; }
    M6() {}
    public static void main(String[] args) {
        System.out.println(new M6().n);
    }
}
```

A. `0`
B. `3`
C. The code does not compile
D. An exception is thrown at runtime

### Mixed answers

**M1 — A.** The first object prints `ABCDEF`: parent static, child static, parent instance, parent constructor, child instance, child constructor. The second object prints `CDEF`. The static steps have already run. The whole line is `ABCDEFCDEF`.

**M2 — A.** `this.n = n` stores the parameter on the object. `a.n` is `1`. `made` is `static`, so both constructors increment the same variable and it ends at `2`. The print is `12`.

**M3 — A.** The constructor copies the characters into a new builder. Appending to `text` changes the caller’s builder. `tag` still holds `a`.

**M4 — B.** There are two boxes. `first = second` drops the only arrow to the first box, so that box is eligible. `first` and `second` both point at the second box, so that box is not eligible.

**M5 — B.** `withdraw(80)` takes the balance to `0`. `withdraw(1)` fails the `amount <= cents` test. The print is `0`.

**M6 — B.** The instance block assigns the blank `final` before the constructor body. The constructor leaves `n` alone. The print is `3`.

---

# Rules to copy onto one card

- A constructor has the class name and no return type. A return type makes it a method. Any constructor you write removes the default no-arg constructor.
- `this.field` is the field. A parameter of the same name hides the field.
- `this(...)` is the first statement. Its arguments cannot be instance members. A cycle of constructors does not compile.
- `static` is one per class and runs once, when the class is first used. A `static` method cannot use instance members.
- For one class: `static` fields and blocks in source order, then instance fields and blocks in source order, then the constructor body.
- Superclass, then subclass: parent static, child static, parent instance, parent constructor, child instance, child constructor. The second `new` skips the static steps.
- `int a = read()` can see the default `0` when `b`’s initializer has not run. `int a = b` before `b` is declared does not compile.
- A blank `final` is assigned once on every constructor path. If the superclass has no no-arg constructor, the subclass starts with `super(...)`.
- `private` is the class. No modifier is the package. `protected` is the package and subclasses. `public` is everywhere.
- Encapsulated fields are private. A getter that returns a mutable object lets the caller change it.
- An immutable class is `final`, with `private final` fields, no setters, and no shared mutable object. A change returns a new object.
- Eligible means unreachable. One live reference keeps the object, including a `static` field. An island with no outside reference is eligible. `System.gc()` is a request.
