from modeltranslation.translator import translator, TranslationOptions
from ehriportal.repositories.models import Repository, Contact

class RepositoryTranslationOptions(TranslationOptions):
    fields = (
        "access_conditions",
        "buildings",
        "collecting_policies",
        "dates_of_existence",
        "disabled_access",
        "finding_aids",
        "functions",
        "general_context",
        "geocultural_context",
        "history",
        "holdings",
        "internal_structures",
        "legal_status",
        "maintenance_notes",
        "mandates",
        "opening_times",
        "places",
        "reproduction_services",
        "research_services",
        "rules",
        "sources",
    )

class ContactTranslationOptions(TranslationOptions):
    fields = (
            "city",
            "region",
            "note",
            "contact_type",
    )

translator.register(Repository, RepositoryTranslationOptions)
translator.register(Contact, ContactTranslationOptions)

