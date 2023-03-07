from utils.services.auto_translate_service import translate_text
from django.db import models


class BaseModel(models.Model):

    TRANSLATED_FIELDS = None
    COPY_FIELDS = None

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def base_model_save(self, *args, **kwargs):
        if not self.id:
            self.set_translations()
        super().save(*args, **kwargs)

    def set_translations(self):
        general_field = None
        general_field_locale = None

        if self.TRANSLATED_FIELDS:
            for field in self.TRANSLATED_FIELDS:
                if getattr(self, field):
                    general_field = field
                    general_field_locale = field.split("_")[1]
                    break
            for field in self.TRANSLATED_FIELDS:
                if field != general_field:
                    setattr(self, field, translate_text(self, general_field_locale, field.split("_")[1], general_field, True))

        if self.COPY_FIELDS:
            for copy_set in self.COPY_FIELDS:
                for field in copy_set:
                    if getattr(self, field):
                        general_field = field
                        break
                for field in copy_set:
                    if field != general_field:
                        setattr(self, field, getattr(self, general_field))

    def __str__(self):
        return f"{self.id}"

    class Meta:
        abstract = True
