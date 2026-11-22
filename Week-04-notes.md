# Week 4 notes — inheritance through pattern matching

**25 hours.** Weekend days are 8 hours. This file follows Week 4 of the study plan. Calendar dates are only in the [15-week plan](OCP-Java-SE-21-study-plan.md). The gate is the mixed OOP questions at **70%** (21 of the 30 questions in this file).

Weekdays are Monday, Wednesday, and Friday, 3 hours each: 20 minutes on yesterday’s misses, 2 hours typing every listing, 40 minutes of questions and the notebook. Saturday and Sunday are 8 hours each. The extra two hours are questions. Monday’s first 20 minutes are the Week 3 misses.

This is the heavy week before the holidays. The exam topic is inheritance, interfaces, records, sealed types, and patterns.

| Day | What the plan says | Where it is in this file |
|---|---|---|
| Mon | `extends`, `super`, overriding rules on one card | Chapter 1, `Zoo`, the overriding card, questions Q1–Q6 |
| Wed | Reference type versus object type, and field hiding | Chapter 2, questions Q1–Q6 |
| Fri | `equals`, `hashCode`, interfaces, and enums | Chapter 3, `Coins`, `Pets`, `Season`, questions Q1–Q6 |
| Sat (8 h) | Records, sealed types, switch patterns, record patterns | Chapter 4, `Coin`, `Shapes`, questions Q1–Q6 |
| Sun (8 h) | Nested-class rules in the notebook, then a mixed OOP set | The notebook page, the mixed set, then score all 30 |

Same checklist as the study plan:

- [ ] `Animal`, `Dog`, and `Cat`. Overriding rules on one card: signature, covariant return, access, checked exceptions.
- [ ] One example where a field is hidden, not overridden. The reference type decides what compiles; the object type decides which override runs.
- [ ] A correct `equals` and `hashCode`, and one broken `equals`. If `equals` is true, the hash codes match.
- [ ] An interface with a default method and a static method, two implementers, and an enum with a field and a method.
- [ ] A sealed interface with an exhaustive switch, a record with a compact constructor, a record pattern, and a `when` guard. A general pattern above a specific one does not compile.
- [ ] Mixed questions on inheritance, interfaces, records, and patterns at 70%. Nested classes: one notebook page on what each kind can see.

Predict each listing before you run it. Each miss goes in the notebook as one rule and a five-line program.

The questions are practice in the exam’s style. They are not copied from the real exam or from a book. Try each one before its answer key.

---

# Chapter 1 — `extends`, `super`, and overriding

> **必睇**　第 6 章 pp. 292–296（“Understanding Inheritance”）、pp. 320–329（“Inheriting Members”），同 “Creating Abstract Classes”（緊接其後，到 “Creating Immutable Objects” 之前）。
>
> **唔使睇**　第 7 章留到本章之後幾日。Review Questions 唔使做。

**Monday** is this chapter, `Zoo`, the overriding card, and questions Q1–Q6.

## What you must know

A class `extends` one superclass. Constructors are not inherited. The first line of a child constructor is `super(...)` or `this(...)`. If you write neither, the compiler inserts `super()`.

An override replaces an instance method for objects of the subclass. Copy this card into the notebook:

- The signature matches: the same name and the same parameter types. A different parameter list is an overload, not an override.
- The return type is the same, or a subtype of the parent’s return type. That is a covariant return.
- The access is the same or wider. `public` cannot become package-private.
- A checked exception is the same, a subtype, or absent. The child cannot throw a broader checked exception, and it cannot add a new one.
- `private`, `static`, and `final` methods are not overridden. A `static` method with the same signature is hidden. A `final` method cannot be redeclared. A `private` method is not visible, so a child method of the same name is a new method.

`@Override` asks the compiler to check that a real override exists. Put it on every override you type this week.

`super.speak()` calls the parent version from inside the child.

An `abstract` class can be extended and cannot be constructed with `new`. A method marked `abstract` has no body. The class that declares it must itself be `abstract`. A concrete subclass implements every abstract method, or that subclass is `abstract` too. An abstract class may still have fields, constructors, and ordinary methods. The child constructor still starts with `super(...)`. `abstract` cannot be combined with `final`, and an abstract method cannot be `private` or `static`.

## Monday lab — `Zoo`

Type this. The file name is `Zoo.java`.

```java
class Animal {
    String kind = "animal";
    String speak() { return "generic"; }
}
class Dog extends Animal {
    String kind = "dog";
    @Override String speak() { return "woof"; }
}
class Cat extends Animal {
    String kind = "cat";
    @Override String speak() { return "meow"; }
}
public class Zoo {
    public static void main(String[] args) {
        Animal dog = new Dog();
        Animal cat = new Cat();
        System.out.println(dog.kind + " " + dog.speak());
        System.out.println(cat.kind + " " + cat.speak());
    }
}
```

The run prints:

```text
animal woof
animal meow
```

`kind` is a field, so it is hidden. The reference type `Animal` selects `animal`. `speak` is overridden. The object type selects `woof` or `meow`. Wednesday uses this listing again.

Monday’s questions are Q1–Q6.

## Chapter 1 questions

**Q1.** Does this compile?

```java
class Animal { Animal create() { return new Animal(); } }
class Dog extends Animal { @Override Dog create() { return new Dog(); } }
```

A. Yes. The return type is covariant
B. Yes, but only if `create` is `static`
C. No. The return type must be identical
D. No. `Dog` cannot extend `Animal`

**Q2.** Does this compile?

```java
class Animal { public void speak() {} }
class Dog extends Animal { void speak() {} }
```

A. Yes
B. Yes, because package access is the default
C. No. The override is less accessible
D. No. `void` methods cannot be overridden

**Q3.** Does this compile?

```java
import java.io.*;
class Animal { void speak() throws IOException {} }
class Dog extends Animal { void speak() throws Exception {} }
```

A. Yes. `Exception` includes `IOException`
B. Yes, because the method is an override
C. No. The checked exception is broader
D. No. `speak` must be `public`

**Q4.** What is the output?

```java
class Animal { static String speak() { return "animal"; } }
class Dog extends Animal { static String speak() { return "dog"; } }
public class Q4 {
    public static void main(String[] args) {
        Animal a = new Dog();
        System.out.println(a.speak());
    }
}
```

A. `dog`
B. `animal`
C. The code does not compile
D. An exception is thrown at runtime

**Q5.** What is the output? The file name is `Q5.java`.

```java
class Animal {
    private String speak() { return "animal"; }
    String call() { return speak(); }
}
class Dog extends Animal {
    public String speak() { return "dog"; }
}
public class Q5 {
    public static void main(String[] args) {
        System.out.println(new Dog().call());
    }
}
```

A. `dog`
B. `animal`
C. The code does not compile
D. An exception is thrown at runtime

**Q6.** Does this compile?

```java
class Animal { void speak() {} }
class Dog extends Animal { @Override void speak(int n) {} }
```

A. Yes. `speak(int)` overrides `speak()`
B. Yes. `@Override` allows a new parameter
C. No. The signature does not match, so this is not an override
D. No. A subclass cannot declare `speak`

### Chapter 1 answers

**Q1 — A.** `Dog` is a subtype of `Animal`, so `Dog create()` is a legal covariant return.

**Q2 — C.** An override cannot narrow access. `public` in the parent cannot become package-private in the child.

**Q3 — C.** `Exception` is broader than `IOException`. An override may throw `IOException`, a subtype such as `FileNotFoundException`, or no checked exception.

**Q4 — B.** A `static` method is hidden, not overridden. The reference type `Animal` selects `animal`.

**Q5 — B.** `Animal.speak` is `private`, so `Dog.speak` does not override it. `call` was compiled against the private method and returns `animal`.

**Q6 — C.** `@Override` requires a matching signature. `speak(int)` overloads `speak()`. Without `@Override` the class would compile, and it still would not be an override.

---

# Chapter 2 — Reference type and object type

> **必睇**　第 7 章 “Understanding Polymorphism”，pp. 410–418。如果星期一未讀 “Hiding Variables”（p. 328），補嗰一頁。
>
> **唔使睇**　唔好由第 7 章開頭順住讀。interfaces、enums、sealed、records、nested classes 係後面幾日。

**Wednesday** is this chapter and questions Q1–Q6. Use `Zoo` from Monday as the hiding example on the checklist.

## What you must know

The reference type is the type on the left of the variable. The object type is the class after `new`.

The reference type decides which names compile. If `fetch` is declared only on `Dog`, `Animal a = new Dog(); a.fetch()` does not compile. A cast compiles when the type is in the hierarchy. A cast to the wrong object throws `ClassCastException` at runtime.

The object type decides which override runs. Fields do not work that way. A field in the subclass hides the parent field. The reference type selects the field, including through a cast: `((Dog) a).kind` reads `Dog`’s field.

`instanceof` tests the object type. `null instanceof Dog` is `false`. It does not throw. A pattern both tests and assigns:

```java
if (a instanceof Dog d) {
    System.out.println(d.kind);
}
```

Inside that block, `d` has type `Dog`.

## Chapter 2 questions

**Q1.** Using `Animal`, `Dog`, and `Cat` from `Zoo`, what is the output?

```java
Animal dog = new Dog();
System.out.println(dog.kind + " " + dog.speak());
```

A. `dog woof`
B. `animal woof`
C. `animal generic`
D. The code does not compile

**Q2.** What is the output?

```java
Animal dog = new Dog();
System.out.println(((Dog) dog).kind);
```

A. `animal`
B. `dog`
C. The code does not compile
D. A `ClassCastException` is thrown

**Q3.** `Dog` declares `void fetch()`. `Animal` does not. What is the result?

```java
Animal a = new Dog();
a.fetch();
```

A. It runs `Dog.fetch`
B. The code does not compile
C. A `ClassCastException` is thrown
D. A `NullPointerException` is thrown

**Q4.** What is the output?

```java
System.out.println(null instanceof Dog);
```

A. `true`
B. `false`
C. The code does not compile
D. A `NullPointerException` is thrown

**Q5.** What is the output? `Dog.kind` is `"dog"`.

```java
Animal a = new Dog();
if (a instanceof Dog d) {
    System.out.println(d.kind);
}
```

A. `animal`
B. `dog`
C. The code does not compile
D. Nothing is printed

**Q6.** What is the result?

```java
Animal a = new Animal();
Dog d = (Dog) a;
```

A. `d` refers to an `Animal`
B. The code does not compile
C. A `ClassCastException` is thrown
D. `d` is `null`

### Chapter 2 answers

**Q1 — B.** The field comes from the reference type. The override comes from the object type. The line is `animal woof`.

**Q2 — B.** The cast changes the reference type used for the field read. `Dog.kind` is `dog`. The object really is a `Dog`, so the cast succeeds.

**Q3 — B.** The compiler looks at `Animal`. `fetch` is not a member of `Animal`, so the call does not compile. The cast `(Dog) a` would make the call legal.

**Q4 — B.** `instanceof` on `null` is `false`.

**Q5 — B.** The pattern succeeds and `d` is a `Dog` reference, so `d.kind` is the hidden field `dog`.

**Q6 — C.** The cast is legal to the compiler because `Dog` extends `Animal`. At runtime the object is not a `Dog`, so the cast throws `ClassCastException`.

---

# Chapter 3 — `equals`, `hashCode`, interfaces, and enums

> **必睇**　第 4 章 “Understanding Equality”，pp. 186–188（第 2 週讀過 `String`，今日重讀 `equals` / `hashCode` 契約）。第 7 章 pp. 360–379：“Implementing Interfaces” 同 “Working with Enums”。private interface method 在 “Declaring Concrete Interface Methods”（p. 367）。
>
> **唔使睇**　sealed 同 record 係星期六。

**Friday** is this chapter, three listings, and questions Q1–Q6.

## What you must know

`equals` is reflexive, symmetric, transitive, and consistent. `x.equals(null)` is `false`. If `a.equals(b)` is `true`, then `a.hashCode()` and `b.hashCode()` return the same `int`. The reverse is not required: equal hash codes do not mean `equals` is true.

A broken `equals` overrides `equals` and leaves `hashCode` as the identity hash from `Object`. A `HashSet` may then hold two objects that say they are equal. This run’s broken set has size 2. The fixed pair has size 1.

### `Coins`

Type this. The file name is `Coins.java`.

```java
import java.util.*;

class Bad {
    int n;
    Bad(int n) { this.n = n; }
    public boolean equals(Object o) { return o instanceof Bad b && b.n == n; }
}
class Good {
    int n;
    Good(int n) { this.n = n; }
    public boolean equals(Object o) { return o instanceof Good g && g.n == n; }
    public int hashCode() { return n; }
}
public class Coins {
    public static void main(String[] args) {
        Set<Bad> bad = new HashSet<>();
        bad.add(new Bad(1));
        bad.add(new Bad(1));
        Set<Good> good = new HashSet<>();
        good.add(new Good(1));
        good.add(new Good(1));
        System.out.println(bad.size() + " " + good.size());
    }
}
```

The run prints:

```text
2 1
```

### `Pets`

An interface can have a default instance method and a static method. The static method is called on the interface name. It is not inherited.

```java
interface Pet {
    String name();
    default String speak() { return "pet"; }
    static String home() { return "home"; }
}
class DogPet implements Pet {
    public String name() { return "Ada"; }
}
class CatPet implements Pet {
    public String name() { return "Bea"; }
    @Override public String speak() { return "meow"; }
}
public class Pets {
    public static void main(String[] args) {
        Pet dog = new DogPet();
        Pet cat = new CatPet();
        System.out.println(dog.speak() + " " + cat.speak() + " " + Pet.home());
    }
}
```

The run prints:

```text
pet meow home
```

`DogPet.home()` does not compile. Two interfaces with the same default method force the class to override that method.

A `private` method in an interface has a body and is visible only inside that interface. Implementing classes do not inherit it and cannot call it. A `private` instance method can be called from a default method. A `private static` method can be called from a static method or a default method. A static method cannot call a private instance method, because a static method has no instance.

```java
interface Steps {
    private static String tag(String s) { return "[" + s + "]"; }
    default String go() { return tag("go"); }
}
class Walk implements Steps {}
```

`new Walk().go()` returns `[go]`. `Steps.tag("go")` and `Walk.tag("go")` do not compile. The private method never leaves the interface.

### `Season`

An enum constant list ends before the other members. The constructor runs once for each constant and is private. `ordinal` starts at 0. `new Season()` does not compile.

```java
enum Season {
    WINTER("cold"), SUMMER("hot");
    private final String feel;
    Season(String feel) { this.feel = feel; }
    String feel() { return feel; }
}
public class Seasons {
    public static void main(String[] args) {
        System.out.println(Season.WINTER.feel());
        System.out.println(Season.SUMMER.ordinal());
    }
}
```

The run prints:

```text
cold
1
```

Friday’s questions are Q1–Q6.

## Chapter 3 questions

**Q1.** What is `new Good(1).equals(null)` using `Good` from `Coins`?

A. `true`
B. `false`
C. The code does not compile
D. A `NullPointerException` is thrown

**Q2.** Which statement matches the contract?

A. Equal hash codes mean `equals` returns `true`
B. If `equals` returns `true`, the hash codes match
C. `hashCode` must return the field `n`
D. `equals` may return `true` for `null`

**Q3.** What does `Coins` print?

A. `1 1`
B. `2 2`
C. `2 1`
D. `1 2`

**Q4.** What does `Pets` print?

A. `pet pet home`
B. `pet meow home`
C. `meow meow home`
D. The code does not compile

**Q5.** Does `DogPet.home()` compile?

A. Yes, and it returns `home`
B. Yes, and it returns `pet`
C. No. An interface static method is called on the interface
D. No. `Pet` has no static method

**Q6.** What is the result of `new Season("warm")`?

A. A new constant named `warm`
B. The code does not compile
C. `WINTER`
D. An exception is thrown at runtime

### Chapter 3 answers

**Q1 — B.** `instanceof` on `null` fails, so this `equals` returns `false`.

**Q2 — B.** Equal objects share a hash code. Matching hash codes do not imply `equals`.

**Q3 — C.** `Bad` does not override `hashCode`, so the two equal objects can both sit in the set. `Good` uses `n` as the hash code, and the set keeps one.

**Q4 — B.** `DogPet` inherits the default `pet`. `CatPet` overrides it with `meow`. `Pet.home()` is the static method.

**Q5 — C.** Static interface methods are not inherited. The call is `Pet.home()`.

**Q6 — B.** An enum constructor is private. Code outside the enum cannot call `new Season(...)`. The constants are `WINTER` and `SUMMER`.

---

# Chapter 4 — Records, sealed types, and patterns

> **必睇**　第 7 章 pp. 380–399：“Sealing Classes” 同 “Encapsulating Data with Records”。第 3 章第 1 週跳過嘅兩節：pp. 106–110（`instanceof` pattern）同 pp. 124–129（`switch` pattern）。
>
> **唔使睇**　nested classes 係星期日。

**Saturday** is 8 hours: this chapter, three listings, and questions Q1–Q6.

## What you must know

A record is a `final` class with one field per component, a canonical constructor, accessors named after the components, and generated `equals`, `hashCode`, and `toString`. The accessor is `cents()`, not `getCents()`.

A compact constructor has the record’s name and no parameter list. You assign the component parameters. The canonical constructor then assigns the fields. Use it to check or fix the values.

```java
public Coin {
    if (cents < 0) cents = 0;
}
```

A sealed type lists its permitted subtypes with `permits`. Each direct subtype is `final`, `sealed`, or `non-sealed`. A record that implements a sealed interface is implicitly `final`. A switch on a sealed type is exhaustive when every permitted type has a case. A `default` is then optional.

A type pattern is `case String s`. A record pattern takes the components: `case Point(int x, int y)`. A `when` guard adds a boolean condition. Patterns are tested from top to bottom. A case that can never run, because an earlier case already covers it, does not compile. That is a dominated pattern. Put the specific pattern first.

`case null` handles a null selector. Without `case null`, a null selector throws `NullPointerException`.

### `Coin`

```java
public record Coin(int cents) {
    public Coin {
        if (cents < 0) cents = 0;
    }
    public static void main(String[] args) {
        System.out.println(new Coin(-5).cents());
    }
}
```

The run prints:

```text
0
```

### `Shapes`

The file name is `Shapes.java`.

```java
sealed interface Shape permits Circle, Rect {}
record Circle(int r) implements Shape {}
record Rect(int w, int h) implements Shape {}

public class Shapes {
    static String describe(Shape s) {
        return switch (s) {
            case Circle c -> "circle" + c.r();
            case Rect r -> "rect";
        };
    }
    public static void main(String[] args) {
        System.out.println(describe(new Circle(3)));
    }
}
```

The run prints:

```text
circle3
```

There is no `default`. The sealed permits list makes the switch exhaustive.

### Record pattern and `when`

```java
record Point(int x, int y) {}
public class Points {
    static String where(Object o) {
        return switch (o) {
            case Point(int x, int y) when x > 0 -> "right";
            case Point(int x, int y) -> "other";
            case null -> "null";
            default -> "no";
        };
    }
    public static void main(String[] args) {
        System.out.println(where(new Point(2, 1)));
        System.out.println(where(new Point(-1, 4)));
        System.out.println(where("no"));
    }
}
```

The run prints:

```text
right
other
no
```

This dominated switch does not compile. The `String` case can never run:

```java
return switch (o) {
    case CharSequence c -> 1;
    case String s -> 2;
    default -> 3;
};
```

Swap the two patterns and it compiles. `String` is more specific than `CharSequence`.

Saturday’s questions are Q1–Q6.

## Chapter 4 questions

**Q1.** What is `new Coin(-5).cents()`?

A. `-5`
B. `0`
C. The code does not compile
D. An exception is thrown at runtime

**Q2.** `record Coin(int cents) {}`. Does `new Coin(1).getCents()` compile?

A. Yes, and it returns `1`
B. Yes, and it returns `0`
C. No. The accessor is `cents()`
D. No. A record cannot have an `int` component

**Q3.** What does `Shapes` print?

A. `circle3`
B. `rect`
C. The code does not compile, because the switch has no `default`
D. An exception is thrown at runtime

**Q4.** Does the dominated switch in this chapter compile?

A. Yes, and a `String` selects case 2
B. Yes, and a `String` selects case 1
C. No. `case String` is dominated by `case CharSequence`
D. No. `switch` cannot use `CharSequence`

**Q5.** What does `where(new Point(2, 1))` print?

A. `right`
B. `other`
C. `no`
D. The code does not compile

**Q6.** What does `where(null)` print in `Points`?

A. `null`
B. `no`
C. The code does not compile
D. A `NullPointerException` is thrown

### Chapter 4 answers

**Q1 — B.** The compact constructor changes the parameter `cents` from `-5` to `0` before the field is stored.

**Q2 — C.** A record accessor uses the component name. `getCents` is not generated.

**Q3 — A.** `Circle` and `Rect` cover the sealed type, so the switch is exhaustive without `default`. The circle’s `r` is `3`.

**Q4 — C.** The compiler rejects a case label dominated by an earlier one. Put `case String s` above `case CharSequence c`.

**Q5 — A.** The record pattern matches, and `when x > 0` is true.

**Q6 — A.** `case null` is present, so the selector `null` selects that case. Remove `case null` and the same call throws `NullPointerException`.

---

# Sunday — nested classes, then the questions

> **必睇**　第 7 章 “Creating Nested Classes”，pp. 400–409。
>
> **唔使睇**　第 7 章 Review Questions。混合題用筆記計分。

The first 20 minutes are Saturday’s misses. Then copy this page into the notebook. Then do the mixed set and score all 30. **21 or more** is the gate.

## Notebook page — what each nested class can see

**Static nested class.** Declared with `static` inside another class. It has no hidden outer instance. It can use the outer class’s private static members. It can use an instance member only through an outer object you pass in. Create it with `new Outer.Nested()`.

**Inner class.** A member class without `static`. Each inner object has a hidden reference to an outer object. Create it with `outer.new Inner()`, or with `new Inner()` inside an instance method of the outer class. It can read the outer class’s private instance members. `Outer.this` is the outer object. On Java 21 an inner class may declare static members.

**Local class.** Declared inside a method. It has no access modifier. It can use the enclosing class’s members, and it can use local variables and parameters that are final or effectively final.

**Anonymous class.** An expression with no name. It extends one class or implements one interface. It has no constructor of its own. An instance initializer is allowed. It can use effectively final locals, the same way a local class can.

## Mixed set

**M1.** An outer class has `private int n = 4`, and its inner class method returns `n`. Does the inner class compile, and what does a call return?

A. It compiles and returns `4`
B. It compiles and returns `0`
C. It does not compile. Inner classes cannot read `private` members
D. It does not compile. Inner classes cannot have methods

**M2.** Does this compile?

```java
void run() {
    int n = 1;
    class Local { int value() { return n; } }
    n = 2;
    System.out.println(new Local().value());
}
```

A. It prints `1`
B. It prints `2`
C. The code does not compile
D. An exception is thrown at runtime

**M3.** What is the output?

```java
Pet pet = new Pet() {
    public String name() { return "Cy"; }
};
System.out.println(pet.speak() + " " + pet.name());
```

`Pet` is the interface from `Pets`.

A. `pet Cy`
B. `meow Cy`
C. The code does not compile
D. An exception is thrown at runtime

**M4.** `Fly` and `Swim` both declare `default String move() { return "go"; }`. `Duck` implements both and does not override `move`. Does `Duck` compile?

A. Yes, and `move` returns `go`
B. Yes, and the call is ambiguous at runtime
C. No. The class must override `move`
D. No. An interface cannot have a default method

**M5.** `sealed interface Shape permits Box {}` and `class Box implements Shape {}`. `Box` is not `final`, `sealed`, or `non-sealed`. Does this compile?

A. Yes
B. Yes, because `Box` is in `permits`
C. No. A permitted class must say how it continues the seal
D. No. A sealed type cannot be an interface

**M6.** `Animal a = new Dog()`, with the classes from `Zoo`. What is `(a instanceof Dog d) ? d.speak() : a.kind`?

A. `animal`
B. `woof`
C. `dog`
D. The code does not compile

### Mixed answers

**M1 — A.** An inner class can read the outer class’s private instance members. The returned value is `4`.

**M2 — C.** `Local` uses `n`, and `n` is assigned again. A local variable used from a local class must be final or effectively final.

**M3 — A.** The anonymous class implements `Pet`, inherits the default `speak`, and supplies `name`. The print is `pet Cy`.

**M4 — C.** Two inherited default methods with the same signature conflict. `Duck` must override `move`.

**M5 — C.** Being listed in `permits` is not enough. The permitted class declares `final`, `sealed`, or `non-sealed`. A record is implicitly `final`, which is why `Circle` could implement `Shape` without writing `final`.

**M6 — B.** The pattern matches the `Dog` object. `d.speak()` runs the override and returns `woof`.

---

# Rules to copy onto one card

- An override matches the signature. The return may be covariant. Access stays the same or gets wider. Checked exceptions stay the same, get narrower, or disappear.
- `static` hides. `private` is not overridden. `final` cannot be overridden. `@Override` checks that an override is real.
- The reference type decides what compiles and which field is read. The object type decides which override runs.
- `instanceof` on `null` is `false`. A bad cast throws `ClassCastException`.
- If `equals` is true, the hash codes match. `equals(null)` is `false`.
- An interface static method is called on the interface. A default method is inherited. Two conflicting defaults must be overridden. A private interface method stays inside the interface.
- An abstract class cannot be constructed. A concrete subclass implements every abstract method. `abstract` is not `final`, and an abstract method is not `private` or `static`.
- A record accessor is the component name. A compact constructor assigns the parameters, and the fields are stored after that.
- A sealed switch is exhaustive when every permitted type has a case. A general pattern above a specific one does not compile. `when` guards a pattern. `case null` handles null.
- A static nested class has no outer instance. An inner class does. Local and anonymous classes see effectively final locals.
