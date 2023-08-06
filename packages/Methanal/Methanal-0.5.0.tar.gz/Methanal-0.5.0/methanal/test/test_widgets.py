"""
Unit tests for L{methanal.widgets}.
"""
from functools import partial

from twisted.trial import unittest

from nevow import inevow

from xmantissa.webtheme import ThemedElement

from methanal import widgets, errors



class TabViewTests(unittest.TestCase):
    """
    Tests for L{methanal.widgets.TabView}.
    """
    def setUp(self):
        self.contentFactory = lambda: []
        self.tabs = [
            widgets.Tab(u'id1', u'Title 1', self.contentFactory),
            widgets.Tab(u'id2', u'Title 2', self.contentFactory),
            widgets.Tab(u'id3', u'Title 3', self.contentFactory)]
        self.tabView = widgets.TabView(self.tabs)


    def test_create(self):
        """
        Creating a L{TabView} widget initialises L{TabView._tabsByID} and
        L{TabView.tabs} with the values originally specified.
        """
        self.assertEquals(
            sorted(self.tabView._tabsByID.keys()),
            [u'id1', u'id2', u'id3'])
        self.assertEquals(
            self.tabView.tabs,
            self.tabs)


    def test_createGroup(self):
        """
        Creating a L{methanal.widgets.TabView} widget initialises
        L{methanal.widgets.TabView._tabsByID}, L{methanal.widgets.TabView.tabs}
        and L{methanal.widgets.TabView._tabGroups} with the values originally
        specified, tab groups are merged in and managed.
        """
        tabGroup = widgets.TabGroup(u'group1', u'Group', tabs=[
            widgets.Tab(u'id4', u'Title 4', self.contentFactory)])
        tabs = self.tabs + [
            tabGroup,
            widgets.Tab(u'id5', u'Title 5', self.contentFactory)]
        tabView = widgets.TabView(tabs)
        self.assertEquals(
            tabView.getTabIDs(),
            [u'id1', u'id2', u'id3', u'id4', u'id5'])
        self.assertEquals(
            tabView._tabGroups,
            {u'group1': tabGroup})


    def test_updateTabs(self):
        """
        Updating tabs on the server side manages them and invokes methods
        on the client side to insert them.
        """
        self.result = None

        def callRemote(methodName, *a):
            self.result = methodName == '_updateTabsFromServer'

        tab = widgets.Tab(u'id4', u'Title 4', self.contentFactory)
        self.patch(self.tabView, 'callRemote', callRemote)
        self.tabView.updateTabs([tab])
        self.assertTrue(self.result)
        self.assertNotIdentical(self.tabView.getTab(u'id4'), None)
        self.assertIdentical(self.tabView.tabs[-1], tab)

        replacementTab = widgets.Tab(u'id1', u'New title', self.contentFactory)
        oldTab = self.tabView.getTab(u'id1')
        self.tabView.updateTabs([replacementTab])
        self.assertIdentical(self.tabView.getTab(u'id1'), replacementTab)
        self.assertNotIn(oldTab, self.tabView.tabs)


    def test_updateGroup(self):
        """
        Updating a group on the server site manages it, and all the tabs it
        contains, and invokes methods on the client side to insert them.
        """
        self.result = None

        def callRemote(methodName, *a):
            self.result = methodName == '_updateTabsFromServer'

        tab = widgets.Tab(u'id4', u'Title 4', self.contentFactory)
        group = widgets.TabGroup(u'group1', u'Group', tabs=[tab])
        self.patch(self.tabView, 'callRemote', callRemote)
        self.tabView.updateGroup(group)
        self.assertTrue(self.result)
        self.assertNotIdentical(self.tabView.getTab(u'id4'), None)
        self.assertNotIdentical(self.tabView.getGroup(u'group1'), None)
        self.assertIdentical(self.tabView.tabs[-1], tab)

        # Update a group, and add a new tab.
        newTab = widgets.Tab(u'id5', u'Title 5', self.contentFactory)
        replacementGroup = widgets.TabGroup(
            u'group1', u'New Group', tabs=[newTab])
        self.tabView.updateGroup(replacementGroup)
        self.assertIdentical(
            self.tabView.getGroup(u'group1'), replacementGroup)
        self.assertNotIdentical(self.tabView.getTab(u'id5'), None)
        self.assertRaises(
            errors.InvalidIdentifier, self.tabView.getTab, u'id4')
        self.assertNotIn(tab, self.tabView.tabs)

        # Remove a tab from a group.
        self.tabView.removeTabs([newTab])
        self.assertRaises(
            errors.InvalidIdentifier, self.tabView.getTab, u'id5')
        self.assertNotIn(newTab, self.tabView.getGroup(u'group1').tabs)


    def test_removeTabs(self):
        """
        Removing tabs on the server side releases them and invokes methods on
        the client side to remove them.
        """
        self.result = None

        def callRemote(methodName, *a):
            self.result = methodName == '_removeTabsFromServer'

        self.patch(self.tabView, 'callRemote', callRemote)
        tab = self.tabView.tabs[0]
        self.tabView.removeTabs([tab])
        self.assertTrue(self.result)
        self.assertRaises(
            errors.InvalidIdentifier, self.tabView.getTab, tab.id)


    def test_invalidRemove(self):
        """
        Trying to remove an unmanaged tab results in C{ValueError} being
        raised.
        """
        # Try a new tab.
        self.assertRaises(ValueError,
            self.tabView.removeTabs, [
                widgets.Tab(u'id99', u'Title 1', self.contentFactory)])

        # Try dupe an ID.
        self.assertRaises(ValueError,
            self.tabView.removeTabs, [
                widgets.Tab(u'id1', u'Title 1', self.contentFactory)])


    def test_repr(self):
        """
        L{methanal.widgets.TabView} has an accurate string representation.
        """
        self.assertEquals(
            repr(self.tabView),
            "<TabView topLevel=False tabs=%r>" % self.tabs)



class StaticTabTests(unittest.TestCase):
    """
    Tests for L{methanal.widgets.StaticTab}.
    """
    def test_create(self):
        """
        Creating a L{methanal.widgets.StaticTab} instance, with the C{content}
        argument, wraps the content in a factory method. Passing a
        C{contentFactory} argument works as intended.
        """
        content = u'A content.'
        tab = widgets.StaticTab(
            id=u'id',
            title=u'Title',
            content=content)
        self.assertEquals(tab.contentFactory(), content)

        tab = widgets.StaticTab(
            id=u'id',
            title=u'Title',
            contentFactory=lambda: content * 2)
        self.assertEquals(tab.contentFactory(), content * 2)


    def test_repr(self):
        """
        L{methanal.widgets.Tab} (and by extension L{methanal.widgets.StaticTab})
        has an accurate string representation.
        """
        tab = widgets.StaticTab(
            id=u'id',
            title=u'Title',
            content=u'A content.')
        self.assertEquals(
            repr(tab),
            "<StaticTab id=u'id' title=u'Title' selected=False group=None>")




class TabGroupTests(unittest.TestCase):
    """
    Tests for L{methanal.widgets.TabGroup}.
    """
    def test_athenaSerializable(self):
        """
        Tab groups implement L{nevow.inevow.IAthenaTransportable}.
        """
        tabs = [
            widgets.Tab(u'id1', u'Title 1', None),
            widgets.Tab(u'id2', u'Title 2', None)]
        tabGroup = widgets.TabGroup(u'id', u'Title', tabs=tabs)
        self.assertEquals(
            inevow.IAthenaTransportable(tabGroup).getInitialArguments(),
            [u'id', u'Title', [u'id1', u'id2']])


    def test_mergeGroups(self):
        """
        L{methanal.widgets.TabGroup.mergeGroups} will merge two
        L{methanal.widgets.TabGroup}s together, preferring the metadata of the
        second specified group.
        """
        tabs = [
            widgets.Tab(u'id1', u'Title 1', None),
            widgets.Tab(u'id2', u'Title 2', None)]
        tabGroup1 = widgets.TabGroup(u'id', u'Title', tabs=tabs)
        tabs = [
            widgets.Tab(u'id3', u'Title 3', None)]
        tabGroup2 = widgets.TabGroup(u'id', u'Hello', tabs=tabs)

        newGroup = widgets.TabGroup.mergeGroups(tabGroup1, tabGroup2)
        self.assertEquals(newGroup.id, u'id')
        self.assertEquals(newGroup.title, u'Hello')
        self.assertEquals(newGroup.tabs, tabGroup1.tabs + tabGroup2.tabs)


    def test_repr(self):
        """
        L{methanal.widgets.TabGroup} has an accurate string representation.
        """
        tabs = [
            widgets.Tab(u'id1', u'Title 1', None),
            widgets.Tab(u'id2', u'Title 2', None)]
        tabGroup = widgets.TabGroup(u'id', u'Title', tabs=tabs)
        self.assertEquals(
            repr(tabGroup),
            "<TabGroup id=u'id' title=u'Title' tabs=%r>" % tabs)



class ComparableLiveElement(ThemedElement):
    """
    C{LiveElement} implementing C{__eq__} comparing C{self.value}.
    """
    def __init__(self, value):
        self.value = value


    def __eq__(self, other):
        try:
            return self.value == other.value
        except AttributeError:
            return False



class ExpanderTests(unittest.TestCase):
    """
    Tests for L{methanal.widgets.Expander}.
    """
    def test_getContent(self):
        """
        L{Expander.getContent} returns the content for the specified node ID,
        C{KeyError} is raised if an unknown node ID is specified.
        """
        expander = widgets.Expander(
            headerFactory=partial(ComparableLiveElement, u'foo'),
            contentFactory=partial(ComparableLiveElement, u'bar'))
        self.assertEqual(
            expander.getContent(u'header').value, u'foo')
        self.assertEqual(
            expander.getContent(u'content').value, u'bar')
        self.assertRaises(
            KeyError, expander.getContent, u'not_a_thing')


    def test_lazyHeaderContent(self):
        """
        L{Expander.getHeaderContent} returns the result of
        L{Expander.headerFactory} if C{currentContent == newContent} returns
        C{False}, otherwise C{None} is returned.
        """
        expander = widgets.Expander(
            headerFactory=partial(ComparableLiveElement, u'content'),
            contentFactory=None)

        # Fresh.
        content = expander.getHeaderContent()
        self.assertNotIdentical(None, content)
        self.assertEqual(u'content', content.value)
        # Same as last time
        self.assertIdentical(None, expander.getHeaderContent())
        # New value.
        expander.headerFactory = partial(ComparableLiveElement, u'other')
        content = expander.getHeaderContent()
        self.assertNotIdentical(None, content)
        self.assertEqual(u'other', content.value)


    def test_lazyExpanderContent(self):
        """
        L{Expander.getExpanderContent} returns the result of
        L{Expander.contentFactory} if C{currentContent == newContent} returns
        C{False}, otherwise C{None} is returned.
        """
        expander = widgets.Expander(
            headerFactory=None,
            contentFactory=partial(ComparableLiveElement, u'content'))

        # Fresh.
        content = expander.getExpanderContent()
        self.assertNotIdentical(None, content)
        self.assertEqual(u'content', content.value)
        # Same as last time
        self.assertIdentical(None, expander.getExpanderContent())
        # New value.
        expander.contentFactory = partial(ComparableLiveElement, u'other')
        content = expander.getExpanderContent()
        self.assertNotIdentical(None, content)
        self.assertEqual(u'other', content.value)
