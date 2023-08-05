from pynYNAB.Entity import Entity, undef
from pynYNAB.schema.Fields import EntityField


class CatalogBudget(Entity):
    Fields= dict(
            budget_name=EntityField(None),
            is_tombstone=EntityField(None)
        )


class UserBudget(Entity):
    Fields= dict(
            budget_id=EntityField(undef),
            user_id=EntityField(None),
            is_tombstone=EntityField(False),
            permissions=EntityField(None)
        )


class UserSetting(Entity):
    Fields= dict(
            setting_name=EntityField(None),
            user_id=EntityField(None),
            setting_value=EntityField(None)
        )


class User(Entity):
    Fields= dict(
            username=EntityField(None),
            trial_expires_on=EntityField(None),
            is_tombstone=EntityField(False),
            email=EntityField(None)
        )


class BudgetVersion(Entity):
    Fields= dict(
            date_format=EntityField(None),
            last_accessed_on=EntityField(None),
            currency_format=EntityField(None),
            budget_id=EntityField(None),
            is_tombstone=EntityField(False),
            version_name=EntityField(None),
        )



