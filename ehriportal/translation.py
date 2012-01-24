from modeltranslation.translator import translator, TranslationOptions
from ehriportal.repositories.models import Repository

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

translator.register(Repository, RepositoryTranslationOptions)
