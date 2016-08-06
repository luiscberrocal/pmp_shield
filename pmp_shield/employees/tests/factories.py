import string

from factory import Iterator, lazy_attribute, post_generation
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText
from faker import Factory as FakerFactory

from ..models import OrganizationUnit, Employee, Phone

faker = FakerFactory.create()


class EmployeeFactory(DjangoModelFactory):

    class Meta:
        model = Employee

    company_id = FuzzyText(length=6, chars=string.digits)
    office = Iterator(OrganizationUnit.objects.filter(parent__isnull=False))
    first_name = faker.first_name()
    middle_name = faker.first_name()
    last_name = faker.last_name()

    @lazy_attribute
    def username(self):
        return '%s.%s' % (self.first_name, self.last_name)

    @lazy_attribute
    def email(self):
        return '%s@mycompany.com' % (self.username)

    @post_generation
    def phones(self, create, extracted, **kwargs):
        if create:
            phone = PhoneFactory.create()
            self.phones.add(phone)
        else:
            return

        if extracted:
            # A list of groups were passed in, use them
            for phone in extracted:
                self.phones.add(phone)


class PhoneFactory(DjangoModelFactory):

    class Meta:
        model = Phone
    phone_number = faker.phone_number()
    phone_type = Iterator(Phone.PHONE_TYPES, getter= lambda c: c[0])

