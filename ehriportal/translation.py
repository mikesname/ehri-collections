from modeltranslation.translator import translator, TranslationOptions
from ehriportal.portal.models import Repository, Contact

class RepositoryTranslationOptions(TranslationOptions):
    fields = [f[0] for f in Repository.translatable_fields]

class ContactTranslationOptions(TranslationOptions):
    fields = (
            "city",
            "region",
            "note",
            "contact_type",
    )

#translator.register(Repository, RepositoryTranslationOptions)
#translator.register(Contact, ContactTranslationOptions)

