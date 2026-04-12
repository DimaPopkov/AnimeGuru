import json
from django.core.management.base import BaseCommand
from main.models import Product, Category, Status, Tags, Album_Pics, Pics

class Command(BaseCommand):
    help = 'Загружает аниме из JSON файла'

    def handle(self, *args, **options):
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        for item in data:
            default_cat = Category.objects.get(name=item.get('category', ''))
            default_status = Status.objects.get(name=item.get('status', ''))
            default_tags = []
            default_album_pics, created = Album_Pics.objects.get_or_create(name=item.get('name', ''))

            pics_info = item.get('pics_name', [])
            
            base_name = pics_info[0]
            pics_count = pics_info[1]
            i = 1
            while i <= pics_count:
                file_path = f"img/pics/{base_name}_pic{i}.webp"

                new_pic = Pics.objects.create(image=file_path)
                default_album_pics.image.add(new_pic)

                i += 1

            for tag in item.get('tags', ''):
                find_tag, _  = Tags.objects.get_or_create(name=tag)
                default_tags.append(find_tag)

        
            product, created = Product.objects.update_or_create(
                name=item['name'],
                defaults={
                    'description': item.get('description', ''),
                    'image': item.get('image', ''),
                    'season': item.get('season', '2026-01-01'),
                    'rating': item.get('rating', 0.0),
                    'age_rating': item.get('age_rating', 16),
                    'episods': item.get('episods', ''),
                    'eng_name': item.get('eng_name', ''),
                    'category': default_cat,
                    'status': default_status,
                    'product_manager': item.get('product_manager', ''),
                    'season_info': item.get('season_info', ''),
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Добавлено: {product.name}'))
            else:
                self.stdout.write(f'Обновлено: {product.name}')
        
            product.tags.set(default_tags)