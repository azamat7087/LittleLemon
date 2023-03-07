import time

from buildings.services.client.process_image import WatermarkImage
from buildings import models
from rest_framework import serializers
from auth_user.celery import app


@app.task
def set_watermark(obj, model=None, force_watermark=False):
    time.sleep(2)
    obj = getattr(models, model).objects.get(pk=obj)
    if model != "Image":
        if getattr(obj, 'main_image') and (not getattr(obj, 'is_watermarked' or force_watermark)):
            if not WatermarkImage(getattr(obj, 'main_image')).set_watermark():
                raise serializers.ValidationError({"exception": "Главное изображение должно быть большего разрешения"})
            else:
                obj.is_watermarked = True
                obj.save()

        if getattr(obj, 'images'):
            for number, image in enumerate(getattr(obj, 'images').filter(is_watermarked=False)):
                if not WatermarkImage(image.link).set_watermark():
                    raise serializers.ValidationError(
                        {"exception": f"Изображение {number + 1} должно быть большего разрешения"})
                else:
                    image.is_watermarked = True
                    image.save()
    else:
        if not obj.is_watermarked:
            if not WatermarkImage(obj.link).set_watermark():
                raise serializers.ValidationError(
                    {"exception": f"Изображение должно быть большего разрешения"})
            else:
                obj.is_watermarked = True
                obj.save()
