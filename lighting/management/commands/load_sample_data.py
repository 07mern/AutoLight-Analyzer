"""
Management command to load sample lighting catalog data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from lighting.models import LightingCatalog
from decimal import Decimal


class Command(BaseCommand):
    help = 'Load sample lighting catalog data and create user groups'

    def handle(self, *args, **kwargs):
        self.stdout.write('Loading sample data...')
        
        # Create user groups
        groups = ['Admin', 'Architect', 'Vendor']
        for group_name in groups:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created group: {group_name}'))
        
        # Create sample lighting fixtures (prices in INR ₹)
        # Expanded catalog with varied price ranges for better recommendations
        fixtures = [
            # Premium LED Panels
            {
                'symbol_name': 'LED_PANEL_600X600',
                'model_number': 'LP-600-40W',
                'brand': 'Philips',
                'lumens': 4000,
                'wattage': 40.0,
                'beam_angle': 120.0,
                'color_temp': 4000,
                'unit_cost': Decimal('2499.00'),
            },
            {
                'symbol_name': 'LED_PANEL_600X600_ECO',
                'model_number': 'LP-600-36W-ECO',
                'brand': 'Syska',
                'lumens': 3800,
                'wattage': 36.0,
                'beam_angle': 120.0,
                'color_temp': 4000,
                'unit_cost': Decimal('1799.00'),
            },
            {
                'symbol_name': 'LED_PANEL_600X600_PRO',
                'model_number': 'LP-600-45W-PRO',
                'brand': 'Havells',
                'lumens': 4500,
                'wattage': 45.0,
                'beam_angle': 120.0,
                'color_temp': 4000,
                'unit_cost': Decimal('3299.00'),
            },
            
            # Downlights - Various ranges
            {
                'symbol_name': 'DOWNLIGHT_12W',
                'model_number': 'DL-12W-CCT',
                'brand': 'Osram',
                'lumens': 1200,
                'wattage': 12.0,
                'beam_angle': 60.0,
                'color_temp': 3000,
                'unit_cost': Decimal('899.00'),
            },
            {
                'symbol_name': 'DOWNLIGHT_12W_BUDGET',
                'model_number': 'DL-12W-STD',
                'brand': 'Wipro',
                'lumens': 1100,
                'wattage': 12.0,
                'beam_angle': 60.0,
                'color_temp': 3000,
                'unit_cost': Decimal('599.00'),
            },
            {
                'symbol_name': 'DOWNLIGHT_15W_PRO',
                'model_number': 'DL-15W-PRO',
                'brand': 'Philips',
                'lumens': 1500,
                'wattage': 15.0,
                'beam_angle': 60.0,
                'color_temp': 3000,
                'unit_cost': Decimal('1299.00'),
            },
            {
                'symbol_name': 'DOWNLIGHT_8W',
                'model_number': 'DL-8W-DIM',
                'brand': 'GE Lighting',
                'lumens': 800,
                'wattage': 8.0,
                'beam_angle': 45.0,
                'color_temp': 2700,
                'unit_cost': Decimal('699.00'),
            },
            {
                'symbol_name': 'DOWNLIGHT_10W',
                'model_number': 'DL-10W-STD',
                'brand': 'Bajaj',
                'lumens': 1000,
                'wattage': 10.0,
                'beam_angle': 60.0,
                'color_temp': 3000,
                'unit_cost': Decimal('749.00'),
            },
            
            # Track Lights
            {
                'symbol_name': 'TRACKLIGHT_20W',
                'model_number': 'TL-20W-ADJ',
                'brand': 'GE Lighting',
                'lumens': 2000,
                'wattage': 20.0,
                'beam_angle': 30.0,
                'color_temp': 3500,
                'unit_cost': Decimal('1599.00'),
            },
            {
                'symbol_name': 'TRACKLIGHT_15W',
                'model_number': 'TL-15W-ECO',
                'brand': 'Syska',
                'lumens': 1800,
                'wattage': 15.0,
                'beam_angle': 30.0,
                'color_temp': 3500,
                'unit_cost': Decimal('1199.00'),
            },
            {
                'symbol_name': 'TRACKLIGHT_25W',
                'model_number': 'TL-25W-PRO',
                'brand': 'Havells',
                'lumens': 2500,
                'wattage': 25.0,
                'beam_angle': 30.0,
                'color_temp': 3500,
                'unit_cost': Decimal('2199.00'),
            },
            
            # Linear LED Fixtures
            {
                'symbol_name': 'LINEAR_LED_40W',
                'model_number': 'LL-1200-40W',
                'brand': 'Philips',
                'lumens': 4800,
                'wattage': 40.0,
                'beam_angle': 110.0,
                'color_temp': 4000,
                'unit_cost': Decimal('2299.00'),
            },
            {
                'symbol_name': 'LINEAR_LED_36W',
                'model_number': 'LL-1200-36W',
                'brand': 'Wipro',
                'lumens': 4500,
                'wattage': 36.0,
                'beam_angle': 110.0,
                'color_temp': 4000,
                'unit_cost': Decimal('1799.00'),
            },
            {
                'symbol_name': 'LINEAR_LED_50W',
                'model_number': 'LL-1500-50W',
                'brand': 'Osram',
                'lumens': 5500,
                'wattage': 50.0,
                'beam_angle': 110.0,
                'color_temp': 4000,
                'unit_cost': Decimal('2899.00'),
            },
            
            # High Bay Lights
            {
                'symbol_name': 'HIGHBAY_150W',
                'model_number': 'HB-150W-IP65',
                'brand': 'Cree',
                'lumens': 18000,
                'wattage': 150.0,
                'beam_angle': 90.0,
                'color_temp': 5000,
                'unit_cost': Decimal('8999.00'),
            },
            {
                'symbol_name': 'HIGHBAY_120W',
                'model_number': 'HB-120W-ECO',
                'brand': 'Bajaj',
                'lumens': 16000,
                'wattage': 120.0,
                'beam_angle': 90.0,
                'color_temp': 5000,
                'unit_cost': Decimal('6999.00'),
            },
            {
                'symbol_name': 'HIGHBAY_200W',
                'model_number': 'HB-200W-PRO',
                'brand': 'Philips',
                'lumens': 22000,
                'wattage': 200.0,
                'beam_angle': 90.0,
                'color_temp': 5000,
                'unit_cost': Decimal('11999.00'),
            },
            
            # Large LED Panels
            {
                'symbol_name': 'PANEL_300X1200',
                'model_number': 'LP-1200-48W',
                'brand': 'Osram',
                'lumens': 5200,
                'wattage': 48.0,
                'beam_angle': 120.0,
                'color_temp': 4000,
                'unit_cost': Decimal('2899.00'),
            },
            {
                'symbol_name': 'PANEL_300X1200_ECO',
                'model_number': 'LP-1200-40W',
                'brand': 'Syska',
                'lumens': 4800,
                'wattage': 40.0,
                'beam_angle': 120.0,
                'color_temp': 4000,
                'unit_cost': Decimal('2199.00'),
            },
            {
                'symbol_name': 'PANEL_300X1200_PRO',
                'model_number': 'LP-1200-55W',
                'brand': 'Havells',
                'lumens': 5800,
                'wattage': 55.0,
                'beam_angle': 120.0,
                'color_temp': 4000,
                'unit_cost': Decimal('3499.00'),
            },
            
            # Bulkhead Lights
            {
                'symbol_name': 'BULKHEAD_18W',
                'model_number': 'BH-18W-IP54',
                'brand': 'Philips',
                'lumens': 1800,
                'wattage': 18.0,
                'beam_angle': 180.0,
                'color_temp': 4000,
                'unit_cost': Decimal('1299.00'),
            },
            {
                'symbol_name': 'BULKHEAD_15W',
                'model_number': 'BH-15W-ECO',
                'brand': 'Wipro',
                'lumens': 1600,
                'wattage': 15.0,
                'beam_angle': 180.0,
                'color_temp': 4000,
                'unit_cost': Decimal('899.00'),
            },
            {
                'symbol_name': 'BULKHEAD_22W',
                'model_number': 'BH-22W-PRO',
                'brand': 'Havells',
                'lumens': 2200,
                'wattage': 22.0,
                'beam_angle': 180.0,
                'color_temp': 4000,
                'unit_cost': Decimal('1699.00'),
            },
            
            # LED Strips
            {
                'symbol_name': 'STRIP_14W',
                'model_number': 'LS-600-14W',
                'brand': 'Osram',
                'lumens': 1400,
                'wattage': 14.0,
                'beam_angle': 120.0,
                'color_temp': 3000,
                'unit_cost': Decimal('799.00'),
            },
            {
                'symbol_name': 'STRIP_10W',
                'model_number': 'LS-500-10W',
                'brand': 'Syska',
                'lumens': 1200,
                'wattage': 10.0,
                'beam_angle': 120.0,
                'color_temp': 3000,
                'unit_cost': Decimal('549.00'),
            },
            {
                'symbol_name': 'STRIP_18W',
                'model_number': 'LS-800-18W',
                'brand': 'Philips',
                'lumens': 1800,
                'wattage': 18.0,
                'beam_angle': 120.0,
                'color_temp': 3000,
                'unit_cost': Decimal('1099.00'),
            },
            
            # Floodlights
            {
                'symbol_name': 'FLOODLIGHT_50W',
                'model_number': 'FL-50W-IP66',
                'brand': 'Cree',
                'lumens': 6000,
                'wattage': 50.0,
                'beam_angle': 90.0,
                'color_temp': 5000,
                'unit_cost': Decimal('2499.00'),
            },
            {
                'symbol_name': 'FLOODLIGHT_30W',
                'model_number': 'FL-30W-ECO',
                'brand': 'Bajaj',
                'lumens': 4500,
                'wattage': 30.0,
                'beam_angle': 90.0,
                'color_temp': 5000,
                'unit_cost': Decimal('1599.00'),
            },
            {
                'symbol_name': 'FLOODLIGHT_70W',
                'model_number': 'FL-70W-PRO',
                'brand': 'Havells',
                'lumens': 7500,
                'wattage': 70.0,
                'beam_angle': 90.0,
                'color_temp': 5000,
                'unit_cost': Decimal('3299.00'),
            },
        ]
        
        for fixture_data in fixtures:
            fixture, created = LightingCatalog.objects.get_or_create(
                symbol_name=fixture_data['symbol_name'],
                defaults=fixture_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created fixture: {fixture.symbol_name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Fixture already exists: {fixture.symbol_name}')
                )
        
        # Create a demo user if it doesn't exist
        if not User.objects.filter(username='demo').exists():
            demo_user = User.objects.create_user(
                username='demo',
                email='demo@autolightanalyser.com',
                password='demo1234',
                first_name='Demo',
                last_name='User'
            )
            architect_group = Group.objects.get(name='Architect')
            demo_user.groups.add(architect_group)
            self.stdout.write(
                self.style.SUCCESS('Created demo user: demo / demo1234')
            )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully loaded sample data!')
        )
