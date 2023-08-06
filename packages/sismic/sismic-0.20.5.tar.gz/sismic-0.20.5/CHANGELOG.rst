Changelog
=========

0.20.5 (2016-04-14)
-------------------

- (Added) Type hinting (see PEP484 and mypy-lang project)

0.20.4 (2016-03-25)
-------------------

- (Changed) Statechart testers are now called property statechart.
- (Changed) Property statechart can describe *desirable* and *undesirable* properties.

0.20.3 (2016-03-22)
-------------------

- (Changed) Step *Event x should be fired* now checks sent events from the beginning of the test, not only for the last
  executed step.
- (Fixed) Internal events that are sequentially sent are now sequentially consumed (and not anymore in reverse order).


0.20.2 (2016-02-24)
-------------------

- (Fixed) ``interpreter.log_trace`` does not anymore log empty macro step.

0.20.1 (2016-02-19)
-------------------

- (Added) A *step ended* event at the end of each step in a tester story.
- (Changed) The name of the events and attributes that are exposed in a tester story has changed.
  Consult the documentation for more information.

0.20.0 (2016-02-17)
-------------------

- (Added) Module ``interpreter`` provides a ``log_trace`` function that takes an interpreter instance and returns
  a (dynamic) list of executed macro steps.
- (Added) Module ``testing`` exposes an ``ExecutionWatcher`` class that can be used to check statechart properties
  with tester statecharts at runtime.
- (Changed) ``Interpreter.__init__`` does not anymore stabilize the statechart. Stabilization is done during the
  first call of ``execute_once``.
- (Changed) ``Story.tell`` returns a list of ``MacroStep`` (the *trace*) instead of an ``Interpreter`` instance.
- (Changed) The name of some attributes of an event in a tester story changes (e.g. *event* becomes *consumed_event*,
  *state* becomes *entered_state* or *exited_state* or *source_state* or *target_state*).
- (Removed) ``Interpreter.trace``, as it can be easily obtained from ``execute_once`` or using ``log_trace``.
- (Removed) ``Interpreter.__init__`` does not accept an ``initial_time`` parameter.
- (Fixed) Parallel state without children does not any more result into an infinite loop.

0.19.0 (2016-02-10)
-------------------

- (Added) BDD can now output coverage data using ``--coverage`` command-line argument.
- (Changed) The YAML definition of a statechart must use *root state:* instead of *initial state:*.
- (Changed) When a contract is evaluated by a ``PythonEvaluator``, ``__old__.x`` raises an ``AttributeError`` instead
  of a ``KeyError`` if ``x`` does not exist.
- (Changed) Behave is now called from Python instead of using a subprocess and thus allows debugging.

0.18.1 (2016-02-03)
-------------------

- (Added) Support for behavior-driven-development using Behave.

0.17.3 (2016-01-29)
-------------------

- (Added) An ``io.text.export_to_tree`` that returns a textual representation of the states.
- (Changed) ``Statechart.rename_to`` does not anymore raise ``KeyError`` but ``exceptions.StatechartError``.
- (Changed) Wheel build should work on Windows

0.17.1 (2016-01-25)
-------------------

Many backward incompatible changes in this update, especially if you used to work with ``model``.
The YAML format of a statechart also changed, look carefully at the changelog and the documentation.

- (Added) YAML: an history state can declare *on entry* and *on exit*.
- (Added) Statechart: new methods to manipulate transitions: ``transitions_from``, ``transitions_to``,
  ``transitions_with``, ``remove_transition`` and ``rotate_transition``.
- (Added) Statechart: new methods to manipulate states: ``remove_state``, ``rename_state``, ``move_state``,
  ``state_for``, ``parent_for``, ``children_for``.
- (Added) Steps: ``__eq__`` for ``MacroStep`` and ``MicroStep``.
- (Added) Stories: ``tell_by_step`` method for a ``Story``.
- (Added) Testing: ``teststory_from_trace`` generates a *step* event at the beginning of each step.
- (Added) Module: a new exceptions hierarchy (see ``exceptions`` module).
  The new exceptions are used in place of the old ones (``Warning``, ``AssertionError`` and ``ValueError``).
- (Changed) YAML: uppermost *states:* should be replaced by *initial state:* and can contain at most one state.
- (Changed) YAML: uppermost *on entry:* should be replaced by *preamble:*.
- (Changed) YAML: initial memory of an history state should be specified using *memory* instead of *initial*.
- (Changed) YAML: contracts for a statechart must be declared on its root state.
- (Changed) Statechart: rename ``StateChart`` to ``Statechart``.
- (Changed) Statechart: rename ``events`` to ``events_for``.
- (Changed) Statechart: ``states`` attribute is now ``Statechart.state_for`` method.
- (Changed) Statechart: ``register_state`` is now ``add_state``.
- (Changed) Statechart: ``register_transition`` is now ``add_transition``.
- (Changed) Statechart: now defines a root state.
- (Changed) Statechart: checks done in ``validate``.
- (Changed) Transition: ``.event`` is a string instead of an ``Event`` instance.
- (Changed) Transition: attributes ``from_state`` and ``to_state`` are renamed into ``source`` and ``target``.
- (Changed) Event: ``__eq__`` takes ``data`` attribute into account.
- (Changed) Event: ``event.foo`` raises an ``AttributeError`` instead of a ``KeyError`` if ``foo`` is not defined.
- (Changed) State: ``StateMixin.name`` is now read-only (use ``Statechart.rename_state``).
- (Changed) State: split ``HistoryState`` into a mixin ``HistoryStateMixin`` and two concrete subclasses,
  namely ``ShallowHistoryState`` and ``DeepHistoryState``.
- (Changed) IO: Complete rewrite of ``io.import_from_yaml`` to load states before transitions. Parameter names have changed.
- (Changed) Module: adapt module hierarchy (no visible API change).
- (Changed) Module: expose module content through ``__all__``.
- (Removed) Transition: ``transitions`` attribute on ``TransitionStateMixin``, use ``Statechart.transitions_for`` instead.
- (Removed) State: ``CompositeStateMixin.children``, use ``Statechart.children_for`` instead.


0.16.0 (2016-01-15)
-------------------

- (Added) An ``InternalEvent`` subclass for ``model.Event``.
- (Added) ``Interpreter`` now exposes its ``statechart``.
- (Added) ``Statechart.validate`` checks that a targeted compound state declares an initial state.
- (Changed) ``Interpreter.queue`` does not accept anymore an ``internal`` parameter.
  Use an instance of ``InternalEvent`` instead (#20).
- (Fixed) ``Story.story_from_trace`` now ignores internal events (#19).
- (Fixed) Condition C3 in ``Statechart.validate``.

0.15.0 (2016-01-12)
-------------------

- (Changed) Rename ``Interpreter.send`` to ``Interpreter.queue`` (#18).
- (Changed) Rename ``evaluator`` module to ``code``.

0.14.3 (2016-01-12)
-------------------

- (Added) Changelog.
- (Fixed) Missing files in MANIFEST.in
