// import Nevow.Test.WidgetUtil
// import Methanal.Widgets
// import Methanal.Util
// import Methanal.Tests.Util
// import Methanal.Tests.MockBrowser



/**
 * A L{Methanal.Widgets.Action} that returns C{false} for C{enableForRow}.
 */
Methanal.Widgets.Action.subclass(
    Methanal.Tests.TestWidgets, 'DisabledAction').methods(
        function enableForRow(self, row) {
            return false;
        });



/**
 * Tests for L{Methanal.Widgets.Table}.
 */
Methanal.Tests.Util.TestCase.subclass(
    Methanal.Tests.TestWidgets, 'TableTest').methods(
    /**
     * Create a L{Methanal.Widgets.Table} widget.
     *
     * @param columnValues: Mapping of column names to mappings of C{'type'},
     *     C{'value'} and C{'link'}, used for creating cells.
     *
     * @type  actions: C{Array} of L{Methanal.Widgets.Action}
     * @param actions: Optional table actions.
     *
     * @type  defaultAction: L{Methanal.Widgets.Action}
     * @param defaultAction: Optional default table action.
     *
     * @rtype: C{Methanal.Widgets.Table}
     */
    function createTable(self, columnValues, actions/*=undefined*/,
        defaultAction/*=undefined*/) {
        var cells = {};
        var columns = [];
        for (var columnID in columnValues) {
            var values = columnValues[columnID];
            columns.push(values.type(columnID, 'title'));
            cells[columnID] = Methanal.Widgets.Cell(values.value, values.link);
        }
        var node = Nevow.Test.WidgetUtil.makeWidgetNode();
        var rows = [Methanal.Widgets.Row(0, cells)];
        var args = {
            'columns': columns,
            'rows': rows};
        var table = Methanal.Widgets.Table(node, args);
        table.actions = actions || null;
        table.defaultAction = defaultAction || null;
        var tableNode = Methanal.Tests.Util.makeWidgetChildNode(
            table, 'table');
        document.body.appendChild(node);
        Methanal.Util.nodeInserted(table);
        return table;
    },


    /**
     * Get an C{Array} of DOM nodes for a table's actions.
     */
    function _getActionNodes(self, table) {
        var rows = table.getBody().rows;
        self.assertIdentical(rows.length > 0, true,
            'Table has no rows.');
        var cells = rows[0].cells;
        if (cells.length < table._columns.length + 1) {
            throw new Error('No actions column.');
        }
        var actionsCell = cells[table._columns.length/* + 1 - 1*/];
        return actionsCell.getElementsByTagName('a');
    },


    /**
     * Assert that C{table} has action DOM nodes that match an C{Array} of
     * L{Methanal.Widgets.Action}.
     */
    function assertHasActions(self, table, actions) {
        var actionDisplayNames = [];
        for (var i = 0; i < actions.length; ++i) {
            actionDisplayNames.push(actions[i].displayName);
        }
        actionDisplayNames.sort();

        var anchors = self._getActionNodes(table);
        self.assertIdentical(anchors.length, actions.length,
            'Number of action nodes does not match number of actions.');

        var textValues = [];
        for (var i = 0; i < anchors.length; ++i) {
            var children = anchors[i].childNodes;
            for (var j = 0; j < children.length; ++j) {
                if (children[j].nodeType == children[j].TEXT_NODE) {
                    textValues.push(children[j].nodeValue);
                    break;
                }
            }
        }
        textValues.sort();

        self.assertArraysEqual(actionDisplayNames, textValues);
    },


    /**
     * Assert that C{table} has no action DOM nodes.
     */
    function assertHasNoActions(self, table) {
        var anchors = self._getActionNodes(table);
        self.assertIdentical(anchors.length, 0,
            'Table has ' + anchors.length + ' actions, expected 0.');
    },


    /**
     * Create a table with actions.
     */
    function test_createTableWithEnabledAction(self) {
        var columnValues = {
            'col1': {type: Methanal.Widgets.BooleanColumn,
                     value: false,
                     link: null}};
        var actions = [Methanal.Widgets.Action('foo', 'Foo')];
        var table = self.createTable(columnValues, actions);

        self.assertHasActions(table, actions);
    },


    /**
     * Create a table with actions that are disabled. An "actions" column
     * should still appear, in this case.
     */
    function test_createTableWithDisabledAction(self) {
        var columnValues = {
            'col1': {type: Methanal.Widgets.BooleanColumn,
                     value: false,
                     link: null}};
        var actions = [
            Methanal.Tests.TestWidgets.DisabledAction('foo', 'Foo')];
        var table = self.createTable(columnValues, actions);

        self.assertHasNoActions(table);
    });


/**
 * Create and test trivial Column types.
 *
 * @ivar columnType: Column type to create.
 *
 * @ivar columnValues: A mapping of column identifiers to mappings of values
 *     for keys named C{id}, C{link}, C{nodeValue}.
 *
 * @ivar columns: A sequence of L{Methanal.Widgets.Column} instances.
 *
 * @ivar rowData: L{Methanal.Widgets.Row} constructed from L{columnValues}.
 */
Methanal.Tests.Util.TestCase.subclass(
    Methanal.Tests.TestWidgets, 'SimpleColumnTest').methods(
    function setUp(self) {
        var _cells = {};
        self.columns = [];
        for (var columnID in self.columnValues) {
            var values = self.columnValues[columnID];
            self.columns.push(self.columnType(columnID, 'title'));
            _cells[columnID] = Methanal.Widgets.Cell(values.value, values.link);
        }
        self.rowData = Methanal.Widgets.Row(0, _cells);
    },


    /**
     * Apply a function over each column.
     */
    function eachColumn(self, fn) {
        for (var i = 0; i < self.columns.length; ++i) {
            fn(self.columns[i]);
        }
    },


    /**
     * Extracting a value for a column from row data matches the original data
     * used to construct the cell. Attempting to extract a value for an
     * identifier that does not exist throws C{TypeError}.
     */
    function test_extractValue(self) {
        self.eachColumn(function (column) {
            self.assertIdentical(
                column.extractValue(self.rowData),
                self.columnValues[column.id].value);
            self.assertThrows(TypeError,
                function () {
                    column.extractValue({});
                });
        });
    },


    /**
     * Extracting a link for a column from row data matches the original data
     * used to construct the cell. Attempting to extract a value for an
     * identifier that does not exist throws C{TypeError}.
     */
    function test_extractLink(self) {
        self.eachColumn(function (column) {
            self.assertIdentical(
                column.extractLink(self.rowData),
                self.columnValues[column.id].link);
            self.assertThrows(TypeError,
                function () {
                    column.extractLink({});
                });
        });
    },


    /**
     * Convert a column value (generally the result of C{extractValue}) to a
     * DOM node.
     */
    function test_valueToDOM(self) {
        self.eachColumn(function (column) {
            var node = column.valueToDOM(column.extractValue(self.rowData));
            self.assertIdentical(node.nodeType, node.TEXT_NODE);
            var nodeValue = self.columnValues[column.id].nodeValue;
            self.assertIdentical(node.nodeValue, nodeValue);
        });
    });



/**
 * Tests for L{Methanal.Widgets.TextColumn}.
 */
Methanal.Tests.TestWidgets.SimpleColumnTest.subclass(
    Methanal.Tests.TestWidgets, 'TestTextColumn').methods(
    function setUp(self) {
        self.columnType = Methanal.Widgets.TextColumn;
        self.columnValues = {
            'a': {value: 'foo',
                  link: null,
                  nodeValue: 'foo'},
            'b': {value: 'bar',
                  link: 'quux',
                  nodeValue: 'bar'}};
        Methanal.Tests.TestWidgets.TestTextColumn.upcall(self, 'setUp');
    });



/**
 * Tests for L{Methanal.Widgets.IntegerColumn}.
 */
Methanal.Tests.TestWidgets.SimpleColumnTest.subclass(
    Methanal.Tests.TestWidgets, 'TestIntegerColumn').methods(
    function setUp(self) {
        self.columnType = Methanal.Widgets.IntegerColumn;
        self.columnValues = {
            'a': {value: 42,
                  link: null,
                  nodeValue: '42'},
            'b': {value: 5144,
                  link: 'quux',
                  nodeValue: '5144'}};
        Methanal.Tests.TestWidgets.TestIntegerColumn.upcall(self, 'setUp');
    });



/**
 * Tests for L{Methanal.Widgets.FloatColumn}.
 */
Methanal.Tests.TestWidgets.SimpleColumnTest.subclass(
    Methanal.Tests.TestWidgets, 'TestFloatColumn').methods(
    function setUp(self) {
        self.columnType = Methanal.Widgets.FloatColumn;
        self.columnValues = {
            'a': {value: 42.0,
                  link: null,
                  nodeValue: '42'},
            'b': {value: 1.23,
                  link: 'quux',
                  nodeValue: '1.23'}};
        Methanal.Tests.TestWidgets.TestFloatColumn.upcall(self, 'setUp');
    });



/**
 * Tests for L{Methanal.Widgets.BooleanColumn}.
 */
Methanal.Tests.TestWidgets.SimpleColumnTest.subclass(
    Methanal.Tests.TestWidgets, 'TestBooleanColumn').methods(
    function setUp(self) {
        self.columnType = Methanal.Widgets.BooleanColumn;
        self.columnValues = {
            'a': {value: false,
                  link: null,
                  nodeValue: 'false'},
            'b': {value: true,
                  link: 'quux',
                  nodeValue: 'true'}};
        Methanal.Tests.TestWidgets.TestBooleanColumn.upcall(self, 'setUp');
    });



/**
 * Tests for L{Methanal.Widgets.TimestampColumn}.
 */
Methanal.Tests.TestWidgets.SimpleColumnTest.subclass(
    Methanal.Tests.TestWidgets, 'TestTimestampColumn').methods(
    function setUp(self) {
        self.columnType = Methanal.Widgets.TimestampColumn;

        var t1 = Methanal.Util.Time.fromTimestamp(1259973381772);
        var t2 = Methanal.Util.Time.fromTimestamp(1149573966000);

        self.columnValues = {
            'a': {value: t1,
                  link: null,
                  nodeValue: t1.asHumanly()},
            'b': {value: t2,
                  link: 'quux',
                  nodeValue: t2.asHumanly()}};
        Methanal.Tests.TestWidgets.TestTimestampColumn.upcall(self, 'setUp');
    });



/**
 * Tests for L{Methanal.Widgets.TabView}.
 */
Methanal.Tests.Util.TestCase.subclass(
    Methanal.Tests.TestWidgets, 'TabViewTest').methods(
    /**
     * Assert that C{tab} is the only selected tab contained in its parent.
     */
    function assertSelected(self, tab) {
        self.assertIdentical(tab.selected, true, 'Tab not selected');
        var tabView = tab.widgetParent;
        self.assertIdentical(
            Methanal.Util.containsElementClass(
                tabView._labels[tab.id], 'selected-tab-label'),
            true,
            'Tab selection style not applied');

        var childWidgets = tabView.childWidgets;
        var labelCount = 0;
        for (var k in tabView._labels) {
            ++labelCount;
        }
        self.assertIdentical(childWidgets.length, labelCount);
        for (var i = 0; i < childWidgets.length; ++i) {
            var otherTab = childWidgets[i];
            if (otherTab === tab) {
                continue;
            }
            self.assertIdentical(
                otherTab.selected, false,
                Methanal.Util.repr(otherTab.id) + ' also selected');
            self.assertIdentical(
                Methanal.Util.containsElementClass(
                    tabView._labels[otherTab.id], 'selected-tab-label'),
                false,
                Methanal.Util.repr(otherTab.id) + ' also has selection style');
        }
    },


    /**
     * Assert that C{node} is not visible.
     *
     * Since we don't have a working render engine we can't check the
     * C{'style'} attribute, so C{'className'} will have to do.
     */
    function assertNodeHidden(self, node) {
        self.assertIdentical(
            Methanal.Util.containsElementClass(node, 'hidden'),
            true, 'Node is visible');
    },


    /**
     * Assert that C{node} is visible.
     */
    function assertNodeVisible(self, node) {
        self.assertThrows(Divmod.UnitTest.AssertionError,
            function() {
                self.assertNodeHidden(node);
            },
        'Node is not visible');
    },


    /**
     * Assert that C{tab} is not visible.
     */
    function assertHidden(self, tab) {
        self.assertIdentical(tab.visible, false, 'Tab is visible');
        var tabView = tab.widgetParent;
        self.assertNodeHidden(tabView._labels[tab.id]);
    },


    /**
     * Assert that C{tab} is visible.
     */
    function assertVisible(self, tab) {
        self.assertThrows(Divmod.UnitTest.AssertionError,
            function() {
                self.assertHidden(tab);
            },
        'Tab is not visible');
    },


    /**
     * Create a L{Methanal.Widgets.TabView}.
     */
    function createTabView(self, tabIDs, tabGroups, topLevel) {
        function _makeThrobber() {
            return {
                'start': function() {},
                'stop': function() {}};
        }

        var _tabIDs = {};
        for (var i = 0; i < tabIDs.length; ++i) {
            _tabIDs[tabIDs[i]] = true;
        }

        tabGroups = tabGroups || [];
        var _tabGroups = {};
        for (var i = 0; i < tabGroups.length; ++i) {
            _tabGroups[tabGroups[i].id] = tabGroups[i];
        }

        var node = Nevow.Test.WidgetUtil.makeWidgetNode();
        var tabView = Methanal.Widgets.TabView(
            node, _tabIDs, _tabGroups, topLevel || false, _makeThrobber);
        Methanal.Tests.Util.makeWidgetChildNode(tabView, 'div', 'throbber');
        Methanal.Tests.Util.makeWidgetChildNode(tabView, 'ul', 'labels');
        Methanal.Tests.Util.makeWidgetChildNode(tabView, 'div', 'contents');
        document.body.appendChild(node);
        Methanal.Util.nodeInserted(tabView);
        return tabView;
    },


    /**
     * Create a L{Methanal.Widgets.Tab} as child of C{tabView}.
     */
    function createTab(self, tabView, id, title, selected /*=false*/,
                       group /*=null*/) {
        var node = Nevow.Test.WidgetUtil.makeWidgetNode();
        var tab = Methanal.Widgets.Tab(node, {
            'id': id,
            'title': title,
            'selected': selected || false,
            'group': group || null});
        tabView.addChildWidget(tab);
        Methanal.Tests.Util.makeWidgetChildNode(tab, 'content');
        tabView.nodeById('contents').appendChild(tab.node);
        Methanal.Util.nodeInserted(tab);
        return tab;
    },


    /**
     * Calling L{Methanal.Widgets.TabView.loadedUp} removes the specified tab
     * from the loading queue and creates a label for it.
     */
    function test_loadedUp(self) {
        var tabView = self.createTabView(['tab1']);
        self.assertIdentical(tabView._labels.tab1, undefined);
        self.assertIdentical(tabView.tabIDs.tab1, true);

        self.createTab(tabView, 'tab1', 'Tab 1');
        self.assertNotIdentical(tabView._labels.tab1, undefined);
        self.assertIdentical(tabView.tabIDs.tab1, undefined);
    },


    /**
     * Tab views are not fully loaded until all the expected tabs have called
     * L{Methanal.Widgets.TabView.loadedUp}.
     */
    function test_fullyLoaded(self) {
        var tabView = self.createTabView(['tab1', 'tab2']);
        self.assertIdentical(tabView.fullyLoaded, false);
        self.createTab(tabView, 'tab1', 'Tab 1');
        self.assertIdentical(tabView.fullyLoaded, false);
        self.createTab(tabView, 'tab2', 'Tab 2');
        self.assertIdentical(tabView.fullyLoaded, true);
    },


    /**
     * L{Methanal.Widgets.TabView.getTab} retrieves a tab by its identifier, or
     * throws L{Methanal.Widgets.UnknownTab} for unknown identifiers.
     */
    function test_getTab(self) {
        var tabView = self.createTabView(['tab1']);

        self.assertThrows(Methanal.Widgets.UnknownTab,
            function () { tabView.getTab('tab1'); });

        var tab1 = self.createTab(tabView, 'tab1', 'Tab 1');
        self.assertIdentical(tabView.getTab('tab1'), tab1);
    },


    /**
     * L{Methanal.Widgets.TabView.selectTab} selects the specified tab and
     * deselects all others.
     */
    function test_selectTab(self) {
        var tabView = self.createTabView(['tab1', 'tab2']);
        var tab1 = self.createTab(tabView, 'tab1', 'Tab 1');
        var tab2 = self.createTab(tabView, 'tab2', 'Tab 2');
        // When there are no other candidates, the first tab is selected.
        self.assertSelected(tab1);
        tabView.selectTab(tab2);
        self.assertSelected(tab2);
    },


    /**
     * Tabs with a true C{'selected'} attribute will be selected when the tab
     * view has finished loading.
     */
    function test_preselectedTab(self) {
        var tabView = self.createTabView(['tab1', 'tab2']);
        var tab1 = self.createTab(tabView, 'tab1', 'Tab 1');
        var tab2 = self.createTab(tabView, 'tab2', 'Tab 2', true);
        self.assertSelected(tab2);
    },


    /**
     * Selecting another tab before the tab view has finished loading will
     * override any tabs with a true C{'selected'} attribute.
     */
    function test_preselectedTabOverride(self) {
        var tabView = self.createTabView(['tab1', 'tab2']);
        var tab1 = self.createTab(tabView, 'tab1', 'Tab 1');
        tabView.selectTab(tab1);
        var tab2 = self.createTab(tabView, 'tab2', 'Tab 2', true);
        self.assertSelected(tab1);
    },


    /**
     * Hiding a tab makes it invisible. Hiding the selected tab also selects
     * the first visible tab. Showing a tab makes it visible. The only tab to
     * be made visible is also selected.
     */
    function test_hideShowTab(self) {
        var tabView = self.createTabView(['tab1', 'tab2']);
        var tab1 = self.createTab(tabView, 'tab1', 'Tab 1');
        var tab2 = self.createTab(tabView, 'tab2', 'Tab 2');
        tabView.hideTab(tab1);
        self.assertHidden(tab1);
        // Hiding the selected tab will focus the first visible one.
        self.assertSelected(tab2);

        tabView.hideTab(tab2);
        self.assertHidden(tab2);
        tabView.showTab(tab1);
        self.assertVisible(tab1);
        // The only tab to be made visible is also selected.
        self.assertSelected(tab1);
    },


    /**
     * Top-level tab views will select tabs specified in
     * C{window.location.hash} as well as using it to track tab selection.
     */
    function test_topLevel(self) {
        window = {
            'location': {
                'hash': '#tab:tab2'}};
        var tabView = self.createTabView(['tab1', 'tab2'], undefined, true);
        var tab1 = self.createTab(tabView, 'tab1', 'Tab 1');
        var tab2 = self.createTab(tabView, 'tab2', 'Tab 2');
        self.assertSelected(tab2);

        tabView.selectTab(tab1);
        self.assertIdentical(window.location.hash, '#tab:tab1');
        window = undefined;
    },


    /**
     * Tab groups are created dynamically and visually group tabs.
     */
    function test_groups(self) {
        function checkGroup(group) {
            var groupNode = tabView._groups[group.id].content;
            self.assertNotIdentical(groupNode, undefined);
            self.assertIdentical(
                groupNode.getElementsByTagName('li').length,
                group.tabIDs.length);
        }

        var group1 = Methanal.Widgets.TabGroup(
            'group1', 'Group 1', ['tab2', 'tab3']);
        var tabView = self.createTabView(
            ['tab1', 'tab2', 'tab3'], [group1]);
        var tab1 = self.createTab(tabView, 'tab1', 'Tab 1');
        var tab2 = self.createTab(
            tabView, 'tab2', 'Tab 2', undefined, group1.id);
        var tab3 = self.createTab(
            tabView, 'tab3', 'Tab 3', undefined, group1.id);
        checkGroup(group1);

        var group2 = Methanal.Widgets.TabGroup(
            'group2', 'Group 2', ['tab4']);
        tabView.tabGroups[group2.id] = group2;
        var tab4 = self.createTab(
            tabView, 'tab4', 'Tab 4', undefined, group2.id);
        checkGroup(group2);
    },


    /**
     * Group visibility is determined by the visibility of the tabs it
     * contains. Removing all the tabs from a group will result in that group
     * becoming invisible.
     */
    function test_groupVisibility(self) {
        var group1 = Methanal.Widgets.TabGroup(
            'group1', 'Group 1', ['tab2', 'tab3']);
        var tabView = self.createTabView(
            ['tab1', 'tab2', 'tab3'], [group1]);
        var tab1 = self.createTab(tabView, 'tab1', 'Tab 1');
        var tab2 = self.createTab(
            tabView, 'tab2', 'Tab 2', undefined, group1.id);
        var tab3 = self.createTab(
            tabView, 'tab3', 'Tab 3', undefined, group1.id);

        var node = tabView._groups[group1.id].content.parentNode;
        tabView.hideTab(tab1);
        self.assertNodeVisible(node);
        tabView.hideTab(tab2);
        self.assertNodeVisible(node);
        tabView.hideTab(tab3);
        self.assertNodeHidden(node);
        tabView.showTab(tab3);
        self.assertNodeVisible(node);

        // Stub out Nevow.Athena.Widget.detach.
        function detach() {}

        tab2.detach = detach;
        tabView.removeTab(tab2);
        self.assertNodeVisible(node);

        tab3.detach = detach;
        tabView.removeTab(tab3);
        self.assertNodeHidden(node);
    });



/**
 * L{Methanal.Widgets.ModalDialogForm} mock implementation.
 */
Methanal.Widgets.ModalDialogForm.subclass(
    Methanal.Tests.TestWidgets, 'MockModalDialogForm').methods(
    function __init__(self, controlNames, viewOnly) {
        viewOnly = viewOnly || false;

        var node = Nevow.Test.WidgetUtil.makeWidgetNode();
        Methanal.Tests.TestWidgets.MockModalDialogForm.upcall(
            self, '__init__', node, viewOnly, controlNames);

        Methanal.Tests.Util.setUpForm(self);
    },


    function focusFirstInput(self) {
    });



/**
 * Tests for L{Methanal.Widgets.ModalDialog} and
 * L{Methanal.Widgets.ModalDialogForm}.
 */
Methanal.Tests.Util.TestCase.subclass(
    Methanal.Tests.TestWidgets, 'ModalDialogTest').methods(
    /**
     * Create a L{Methanal.Widgets.ModalDialog}.
     */
    function createDialog(self) {
        var parentNode = document.createElement('div');
        var node = Nevow.Test.WidgetUtil.makeWidgetNode();
        parentNode.appendChild(node);
        var m = Methanal.Widgets.ModalDialog(node);
        Methanal.Util.nodeInserted(m);
        return m;
    },


    /**
     * Create a L{Methanal.Widgets.ModalDialogForm}.
     */
    function createDialogForm(self) {
        var controlNames = [];
        form = Methanal.Tests.TestWidgets.MockModalDialogForm(controlNames);
        Methanal.Util.nodeInserted(form);
        return form;
    },


    /**
     * L{Methanal.Widgets.ModalDialogForm} only closes a modal dialog if the
     * form was successfully submitted.
     */
    function test_closeOnSuccess(self) {
        var form = self.createDialogForm();
        var dlg = self.createDialog();
        form.setWidgetParent(dlg);

        var closed;

        dlg.close = function close() {
            closed = true;
        };

        function succeed(methodName, data) {
            closed = false;
            return Divmod.Defer.succeed(data);
        }

        function fail(methodName, data) {
            closed = false;
            return Divmod.Defer.fail('too bad');
        }

        form.callRemote = succeed;
        form.submit();
        self.assertIdentical(closed, true,
            'Dialog was NOT closed');

        form.callRemote = fail;
        form.submit();
        self.assertIdentical(closed, false,
            'Dialog was closed');
    });
