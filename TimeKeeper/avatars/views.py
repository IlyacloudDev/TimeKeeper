from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from .forms import AvatarForm
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import io

# Максимальный размер изображения
max_dimension = 3000


def handle_uploaded_image(image):
    """
    Function for formatting the image to the desired scale
    """
    img = Image.open(image)

    # Проверка размера изображения
    width, height = img.size
    if width > max_dimension or height > max_dimension:
        raise ValueError(f"Размер изображения не должен превышать {max_dimension}x{max_dimension} пикселей.")

    # Преобразование изображения в квадрат (масштаб 1:1)
    min_side = min(width, height)
    left = (width - min_side) / 2
    top = (height - min_side) / 2
    right = (width + min_side) / 2
    bottom = (height + min_side) / 2
    img = img.crop((left, top, right, bottom))

    # Сохранение изображения в памяти
    img_io = io.BytesIO()
    img.save(img_io, format='JPEG', quality=85)
    img_io.seek(0)

    # Создание файла для хранения
    new_image = InMemoryUploadedFile(
        img_io,
        'ImageField',
        f"{image.name.split('.')[0]}_formatted.jpg",
        'image/jpeg',
        img_io.getbuffer().nbytes,
        None
    )

    # Сохранение файла через default_storage
    filename = default_storage.save(f"formatting_avatars/{new_image.name}", ContentFile(new_image.read()))

    # Возврат пути к сохраненному файлу
    return default_storage.url(filename)


class FormattingAvatar(LoginRequiredMixin, View):
    """
    View for processing a custom image in order to change the scale and give a link to download a new avatar
    """
    def get(self, request):
        form = AvatarForm()
        return render(request, 'avatars/formatting.html', context={'form': form})

    def post(self, request):
        form = AvatarForm(request.POST, request.FILES)

        if form.is_valid():
            image = form.cleaned_data.get('avatar')

            try:
                # Обработка изображения и получение ссылки на сохраненное изображение
                download_url = handle_uploaded_image(image)

                # Передача ссылки в шаблон
                return render(request, 'avatars/formatting.html', context={
                    'form': form,
                    'download_url': download_url
                })

            except ValueError as e:
                form.add_error('avatar', str(e))

        return render(request, 'avatars/formatting.html', context={'form': form})
