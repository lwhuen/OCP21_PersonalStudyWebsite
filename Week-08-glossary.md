# Week 8 glossary — I/O, modules, and threads

Terms from [Week-08-notes.md](Week-08-notes.md). The exam words are English.

## Monday — files and paths

| Term | Meaning |
|---|---|
| `InputStream` / `OutputStream` | Move bytes. |
| `Reader` / `Writer` | Move characters. `InputStreamReader` bridges a byte stream to a character stream. |
| `BufferedReader` | Wraps another reader so you can read lines. Close the outermost wrapper. |
| `Path` | A location. `Path.of` builds one. |
| `resolve` | A relative argument is appended. An absolute argument replaces the original path. |
| `relativize` | The path from the first location to the second. |
| `normalize` | Removes `.` and applies `..`. |
| `Files.readString` | Reads a whole file as one `String`. Throws the checked `IOException`. |
| `Files.writeString` | Writes a `String` to a file. Throws `IOException`. |
| `Files.lines` / `Files.walk` | Return streams. Close them, usually with try-with-resources. |
| `System.in` / `System.out` | Console byte streams. `System.in` is an `InputStream`. `System.out` is a `PrintStream`. Do not close either one. |

## Wednesday — serialization, locales, recognition

| Term | Meaning |
|---|---|
| `Serializable` | The marker interface that lets `ObjectOutputStream` write an object and `ObjectInputStream` read it back. |
| `serialVersionUID` | A `static final long` that names the class shape. A mismatch with the stream throws `InvalidClassException`. |
| `transient` | The field is not written. On the way back it receives the default: `0`, `false`, or `null`. |
| Deserialization | Restores the object without running its constructor. `static` fields are not part of one object’s saved state. |
| `Locale` | A language, and optionally a country. `Locale.US`. `Locale.forLanguageTag("fr-FR")`. |
| `NumberFormat` | Formats a number for a locale. The US currency format of `1.5` is `$1.50`. `getPercentInstance` multiplies by 100, so `0.25` in `Locale.US` is `25%`. |
| Resource bundle | A set of property files for one base name. `ResourceBundle.getBundle("messages", locale).getString("hello")`. For a French locale the search is `messages_fr_FR`, then `messages_fr`, then `messages`. A missing key can come from the parent file. |
| `MessageFormat` | Replaces `{0}`, `{1}`, and so on. `MessageFormat.format("Hello {0}", "Ada")` is `Hello Ada`. |
| `MissingResourceException` | Thrown when `getBundle` cannot find the base bundle. |
| `@Override` | Checks that a method really overrides. |
| `@FunctionalInterface` | Checks that an interface has one abstract method. |
| `@Deprecated` | Marks an element you should stop using. |
| `@SuppressWarnings` | Silences a named warning. |
| Logger | `System.Logger` or `java.util.logging`. A call records a level and a message. Recognition level only this week. |

## Friday — modules

| Term | Meaning |
|---|---|
| Module | A named group of packages, described by `module-info.java`. |
| `requires` | This module reads another module. |
| `exports` | Makes a package visible to modules that read this one. A package that is not exported is not visible. |
| `provides ... with ...` | This module offers a service implementation. |
| `uses` | This module loads that service with `ServiceLoader`. The consumer does not `require` the provider by name. |
| Module path | The directories or jars given to `-p`. |
| `-m` | The module and the main class, as in `com.example.app/com.example.app.Main`. |
| Not visible | The compiler error when code imports a package that its required module does not export. |
| `opens` | Allows reflective access to a package. `exports` does not grant `setAccessible`. |
| `requires transitive` | A module that reads yours also reads that dependency. |
| Unnamed module | All code on the classpath. It reads every resolved module. A named module cannot `requires` it. |
| Automatic module | A JAR with no `module-info` on the module path. It exports and opens every package. The name comes from the JAR file name, or from `Automatic-Module-Name` in the manifest. |
| Modular jar | A jar that contains `module-info.class`. Run it with `-p` and `-m`. |
| `jlink` | Builds a runtime image that contains the modules you name and the modules they need. |

## Saturday — threads

| Term | Meaning |
|---|---|
| `NEW` | A `Thread` that has not been started. |
| `RUNNABLE` | Eligible to run, or running. |
| `BLOCKED` | Waiting to enter a `synchronized` block. |
| `WAITING` | Waiting with no timeout, such as `join()` or `Object.wait()`. |
| `TIMED_WAITING` | `sleep`, `wait(millis)`, or `join(millis)`. |
| `TERMINATED` | The body has finished. |
| `Runnable` | `void run()`. Cannot throw a checked exception. |
| `Callable` | `call` returns a value and can throw `Exception`. |
| `start` | Schedules the thread. Calling it twice throws `IllegalThreadStateException`. |
| `run` | An ordinary call. The body runs on the current thread. It does not schedule a new thread. |
| `ExecutorService` | Runs tasks. `newFixedThreadPool` reuses platform threads. `newVirtualThreadPerTaskExecutor` starts a virtual thread per task. |
| `Future.get` | Blocks until the task finishes and returns its value. A task that throws is delivered as `ExecutionException`. |
| `shutdown` | Rejects new tasks and lets current tasks finish. |
| `shutdownNow` | Interrupts running tasks and returns the tasks that had not started. |
| Lost update | Two threads read the same `int` and both write that number plus one. One increment disappears. |
| `AtomicInteger` | `incrementAndGet` updates the number without a lost update. A `synchronized` block can do the same. |
| Virtual thread | A lightweight thread. Start one with `Thread.ofVirtual().start` or `Thread.startVirtualThread`. Do not build a pool of them by hand. |
| `ReentrantLock` | `lock()`, then `unlock()` in a `finally` block. Unlike `synchronized`, leaving the block does not unlock it. The same thread may lock it again, and each `lock` needs an `unlock`. |
| `ConcurrentHashMap` | A map that concurrent tasks may update. A `null` key or a `null` value throws `NullPointerException`. |
| `parallelStream` | A parallel stream of a collection. An associative sum matches the sequential sum. `forEach` may run in any order. |
