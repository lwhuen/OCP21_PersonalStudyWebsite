# Week 8 notes — I/O, modules, and threads

**25 hours.** Weekend days are 8 hours. This file follows Week 8 of the study plan. Calendar dates are only in the [15-week plan](OCP-Java-SE-21-study-plan.md). The gate is the mixed quiz at **65%** (13 of the 20 questions in this file). When this week ends, the syllabus is closed. After that the book is a reference.

Weekdays are Monday, Wednesday, and Friday, 3 hours each: 20 minutes on yesterday’s misses, 2 hours typing every listing, 40 minutes of questions and the notebook. Saturday and Sunday are 8 hours each. The extra two hours are questions. Monday’s first 20 minutes are the Week 7 misses.

| Day | What the plan says | Where it is in this file |
|---|---|---|
| Mon | Byte and character streams, `Path`, and `Files` | Chapter 1, `Words`, the three path lines, questions Q1–Q4 |
| Wed | Serialization, locales, resource bundles | Chapter 2, `Bag`, questions Q1–Q4 |
| Fri | Modules, compiled in a terminal | Chapter 3, the two modules, the service, the broken export, questions Q1–Q4 |
| Sat (8 h) | Threads, executors, a race, virtual threads | Chapter 4, `Race`, questions Q1–Q4 |
| Sun (8 h) | Mixed quiz and the weak-topic list | The mixed set, score all 20, write the three weakest topics |

Same checklist as the study plan:

- [ ] With `Path` and try-with-resources, read a file, count words, and write a report. One notebook example each for `resolve`, `relativize`, and `normalize`.
- [ ] State what `transient` and `serialVersionUID` do. A resource bundle in two locales, printing a date and a currency. Search order is full locale, then language, then the base bundle.
- [ ] Two modules, one `exports` and one `requires`, run with `java -p` and `-m`. Then a service with `provides`, `with`, and `uses`. Break a missing `exports` once and save the error.
- [ ] A counter that loses updates, then the same counter fixed with `synchronized` or `AtomicInteger`. Run tasks on a fixed pool and on `newVirtualThreadPerTaskExecutor`.
- [ ] From memory: thread states, `Runnable` versus `Callable`, `start` versus `run`, `shutdown` versus `shutdownNow`. Calling `run` does not start a thread. `Future.get` blocks.
- [ ] Mixed quiz on I/O, locale, modules, and threads at 65%. Write your three weakest topics at the top of the notebook. The book is now a reference, not a reading plan.

Predict each listing before you run it. Each miss goes in the notebook as one rule and a five-line program.

The questions are practice in the exam’s style. They are not copied from the real exam or from a book. Try each one before its answer key.

Annotations and logging are on the exam at recognition level. They sit at the end of Chapter 2. You do not build a logging application this week.

---

# Chapter 1 — Streams of bytes and characters, `Path`, and `Files`

> **必睇**　第 14 章 I/O，pp. 812–847（`Path`、`Files`、byte 同 character streams）同 pp. 856–871（“Interacting with Users”、file attributes、走訪目錄）。
>
> **略讀**　“Review of Key APIs”，p. 872。只核對筆記未出現過嘅方法名。
>
> **唔使睇**　“Serializing Data”（pp. 848–855）係星期三。Review Questions 唔使做。

**Monday** is this chapter, `Words`, three notebook lines, and questions Q1–Q4.

## What you must know

`InputStream` and `OutputStream` move bytes. `Reader` and `Writer` move characters. `InputStreamReader` bridges a byte stream to a character stream with a charset. `BufferedReader` and `BufferedWriter` wrap another stream so you can read lines. Close the outermost wrapper. Try-with-resources, from Week 5, is how you close it.

`Path` is a location. `Path.of("docs", "notes", "week.txt")` builds one. These three go in the notebook. On Windows the separator in the print is `\`.

| Call | Result on this PC |
|---|---|
| `Path.of("docs", "notes", "week.txt").resolve("extra.txt")` | `docs\notes\week.txt\extra.txt` |
| `Path.of("docs", "notes", "week.txt").resolve(Path.of("C:\\temp\\x.txt"))` | `C:\temp\x.txt` |
| `Path.of("docs", "notes").relativize(Path.of("docs", "code", "A.java"))` | `..\code\A.java` |
| `Path.of("a", "..", "b", ".", "c").normalize()` | `b\c` |

`resolve` of a relative path appends. `resolve` of an absolute path replaces the original. `relativize` builds the path from the first location to the second. `normalize` removes `.` and applies `..`.

`Files.readString`, `Files.writeString`, `Files.readAllLines`, `Files.lines`, `Files.exists`, `Files.createDirectories`, `Files.copy`, and `Files.walk` are the methods to recognize. `lines` and `walk` return streams. Close them. They throw the checked `IOException`.

Console input and output use the same streams. `System.in` is an `InputStream`. `System.out` is a `PrintStream`, which is an `OutputStream`. A line from the console is `new BufferedReader(new InputStreamReader(System.in)).readLine()`. Do not close `System.in` or `System.out`. Closing either one closes the console for the rest of the program.

### `Words`

Create `notes.txt` in the working directory with one line, `Ada loves Java`. Then type this.

```java
import java.nio.file.*;

public class Words {
    public static void main(String[] args) throws Exception {
        Path in = Path.of("notes.txt");
        String text = Files.readString(in);
        int words = text.isBlank() ? 0 : text.trim().split("\\s+").length;
        Path report = Path.of("report.txt");
        Files.writeString(report, "words=" + words + System.lineSeparator());
        System.out.println(Files.readString(report).trim());
    }
}
```

The run prints:

```text
words=3
```

Monday’s questions are Q1–Q4.

## Chapter 1 questions

**Q1.** Which type reads characters rather than raw bytes?

A. `FileInputStream`
B. `BufferedReader`
C. `FileOutputStream`
D. `DataOutputStream`

**Q2.** `base` is `Path.of("docs", "notes", "week.txt")`. What does `base.resolve(Path.of("C:\\temp\\x.txt"))` point at, on Windows?

A. `docs\notes\week.txt\C:\temp\x.txt`
B. `C:\temp\x.txt`
C. `docs\temp\x.txt`
D. The code does not compile

**Q3.** What is `Path.of("a", "..", "b", ".", "c").normalize()` on Windows?

A. `a\..\b\.\c`
B. `b\c`
C. `a\b\c`
D. `c`

**Q4.** `notes.txt` contains `Ada loves Java`. What does `Words` print?

A. `words=2`
B. `words=3`
C. `words=14`
D. An exception is thrown because `writeString` needs try-with-resources

### Chapter 1 answers

**Q1 — B.** A `Reader` uses characters. The three `Stream` names in the other options use bytes. `InputStreamReader` is the bridge from bytes to characters.

**Q2 — B.** An absolute argument to `resolve` replaces the receiver. A relative argument would have been appended.

**Q3 — B.** `..` removes `a`. `.` is dropped. The remaining elements are `b` and `c`.

**Q4 — B.** `trim` removes the line ending, and `split("\\s+")` finds three words. `writeString` throws `IOException`, which `main` declares. It does not by itself require a try-with-resources.

---

# Chapter 2 — Serialization, locales, and bundles

> **必睇**　第 14 章 “Serializing Data”，pp. 848–855。第 11 章 p. 646（“Formatting Numbers”，貨幣同百分比）同 pp. 651–667（locale、resource bundle、`MessageFormat`）。
>
> **唔使睇**　日期 pattern（pp. 647–650）第 5 週已讀。書冇 logging 或 annotations 嘅獨立章。筆記本章尾嘅 recognition 段就係考試要認到嘅程度。

**Wednesday** is this chapter, `Bag`, and questions Q1–Q4.

## What you must know

A class implements `Serializable` so `ObjectOutputStream` can write it and `ObjectInputStream` can read it back. `serialVersionUID` is a `static final long`. If the class changes shape and the stored id does not match, reading throws `InvalidClassException`.

`transient` fields are not written. On the way back they receive the default for their type: `0`, `false`, or `null`. `static` fields are not part of one object’s saved state. Deserialization does not run the constructor.

### `Bag`

```java
import java.io.*;

class Bag implements Serializable {
    static int constructed;
    int n = 1;
    transient int t = 2;
    Bag() { constructed++; }
}
public class BagLab {
    public static void main(String[] args) throws Exception {
        Bag bag = new Bag();
        bag.n = 7;
        bag.t = 9;
        var raw = new ByteArrayOutputStream();
        try (var out = new ObjectOutputStream(raw)) {
            out.writeObject(bag);
        }
        try (var in = new ObjectInputStream(new ByteArrayInputStream(raw.toByteArray()))) {
            Bag back = (Bag) in.readObject();
            System.out.println(back.n + " " + back.t + " " + Bag.constructed);
        }
    }
}
```

The run prints:

```text
7 0 1
```

`n` was saved. `t` came back as the default `0`. The constructor ran once, for the original `new Bag()`, and not again while reading.

### Locales and bundles

A `Locale` is a language, and optionally a country. `Locale.US` and `Locale.forLanguageTag("fr-FR")` are the two you need this week.

`NumberFormat.getCurrencyInstance(Locale.US).format(1.5)` prints `$1.50`. A French locale uses a comma as the decimal mark and the euro sign. `NumberFormat.getPercentInstance(Locale.US).format(0.25)` prints `25%`, because the percent formatter multiplies by 100. `DateTimeFormatter.ofLocalizedDate(FormatStyle.SHORT).withLocale(Locale.US)` prints `12/21/26` for 21 December 2026.

`ResourceBundle.getBundle("messages", Locale.FRANCE).getString("hello")` is the call that walks the search list below. `MessageFormat.format("Hello {0}", "Ada")` replaces `{0}` and returns `Hello Ada`. `{1}` is the second argument. `MessageFormat.format("Hello {1}", "Ada")` has no argument at index 1, so the result stays `Hello {1}`. Write one argument per index you use.

A resource bundle is a set of property files. For `Locale.FRANCE` and the base name `messages`, the search order on the checklist is:

1. `messages_fr_FR`
2. `messages_fr`
3. `messages`

If the key is still missing, Java repeats that idea for the default locale. If the base bundle is missing too, `getBundle` throws `MissingResourceException`. A key found in a parent file is used when the more specific file does not define it.

Put `messages.properties` (`hello=Hello`) and `messages_fr.properties` (`hello=Bonjour`) on the classpath and print both locales. That is the two-locale checklist item.

### Recognition only

`@Override` checks an override. `@FunctionalInterface` checks that an interface has one abstract method. `@Deprecated` marks an element you should stop using. `@SuppressWarnings` silences a named warning. You will see these in snippets. You do not need to declare your own annotation type.

`System.Logger` and `java.util.logging` are the logging names on the exam. A logger has levels. You log a level and a message. You do not configure a logging framework this week.

Wednesday’s questions are Q1–Q4.

## Chapter 2 questions

**Q1.** After the round trip in `BagLab`, what are `n`, `t`, and `constructed`?

A. `7 9 1`
B. `7 0 1`
C. `7 0 2`
D. `1 2 1`

**Q2.** What does `transient` do?

A. It saves the field first
B. It skips the field, and the restored field gets the type’s default
C. It makes the field `static`
D. It encrypts the field

**Q3.** What does `NumberFormat.getCurrencyInstance(Locale.US).format(1.5)` print?

A. `1.50`
B. `$1.50`
C. `1,50 €`
D. `USD 1.5`

**Q4.** `messages_fr.properties` defines `hello`, and `messages.properties` defines `hello` and `bye`. For `Locale.FRENCH`, which file supplies `bye`?

A. `messages_fr.properties` only, so the key is missing
B. `messages.properties`
C. `messages_fr_FR.properties`
D. The search starts at the base file

### Chapter 2 answers

**Q1 — B.** The ordinary field `n` is restored as `7`. The transient field `t` is restored as `0`. Deserialization does not run `Bag()`, so `constructed` stays `1`.

**Q2 — B.** `transient` leaves the field out of the byte stream. The default for an `int` is `0`.

**Q3 — B.** The US currency format includes the dollar sign and two decimal places. The symbol and the separators come from the locale.

**Q4 — B.** `Locale.FRENCH` searches `messages_fr` and then the base `messages`. `bye` is not in the French file, so the base file supplies it.

---

# Chapter 3 — Modules

> **必睇**　第 12 章 Modules，pp. 684–718（由介紹到 `jlink`）同 pp. 724–734（module 種類同 migration）。
>
> **唔使睇**　`jpackage`（p. 719）。Review Questions 唔使做。

**Friday** is this chapter. Compile it in a terminal. Questions Q1–Q4 come after the broken export.

## What you must know

A module is a named group of packages, described by `module-info.java` in the module root.

- `requires other` reads that module.
- `exports pkg` makes that package visible to modules that read this one.
- `provides com.example.api.Speaker with com.example.hello.HelloSpeaker` offers a service.
- `uses com.example.api.Speaker` means this module loads that service.

A package that is not exported is not visible, even when the other module `requires` you.

Create this tree under a folder named `mods`.

`mods/com.example.api/module-info.java`

```java
module com.example.api {
    exports com.example.api;
}
```

`mods/com.example.api/com/example/api/Speaker.java`

```java
package com.example.api;
public interface Speaker {
    String speak();
}
```

`mods/com.example.hello/module-info.java`

```java
module com.example.hello {
    requires com.example.api;
    provides com.example.api.Speaker with com.example.hello.HelloSpeaker;
}
```

`mods/com.example.hello/com/example/hello/HelloSpeaker.java`

```java
package com.example.hello;
import com.example.api.Speaker;
public class HelloSpeaker implements Speaker {
    public String speak() { return "hello"; }
}
```

`mods/com.example.app/module-info.java`

```java
module com.example.app {
    requires com.example.api;
    uses com.example.api.Speaker;
}
```

`mods/com.example.app/com/example/app/Main.java`

```java
package com.example.app;
import com.example.api.Speaker;
import java.util.ServiceLoader;
public class Main {
    public static void main(String[] args) {
        ServiceLoader.load(Speaker.class).forEach(s -> System.out.println(s.speak()));
    }
}
```

From the folder that contains `mods`:

```text
javac -d out --module-source-path mods mods\com.example.api\module-info.java mods\com.example.api\com\example\api\Speaker.java mods\com.example.hello\module-info.java mods\com.example.hello\com\example\hello\HelloSpeaker.java mods\com.example.app\module-info.java mods\com.example.app\com\example\app\Main.java
java -p out -m com.example.app/com.example.app.Main
```

The run prints:

```text
hello
```

`-p` is the module path. `-m` is the module and the main class.

Break it once. Remove `exports com.example.api;` and compile an app that imports `Speaker`. Save this error in the notebook:

```text
package com.example.api is not visible
(package com.example.api is declared in module com.example.api, which does not export it)
```

The hidden-package drill in the checklist uses the same message. Put the package you actually hid into that sentence.

## Migration, jars, and a runtime image

`exports` makes the public types of a package usable by other modules. `opens` allows reflective access, including `setAccessible` on members that are not public. `exports` alone does not grant that reflection. `exports com.example.hello to com.example.app` and `opens com.example.hello to com.example.app` limit the right to one named module.

`requires transitive com.example.util` means a module that `requires` yours also reads `com.example.util`. That caller can use `com.example.util`’s exported types without writing its own `requires`. A plain `requires` does not pass the dependency on.

A JAR with no `module-info` that you put on the classpath belongs to the unnamed module. The unnamed module reads every resolved module, and all of its packages are open. A named module cannot `requires` the unnamed module.

The same JAR placed on the module path is an automatic module. Its name comes from the JAR file name, unless the manifest sets `Automatic-Module-Name`. An automatic module exports and opens every package, and it reads every other resolved module, including the unnamed module.

`jar --create --file app.jar -C out .` builds a non-modular jar when `out` has no `module-info.class`. Run it with `java -cp app.jar com.example.app.Main`. A jar that contains `module-info.class` is a modular jar. Run it with `java -p app.jar -m com.example.app/com.example.app.Main`.

`jlink` builds a runtime image with only the modules you name and the modules they need. The module path includes the JDK’s `jmods` folder, because that is where `java.base` lives.

```text
jlink --module-path "%JAVA_HOME%\jmods;out" --add-modules com.example.app --output image
```

The program is then `image\bin\java -m com.example.app/com.example.app.Main`.

Friday’s questions are Q1–Q4.

## Chapter 3 questions

**Q1.** Which directive lets another module read a package?

A. `requires`
B. `exports`
C. `uses`
D. `opens` is required for every read

**Q2.** The app module calls `ServiceLoader.load(Speaker.class)`. Which pair belongs in the module descriptors?

A. The provider `uses` the service, and the app `provides` it
B. The provider `provides ... with ...`, and the app `uses` the service
C. Both modules `exports` the service class
D. `requires` alone publishes the service

**Q3.** What does `java -p out -m com.example.app/com.example.app.Main` do?

A. It compiles the module
B. It runs `Main` using the modules in `out`
C. It exports every package
D. It ignores `module-info.java`

**Q4.** A module `requires` another module, and the package it imports is not exported. What is the compile error about?

A. A missing `main`
B. A cycle of `requires`
C. The package is not visible, because the module does not export it
D. `ServiceLoader` cannot see a class

### Chapter 3 answers

**Q1 — B.** `exports` makes a package visible to readers. `requires` is how a module reads another module. Both are needed for a normal call across modules. `opens` is reflective access, not a substitute for `exports`.

**Q2 — B.** The provider module says `provides Interface with Implementation`. The consumer says `uses Interface`. The consumer does not `require` the provider module by name.

**Q3 — B.** `-p out` is the module path. `-m` names the module and the class. The matching compile command is `javac -d out --module-source-path mods`.

**Q4 — C.** `requires` does not export packages. The compiler reports that the package is not visible and names the module that failed to export it.

---

# Chapter 4 — Threads

> **必睇**　第 13 章 Concurrency，pp. 746–785：threads、virtual threads、executors、`Lock`、`CyclicBarrier`、concurrent collections、race。
>
> **唔使睇**　“Working with Parallel Streams”（pp. 786–794）第 7 週讀過就跳過。Review Questions 唔使做。

**Saturday** is 8 hours: this chapter, `Race`, and questions Q1–Q4.

## What you must know

A thread’s states are `NEW`, `RUNNABLE`, `BLOCKED`, `WAITING`, `TIMED_WAITING`, and `TERMINATED`. `BLOCKED` means it is waiting to enter a `synchronized` block. `WAITING` is a wait with no timeout, such as `join()` or `Object.wait()`. `TIMED_WAITING` is `sleep`, `wait(millis)`, or `join(millis)`.

`Runnable.run` returns void and cannot throw a checked exception. `Callable.call` returns a value and can throw `Exception`.

`thread.start()` schedules the thread. `thread.run()`, or calling `run` on the `Runnable` yourself, executes the body on the current thread and does not schedule a new one. Calling `start` twice throws `IllegalThreadStateException`.

`ExecutorService` runs tasks. `Executors.newFixedThreadPool(1)` reuses one platform thread. `Executors.newVirtualThreadPerTaskExecutor()` starts a virtual thread per task. `Future.get` blocks until the task finishes and returns its value. `shutdown` rejects new tasks and lets the current tasks finish. `shutdownNow` interrupts running tasks and returns the tasks that had not started.

A plain `int` updated from two threads can lose increments. The two reads can see the same number and both write that number plus one. `AtomicInteger.incrementAndGet` and a `synchronized` block do not lose those updates.

`synchronized` releases the monitor when the block ends, including when the block throws. A `ReentrantLock` does not. Call `lock()` and put `unlock()` in a `finally` block. The same thread may lock it again. Each `lock` needs its own `unlock`.

`ConcurrentHashMap` is a map that concurrent tasks may update. It rejects a `null` key and a `null` value. `HashMap` accepts one `null` key and does not survive concurrent updates.

`list.parallelStream()` is the parallel stream from Week 7. A sum of the elements matches the sequential sum. `forEach` may run in any order.

`Thread.ofVirtual().start(...)` and `Thread.startVirtualThread(...)` create virtual threads. Do not build a pool of virtual threads by hand. The per-task executor is the tool from the checklist.

### `Race`

The atomic counter is the one to trust. Two virtual threads each increment 1000 times.

```java
import java.util.concurrent.atomic.AtomicInteger;

public class Race {
    public static void main(String[] args) throws Exception {
        AtomicInteger atom = new AtomicInteger();
        Thread a = Thread.startVirtualThread(() -> {
            for (int i = 0; i < 1000; i++) atom.incrementAndGet();
        });
        Thread b = Thread.startVirtualThread(() -> {
            for (int i = 0; i < 1000; i++) atom.incrementAndGet();
        });
        a.join();
        b.join();
        System.out.println(atom.get());
    }
}
```

The run prints:

```text
2000
```

For the broken counter, repeat the same loops on a shared `int` with `count = count + 1` and no lock. Run it several times. Some totals are below 2000. That is the lost update. Then wrap the increment in `synchronized (lock)` and the total is 2000 again.

A fixed pool of one thread, given `Callable<String>` that returns `"ok"`, prints `ok` from `future.get()`, and `shutdown()` lets that task finish.

Saturday’s questions are Q1–Q4.

## Chapter 4 questions

**Q1.** What does calling `run()` on a `Runnable` do?

A. It schedules a new thread
B. It runs the body on the current thread
C. It moves a thread from `NEW` to `TERMINATED` without running the body
D. It throws `IllegalThreadStateException`

**Q2.** What does `Future.get` do when the task is still running?

A. It returns `null` immediately
B. It blocks until the task finishes
C. It cancels the task
D. It throws `IllegalStateException` immediately

**Q3.** Which pair matches the methods?

A. `shutdown` interrupts running tasks. `shutdownNow` only rejects new ones
B. `shutdown` rejects new tasks and lets current tasks finish. `shutdownNow` interrupts running tasks
C. Both wait forever for new tasks
D. Both are illegal on a virtual-thread executor

**Q4.** Two threads each run `count = count + 1` a thousand times on a shared `int`, with no lock. Which statement is true?

A. The total is always 2000
B. The total can be below 2000
C. The code does not compile
D. The total is always 1000

### Chapter 4 answers

**Q1 — B.** `run` is an ordinary method call. `start` is the call that schedules a thread. A second `start` on the same `Thread` throws `IllegalThreadStateException`.

**Q2 — B.** `get` waits for the result. A task that throws delivers that failure as `ExecutionException` from `get`.

**Q3 — B.** `shutdown` is the orderly stop. `shutdownNow` tries to stop work that is already running and hands back the queue of tasks that had not started.

**Q4 — B.** Both threads can read the same `count` and write the same next number. One update is lost. `AtomicInteger.incrementAndGet` for the same two loops of 1000 ends at 2000.

---

# Sunday — mixed quiz, then the syllabus closes

> **唔使睇**　混合測驗用筆記計分。由今日起書變成參考，唔使再逐章重讀。

The first 20 minutes are Saturday’s misses. Then this set. Score Chapter 1 (4), Chapter 2 (4), Chapter 3 (4), Chapter 4 (4), and the mixed set (4). **13 or more** of the 20 questions is the gate.

Write your three weakest topics at the top of the notebook. The book is now a reference. Week 9 starts from that list.

## Mixed set

**M1.** `Path.of("docs", "notes").relativize(Path.of("docs", "code", "A.java"))` on Windows is which path?

A. `docs\code\A.java`
B. `..\code\A.java`
C. `notes\code\A.java`
D. `code\A.java`

**M2.** What is `serialVersionUID` for?

A. It saves `transient` fields
B. It names the class shape. A mismatch with the stream throws `InvalidClassException`
C. It locks the object during `readObject`
D. It replaces `Serializable`

**M3.** `provides` and `uses` are in place, and `java -p out -m com.example.app/com.example.app.Main` runs. What does the service `Main` in this chapter print?

A. nothing
B. `hello`
C. the module name
D. An exception, because the app did not `require` the provider module

**M4.** Which state means a thread is in `Thread.sleep`?

A. `NEW`
B. `BLOCKED`
C. `TIMED_WAITING`
D. `TERMINATED`

### Mixed answers

**M1 — B.** `relativize` is the step from `docs\notes` up to `docs` and then down into `docs\code`. The print is `..\code\A.java`.

**M2 — B.** `serialVersionUID` identifies the class shape. Reading a stream whose id does not match the class throws `InvalidClassException`.

**M3 — B.** `ServiceLoader` finds `HelloSpeaker` because the provider is on the module path and the app module `uses` the service. The app does not `require` the provider by name. The print is `hello`.

**M4 — C.** `sleep` is a timed wait. `BLOCKED` is the state for waiting on a monitor. `NEW` is before `start`. `TERMINATED` is after the body has finished.

---

# Rules to copy onto one card

- Byte streams use `InputStream` and `OutputStream`. Character streams use `Reader` and `Writer`. Close the outer wrapper. Do not close `System.in` or `System.out`.
- `resolve` appends a relative path and replaces with an absolute path. `relativize` is the path from one location to another. `normalize` drops `.` and applies `..`.
- `transient` is not saved and comes back as the default. Deserialization does not run the constructor. `serialVersionUID` names the class shape.
- Bundle search for a locale is the full locale, then the language, then the base file. Currency and short dates follow the locale. Percent format multiplies by 100. `MessageFormat` replaces `{0}`.
- `exports` makes a package visible. `opens` allows reflection. `requires transitive` passes a read on. `provides ... with ...` and `uses` publish and load a service. A missing `exports` makes the package not visible.
- Classpath code is the unnamed module. A JAR with no `module-info` on the module path is an automatic module. `jlink` builds a runtime image.
- `start` schedules a thread. `run` does not. `Future.get` blocks. `shutdown` finishes current work. `shutdownNow` interrupts it.
- A shared `int` increment can lose updates. `AtomicInteger` or `synchronized` keeps them. `ReentrantLock` needs `unlock` in `finally`. `ConcurrentHashMap` rejects null. Virtual threads are one per task, not a hand-built pool.
