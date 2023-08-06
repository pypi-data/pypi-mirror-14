import pytest
from datetime import datetime
from bson import ObjectId, DBRef
from functools import namedtuple

from .fixtures import collection_moke, dal_moke, moked_lazy_loader

from umongo import Document, Schema, fields, exceptions
from umongo.abstract import AbstractDal
from umongo.registerer import default_registerer


class Student(Document):

    name = fields.StrField(required=True)
    birthday = fields.DateTimeField()
    gpa = fields.FloatField()

    class Meta:
        allow_inheritance = True


class TestDocument:

    def setup(self):
        default_registerer.documents = {}

    def test_repr(self):
        # I love readable stuff !
        john = Student(name='John Doe', birthday=datetime(1995, 12, 12), gpa=3.0)
        assert 'tests.test_document.Student' in repr(john)
        assert 'name' in repr(john)
        assert 'birthday' in repr(john)
        assert 'gpa' in repr(john)

    def test_create(self):
        john = Student(name='John Doe', birthday=datetime(1995, 12, 12), gpa=3.0)
        assert john.to_mongo() == {
            'name': 'John Doe',
            'birthday': datetime(1995, 12, 12),
            'gpa': 3.0
        }
        assert john.created is False
        with pytest.raises(exceptions.NotCreatedError):
            john.to_mongo(update=True)

    def test_from_mongo(self):
        john = Student.build_from_mongo(data={
            'name': 'John Doe', 'birthday': datetime(1995, 12, 12), 'gpa': 3.0})
        assert john.to_mongo(update=True) is None
        assert john.created is True
        assert john.to_mongo() == {
            'name': 'John Doe',
            'birthday': datetime(1995, 12, 12),
            'gpa': 3.0
        }

    def test_update(self):
        john = Student.build_from_mongo(data={
            'name': 'John Doe', 'birthday': datetime(1995, 12, 12), 'gpa': 3.0})
        john.name = 'William Doe'
        john.birthday = datetime(1996, 12, 12)
        assert john.to_mongo(update=True) == {
            '$set': {'name': 'William Doe', 'birthday': datetime(1996, 12, 12)}}
        john.clear_modified()
        assert john.to_mongo(update=True) is None

    def test_dump(self):
        john = Student.build_from_mongo(data={
            'name': 'John Doe', 'birthday': datetime(1995, 12, 12), 'gpa': 3.0})
        assert john.dump() == {
            'name': 'John Doe',
            'birthday': '1995-12-12T00:00:00+00:00',
            'gpa': 3.0
        }

    def test_fields_by_attr(self):
        john = Student.build_from_mongo(data={
            'name': 'John Doe', 'birthday': datetime(1995, 12, 12), 'gpa': 3.0})
        assert john.name == 'John Doe'
        john.name = 'William Doe'
        assert john.name == 'William Doe'
        del john.name
        assert john.name is None
        with pytest.raises(AttributeError):
            john.missing
        with pytest.raises(AttributeError):
            john.missing = None
        with pytest.raises(AttributeError):
            del john.missing
        with pytest.raises(AttributeError):
            del john.commit

    def test_fields_by_items(self):
        john = Student.build_from_mongo(data={
            'name': 'John Doe', 'birthday': datetime(1995, 12, 12), 'gpa': 3.0})
        assert john['name'] == 'John Doe'
        john['name'] = 'William Doe'
        assert john['name'] == 'William Doe'
        del john['name']
        assert john['name'] is None
        with pytest.raises(KeyError):
            john['missing']
        with pytest.raises(KeyError):
            john['missing'] = None
        with pytest.raises(KeyError):
            del john['missing']

    def test_pk(self):
        john = Student.build_from_mongo(data={
            'name': 'John Doe', 'birthday': datetime(1995, 12, 12), 'gpa': 3.0})
        assert john.pk is None
        john_id = ObjectId("5672d47b1d41c88dcd37ef05")
        john = Student.build_from_mongo(data={
            '_id': john_id, 'name': 'John Doe',
            'birthday': datetime(1995, 12, 12), 'gpa': 3.0})
        assert john.pk == john_id

        # Don't do that in real life !
        class CrazyNaming(Document):
            id = fields.IntField(attribute='in_mongo_id')
            _id = fields.IntField(attribute='in_mongo__id')
            pk = fields.IntField()
            real_pk = fields.IntField(attribute='_id')

        crazy = CrazyNaming.build_from_mongo(data={
            '_id': 1, 'in_mongo__id': 2, 'in_mongo__id': 3, 'pk': 4
            })
        assert crazy.pk == crazy.real_pk == 1
        assert crazy['pk'] == 4

    def test_dbref(self, collection_moke):

        class ConfiguredStudent(Student):
            id = fields.IntField(attribute='_id')

            class Meta:
                collection = collection_moke

        student = ConfiguredStudent()

        with pytest.raises(exceptions.NotCreatedError):
            student.dbref

        # Fake document creation
        student.id = 1
        student.created = True
        student.clear_modified()

        assert student.dbref == DBRef(collection=collection_moke.name, id=1)

    def test_equality(self, collection_moke):

        class ConfiguredStudent(Student):
            id = fields.IntField(attribute='_id')

            class Meta:
                collection = collection_moke

        john_data = {
            '_id': 42, 'name': 'John Doe', 'birthday': datetime(1995, 12, 12), 'gpa': 3.0
        }
        john = ConfiguredStudent.build_from_mongo(data=john_data)
        john2 = ConfiguredStudent.build_from_mongo(data=john_data)
        phillipe = ConfiguredStudent.build_from_mongo(data={
            '_id': 3, 'name': 'Phillipe J. Fry', 'birthday': datetime(1995, 12, 12), 'gpa': 3.0})

        assert john != phillipe
        assert john2 == john
        assert john == DBRef(collection=collection_moke.name, id=john.pk)

        john.name = 'William Doe'
        assert john == john2

        newbie = ConfiguredStudent(name='Newbie')
        newbie2 = ConfiguredStudent(name='Newbie')
        assert newbie != newbie2

    def test_dal_connection(self, collection_moke):

        class ConfiguredStudent(Student):
            id = fields.IntField(attribute='_id')

            class Meta:
                collection = collection_moke

        newbie = ConfiguredStudent(name='Newbie')

        def commiter(doc, io_validate_all=False):
            doc.created = True

        collection_moke.push_callback('commit', callback=commiter)
        collection_moke.push_callback('reload')
        collection_moke.push_callback('delete')
        collection_moke.push_callback('find_one')
        collection_moke.push_callback('find')
        collection_moke.push_callback('io_validate')

        with collection_moke:
            newbie.commit()
            newbie.reload()
            newbie.delete()
            newbie.find_one()
            newbie.find()
            newbie.io_validate()

    def test_required_fields(self):

        # Should be able to instanciate document without there required field
        student = Student()
        student = Student(gpa=2.8)
        # Required check is done in `io_validate`, cannot go further without a dal

    def test_auto_id_field(self):
        my_id = ObjectId('5672d47b1d41c88dcd37ef05')

        class AutoId(Document):

            class Meta:
                register = False
                allow_inheritance = True

        assert 'id' in AutoId.schema.fields

        # default id field is only dumpable
        with pytest.raises(exceptions.ValidationError):
            AutoId(id=my_id)

        autoid = AutoId.build_from_mongo({'_id': my_id})
        assert autoid.id == my_id
        assert autoid.pk == autoid.id
        assert autoid.dump() == {'id': '5672d47b1d41c88dcd37ef05'}

        class AutoIdInheritance(AutoId):
            pass

        assert 'id' in AutoIdInheritance.schema.fields

    def test_custom_id_field(self):
        my_id = ObjectId('5672d47b1d41c88dcd37ef05')

        class CustomId(Document):
            int_id = fields.IntField(attribute='_id')

            class Meta:
                register = False
                allow_inheritance = True

        assert 'id' not in CustomId.schema.fields
        with pytest.raises(exceptions.ValidationError):
            CustomId(id=my_id)
        customid = CustomId(int_id=42)
        assert customid.int_id == 42
        assert customid.pk == customid.int_id
        assert customid.to_mongo() == {'_id': 42}

        class CustomIdInheritance(CustomId):
            pass

        assert 'id' in CustomIdInheritance.schema.fields


class TestConfig:

    def test_missing_schema(self):
        # No exceptions should occur

        class Doc1(Document):
            pass

        d = Doc1()
        assert isinstance(d.schema, Schema)

    def test_base_config(self):

        class Doc2(Document):
            pass

        assert Doc2.opts.collection is None
        assert Doc2.opts.lazy_collection is None
        assert Doc2.opts.dal is None
        assert Doc2.opts.register_document is True

    def test_lazy_collection(self, moked_lazy_loader, collection_moke):

        def lazy_factory():
            return collection_moke

        class Doc3(Document):

            class Meta:
                lazy_collection = moked_lazy_loader(lazy_factory)

        assert Doc3.opts.collection is None
        assert Doc3.opts.dal is Doc3.Meta.lazy_collection.dal
        assert issubclass(Doc3, Doc3.Meta.lazy_collection.dal)
        # Try to do the dereferencing
        assert Doc3.collection is collection_moke
        d = Doc3()
        assert d.collection is collection_moke

    def test_custom_dal_lazy_collection(self, request, moked_lazy_loader, collection_moke):

        dal_moke_2 = dal_moke(request, collection_moke)

        def lazy_factory():
            return collection_moke

        class Doc3(Document):

            class Meta:
                lazy_collection = moked_lazy_loader(lazy_factory)
                dal = dal_moke_2
                register_document = False

        assert Doc3.opts.dal is dal_moke_2
        assert issubclass(Doc3, dal_moke_2)

    def test_inheritance(self, request):
        col1 = collection_moke(request, name='col1')
        col2 = collection_moke(request, name='col2')

        class AbsDoc(Document):

            class Meta:
                register_document = False
                abstract = True

        class Doc4Child1(AbsDoc):

            class Meta:
                collection = col1
                allow_inheritance = True
                register_document = False

        class Doc4Child1Child(Doc4Child1):
            pass

        class Doc4Child2(AbsDoc):

            class Meta:
                collection = col2

        assert Doc4Child1.opts.collection is col1
        assert Doc4Child1Child.opts.collection is col1
        assert Doc4Child1Child.opts.allow_inheritance is False
        assert Doc4Child1.opts.register_document is False
        assert Doc4Child2.opts.register_document is True
        assert Doc4Child2.opts.collection == col2
        assert Doc4Child2.opts.register_document is True

    def test_bad_inheritance(self, request):
        with pytest.raises(exceptions.DocumentDefinitionError) as exc:
            class BadAbstractDoc(Document):
                class Meta:
                    allow_inheritance = False
                    abstract = True
        assert exc.value.args[0] == "Abstract document cannot disable inheritance"

        class NotParent(Document):
            pass

        assert not NotParent.opts.allow_inheritance

        with pytest.raises(exceptions.DocumentDefinitionError) as exc:
            class ImpossibleChildDoc(NotParent):
                pass
        assert exc.value.args[0] == ("Document"
            " <class 'tests.test_document.TestConfig.test_bad_inheritance.<locals>.NotParent'>"
            " doesn't allow inheritance")

        class NotAbstractParent(Document):
            class Meta:
                allow_inheritance = True

        with pytest.raises(exceptions.DocumentDefinitionError) as exc:
            class ImpossibleChildDoc(NotAbstractParent):
                class Meta:
                    abstract = True
        assert exc.value.args[0] == "Abstract document should have all it parents abstract"

        col1 = collection_moke(request, name='col1')
        col2 = collection_moke(request, name='col2')

        class ParentWithCol1(Document):
            class Meta:
                allow_inheritance = True
                collection = col1

        class ParentWithCol2(Document):
            class Meta:
                allow_inheritance = True
                collection = col2

        with pytest.raises(exceptions.DocumentDefinitionError) as exc:
            class ImpossibleChildDoc(ParentWithCol1, ParentWithCol2):
                pass
        assert exc.value.args[0].startswith("collection cannot be defined multiple times")


    def test_bad_config(self):
        with pytest.raises(exceptions.NoCollectionDefinedError) as exc:
            class BadConf(Document):
                class Meta:
                    collection = object()
                    lazy_collection = lambda: None
        assert exc.value.args[0] == (
            "Cannot define at the same time `collection` and `lazy_collection`")

    def test_no_collection(self):

        class Doc5(Document):
            pass

        with pytest.raises(exceptions.NoCollectionDefinedError):
            Doc5.collection

        with pytest.raises(exceptions.NoCollectionDefinedError):
            Doc5().collection

    def test_bad_lazy_collection(self, dal_moke):

        # Bad `dal` attribute
        with pytest.raises(exceptions.NoCollectionDefinedError) as exc:

            class Doc7(Document):

                class Meta:
                    lazy_collection = lambda: None

                    class dal:
                        pass
        assert exc.value.args[0] == (
            "`dal` attribute must be a subclass of <class 'umongo.abstract.AbstractDal'>")

        # Invalid lazy_collection's dal
        LazyCollection = namedtuple('LazyCollection', ('dal', 'load'))

        class BadDal:
            pass

        def load_collection():
            pass

        with pytest.raises(exceptions.NoCollectionDefinedError) as exc:
            class Doc8(Document):
                class Meta:
                    lazy_collection = LazyCollection(BadDal, load_collection)
        assert exc.value.args[0] == (
            "`dal` attribute must be a subclass of <class 'umongo.abstract.AbstractDal'>")

        # Invalid lazy_collection's load
        class GoodDal(AbstractDal):
            @staticmethod
            def io_validate_patch_schema(schema):
                pass

        class Doc9(Document):
            class Meta:
                lazy_collection = LazyCollection(GoodDal, load_collection)

        with pytest.raises(exceptions.NoCollectionDefinedError) as exc:
            Doc9.collection
        assert exc.value.args[0] == "lazy_collection didn't returned a collection"
