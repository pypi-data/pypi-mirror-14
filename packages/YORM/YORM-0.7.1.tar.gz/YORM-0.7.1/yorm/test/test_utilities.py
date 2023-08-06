# pylint: disable=unused-variable,expression-not-assigned
# pylint: disable=missing-docstring,no-self-use,no-member,misplaced-comparison-constant

import logging
from unittest.mock import patch, Mock

import pytest
from expecter import expect

from yorm import exceptions
from yorm import utilities
from yorm.bases import Converter, Mappable

log = logging.getLogger(__name__)

# CLASSES ######################################################################


class MockConverter(Converter):
    """Sample converter class."""

    @classmethod
    def create_default(cls):
        return None

    @classmethod
    def to_value(cls, *_):
        return None

    @classmethod
    def to_data(cls, _):
        return None


class MockConverter0(MockConverter):
    """Sample converter class."""


class MockConverter1(MockConverter):
    """Sample converter class."""


class MockConverter2(MockConverter):
    """Sample converter class."""


class MockConverter3(MockConverter):
    """Sample converter class."""


class MockConverter4(MockConverter):
    """Sample converter class."""


class MockMappable(Mappable):
    """Sample mappable class."""

    __mapper__ = Mock()
    __mapper__.attrs = {}


# TESTS ########################################################################


@patch('yorm.diskutils.write', Mock())
@patch('yorm.diskutils.stamp', Mock())
@patch('yorm.diskutils.read', Mock(return_value=""))
class TestSyncObject:
    """Unit tests for the `sync_object` function."""

    class Sample:
        """Sample class."""

    def test_no_attrs(self):
        """Verify mapping can be enabled with no attributes."""
        sample = utilities.sync(self.Sample(), "sample.yml")
        assert "sample.yml" == sample.__mapper__.path
        assert {} == sample.__mapper__.attrs

    def test_with_attrs(self):
        """Verify mapping can be enabled with with attributes."""
        attrs = {'var1': MockConverter}
        sample = utilities.sync(self.Sample(), "sample.yml", attrs)
        assert "sample.yml" == sample.__mapper__.path
        assert {'var1': MockConverter} == sample.__mapper__.attrs

    def test_multiple(self):
        """Verify mapping cannot be enabled twice."""
        sample = utilities.sync(self.Sample(), "sample.yml")
        with pytest.raises(exceptions.MappingError):
            utilities.sync(sample, "sample.yml")

    @patch('yorm.diskutils.exists', Mock(return_value=True))
    def test_init_existing(self):
        """Verify an existing file is read."""
        with patch('yorm.diskutils.read', Mock(return_value="abc: 123")):
            sample = utilities.sync(self.Sample(), "sample.yml", strict=False)
        assert 123 == sample.abc

    @patch('yorm.diskutils.exists', Mock(return_value=False))
    def test_exception_when_file_expected_but_missing(self):
        utilities.sync(self.Sample(), "sample.yml", existing=False)
        with pytest.raises(exceptions.FileMissingError):
            utilities.sync(self.Sample(), "sample.yml", existing=True)

    @patch('yorm.diskutils.exists', Mock(return_value=True))
    def test_exception_when_file_not_expected_but_found(self):
        utilities.sync(self.Sample(), "sample.yml", existing=True)
        with pytest.raises(exceptions.FileAlreadyExistsError):
            utilities.sync(self.Sample(), "sample.yml", existing=False)


@patch('yorm.diskutils.write', Mock())
@patch('yorm.diskutils.stamp', Mock())
@patch('yorm.diskutils.read', Mock(return_value=""))
class TestSyncInstances:
    """Unit tests for the `sync_instances` decorator."""

    @utilities.sync("sample.yml", strict=False)
    class SampleDecorated:
        """Sample decorated class using a single path."""

        def __repr__(self):
            return "<decorated {}>".format(id(self))

    @utilities.sync("{UUID}.yml")
    class SampleDecoratedIdentifiers:
        """Sample decorated class using UUIDs for paths."""

        def __repr__(self):
            return "<decorated w/ UUID {}>".format(id(self))

    @utilities.sync("path/to/{n}.yml", {'n': 'name'})
    class SampleDecoratedAttributes:
        """Sample decorated class using an attribute value for paths."""

        def __init__(self, name):
            self.name = name

        def __repr__(self):
            return "<decorated w/ specified attributes {}>".format(id(self))

    @utilities.sync("path/to/{self.name}.yml")
    class SampleDecoratedAttributesAutomatic:
        """Sample decorated class using an attribute value for paths."""

        def __init__(self, name):
            self.name = name

        def __repr__(self):
            return "<decorated w/ automatic attributes {}>".format(id(self))

    @utilities.sync("{self.a}/{self.b}/{c}.yml", {'self.b': 'b', 'c': 'c'})
    class SampleDecoratedAttributesCombination:
        """Sample decorated class using an attribute value for paths."""

        def __init__(self, a, b, c):
            self.a = a
            self.b = b
            self.c = c

        def __repr__(self):
            return "<decorated w/ attributes {}>".format(id(self))

    @utilities.sync("sample.yml", attrs={'var1': MockConverter})
    class SampleDecoratedWithAttributes:
        """Sample decorated class using a single path."""

    @utilities.sync("sample.yml", attrs={'var1': MockConverter}, auto=False)
    class SampleDecoratedWithAttributesAutoOff:
        """Sample decorated class using a single path."""

    def test_no_attrs(self):
        """Verify mapping can be enabled with no attributes."""
        sample = self.SampleDecorated()
        assert "sample.yml" == sample.__mapper__.path
        assert {} == sample.__mapper__.attrs

    def test_with_attrs(self):
        """Verify mapping can be enabled with with attributes."""
        sample = self.SampleDecoratedWithAttributes()
        assert "sample.yml" == sample.__mapper__.path
        assert ['var1'] == list(sample.__mapper__.attrs.keys())

    @patch('yorm.diskutils.exists', Mock(return_value=True))
    def test_init_existing(self):
        """Verify an existing file is read."""
        with patch('yorm.diskutils.read', Mock(return_value="abc: 123")):
            sample = self.SampleDecorated()
        assert 123 == sample.abc

    @patch('uuid.uuid4', Mock(return_value=Mock(hex='abc123')))
    def test_filename_uuid(self):
        """Verify UUIDs can be used for filename."""
        sample = self.SampleDecoratedIdentifiers()
        assert "abc123.yml" == sample.__mapper__.path
        assert {} == sample.__mapper__.attrs

    def test_filename_attributes(self):
        """Verify attributes can be used to determine filename."""
        sample1 = self.SampleDecoratedAttributes('one')
        sample2 = self.SampleDecoratedAttributes('two')
        assert "path/to/one.yml" == sample1.__mapper__.path
        assert "path/to/two.yml" == sample2.__mapper__.path

    def test_filename_attributes_automatic(self):
        """Verify attributes can be used to determine filename (auto)."""
        sample1 = self.SampleDecoratedAttributesAutomatic('one')
        sample2 = self.SampleDecoratedAttributesAutomatic('two')
        assert "path/to/one.yml" == sample1.__mapper__.path
        assert "path/to/two.yml" == sample2.__mapper__.path

    def test_filename_attributes_combination(self):
        """Verify attributes can be used to determine filename (combo)."""
        log.info("Creating first object...")
        sample1 = self.SampleDecoratedAttributesCombination('A', 'B', 'C')
        log.info("Creating second object...")
        sample2 = self.SampleDecoratedAttributesCombination(1, 2, 3)
        assert "A/B/C.yml" == sample1.__mapper__.path
        assert "1/2/3.yml" == sample2.__mapper__.path


def describe_attr():

    path = "mock/path"

    @utilities.attr(var1=MockConverter1)
    @utilities.sync(path)
    class SampleDecoratedSingle:
        """Class using single `attr` decorator."""

    @utilities.attr(var1=MockConverter1)
    @utilities.attr(var2=MockConverter2)
    @utilities.sync(path)
    class SampleDecoratedMultiple:
        """Class using multiple `attr` decorators."""

    @utilities.attr(var2=MockConverter2)
    @utilities.sync(path, attrs={'var1': MockConverter1})
    class SampleDecoratedCombo:
        """Class using `attr` decorator and providing a mapping."""

    @utilities.sync(path, attrs={'var1': MockConverter1})
    @utilities.attr(var2=MockConverter2)
    class SampleDecoratedBackwards:
        """Class using `attr` decorator after `sync` decorator."""

    def it_accepts_one_argument():
        sample = SampleDecoratedSingle()
        expect(sample.__mapper__.attrs) == {'var1': MockConverter1}

    def it_rejects_zero_arguments():
        with expect.raises(ValueError):
            utilities.attr()

    def it_rejects_more_than_one_argument():
        with expect.raises(ValueError):
            utilities.attr(foo=1, bar=2)

    def it_can_be_applied_multiple_times():
        sample = SampleDecoratedMultiple()
        expect(sample.__mapper__.attrs) == {'var1': MockConverter1,
                                            'var2': MockConverter2}

    def it_can_be_applied_before_sync():
        sample = SampleDecoratedCombo()
        expect(sample.__mapper__.attrs) == {'var1': MockConverter1,
                                            'var2': MockConverter2}

    def it_can_be_applied_after_sync():
        sample = SampleDecoratedBackwards()
        expect(sample.__mapper__.attrs) == {'var1': MockConverter1,
                                            'var2': MockConverter2}


class TestUpdate:
    """Unit tests for the `update` function."""

    def test_update(self):
        """Verify the object and file are updated."""
        instance = MockMappable()
        instance.__mapper__.reset_mock()

        utilities.update(instance)

        assert instance.__mapper__.fetch.called
        assert instance.__mapper__.store.called

    def test_update_object_only(self):
        """Verify only the object is updated."""
        instance = MockMappable()
        instance.__mapper__.reset_mock()

        utilities.update(instance, store=False)

        assert instance.__mapper__.fetch.called
        assert not instance.__mapper__.store.called

    def test_update_file_only(self):
        """Verify only the file is updated."""
        instance = MockMappable()
        instance.__mapper__.reset_mock()

        utilities.update(instance, fetch=False)

        assert not instance.__mapper__.fetch.called
        assert instance.__mapper__.store.called

    def test_update_wrong_base(self):
        """Verify an exception is raised with the wrong base."""
        instance = Mock()

        with pytest.raises(exceptions.MappingError):
            utilities.update(instance)


class TestUpdateObject:
    """Unit tests for the `update_object` function."""

    def test_update(self):
        """Verify only the object is updated."""
        instance = MockMappable()
        instance.__mapper__.reset_mock()

        utilities.update_object(instance)

        assert instance.__mapper__.fetch.called
        assert not instance.__mapper__.store.called

    def test_update_wrong_base(self):
        """Verify an exception is raised with the wrong base."""
        instance = Mock()

        with pytest.raises(exceptions.MappingError):
            utilities.update_object(instance)


class TestUpdateFile:
    """Unit tests for the `update_file` function."""

    def test_update(self):
        """Verify only the file is updated."""
        instance = MockMappable()
        instance.__mapper__.reset_mock()

        utilities.update_file(instance)

        assert False is instance.__mapper__.fetch.called
        assert True is instance.__mapper__.store.called

    def test_update_wrong_base(self):
        """Verify an exception is raised with the wrong base."""
        instance = Mock()

        with pytest.raises(exceptions.MappingError):
            utilities.update_file(instance)

    def test_store_not_called_with_auto_off(self):
        instance = MockMappable()
        instance.__mapper__.reset_mock()
        instance.__mapper__.auto = False

        utilities.update_file(instance, force=False)

        assert False is instance.__mapper__.fetch.called
        assert False is instance.__mapper__.store.called

    def test_create_called_if_the_file_is_missing(self):
        instance = MockMappable()
        instance.__mapper__.reset_mock()
        instance.__mapper__.exists = False

        utilities.update_file(instance)

        assert False is instance.__mapper__.fetch.called
        assert True is instance.__mapper__.create.called
        assert True is instance.__mapper__.store.called
