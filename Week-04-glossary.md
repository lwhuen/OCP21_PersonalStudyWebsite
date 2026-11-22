# Week 4 glossary — inheritance through pattern matching

Terms from [Week-04-notes.md](Week-04-notes.md). The exam words are English.

## Monday — overriding

| Term | Meaning |
|---|---|
| `extends` | A class has one superclass. The child constructor calls a parent constructor first. |
| Override | An instance method in the subclass replaces the parent method for objects of the subclass. |
| Covariant return | An override may return the parent’s return type or a subtype of it. `Dog create()` can override `Animal create()`. |
| Override access | The same access or wider. `public` cannot become package-private. |
| Override exceptions | A checked exception stays the same, becomes a subtype, or disappears. The child cannot throw a broader checked exception. |
| `@Override` | Asks the compiler to check that a real override exists. A different parameter list is an overload, so `@Override` on that method does not compile. |
| Hidden static method | A `static` method with the same signature in the subclass hides the parent method. The reference type selects it. It is not an override. |
| `private` method | Not visible to the subclass, so a child method of the same name is a new method. A parent method that calls the private one does not dispatch to the child. |
| `final` method | Cannot be redeclared in a subclass. |
| `abstract` class | Cannot be constructed with `new`. It may have fields, constructors, and ordinary methods. A concrete subclass implements every abstract method. |
| `super.speak()` | Calls the parent version from inside the child. |

## Wednesday — reference type and object type

| Term | Meaning |
|---|---|
| Reference type | The type written on the variable. It decides which names compile and which field is read. |
| Object type | The class after `new`. It decides which override runs. |
| Field hiding | A field in the subclass hides the parent field. It is not overridden. `((Dog) a).kind` reads `Dog`’s field. |
| `instanceof` | Tests the object type. `null instanceof Dog` is `false` and does not throw. |
| Pattern `instanceof` | `if (a instanceof Dog d)` both tests and assigns. Inside the block, `d` has type `Dog`. |
| `ClassCastException` | Thrown when a cast’s type is in the hierarchy but the object is not that type. `(Dog) new Animal()` throws it. |

## Friday — `equals`, interfaces, enums

| Term | Meaning |
|---|---|
| `equals` contract | Reflexive, symmetric, transitive, and consistent. `x.equals(null)` is `false`. |
| `hashCode` contract | If `a.equals(b)` is true, the hash codes match. Matching hash codes do not imply `equals`. |
| Broken `equals` | An `equals` that compares values while `hashCode` stays the identity hash from `Object`. A `HashSet` can then hold two objects that say they are equal. |
| Default method | An instance method in an interface with a body. Implementing classes inherit it and may override it. |
| Interface static method | Called on the interface name, as in `Pet.home()`. It is not inherited. `DogPet.home()` does not compile. |
| Conflicting defaults | Two interfaces with the same default signature. The class must override that method. |
| Private interface method | Has a body and is visible only inside that interface. Implementers do not inherit it. A static interface method cannot call a private instance method. |
| Enum | A fixed set of constants. The constructor is private. `new Season(...)` from outside does not compile. `ordinal` starts at 0. |

## Saturday — records, sealed types, patterns

| Term | Meaning |
|---|---|
| Record | A `final` class with one field per component, a canonical constructor, accessors named after the components, and generated `equals`, `hashCode`, and `toString`. |
| Record accessor | The component name. `cents()`, not `getCents()`. |
| Compact constructor | `public Coin { ... }` with no parameter list. You assign the component parameters. The fields are stored after that. |
| Sealed type | Lists its permitted subtypes with `permits`. Each direct subtype is `final`, `sealed`, or `non-sealed`. A record that implements a sealed interface is implicitly `final`. |
| Exhaustive switch | A switch that covers every remaining value. On a sealed type, one case per permitted type is enough, so `default` is optional. |
| Type pattern | `case String s`. It tests the type and assigns the variable. |
| Record pattern | `case Point(int x, int y)`. It takes the components out of a matching record. |
| `when` | A boolean guard on a pattern. `case Point(int x, int y) when x > 0`. |
| Dominated pattern | A later case that can never run because an earlier case already covers it. It does not compile. Put the more specific pattern first. |
| `case null` | Handles a null selector. Without it, a null selector throws `NullPointerException`. |

## Sunday — nested classes

| Term | Meaning |
|---|---|
| Static nested class | Declared with `static`. No hidden outer instance. It can use the outer class’s private static members. Created with `new Outer.Nested()`. |
| Inner class | A member class without `static`. Each object has a hidden outer object. It can read the outer class’s private instance members. `Outer.this` is that outer object. |
| Local class | Declared inside a method. No access modifier. It can use effectively final local variables and parameters. |
| Anonymous class | An expression with no name. It extends one class or implements one interface. No constructor of its own. It can use effectively final locals. |
| Effectively final | A local variable that is assigned once and never assigned again. Local and anonymous classes, and lambdas in Week 7, may use only these locals. |
