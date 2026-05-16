import os
from pathlib import Path
from decimal import Decimal
import sys
import django

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brfn.settings')
django.setup()

from products.models import Category, Product
from users.models import User

MEDIA_PRODUCTS_DIR = BASE_DIR / 'media' / 'products'
if not MEDIA_PRODUCTS_DIR.exists():
    raise SystemExit(f'Missing media/products directory at {MEDIA_PRODUCTS_DIR}')

houseplants_category, _ = Category.objects.get_or_create(
    name='Houseplants',
    defaults={'description': 'Indoor and decorative houseplants for every cozy corner.'}
)

producer_ids = list(Product.objects.values_list('producer_id', flat=True).distinct())
producers = list(User.objects.filter(id__in=producer_ids))
if not producers:
    raise SystemExit('No producer users found in the database. Create at least one producer before importing products.')

producer_cycle = iter(producers)

captions = {
    'Cau tiểu trâm': 'Cây đôi môi xanh dễ thương, mang lại may mắn nhỏ xinh cho góc nhà.',
    'Combo Sen đá & Móng rồng đỏ': 'Bộ đôi sen đá & móng rồng đỏ: ngọt ngào và cá tính cho bàn làm việc.',
    'Cây Hạnh Phúc': 'Hạnh phúc xanh mượt, tỏa năng lượng bình yên cho mọi không gian.',
    'Cây Kim Tiền': 'Kim tiền sang trọng, dễ chăm như một vị thần may mắn nhỏ.',
    'Cây Vạn Niên Thanh': 'Vạn niên thanh xanh mướt, biểu tượng cho sự bền bỉ và thịnh vượng.',
    'Cẩm nhung': 'Cẩm nhung mềm như nhung, tạo điểm nhấn dịu dàng cho kệ sách.',
    'Hạnh Phúc (cây thân gỗ)': 'Hạnh phúc thân gỗ – phong cách, đậm chất hoài cổ và vẫn cực dễ tính.',
    'Hồng Môn đỏ biggggg': 'Hồng môn đỏ rực rỡ, đầy cảm hứng và rất yêu ánh sáng nhẹ.',
    'Hồng môn đỏ': 'Hồng môn đỏ tươi tắn, dịu dàng và luôn là điểm nhấn cho góc xanh.',
    'Lưỡi Hổ Thái (dạng lùn)': 'Lưỡi Hổ Thái bé xinh, kiêu sa và vững chãi trong mọi góc.',
    'Phát lộc (Trúc phát tài)': 'Phát lộc tươi mát, phù hợp cho góc làm việc thêm thịnh vượng.',
    'Phát tài núi': 'Phát tài núi khỏe khoắn, dễ sống và mang đến tài lộc xanh.',
    'Sen đá bông hồng (nhuộm)': 'Sen đá bông hồng nhuộm – dịu dàng như một chiếc nụ hồng thu nhỏ.',
    'Sen đá móng rồng đỏ': 'Sen đá móng rồng đỏ siêu cá tính, tươi tắn trên bàn học hay bàn làm việc.',
    'Sen đá Thái Sen Đá Xanh': 'Sen đá Thái xanh mướt, bình yên như một bản nhạc buổi sáng.',
    'Thiết mộc lan (Phát tài gốc)': 'Thiết mộc lan phát tài gốc, tươi tốt và cực kỳ dễ chăm.',
    'Thiết Mộc Lan': 'Thiết Mộc Lan thanh lịch, luôn sẵn sàng cho một góc nội thất sang.',
    'Trầu bà Thanh Xuân': 'Trầu bà Thanh Xuân mềm mại, dịu dàng như một chiếc khăn lụa xanh.',
    'Tùng bồng lai': 'Tùng bồng lai cổ điển, mang đến cảm giác bình yên cho góc ban công.',
    'Vạn lộc đỏ': 'Vạn lộc đỏ tươi, mang nét rực rỡ và may mắn cho không gian.',
    'Xương rồng Bánh sinh nhật': 'Xương rồng bánh sinh nhật đáng yêu, là món quà xanh không thể ngó lơ.',
    'Xương rồng trụ (bụi)': 'Xương rồng trụ bụi, dáng đứng uy nghi và vẫn rất dễ chăm.',
    'Đuôi công sọc (Calathea)': 'Đuôi công sọc Calathea, họa tiết xinh xắn cho bàn làm việc tươi mới.',
}

def choose_producer():
    global producer_cycle
    try:
        return next(producer_cycle)
    except StopIteration:
        producer_cycle = iter(producers)
        return next(producer_cycle)

new_names = []
for media_file in sorted(MEDIA_PRODUCTS_DIR.glob('*.jpg')):
    product_name = media_file.stem
    new_names.append(product_name)

# Hide old products not part of the new plant collection.
old_products = Product.objects.exclude(name__in=new_names)
updated_old = old_products.update(availability='unavailable', stock_quantity=0)
print(f'Hid {updated_old} old product(s) from the storefront.')

created = 0
updated = 0
for media_file in sorted(MEDIA_PRODUCTS_DIR.glob('*.jpg')):
    product_name = media_file.stem
    description = captions.get(product_name, 'Cây cảnh xinh xắn, hoàn hảo cho góc xanh của bạn.')
    defaults = {
        'description': description,
        'price': Decimal('249000.00'),
        'unit': 'item',
        'availability': 'year_round',
        'stock_quantity': 20,
        'allergen_info': '',
        'is_organic': False,
        'category': houseplants_category,
        'producer': choose_producer(),
        'image': f'products/{media_file.name}',
    }
    product, created_flag = Product.objects.update_or_create(
        name=product_name,
        defaults=defaults,
    )
    if created_flag:
        created += 1
    else:
        updated += 1
print(f'Created {created} plant products, updated {updated} existing products.')
print('Done importing plant products.')
