// import Divmod.Defer
// import Divmod.UnitTest
// import Nevow.Test.WidgetUtil
// import Methanal.View
// import Methanal.Util
// import Methanal.Tests.Util
// import Methanal.Tests.MockBrowser



/**
 * L{Methanal.View.LiveForm} mock implementation.
 */
Methanal.View.LiveForm.subclass(
    Methanal.Tests.TestView, 'MockLiveForm').methods(
    function __init__(self, controlNames, args/*=undefined*/) {
        args = args || {};
        var node = Nevow.Test.WidgetUtil.makeWidgetNode();
        Methanal.Tests.TestView.MockLiveForm.upcall(
            self, '__init__', node, args, controlNames);
        Methanal.Tests.Util.setUpForm(self);
    });



/**
 * Create a control container.
 *
 * @type  widgetParent: C{Nevow.Athena.Widget}
 * @param widgetParent: Container parent widget.
 *
 * @param containerType: Container type constructor.
 *
 * @type  children: C{Array} of C{Nevow.Athena.Widget}
 * @param children: Controls to add as children of the container.
 *
 * @return: A control container of type C{containerType} with C{children} as
 *     child controls.
 */
Methanal.Tests.TestView.createContainer = function createContainer(
    widgetParent, containerType, children) {
    var container = containerType(
        Nevow.Test.WidgetUtil.makeWidgetNode());
    Methanal.Tests.Util.makeWidgetChildNode(
        container, 'span', 'error-text');

    for (var i = 0; i < children.length; ++i) {
        var child = children[i];
        container.addChildWidget(child);
        container.node.appendChild(child.node);
    }

    widgetParent.addChildWidget(container);

    return container;
};



/**
 * Tests for L{Methanal.View.LiveForm}.
 */
Methanal.Tests.Util.TestCase.subclass(
    Methanal.Tests.TestView, 'TestLiveForm').methods(
    /**
     * Create a C{Methanal.View.LiveForm}.
     */
    function createForm(self, args, controls/*=undefined*/,
                        postFormInsertion/*=undefined*/) {
        controls = controls || [];
        var controlNames = [];
        for (var i = 0; i < controls.length; ++i) {
            controlNames.push(controls[i].name);
        }

        var form = Methanal.Tests.TestView.MockLiveForm(controlNames, args);
        Methanal.Tests.Util.setUpForm(form);
        Methanal.Util.nodeInserted(form);
        if (postFormInsertion) {
            postFormInsertion(form);
        }
        for (var i = 0; i < controls.length; ++i) {
            var control = controls[i];
            form.addChildWidget(control);
            form.loadedUp(control);
        }
        return form;
    },


    /**
     * Create an input.
     */
    function createControl(self, args) {
        var node = Nevow.Test.WidgetUtil.makeWidgetNode();
        var control = Methanal.View.TextInput(node, args);
        node.appendChild(document.createElement('input'));
        Methanal.Tests.Util.makeWidgetChildNode(control, 'span', 'error');
        Methanal.Tests.Util.makeWidgetChildNode(
            control, 'span', 'displayValue');
        return control;
    },


    /**
     * Freezing and thawing the form increments and decrements the frozen
     * counter. Attempting to thaw a form without a freeze call results in
     * an exception.
     */
    function test_freezeThaw(self) {
        var control = self.createControl({'name': 'a'});
        var args = {
            'viewOnly': false};
        var form = self.createForm(args, [control]);
        form.freeze();
        self.assertIdentical(form._frozen, 1);
        form.freeze();
        self.assertIdentical(form._frozen, 2);
        form.thaw();
        form.thaw();
        self.assertIdentical(form._frozen, 0);
        self.assertThrows(Methanal.View.FreezeThawMismatch,
            function() {
                form.thaw();
            });
    },


    /**
     * Setting the form valid / invalid enables / disables the actions.
     */
    function test_validInvalid(self) {
        var args = {
            'viewOnly': false};
        var form = self.createForm(args);
        form.setValid();
        self.assertIdentical(form.valid, true);
        self.assertIdentical(form.actions._disabled, false);
        form.setInvalid();
        self.assertIdentical(form.valid, false);
        self.assertIdentical(form.actions._disabled, true);
    },


    /**
     * Submitting a form calls L{Methanal.View.LiveForm.submitSuccess} upon
     * successful submission and L{Methanal.View.LiveForm.submitFailure} upon
     * a failed submission.
     */
    function test_submission(self) {
        var success;
        var control = self.createControl({'name': 'a'});
        var args = {
            'viewOnly': false};
        var form = self.createForm(args, [control]);

        function succeed(methodName, data) {
            self.assertIdentical(form.actions._disabled, true);
            return Divmod.Defer.succeed(data);
        }

        function fail(methodName, data) {
            self.assertIdentical(form.actions._disabled, true);
            return Divmod.Defer.fail('too bad');
        }

        form.callRemote = succeed;
        form.formModified(true);
        self.assertIdentical(form.modified, true);
        form.submit();
        self.assertIdentical(form.modified, false);
        self.assertIdentical(form.actions._disabled, false);

        form.callRemote = fail;
        form.formModified(true);
        self.assertIdentical(form.modified, true);
        form.submit();
        // An unsuccessful submission will not remove the modified indicator.
        self.assertIdentical(form.modified, true);
        self.assertIdentical(form.actions._disabled, false);
    },


    /**
     * Visit all C{FormRow}s in C{widgetParent} and return an C{Array} of all
     * active rows.
     */
    function gatherActiveRows(self, widgetParent, fn) {
        var rows = [];
        Methanal.View.visitRows(widgetParent, function (row) {
            if (fn !== undefined) {
                fn(row);
            }
            if (row.active) {
                rows.push(row);
            }
        });
        return rows;
    },


    /**
     * L{Methanal.View.visitRows} recursively visits L{Methanal.View.FormRow}
     * widgets and applies a function to every C{FormRow}.
     */
    function test_visitRows(self) {
        function createRows(widgetParent, n) {
            var rows = [];
            for (var i = 0; i < n; ++i) {
                var row = Methanal.Tests.TestView.createContainer(
                    widgetParent, Methanal.View.FormRow, []);
                rows.push(row);
            }
            return rows;
        }

        var form = self.createForm();
        var rows = createRows(form, 3);
        self.assertArraysEqual(self.gatherActiveRows(form), rows);

        var group = Methanal.Tests.TestView.createContainer(
            form, Methanal.View.InputContainer, []);
        var innerRows = createRows(group, 3);
        self.assertArraysEqual(self.gatherActiveRows(group), innerRows);

        // The form contains all descendent FormRows.
        self.assertArraysEqual(
            self.gatherActiveRows(form),
            rows.concat(innerRows));

        function frob(row) {
            row.frobbed = true;
        }

        form = self.createForm();
        rows = createRows(form, 3);
        rows[1].active = false;
        var gathered = self.gatherActiveRows(form, frob);
        // gatherActiveRows only gathers active rows.
        self.assertArraysEqual(
            gathered,
            [rows[0], rows[2]]);

        // gatherActiveRows applies fn to every row, regardless of its active state.
        for (var i = 0; i < rows.length; ++i) {
            self.assertIdentical(rows[i].frobbed, true);
        }
    },


    /**
     * L{Methanal.View.LiveForm.valueChanged} calls
     * L{Methanal.View.LiveForm.formModified} to indicate that the form's
     * modification state changed.
     */
    function test_formModified(self) {
        var control = self.createControl({'name': 'a'});
        var args = {
            'viewOnly': false,
            'submitted': true};
        var form = self.createForm(args, [control]);
        var containsElementClass = Methanal.Util.containsElementClass;
        self.assertIdentical(form.modified, false);
        control.onChange();
        self.assertIdentical(form.modified, true);
    },


    /**
     * Callback fired once when the form has fully and finally loaded.
     */
    function test_formLoaded(self) {
        var success = false;
        var control = self.createControl({'name': 'a'});
        var args = {
            'viewOnly': false,
            'submitted': true};
        var form = self.createForm(args, [control], function (form) {
            self.assertIdentical(
                success,
                false);

            form.formLoaded = function () {
                success = true;
            };
        });

        self.assertIdentical(
            success,
            true);
    });



/**
 * Base class for L{Methanal.View.FormInput} mock implementations.
 */
Methanal.Tests.Util.TestCase.subclass(
    Methanal.Tests.TestView, 'FormInputTestCase').methods(
    /**
     * Create the mock Methanal control.
     *
     * @param args: Mapping of argument names to values, C{name} and C{label}
     *     are required
     *
     * @rtype: L{Methanal.View.FormInput}
     */
    function createControl(self, args) {
        throw new Error('Subclasses must implement "createControl".');
    },


    /**
     * Create the control container.
     */
    function createContainer(self, widgetParent, child) {
        return Methanal.Tests.TestView.createContainer(
            widgetParent,
            Methanal.View.FormRow,
            [child]);
    },


    /**
     * Perform tests on an C{Array} of controls.
     *
     * Once the tests have completed (successfully or not) the controls are
     * removed from the document and forgotten about.
     *
     * @type  controls: C{Array} of L{Methanal.View.FormInput}
     *
     * @type  testingFunc: C{function} taking an C{Array} of
     *     L{Methana.View.FormInput}
     */
    function testControls(self, controls, testingFunc) {
        var map = Methanal.Util.map;

        var controlNames = [];
        map(function (control) {
            controlNames.push(control.name);
        }, controls);

        var form = Methanal.Tests.TestView.MockLiveForm(controlNames);
        var containers = [];
        map(function (control) {
            var container = self.createContainer(form, control);
            document.body.appendChild(container.node);
            containers.push(container);
        }, controls);
        Methanal.Util.nodeInserted(form);

        try {
            testingFunc(controls);
        } finally {
            map(function (container) {
                form.removeChildWidget(container);
                document.body.removeChild(container.node);
            }, containers);
        }
    },


    /**
     * Create a new control and perform some tests on it.
     *
     * Once the tests have completed (successfully or not) the control is
     * removed from the document and forgotten about.
     *
     * @param args: Control argument mapping, if C{name}, C{label} or C{value}
     *     are not provided, suitable defaults will be chosen
     *
     * @type  testingFunc: C{function} taking L{Methana.View.FormInput}
     * @param testingFunc: Function called with the control once it has been
     *     initialised and its node inserted
     */
    function testControl(self, args, testingFunc) {
        function defaultArg(name, value) {
            if (args[name] === undefined || args[name] === null) {
                args[name] = value;
            }
        }

        args = args || {};
        defaultArg('name', 'methanalControl');
        defaultArg('label', 'a_label');
        defaultArg('value', null);

        var control = self.createControl(args);
        self.testControls([control], function (controls) {
            testingFunc(controls[0]);
        });
    },


    /**
     * Assert that C{value} is valid input for C{control}.
     *
     * Set the input node's value to C{value} and passes the result of
     * C{control.getValue} to C{control.baseValidator}.
     */
    function assertValidInput(self, control, value, msg) {
        control.inputNode.value = value;
        if (msg === undefined) {
            msg = (Methanal.Util.repr(value) + ' is NOT valid input for ' +
                Methanal.Util.repr(control));
        }
        self.assertIdentical(
            control.baseValidator(control.getValue()), undefined, msg);
    },


    /**
     * Assert that C{value} is not valid input for C{control}.
     *
     * Set the input node's value to C{value} and passes the result of
     * C{control.getValue} to C{control.baseValidator}.
     */
    function assertInvalidInput(self, control, value) {
        var oldValue = control.inputNode.value;
        control.inputNode.value = value;
        var msg = (Methanal.Util.repr(value) + ' IS valid input for ' +
            Methanal.Util.repr(control));
        self.assertNotIdentical(
            control.baseValidator(control.getValue()), undefined, msg);
        control.inputNode.value = oldValue;
    });



/**
 * Tests for L{Methanal.View.SelectInput}.
 */
Methanal.Tests.TestView.FormInputTestCase.subclass(
    Methanal.Tests.TestView, 'TestSelectInput').methods(
    function setUp(self) {
        self.controlType = Methanal.View.SelectInput;
    },


    function createControl(self, args) {
        var node = Nevow.Test.WidgetUtil.makeWidgetNode();
        var control = self.controlType(node, args);
        node.appendChild(document.createElement('select'));
        Methanal.Tests.Util.makeWidgetChildNode(control, 'span', 'error');
        return control;
    },


    /**
     * Assert than an "option" DOM node has specific values.
     */
    function assertOption(self, optionNode, value, description) {
        self.assertIdentical(optionNode.tagName, 'OPTION');
        self.assertIdentical(optionNode.value, value);
        self.assertIdentical(optionNode.text, description);
    },


    /**
     * L{Methanal.View.SelectInput._createOption} creates an "option" node.
     */
    function test_createOption(self) {
        self.testControl({},
            function (control) {
                self.assertOption(
                    control._createOption('value', 'desc'),
                    'value', 'desc');
            });
    },


    /**
     * L{Methanal.View.SelectInput.setValue} creates a placeholder when given
     * a C{null} value, create no placeholder when given an empty value, and
     * sets the input node's C{value} attribute to the given value when one
     * is given.
     */
    function test_setValue(self) {
        self.testControl({value: null, label: 'placeholder'},
            function (control) {
                self.assertIdentical(control.inputNode.options.length, 1);
                self.assertOption(
                    control.inputNode.options[0], '', 'placeholder');
            });

        self.testControl({value: ''},
            function (control) {
                self.assertIdentical(control.inputNode.options.length, 0);
            });

        self.testControl({value: ''},
            function (control) {
                control.append('v1', 'd1');
                self.assertIdentical(control.inputNode.options.length, 1);
                self.assertIdentical(control.inputNode.value, '');
                control.setValue('v1');
                self.assertIdentical(control.inputNode.value, 'v1');

                control.append(1, 'd2');
                control.setValue('1');
                self.assertIdentical(control.inputNode.value, '1');
                // Coerce values of select inputs and options.
                control.setValue(1);
                self.assertIdentical(control.inputNode.value, '1');
            });
    },


    /**
     * L{Methanal.View.SelectInput.getValue} returns the input node's C{value}
     * attribute or C{null} when the attribute is C{null} or empty.
     */
    function test_getValue(self) {
        self.testControl({value: ''},
            function (control) {
                self.assertIdentical(control.getValue(), null);
            });

        self.testControl({value: null},
            function (control) {
                self.assertIdentical(control.getValue(), null);
            });

        self.testControl({value: ''},
            function (control) {
                control.append('v1', 'd1');
                control.inputNode.value = 'v1';
                self.assertIdentical(control.getValue(), 'v1');
            });
    },


    /**
     * Appending and inserting values into a select.
     */
    function _testAppendInsert(self, control) {
        control.append('v1', 'd1');
        self.assertIdentical(control.inputNode.options.length, 1);
        self.assertOption(control.inputNode.options[0], 'v1', 'd1');
        // Insert it as the first option.
        control.insert('v2', 'd2', control.inputNode.options[0]);
        self.assertIdentical(control.inputNode.options.length, 2);
        self.assertOption(control.inputNode.options[0], 'v2', 'd2');
    },


    /**
     * L{Methanal.View.SelectInput.append} and
     * L{Methanal.View.SelectInput.insert} modify the input node's options
     * collection.
     */
    function test_appendInsert(self) {
        self.testControl({value: ''},
            function (control) {
                self._testAppendInsert(control);
            });
    },


    /**
     * Remove all options of this input.
     */
    function test_clear(self) {
        self.testControl({value: ''},
            function (control) {
                control.append('v1', 'd1');
                self.assertIdentical(control.inputNode.options.length, 1);
                self.assertOption(control.inputNode.options[0], 'v1', 'd1');

                control.clear();
                self.assertIdentical(control.inputNode.options.length, 0);
            });
    },


    /**
     * L{Methanal.View.SelectInput.insert} still works even when faced with
     * a broken implementation like Internet Explorer's.
     */
    function test_appendInsertInIE(self) {
        self.testControl({value: ''},
            function (control) {
                var originalType = document.registerElementTag(
                    'select', Methanal.Tests.TestView.MockIEHTMLSelectElement);
                try {
                    control.inputNode = document.createElement('select');
                    self.assertIsInstanceOf(control.inputNode,
                        Methanal.Tests.TestView.MockIEHTMLSelectElement);
                    self._testAppendInsert(control);
                } finally {
                    document.registerElementTag('select', originalType);
                }
            });
    });



/**
 * Mimic Internet Explorer's broken C{HTMLSelectElement.add} behaviour.
 */
Methanal.Tests.MockBrowser.MockHTMLSelectElement.subclass(
    Methanal.Tests.TestView, 'MockIEHTMLSelectElement').methods(
    function add(self, element, before) {
        if (before === null) {
            throw new Error('Guess again, before cannot be null.');
        } else if (before !== undefined) {
            if (typeof before !== 'number') {
                throw new Error('Guess again, before must be an integer.');
            }
            // Fish the correct element out of the array.
            before = self.options[before];
        }
        Methanal.Tests.TestView.MockIEHTMLSelectElement.upcall(
            self, 'add', element, before);
    });



/**
 * Tests for L{Methanal.View.MultiSelectInput}.
 */
Methanal.Tests.TestView.FormInputTestCase.subclass(
    Methanal.Tests.TestView, 'TestMultiSelectInputOnChange').methods(
    function createControl(self, args) {
        var node = Nevow.Test.WidgetUtil.makeWidgetNode();
        var control = Methanal.View.MultiSelectInput(node, args);
        node.appendChild(document.createElement('select'));
        Methanal.Tests.Util.makeWidgetChildNode(control, 'span', 'error');

        // Monkey-patch the "onChange" handler to fail the test if it is
        // called.
        control.onChange = function () {
            self.fail('This should not be called.');
        };
        return control;
    },


    function test_onChangeNotCalledEarly(self) {
        self.testControl({value: null},
            function (control) {
                // Our monkey-patched "onChange" handler should not fire and
                // things should just carry on all happy and shiny.
            });
    });



/**
 * Common control creation for L{Methanal.View.TextInput} inputs.
 */
Methanal.Tests.TestView.FormInputTestCase.subclass(
    Methanal.Tests.TestView, 'BaseTestTextInput').methods(
    function createControl(self, args) {
        var node = Nevow.Test.WidgetUtil.makeWidgetNode();
        var control = self.controlType(node, args);
        node.appendChild(document.createElement('input'));
        Methanal.Tests.Util.makeWidgetChildNode(
            control, 'span', 'displayValue');
        Methanal.Tests.Util.makeWidgetChildNode(control, 'span', 'error');
        return control;
    });



/**
 * Tests for L{Methanal.View.TextInput}.
 */
Methanal.Tests.TestView.BaseTestTextInput.subclass(
    Methanal.Tests.TestView, 'TestTextInput').methods(
    function setUp(self) {
        self.controlType = Methanal.View.TextInput;
    },


    /**
     * L{Methanal.View.TextInput.setValue} sets the node value to a string.
     */
    function test_setValue(self) {
        self.testControl({value: null},
            function (control) {
                control.setValue(null);
                self.assertIdentical(control.getValue(), '');

                control.setValue('');
                self.assertIdentical(control.getValue(), '');

                control.setValue('hello');
                self.assertIdentical(control.getValue(), 'hello');

                control.setValue('  hello ');
                self.assertIdentical(control.getValue(), '  hello ');
            });
    },


    /**
     * When C{embeddedLabel} is C{true}, L{Methanal.View.TextInput.setValue}
     * sets the node value to a string when it is not empty, otherwise it sets
     * the node value to a label; L{Methanal.View.TextInput.getValue} ignores
     * the label.
     */
    function test_setValueWithLabel(self) {
        self.testControl({value: null, label: 'A label', embeddedLabel: true},
            function (control) {
                control.setValue(null);
                self.assertIdentical(control.inputNode.value, 'A label');
                self.assertIdentical(control.getValue(), '');

                control.setValue('');
                self.assertIdentical(control.inputNode.value, 'A label');
                self.assertIdentical(control.getValue(), '');

                control.setValue('hello');
                self.assertIdentical(control.inputNode.value, 'hello');
                self.assertIdentical(control.getValue(), 'hello');
            });
    },


    /**
     * Focussing a L{Methanal.View.TextInput} removes any label it might have
     * and removing the focus applies a label, should it need one.
     */
    function test_focusBehaviourWithLabel(self) {
        self.testControl({value: null, label: 'A label', embeddedLabel: true},
            function (control) {
                control.setValue('');
                self.assertIdentical(control.inputNode.value, 'A label');

                control.onFocus(control.inputNode);
                self.assertIdentical(control.inputNode.value, '');

                control.onBlur(control.inputNode);
                self.assertIdentical(control.inputNode.value, 'A label');
            });
    },


    /**
     * Display value-enabled L{Methanal.View.TextInput}s call
     * L{Methanal.View.TextInput.makeDisplayValue} and set the "display
     * value" node when input changes.
     */
    function test_displayValue(self) {
        self.testControl({value: null},
            function (control) {
                control.enableDisplayValue();

                var called = 0;
                var displayValue = '';
                control._originalMakeDisplayValue = control.makeDisplayValue;
                control.makeDisplayValue = function (value) {
                    called++;
                    displayValue = control._originalMakeDisplayValue(value);
                    return '';
                };
                control.setValue('hello');
                self.assertIdentical(called, 1);
                self.assertIdentical(displayValue, '');
                control.onKeyUp(control.inputNode);
                self.assertIdentical(called, 2);
                self.assertIdentical(displayValue, '');
            });
    },


    /**
     * L{Methanal.View.TextInput.getValue} strips whitespace when
     * L{Methanal.View.TextInput.stripWhitespace} is C{true}.
     */
    function test_getValueStripped(self) {
        self.testControl({value: null},
            function (control) {
                control.stripWhitespace = true;

                control.setValue(' foo bar baz ');
                self.assertIdentical(control.getValue(), 'foo bar baz');

                control.setValue('foo');
                self.assertIdentical(control.getValue(), 'foo');
            });
    });



/**
 * Tests for L{Methanal.View.FilteringTextInput}
 */
Methanal.Tests.TestView.BaseTestTextInput.subclass(
    Methanal.Tests.TestView, 'TestFilteringTextInput').methods(
    function setUp(self) {
        self.controlType = Methanal.View.FilteringTextInput;
    },


    /**
     * If C{expression} is given then input that doesn't match the expression
     * is treated as being invalid.
     */
    function test_expression(self) {
        self.testControl({value: null, expression: '[a-z0-9-]'},
            function (control) {
                self.assertValidInput(control, 'valid-input');
                self.assertInvalidInput(control, 'INvalid input!');
            });
    },


    /**
     * L{Methanal.View.FilteringTextInput}'s onKeyUp and onChange event
     * handlers transform the input being entered in real time according to all
     * filtration functions specified in the control's filters attribute.
     */
    function test_filters(self) {
        self.testControl({value: null, expression: '[a-z0-9]'},
            function (control) {
                control.addFilters([
                    function(value) { return value.toLowerCase(); },
                    function(value) { return value.replace(/[^a-z0-9]/g, ''); }
                    ]);
                control.setValue('A+');
                control.onKeyUp(control.inputNode);
                self.assertIdentical(control.getValue(), 'a');
                control.setValue('ValId InpUt!');
                control.onChange(control.inputNode);
                self.assertIdentical(control.getValue(), 'validinput');
            });
    },


    /**
     * When no expression is given, the control will validate any text input.
     */
    function test_noExpression(self) {
        self.testControl({value: null, expression: null},
            function (control) {
                self.assertValidInput(control, 'VaL1d 1NPut!@#$');
            });
    },


    /**
     * If an expression is given and no filters are added to the control, input
     * will not be transformed but validation will occur, and otherwise will
     * act like a regular TextInput.
     */
    function test_noFilters(self) {
        self.testControl({value: null, expression: '[a-z0-9]'},
            function (control) {
                var value = 'INvalid input!';
                control.setValue(value);
                control.onChange(control.inputNode);
                self.assertIdentical(control.getValue(), value);
                self.assertInvalidInput(control, value);
            });
    });



/**
 * Tests for L{Methanal.View.PrePopulatingTextInput}.
 */
Methanal.Tests.TestView.BaseTestTextInput.subclass(
    Methanal.Tests.TestView, 'TestPrePopulatingTextInput').methods(
    function setUp(self) {
        self.controlType = Methanal.View.PrePopulatingTextInput;
        self.targetControlName = 'targetControl';
    },


    /**
     * Create a target control to be pre-populated.
     */
    function createTargetControl(self, controlType, args) {
        var node = Nevow.Test.WidgetUtil.makeWidgetNode();
        var control = controlType(node, args);
        node.appendChild(document.createElement('input'));
        Methanal.Tests.Util.makeWidgetChildNode(
            control, 'span', 'displayValue');
        Methanal.Tests.Util.makeWidgetChildNode(control, 'span', 'error');
        return control;
    },


    /**
     * L{Methanal.View.PrePopulatingTextInput}'s onKeyUp and onChange event
     * handlers send their input values to the control specified at creation.
     */
    function test_prePopulation(self) {
        var control = self.createControl({
            value: null,
            targetControlName: self.targetControlName});
        var targetControl = self.createTargetControl(
            Methanal.View.TextInput, {
                name: self.targetControlName,
                value: null});
        self.testControls([control, targetControl],
            function (controls) {
                control.setValue('hello');
                control.onKeyUp(control.inputNode);
                self.assertIdentical(targetControl.getValue(), 'hello');
                control.setValue('hello world');
                control.onChange(control.inputNode);
                self.assertIdentical(targetControl.getValue(), 'hello world');
            });
    },


    /**
     * When the target control is a L{Methanal.View.FilteringTextInput},
     * the target's filters, if any, will be applied after pre-population.
     */
    function test_filteringTextInputCompatibility(self) {
        var control = self.createControl({
            value: null,
            targetControlName: self.targetControlName});
        var targetControl = self.createTargetControl(
            Methanal.View.FilteringTextInput, {
                name: self.targetControlName,
                value: null,
                expression: '[a-z]'});
        self.testControls([control, targetControl],
            function (controls) {
                targetControl.addFilters([
                    function(value) { return value.toLowerCase(); },
                    function(value) { return value.replace(/[^a-z]/g, '*'); }
                    ]);
                control.setValue('Hello World.');
                control.onChange(control.inputNode);
                self.assertIdentical(targetControl.getValue(), 'hello*world*');
            });
    },


    /**
     * Resetting a L{PrePopulatingTextInput} resets the target control with the
     * L{PrePopulatingTextInput}'s value too.
     */
    function test_reset(self) {
        var control = self.createControl({
            value: 'foo',
            targetControlName: self.targetControlName});
        var targetControl = self.createTargetControl(
            Methanal.View.TextInput, {
                name: self.targetControlName,
                value: 'bar'});
        self.testControls([control, targetControl],
            function (controls) {
                self.assertIdentical(targetControl.getValue(), 'bar');
                control.reset();
                self.assertIdentical(targetControl.getValue(), 'foo');
            });
    },


    /**
     * Resetting a L{PrePopulatingTextInput} with an invalid target control
     * only resets the L{PrePopulatingTextInput}'s value without throwing any
     * exceptions.
     */
    function test_resetMissingTargetControl(self) {
        self.testControl({value: 'foo', targetControlName: 'doesnotexist'},
            function (control) {
                control.setValue('bar');
                self.assertIdentical(control.getValue(), 'bar');
                control.reset();
                self.assertIdentical(control.getValue(), 'foo');
            });
    });



/**
 * Tests for L{Methanal.View.DateInput}.
 */
Methanal.Tests.TestView.BaseTestTextInput.subclass(
    Methanal.Tests.TestView, 'TestDateInput').methods(
    function setUp(self) {
        self.controlType = Methanal.View.DateInput;
    },


    /**
     * L{Methanal.View.DateInput.makeDisplayValue} creates a human-readable
     * value for valid date values.
     */
    function test_displayValue(self) {
        self.testControl({value: '2012-07-18'},
            function (control) {
                // TextInput._updateDisplayValue should have been called by the
                // time the node has been inserted, if it has then the first
                // child of _displayValueNode will be defined.
                var displayValueText = control._displayValueNode.childNodes[0];
                self.assertNotIdentical(displayValueText, undefined);

                var called = 0;
                var displayValue = '';
                control._originalMakeDisplayValue = control.makeDisplayValue;
                control.makeDisplayValue = function (value) {
                    called++;
                    displayValue = control._originalMakeDisplayValue(value);
                    return '';
                };
                control.setValue('NOTAVALIDDATE');
                self.assertIdentical(called, 0);
                control.setValue('2009-01-01');
                self.assertIdentical(called, 1);
                var t = Methanal.Util.Time.fromDate(new Date(2009, 0, 1));
                self.assertIdentical(displayValue, t.oneDay().asHumanly());
                control.onKeyUp(control.inputNode);
                self.assertIdentical(called, 2);
            });
    },


    /**
     * L{Methanal.View.DateInput.getValue} returns a timestamp in milliseconds
     * if the input node's value is a valid date, C{null} if it is blank and
     * C{undefined} if the value is not a parsable date format.
     */
    function test_getValue(self) {
        self.testControl({value: null},
            function (control) {
                control.setValue(null);
                self.assertIdentical(control.getValue(), null);
                control.setValue('');
                self.assertIdentical(control.getValue(), null);
                control.setValue('NOTAVALIDDATE');
                self.assertIdentical(control.getValue(), undefined);
                control.setValue('2009-01-01');
                self.assertIdentical(control.getValue(), 1230760800000);
            });
    },


    /**
     * L{Methanal.View.DateInput} only accepts input that is a valid date, in a
     * parseable format.
     */
    function test_inputValidation(self) {
        self.testControl({value: null},
            function (control) {
                self.assertValidInput(control, null);
                self.assertValidInput(control, '');
                self.assertValidInput(control, '2009-01-01');
                self.assertInvalidInput(control, 'a');
                self.assertInvalidInput(control, '1');
                self.assertInvalidInput(control, '2009-02-29');
            });
    });



/**
 * Tests for L{Methanal.View.IntegerInput}.
 */
Methanal.Tests.TestView.BaseTestTextInput.subclass(
    Methanal.Tests.TestView, 'TestIntegerInput').methods(
    function setUp(self) {
        self.controlType = Methanal.View.IntegerInput;
    },


    /**
     * L{Methanal.View.IntegerInput.getValue} returns an integer value if the
     * input node's value is a valid number, C{null} if it is blank and
     * C{undefined} if the value is invalid.
     */
    function test_getValue(self) {
        var CASES = [
            [null,  null],
            ['',    null],
            ['abc', undefined],
            ['0.5', undefined],
            ['1a',  undefined],
            ['0',   0],
            ['-1',  -1],
            ['42',  42]];

        self.testControl({value: null},
            function (control) {
                Methanal.Tests.Util.assertCases(
                    self,
                    function (value) {
                        control.setValue(value);
                        return control.getValue();
                    }, CASES);
            });
    },


    /**
     * L{Methanal.View.IntegerInput} only accepts input that is a valid integer.
     */
    function test_inputValidation(self) {
        self.testControl({value: null},
            function (control) {
                self.assertValidInput(control, null);
                self.assertValidInput(control, '');
                self.assertValidInput(control, '1');
                self.assertInvalidInput(control, 'a');
                self.assertInvalidInput(control, '1.2');
            });
    },


    /**
     * L{Methanal.View.IntegerInput} validates that values fall within a certain
     * exclusive range.
     */
    function test_bounds(self) {
        self.testControl({value: null,
                          lowerBound: -11,
                          upperBound:   8},
            function (control) {
                self.assertValidInput(control, '-10');
                self.assertInvalidInput(control, '-11');
                self.assertValidInput(control, '7');
                self.assertInvalidInput(control, '8');
            });
    },


    /**
     * L{Methanal.View.IntegerInput} validates that values fall within a certain
     * exclusive range, even for really big numbers that have precision
     * problems in Javascript.
     */
    function test_bigBounds(self) {
        // These turn into -9223372036854776000 and 9223372036854776000.
        self.testControl({value: null,
                          lowerBound: -9223372036854775809,
                          upperBound:  9223372036854775808},
            function (control) {
                self.assertValidInput(control, null);
                self.assertValidInput(control, '');
                self.assertValidInput(control, '1');
                self.assertInvalidInput(control, '-9223372036854775800');
                self.assertInvalidInput(control, '-9223372036854775809');
                self.assertInvalidInput(control, '-92233720368547758090');
                self.assertInvalidInput(control,  '9223372036854775800');
                self.assertInvalidInput(control,  '9223372036854775808');
                self.assertInvalidInput(control,  '92233720368547758080');
            });
    });



/**
 * Tests for L{Methanal.View.FloatInput}.
 */
Methanal.Tests.TestView.BaseTestTextInput.subclass(
    Methanal.Tests.TestView, 'TestFloatInput').methods(
    function setUp(self) {
        self.controlType = Methanal.View.FloatInput;
    },


    /**
     * L{Methanal.View.FloatInput.getValue} returns an float value if the
     * input node's value is a valid number, C{null} if it is blank and
     * C{undefined} if the value is invalid.
     */
    function test_getValue(self) {
        var CASES = [
            [null,  null],
            ['',    null],
            ['abc', undefined],
            ['0.5', 0.5],
            ['.5',  0.5],
            ['-.5', -0.5],
            ['1a',  undefined],
            ['0',   0],
            ['-1',  -1],
            ['42',  42],
            ['1.2', 1.2]];

        self.testControl({value: null},
            function (control) {
                Methanal.Tests.Util.assertCases(
                    self,
                    function (value) {
                        control.setValue(value);
                        return control.getValue();
                    }, CASES);
            });
    },


    /**
     * L{Methanal.View.FloatInput} only accepts input that is a valid float.
     */
    function test_inputValidation(self) {
        self.testControl({value: null},
            function (control) {
                self.assertValidInput(control, null);
                self.assertValidInput(control, '');
                self.assertValidInput(control, '1');
                self.assertValidInput(control, '1.1');
                self.assertValidInput(control, '+1.0');
                self.assertValidInput(control, '1.');
                self.assertValidInput(control, '-1.0');
                self.assertValidInput(control, '.1');
                self.assertValidInput(control, '+.1');
                self.assertValidInput(control, '-.1');
                self.assertValidInput(control, '.0');
                self.assertInvalidInput(control, 'a');
                self.assertInvalidInput(control, '1.2.1');
            });
    },


    /**
     * L{Methanal.View.FloatInput} validates that values fall within a certain
     * exclusive range.
     */
    function test_bounds(self) {
        self.testControl({value: null,
                          lowerBound: -11,
                          upperBound:   8},
            function (control) {
                self.assertValidInput(control, '-10.99');
                self.assertInvalidInput(control, '-11.0');
                self.assertValidInput(control, '7.99');
                self.assertInvalidInput(control, '8.0');
            });
    },


    /**
     * L{Methanal.View.FloatInput} validates that values fall within a certain
     * exclusive range, even for really big numbers that have precision
     * problems in Javascript.
     */
    function test_bigBounds(self) {
        // These turn into -9223372036854776000 and 9223372036854776000.
        self.testControl({value: null,
                          decimalPlaces: 2,
                          lowerBound: -9223372036854775809.5,
                          upperBound:  9223372036854775808.5},
            function (control) {
                self.assertValidInput(control, null);
                self.assertValidInput(control, '');
                self.assertValidInput(control, '1');
                self.assertInvalidInput(control, '-9223372036854775800');
                self.assertInvalidInput(control, '-9223372036854775809');
                self.assertInvalidInput(control, '-9223372036854775808.5');
                self.assertInvalidInput(control, '-92233720368547758090');
                self.assertInvalidInput(control,  '9223372036854775800');
                self.assertInvalidInput(control,  '9223372036854775808');
                self.assertInvalidInput(control,  '9223372036854775807.5');
                self.assertInvalidInput(control,  '92233720368547758080');
            });
    });



/**
 * Tests for L{Methanal.View.DecimalInput}.
 */
Methanal.Tests.TestView.BaseTestTextInput.subclass(
    Methanal.Tests.TestView, 'TestDecimalInput').methods(
    function setUp(self) {
        self.controlType = Methanal.View.DecimalInput;
    },


    /**
     * L{Methanal.View.DecimalInput.makeDisplayValue} creates a human-readable
     * value for valid decimal numbers.
     */
    function test_displayValue(self) {
        self.testControl({value: null, decimalPlaces: 2},
            function (control) {
                var called = 0;
                var displayValue = '';
                control._originalMakeDisplayValue = control.makeDisplayValue;
                control.makeDisplayValue = function (value) {
                    called++;
                    displayValue = control._originalMakeDisplayValue(value);
                    return '';
                };
                control.setValue('NOTAVALIDDECIMAL');
                self.assertIdentical(called, 0);
                control.setValue(1234.56);
                self.assertIdentical(called, 1);
                self.assertIdentical(displayValue, '1,234.56');
                control.onKeyUp(control.inputNode);
                self.assertIdentical(called, 2);
            });
    },


    /**
     * L{Methanal.View.DecimalInput.getValue} returns a C{Float} if the input
     * node's value is a valid decimal number, C{null} if it is blank and
     * C{undefined} if the value is not a valid decimal number.
     */
    function test_getValue(self) {
        self.testControl({value: null, decimalPlaces: 2},
            function (control) {
                control.setValue(null);
                self.assertIdentical(control.getValue(), null);
                control.setValue('');
                self.assertIdentical(control.getValue(), null);
                control.inputNode.value = 'NOTAVALIDDECIMAL';
                self.assertIdentical(control.getValue(), undefined);
                control.setValue(1234.564);
                self.assertIdentical(control.getValue(), 1234.56);
            });
    },


    /**
     * L{Methanal.View.DecimalInput} only accepts input that is a valid decimal
     * number with the correct number of decimal places.
     */
    function test_inputValidation(self) {
        self.testControl({value: null, decimalPlaces: 2},
            function (control) {
                self.assertValidInput(control, null);
                self.assertValidInput(control, '');
                self.assertValidInput(control, '1');
                self.assertValidInput(control, '1.');
                self.assertValidInput(control, '1.2');
                self.assertValidInput(control, '1.23');
                self.assertInvalidInput(control, 'a');
                self.assertInvalidInput(control, '1.234');
            });
    },


    /**
     * L{Methanal.View.DecimalInput} validates that values fall within a certain
     * exclusive range.
     */
    function test_bounds(self) {
        self.testControl({value: null,
                          decimalPlaces: 2,
                          lowerBound: -10.5,
                          upperBound:   7.5},
            function (control) {
                self.assertValidInput(control, '-10');
                self.assertValidInput(control, '-10.4');
                self.assertInvalidInput(control, '-11');
                self.assertInvalidInput(control, '-10.6');
                self.assertValidInput(control, '7');
                self.assertValidInput(control, '7.4');
                self.assertInvalidInput(control, '8');
                self.assertInvalidInput(control, '7.6');
            });
    },


    /**
     * L{Methanal.View.DecimalInput} validates that values fall within a certain
     * exclusive range, even for really big numbers that have precision
     * problems in Javascript.
     */
    function test_bigBounds(self) {
        // These turn into -9223372036854776000 and 9223372036854776000.
        self.testControl({value: null,
                          decimalPlaces: 2,
                          lowerBound: -9223372036854775809.5,
                          upperBound:  9223372036854775808.5},
            function (control) {
                self.assertValidInput(control, null);
                self.assertValidInput(control, '');
                self.assertValidInput(control, '1');
                self.assertInvalidInput(control, '-9223372036854775800');
                self.assertInvalidInput(control, '-9223372036854775809');
                self.assertInvalidInput(control, '-9223372036854775808.5');
                self.assertInvalidInput(control, '-92233720368547758090');
                self.assertInvalidInput(control,  '9223372036854775800');
                self.assertInvalidInput(control,  '9223372036854775808');
                self.assertInvalidInput(control,  '9223372036854775807.5');
                self.assertInvalidInput(control,  '92233720368547758080');
            });
    });



/**
 * Tests for L{Methanal.View.PercentInput}.
 */
Methanal.Tests.TestView.BaseTestTextInput.subclass(
    Methanal.Tests.TestView, 'TestPercentInput').methods(
    function setUp(self) {
        self.controlType = Methanal.View.PercentInput;
    },


    /**
     * L{Methanal.View.PercentInput.makeDisplayValue} creates a human-readable
     * value for valid percentages.
     */
    function test_displayValue(self) {
        self.testControl({value: null, decimalPlaces: 4},
            function (control) {
                var called = 0;
                var displayValue = '';
                control._originalMakeDisplayValue = control.makeDisplayValue;
                control.makeDisplayValue = function (value) {
                    called++;
                    displayValue = control._originalMakeDisplayValue(value);
                    return '';
                };
                control.setValue('INVALID');
                self.assertIdentical(called, 0);
                control.setValue(0.1234);
                self.assertIdentical(called, 1);
                self.assertIdentical(displayValue, '12.34%');
                control.onKeyUp(control.inputNode);
                self.assertIdentical(called, 2);
            });
    },


    /**
     * L{Methanal.View.PercentInput.getValue} returns a C{Float} if the input
     * node's value is a valid decimal number, C{null} if it is blank and
     * C{undefined} if the value is not a valid percentage.
     */
    function test_getValue(self) {
        self.testControl({value: null, decimalPlaces: 4},
            function (control) {
                control.setValue(null);
                self.assertIdentical(control.getValue(), null);
                control.setValue('');
                self.assertIdentical(control.getValue(), null);
                control.inputNode.value = 'INVALID';
                self.assertIdentical(control.getValue(), undefined);
                control.setValue(12.34);
                self.assertIdentical(control.getValue(), 12.34);
            });
    },


    /**
     * L{Methanal.View.PercentInput} only accepts input that is a valid decimal
     * percentage between 0 and 100%, with the correct number of decimal places
     * and optionally a C{%} symbol too.
     */
    function test_inputValidation(self) {
        self.testControl({value: null, decimalPlaces: 4},
            function (control) {
                self.assertValidInput(control, null);
                self.assertValidInput(control, '');
                self.assertValidInput(control, '1');
                self.assertValidInput(control, '1.');
                self.assertValidInput(control, '1.2');
                self.assertValidInput(control, '1.23');
                self.assertValidInput(control, '0');
                self.assertValidInput(control, '100');
                self.assertValidInput(control, '100%');
                self.assertInvalidInput(control, 'a');
                self.assertInvalidInput(control, '1.234');
                self.assertInvalidInput(control, '101');
                self.assertInvalidInput(control, '101%');
                self.assertInvalidInput(control, '-1');
            });
    });



/**
 * Tests for L{Methanal.View.VerifiedPasswordInput}.
 */
Methanal.Tests.TestView.BaseTestTextInput.subclass(
    Methanal.Tests.TestView, 'TestVerifiedPasswordInput').methods(
    function setUp(self) {
        self.controlType = Methanal.View.VerifiedPasswordInput;
    },


    /**
     * Assert that C{password}, and optionally C{confirmPassword}, are a good
     * input.
     */
    function assertGoodPassword(self, control, password, confirmPassword) {
        if (confirmPassword === undefined) {
            confirmPassword = password;
        }
        control._confirmPasswordNode.value = confirmPassword;
        self.assertValidInput(
            control, password,
            Methanal.Util.repr(password) + ' is NOT a good password');
    },


    /**
     * Assert that C{password}, and optionally C{confirmPassword}, are a bad
     * input.
     */
    function assertBadPassword(self, control, password, confirmPassword) {
        if (confirmPassword === undefined) {
            confirmPassword = password;
        }
        control._confirmPasswordNode.value = confirmPassword;
        self.assertInvalidInput(
            control, password,
            Methanal.Util.repr(password) + ' IS a good password');
    },


    function createControl(self, args) {
        var control = Methanal.Tests.TestView.TestVerifiedPasswordInput.upcall(
            self, 'createControl', args);
        Methanal.Tests.Util.makeWidgetChildNode(
            control, 'input', 'confirmPassword');
        return control;
    },


    /**
     * Validation will fail under the following conditions:
     *     1. The input and confirmPasswordNode node values don't match.
     *     2. If either of the above node values have no length (are blank).
     */
    function test_inputValidation(self) {
        self.testControl({value: null},
            function (control) {
                // Test condition 1
                self.assertBadPassword(control, 'match', 'no match');
                self.assertGoodPassword(control, 'match', 'match');
                // Test condition 2
                self.assertBadPassword(control, '', '');
            });
    },


    /**
     * Changing the password strength criteria results in different validation
     * criteria for the control.
     */
    function test_strengthCriteria(self) {
        // Override the default criteria of 5 or more characters.
        self.testControl({value: null, minPasswordLength: 3},
            function (control) {
                self.assertBadPassword(control, '12');
                self.assertGoodPassword(control, '123');

                control.setStrengthCriteria(['ALPHA']);
                self.assertGoodPassword(control, 'Abc');
                self.assertBadPassword(control, '123');

                control.setStrengthCriteria(['NUMERIC']);
                self.assertBadPassword(control, 'Abc');
                self.assertGoodPassword(control, '123');

                control.setStrengthCriteria(['ALPHA', 'NUMERIC']);
                self.assertBadPassword(control, 'Abc');
                self.assertBadPassword(control, '123');
                self.assertGoodPassword(control, 'Abc123');

                control.setStrengthCriteria(['MIXEDCASE']);
                self.assertGoodPassword(control, 'Abc');
                self.assertGoodPassword(control, 'abC');
                self.assertBadPassword(control, 'abc');
                self.assertBadPassword(control, '123');

                control.setStrengthCriteria(['SYMBOLS']);
                self.assertGoodPassword(control, '!@#_');
                self.assertBadPassword(control, ' ');
                self.assertBadPassword(control, 'abc');

                control.setStrengthCriteria([]);
                self.assertGoodPassword(control, '!@#_');
                self.assertGoodPassword(control, 'abc');
                self.assertGoodPassword(control, '123');

                self.assertThrows(Methanal.View.InvalidStrengthCriterion,
                    function () {
                        control.setStrengthCriteria(['DANGERWILLROBINSON']);
                    });
            });
    });



/**
 * Tests for L{Methanal.View.InputContainer}.
 *
 * Be aware that these tests test containers containing multiple controls,
 * because this sort of breaks the mold of the control testing framework these
 * tests look slightly different.
 */
Methanal.Tests.TestView.BaseTestTextInput.subclass(
    Methanal.Tests.TestView, 'TestFormGroup').methods(
    function setUp(self) {
        self.controlType = Methanal.View.TextInput;
    },


    /**
     * Specially designed to accept multiple children.
     */
    function createContainer(self, widgetParent, children) {
        var containedChildren = Methanal.Util.map(function (child) {
            return Methanal.Tests.TestView.TestFormGroup.upcall(
                self, 'createContainer', widgetParent, child);
        }, children);

        return Methanal.Tests.TestView.createContainer(
            widgetParent, Methanal.View.InputContainer, containedChildren);
    },


    function _createControls(self) {
        return [
            self.createControl({name: 'one', value: null}),
            self.createControl({name: 'two', value: null})];
    },


    /**
     * Any active children means the container is visible.
     */
    function test_activeChildren(self) {
        var controls = self._createControls();
        self.testControls([controls],
            function (controlsArray) {
                var one = controlsArray[0][0];
                var two = controlsArray[0][1];
                var group = one.widgetParent.widgetParent;
                self.assertIsInstanceOf(group, Methanal.View.InputContainer);

                one.setActive(true);
                self.assertIdentical(group.active, true);
                two.setActive(false);
                self.assertIdentical(group.active, true);
            });
    },


    /**
     * No active children means the container is not visible.
     */
    function test_noActiveChildren(self) {
        var controls = self._createControls();
        self.testControls([controls],
            function (controlsArray) {
                var one = controlsArray[0][0];
                var two = controlsArray[0][1];
                var group = one.widgetParent.widgetParent;
                self.assertIsInstanceOf(group, Methanal.View.InputContainer);
                one.setActive(false);
                two.setActive(true);
                self.assertIdentical(group.active, true);
                two.setActive(false);
                self.assertIdentical(group.active, false);
            });
    });



/**
 * Tests for L{Methanal.View.RadioGroupInput}.
 */
Methanal.Tests.TestView.FormInputTestCase.subclass(
    Methanal.Tests.TestView, 'TestRadioGroupInput').methods(
    function setUp(self) {
        self.controlType = Methanal.View.RadioGroupInput;
    },


    function createControl(self, args) {
        var node = Nevow.Test.WidgetUtil.makeWidgetNode();
        var control = self.controlType(node, args);
        Methanal.Tests.Util.makeWidgetChildNode(control, 'span', 'error');
        Methanal.Tests.Util.makeWidgetChildNode(control, 'input').value = '42';
        Methanal.Tests.Util.makeWidgetChildNode(control, 'input').value = '13';
        return control;
    },


    /**
     * L{RadioGroupInput.getValue} never returns undefined.
     */
    function test_getValueNoSelection(self) {
        self.testControl({value: null},
            function (control) {
                self.assertNotIdentical(control.getValue(), undefined);
            });
    },


    /**
     * L{RadioGroupInput.getValue} returns the value of the first selected
     * input.
     */
    function test_getValue(self) {
        function getInputNode(widget, index) {
            return widget.node.getElementsByTagName('input')[index];
        }

        self.testControl({value: null},
            function (control) {
                getInputNode(control, 0).checked = true;
                self.assertIdentical(control.getValue(), '42');
            });
        self.testControl({value: null},
            function (control) {
                getInputNode(control, 1).checked = true;
                self.assertIdentical(control.getValue(), '13');
            });
        self.testControl({value: null},
            function (control) {
                getInputNode(control, 0).checked = true;
                getInputNode(control, 1).checked = true;
                self.assertIdentical(control.getValue(), '42');
            });
    });



/**
 * Tests for L{Methanal.View.MultiCheckboxInput}.
 */
Methanal.Tests.TestView.FormInputTestCase.subclass(
    Methanal.Tests.TestView, 'TestMultiCheckboxInput').methods(
    function setUp(self) {
        self.controlType = Methanal.View.MultiCheckboxInput;
    },


    function createControl(self, args) {
        var node = Nevow.Test.WidgetUtil.makeWidgetNode();
        var control = self.controlType(node, args);
        Methanal.Tests.Util.makeWidgetChildNode(control, 'span', 'error');
        Methanal.Tests.Util.makeWidgetChildNode(control, 'input').value = '42';
        Methanal.Tests.Util.makeWidgetChildNode(control, 'input').value = '13';
        return control;
    },


    /**
     * L{MultiCheckboxInput.setValue} sets the checked state on all inputs to
     * match the given value.
     */
    function test_setValue(self) {
        self.testControl({value: null},
            function (control) {
                self.assertArraysEqual(control.getValue(), []);
            });

        self.testControl({value: ['42']},
            function (control) {
                self.assertArraysEqual(control.getValue(), ['42']);
            });

        self.testControl({value: ['13', '42']},
            function (control) {
                self.assertArraysEqual(control.getValue(), ['42', '13']);
            });
    },


    /**
     * L{MultiCheckboxInput.setValue} ignores values that do not correlate with
     * any checkbox control.
     */
    function test_badSetValue(self) {
        self.testControl({value: '1'},
            function (control) {
                self.assertArraysEqual(control.getValue(), []);
            });

        self.testControl({value: ['foo']},
            function (control) {
                self.assertArraysEqual(control.getValue(), []);
            });

        self.testControl({value: ['foo', '42']},
            function (control) {
                self.assertArraysEqual(control.getValue(), ['42']);
            });
    },


    /**
     * L{MultiCheckboxInput.getValue} returns the values of all selected
     * options.
     */
    function test_getValue(self) {
        function getInputNode(widget, index) {
            return widget.node.getElementsByTagName('input')[index];
        }

        self.testControl({value: null},
            function (control) {
                getInputNode(control, 0).checked = true;
                self.assertArraysEqual(control.getValue(), ['42']);
            });
        self.testControl({value: null},
            function (control) {
                getInputNode(control, 1).checked = true;
                self.assertArraysEqual(control.getValue(), ['13']);
            });
        self.testControl({value: null},
            function (control) {
                getInputNode(control, 0).checked = true;
                getInputNode(control, 1).checked = true;
                self.assertArraysEqual(control.getValue(), ['42', '13']);
            });
    });
