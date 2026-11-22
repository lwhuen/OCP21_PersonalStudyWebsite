# Week 3 glossary — classes and memory

Terms from [Week-03-notes.md](Week-03-notes.md). The exam words are English. Overriding, interfaces, records, and sealed types are Week 4.

## Monday — constructors and `this`

| Term | Meaning |
|---|---|
| Constructor | A block whose name is the class name and which has no return type. `new` allocates the object and runs a constructor. `void Person()` is a method. `new` does not call it. |
| Default constructor | The no-arg constructor the compiler adds only when you write none. It has the same access as the class. The first constructor you write removes it. |
| Top-level class | `public` or package-private. A file has at most one `public` top-level class, and the file name matches it. `private` and `protected` are not allowed on a top-level class. |
| `this.field` | The field. A parameter of the same name hides the field. `n = n` assigns the parameter to itself and leaves the field at its default. |
| `this(...)` | A call to another constructor of the same class. It is the first statement. Its arguments cannot be instance fields or instance methods. A cycle of constructors does not compile. |
| Instance initializer | A `{ }` block in the class body. It runs in the constructor that actually builds the object, not in a constructor that starts with `this(...)`. |

## Wednesday — `static` and initialization order

| Term | Meaning |
|---|---|
| `static` member | One copy for the class, shared by every object. A `static` method cannot use `this` or an instance member. An instance method can use a `static` member. |
| `static` initializer | A `static { }` block. It runs once, when the class is first used. If `main` is inside that class, it runs before the first line of `main`. |
| Initialization order | For one class: `static` fields and blocks in source order, once. Then each `new` runs instance fields and blocks in source order, then the constructor body. |
| Superclass, then subclass | Parent static, child static, parent instance, parent constructor, child instance, child constructor. The second `new` skips the static steps. |
| `super()` | The parent constructor call. If you write neither `this(...)` nor `super(...)`, the compiler inserts `super()`. That call needs a no-arg constructor on the parent. Constructors are not inherited. |
| Blank `final` | A `final` instance field with no initializer. It is assigned once on every constructor path: in the declaration, an instance block, or the constructor. A second assignment does not compile. |
| Illegal forward reference | `int a = b` does not compile when `b` is declared later. `int a = read()` can compile and see `b`’s default `0`, because `b`’s initializer has not run yet. |

## Friday — encapsulation

| Term | Meaning |
|---|---|
| Encapsulation | Fields are private, and every change goes through a method. Another class cannot assign the field. |
| `private` | Visible in the declaring class only, including that class’s own `main`. |
| Package-private | No modifier. Visible to classes in the same package. Classes in the same file share a package. |
| `protected` | Visible in the same package, and in subclasses. A subclass in another package is practiced in Week 4. |
| `public` | Visible to every class. |
| Mutable escape | A getter that returns a `StringBuilder`, an array, or a list hands out the object you stored. The caller can change it. Return a copy. A returned `String` is safe, because a `String` cannot be changed. |

## Saturday — immutability and garbage collection

| Term | Meaning |
|---|---|
| Immutable class | `final`, with `private final` fields, no setters, and no shared mutable object. A method that looks like a change returns a new object. |
| `final` reference | The field cannot be pointed at a different object. The `StringBuilder` or list it already points at can still change. Copy on the way in and on the way out. |
| Eligible | No live reference can reach the object, so the collector is allowed to reclaim it. Eligible is not the same as already collected. |
| Live reference | A local variable that still holds the object, a field of a reachable object, or a `static` field. One remaining reference keeps the object alive. |
| Island | Two or more objects that point only at each other. With no reference from outside, all of them are eligible. |
| `System.gc()` | A request for a collection. It does not make a reachable object eligible, and it does not promise that anything was collected. |
