from models import City, Country
import factory


class CityFactory(factory.DjangoModelFactory):
    remote_id = factory.Sequence(lambda n: n + 1)

    class Meta:
        model = City


class CountryFactory(factory.DjangoModelFactory):
    remote_id = factory.Sequence(lambda n: n + 1)

    class Meta:
        model = Country
