// import Divmod.MockBrowser



Divmod.MockBrowser.Element.subclass(
    Methanal.Tests.MockBrowser, 'Element').methods(
    function __init__(self, tagName) {
        Methanal.Tests.MockBrowser.Element.upcall(self, '__init__', tagName);
        self._updateChildProperties();
    },


    function _updateChildProperties(self) {
        self.firstChild = self.childNodes[0] || null;
        self.lastChild = self.childNodes[self.childNodes.length - 1] || null;
    },


    function appendChild(self, child) {
        Methanal.Tests.MockBrowser.Element.upcall(self, 'appendChild', child);
        self._updateChildProperties();
    },


    function removeChild(self, child) {
        Methanal.Tests.MockBrowser.Element.upcall(self, 'removeChild', child);
        self._updateChildProperties();
    });



/**
 * HTMLSelectElement mock implementation.
 *
 * Assigning to the C{'value'} attribute tries to follow the behaviour of HTML5
 * (which is generally the behaviour that Firefox (as of 3.6.7) follows too)::
 *     The value IDL attribute, on getting, must return the value of the first
 *     option element in the list of options in tree order that has its
 *     selectedness set to true, if any. If there isn't one, then it must
 *     return the empty string.
 *
 *     On setting, the value attribute must set the selectedness of all the
 *     option elements in the list of options to false, and then first the
 *     option element in the list of options, in tree order, whose value is
 *     equal to the given new value, if any, must have its selectedness set to
 *     true.
 */
Methanal.Tests.MockBrowser.Element.subclass(
    Methanal.Tests.MockBrowser, 'MockHTMLSelectElement').methods(
    function __init__(self) {
        Methanal.Tests.MockBrowser.MockHTMLSelectElement.upcall(
            self, '__init__', 'select');
        self.options = [];

        Methanal.Tests.Util.defineGetter(self, 'value', function () {
            for (var i = 0; i < self.options.length; ++i) {
                var option = self.options[i];
                if (option.selected) {
                    return option.value;
                }
            }
            return '';
        });

        Methanal.Tests.Util.defineSetter(self, 'value', function (v) {
            var found = false;
            for (var i = 0; i < self.options.length; ++i) {
                var option = self.options[i];
                if (found === false && v == option.value) {
                    option.selected = true;
                    found = true;
                } else {
                    option.selected = false;
                }
            }
        });
    },


    /**
     * Add a new element to the collection of OPTION elements for this SELECT.
     */
    function add(self, element, before) {
        var index = Methanal.Util.arrayIndexOf(self.options, before);
        if (index == -1) {
            index = self.options.length;
            self.options.push(element);
        } else {
            self.options.splice(index, 0, element);
        }
        element.index = index;
    },


    /**
     * Remove an element from the collection of OPTION elements for this
     * SELECT. Does nothing if no element has the given index.
     */
    function remove(self, index) {
        self.options.splice(index, 1);
    });



/**
 * HTMLOptionElement mock implementation.
 *
 * Assignments to the C{'value'} attribute try to follow the behaviour of
 * Firefox (as of 3.6.7), generally this means the value is coerced to a
 * C{String}.
 */
Methanal.Tests.MockBrowser.Element.subclass(
    Methanal.Tests.MockBrowser, 'MockHTMLOptionElement').methods(
    function __init__(self) {
        Methanal.Tests.MockBrowser.MockHTMLOptionElement.upcall(
            self, '__init__', 'option');
        self.selected = false;
        self._value = '';

        Methanal.Tests.Util.defineGetter(self, 'value', function () {
            return self._value;
        });

        Methanal.Tests.Util.defineSetter(self, 'value', function (v) {
            if (v === undefined) {
                /* Seriously, this is real (Firefox 3.6.7):
                 *  >>> o
                 *  <option value="">
                 *  >>> o.value = undefined;
                 *  >>> o.value
                 *  "undefined"
                 *  >>> o.value = null;
                 *  >>> o.value
                 *  ""
                 */
                v = 'undefined';
            } else if (v === null) {
                v = '';
            } else {
                v = v.toString();
            }
            self._value = v;
        });
    });



/**
 * HTMLTableRowElement mock implementation.
 */
Methanal.Tests.MockBrowser.Element.subclass(
    Methanal.Tests.MockBrowser, 'MockHTMLTableRowElement').methods(
    function __init__(self) {
        Methanal.Tests.MockBrowser.MockHTMLTableRowElement.upcall(
            self, '__init__', 'tr');
        self.cells = [];
    },


    /**
     * Insert an empty TD cell into this row. If index is -1 or equal to the
     * number of cells, the new cell is appended.
     */
    function insertCell(self, index) {
        var cell = document.createElement('td');
        if (index == -1) {
            self.cells.push(cell);
        } else {
            self.cells.splice(index, 0, cell);
        }
        return cell;
    });



/**
 * HTMLTableSectionElement mock implementation.
 */
Methanal.Tests.MockBrowser.Element.subclass(
    Methanal.Tests.MockBrowser, 'MockHTMLTableSectionElement').methods(
    function __init__(self, tagName) {
        Methanal.Tests.MockBrowser.MockHTMLTableSectionElement.upcall(
            self, '__init__', tagName);
        self.rows = [];
    },


    /**
     * Insert a new empty row in the table. The new row is inserted immediately
     * before and in the same section as the current indexth row in the table.
     * If index is -1 or equal to the number of rows, the new row is appended.
     * In addition, when the table is empty the row is inserted into a TBODY
     * which is created and inserted into the table.
     */
    function insertRow(self, index) {
        var row = document.createElement('tr');
        if (index == -1) {
            self.rows.push(row);
        } else {
            self.rows.splice(index, 0, row);
        }
        return row;
    });



/**
 * HTMLTableElement mock implementation.
 */
Methanal.Tests.MockBrowser.Element.subclass(
    Methanal.Tests.MockBrowser, 'MockHTMLTableElement').methods(
    function __init__(self) {
        Methanal.Tests.MockBrowser.MockHTMLTableElement.upcall(
            self, '__init__', 'table');
        self.deleteTHead();
        self.tBodies = [document.createElement('tbody')];
    },


    /**
     * Delete the header from the table, if one exists.
     */
    function deleteTHead(self) {
        self.tHead = null;
    },


    /**
     * Create a table header row or return an existing one.
     */
    function createTHead(self) {
        if (self.tHead !== null) {
            return self.tHead;
        }
        self.tHead = document.createElement('thead');
    });



/**
 * HTMLDocument mock implementation.
 */
Divmod.MockBrowser.Document.subclass(
    Methanal.Tests.MockBrowser, 'Document').methods(
    function __init__(self) {
        self._elementTags = {};
        Methanal.Tests.MockBrowser.Document.upcall(self, '__init__');
    },


    /**
     * Register a new type for a tag name.
     */
    function registerElementTag(self, tagName, type) {
        var old = self._elementTags[tagName];
        self._elementTags[tagName] = type;
        return old;
    },


    function createElement(self, tagName) {
        var el;
        if (self._elementTags[tagName]) {
            el = self._elementTags[tagName](tagName);
        } else {
            el = Methanal.Tests.MockBrowser.Element(tagName);
        }
        el._setOwnerDocument(self);
        self._allElements.push(el);
        return el;
    });



// Only override Divmod's mock document.
if (document instanceof Divmod.MockBrowser.Document) {
    if (!(document instanceof Methanal.Tests.MockBrowser.Document)) {
        document = Methanal.Tests.MockBrowser.Document();
        document.registerElementTag(
            'select', Methanal.Tests.MockBrowser.MockHTMLSelectElement);
        document.registerElementTag(
            'option', Methanal.Tests.MockBrowser.MockHTMLOptionElement);
        document.registerElementTag(
            'table', Methanal.Tests.MockBrowser.MockHTMLTableElement);
        document.registerElementTag(
            'thead', Methanal.Tests.MockBrowser.MockHTMLTableSectionElement);
        document.registerElementTag(
            'tbody', Methanal.Tests.MockBrowser.MockHTMLTableSectionElement);
        document.registerElementTag(
            'tr', Methanal.Tests.MockBrowser.MockHTMLTableRowElement);
    }
}
