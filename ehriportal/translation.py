from modeltranslation.translator import translator, TranslationOptions
from ehriportal.repositories.models import Repository, Contact

class RepositoryTranslationOptions(TranslationOptions):
    fields = (
        "history",
        "places",
        "legal_status",
        "functions",
        "mandates",
        "internal_structures",
        "general_context",
        "rules_conventions",
        "sources",
        "maintenance_notes",
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

