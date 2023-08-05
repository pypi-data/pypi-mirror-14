from pydoc import locate

COMPARISON_EXACT = 'iexact'
COMPARISONS = (
    COMPARISON_EXACT,
)

CONNECTORS_OR = 'OR'
CONNECTORS_AND = 'AND'
CONNECTORS = (
    CONNECTORS_OR,
    CONNECTORS_AND,
)

AGGREGATES_SUM = 'SUM'
AGGREGATES = (
    AGGREGATES_SUM,
)

DjangoQ = locate('django.db.models.Q')
DjangoQuerySet = locate('django.db.models.QuerySet')
ObjectDoesNotExist = locate('django.core.exceptions.ObjectDoesNotExist')
MultipleObjectsReturned = locate('django.core.exceptions.MultipleObjectsReturned')
