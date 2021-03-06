
from datetime import date

from factory import Sequence, post_generation, SubFactory
from factory.alchemy import SQLAlchemyModelFactory
from factory.fuzzy import FuzzyChoice, FuzzyText, FuzzyDate


from lemur.database import db
from lemur.authorities.models import Authority
from lemur.certificates.models import Certificate
from lemur.destinations.models import Destination
from lemur.notifications.models import Notification
from lemur.users.models import User
from lemur.roles.models import Role

from .vectors import INTERNAL_VALID_SAN_STR, PRIVATE_KEY_STR


class BaseFactory(SQLAlchemyModelFactory):
    """Base factory."""

    class Meta:
        """Factory configuration."""
        abstract = True
        sqlalchemy_session = db.session


class CertificateFactory(BaseFactory):
    """Certificate factory."""
    name = Sequence(lambda n: 'certificate{0}'.format(n))
    chain = INTERNAL_VALID_SAN_STR
    body = INTERNAL_VALID_SAN_STR
    private_key = PRIVATE_KEY_STR
    owner = 'joe@example.com'
    status = FuzzyChoice(['valid', 'revoked', 'unknown'])
    deleted = False
    description = FuzzyText(length=128)
    active = True
    date_created = FuzzyDate(date(2016, 1, 1), date(2020, 1, 1))

    class Meta:
        """Factory Configuration."""
        model = Certificate

    @post_generation
    def user(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.user_id = extracted.id

    @post_generation
    def authority(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.authority_id = extracted.id

    @post_generation
    def notifications(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for notification in extracted:
                self.notifications.append(notification)

    @post_generation
    def destinations(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for destination in extracted:
                self.destintations.append(destination)

    @post_generation
    def replaces(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for replace in extracted:
                self.replaces.append(replace)

    @post_generation
    def sources(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for source in extracted:
                self.sources.append(source)

    @post_generation
    def domains(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for domain in extracted:
                self.domains.append(domain)

    @post_generation
    def roles(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for domain in extracted:
                self.roles.append(domain)


class AuthorityFactory(BaseFactory):
    """Authority factory."""
    name = Sequence(lambda n: 'authority{0}'.format(n))
    owner = 'joe@example.com'
    plugin = {'slug': 'test-issuer'}
    authority_certificate = SubFactory(CertificateFactory)

    class Meta:
        """Factory configuration."""
        model = Authority

    @post_generation
    def roles(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for role in extracted:
                self.roles.append(role)


class DestinationFactory(BaseFactory):
    """Destination factory."""
    plugin_name = Sequence(lambda n: 'destination{0}'.format(n))
    label = Sequence(lambda n: 'destination{0}'.format(n))

    class Meta:
        """Factory Configuration."""
        model = Destination


class NotificationFactory(BaseFactory):
    """Notification factory."""
    plugin_name = Sequence(lambda n: 'notification{0}'.format(n))
    label = Sequence(lambda n: 'notification{0}'.format(n))

    class Meta:
        """Factory Configuration."""
        model = Notification


class RoleFactory(BaseFactory):
    """Role factory."""
    name = Sequence(lambda n: 'role{0}'.format(n))

    class Meta:
        """Factory Configuration."""
        model = Role

    @post_generation
    def users(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for user in extracted:
                self.users.append(user)


class UserFactory(BaseFactory):
    """User Factory."""
    username = Sequence(lambda n: 'user{0}'.format(n))
    email = Sequence(lambda n: 'user{0}@example.com'.format(n))
    active = True
    password = FuzzyText(length=24)

    class Meta:
        """Factory Configuration."""
        model = User

    @post_generation
    def roles(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for role in extracted:
                self.roles.append(role)

    @post_generation
    def certificates(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for cert in extracted:
                self.certificates.append(cert)

    @post_generation
    def authorities(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for authority in extracted:
                self.authorities.append(authority)
