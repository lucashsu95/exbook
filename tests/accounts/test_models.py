import pytest
from django.db import IntegrityError

from accounts.models import UserProfile
from tests.factories import UserFactory, UserProfileFactory


pytestmark = pytest.mark.django_db


class TestUserProfile:
    def test_create(self):
        profile = UserProfileFactory()
        assert profile.pk is not None
        assert profile.user is not None
        assert profile.created_at is not None
        assert profile.updated_at is not None

    def test_default_transferability(self):
        profile = UserProfileFactory()
        assert profile.default_transferability == UserProfile.Transferability.RETURN

    def test_str_nickname(self):
        profile = UserProfileFactory(nickname='小明')
        assert str(profile) == '小明'

    def test_str_fallback_full_name(self):
        user = UserFactory(first_name='明', last_name='王')
        profile = UserProfileFactory(user=user, nickname='')
        result = str(profile)
        # Falls back to get_full_name() or username
        assert result  # Non-empty

    def test_str_fallback_username(self):
        user = UserFactory(first_name='', last_name='')
        profile = UserProfileFactory(user=user, nickname='')
        assert str(profile) == user.username

    def test_one_to_one_user(self):
        user = UserFactory()
        UserProfileFactory(user=user)
        with pytest.raises(IntegrityError):
            UserProfileFactory(user=user)

    def test_transferability_choices(self):
        assert UserProfile.Transferability.TRANSFER == 'TRANSFER'
        assert UserProfile.Transferability.RETURN == 'RETURN'

    def test_available_schedule_default(self):
        profile = UserProfileFactory()
        assert profile.available_schedule == []

    def test_db_table(self):
        assert UserProfile._meta.db_table == 'exbook_user_profile'
