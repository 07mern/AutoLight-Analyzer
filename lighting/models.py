from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
import math


class LightingCatalog(models.Model):
    """Catalog of available lighting fixtures"""
    symbol_name = models.CharField(max_length=100, unique=True, help_text="Symbol name as it appears in CAD")
    model_number = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    lumens = models.IntegerField(validators=[MinValueValidator(0)], help_text="Light output in lumens")
    wattage = models.FloatField(validators=[MinValueValidator(0)], help_text="Power consumption in watts")
    beam_angle = models.FloatField(validators=[MinValueValidator(0)], help_text="Beam angle in degrees")
    color_temp = models.IntegerField(validators=[MinValueValidator(0)], help_text="Color temperature in Kelvin")
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], help_text="Cost in Indian Rupees (₹)")
    image = models.ImageField(upload_to='fixtures/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['symbol_name']
        verbose_name = "Lighting Catalog Entry"
        verbose_name_plural = "Lighting Catalog"

    def __str__(self):
        return f"{self.symbol_name} - {self.brand} {self.model_number}"


class CADFile(models.Model):
    """Uploaded CAD files"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cad_files')
    project_name = models.CharField(max_length=255, default="Untitled Project")
    filename = models.CharField(max_length=255)
    file = models.FileField(upload_to='cad_files/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = "CAD File"
        verbose_name_plural = "CAD Files"

    def __str__(self):
        return f"{self.project_name} - {self.filename}"


class Room(models.Model):
    """Room detected from CAD file"""
    
    # Room type choices with standard lux recommendations
    ROOM_TYPE_CHOICES = [
        ('bedroom', 'Bedroom'),
        ('living_room', 'Living Room'),
        ('kitchen', 'Kitchen'),
        ('bathroom', 'Bathroom'),
        ('office', 'Office'),
        ('classroom', 'Classroom'),
        ('conference_room', 'Conference Room'),
        ('hallway', 'Hallway/Corridor'),
        ('showroom', 'Showroom/Retail'),
        ('warehouse', 'Warehouse'),
        ('laboratory', 'Laboratory'),
        ('hospital_room', 'Hospital Room'),
        ('other', 'Other'),
    ]
    
    # Standard lux levels per room type (in lux)
    LUX_STANDARDS = {
        'bedroom': 150,
        'living_room': 200,
        'kitchen': 400,
        'bathroom': 200,
        'office': 500,
        'classroom': 500,
        'conference_room': 300,
        'hallway': 150,
        'showroom': 750,
        'warehouse': 200,
        'laboratory': 500,
        'hospital_room': 300,
        'other': 300,
    }
    
    cad_file = models.ForeignKey(CADFile, on_delete=models.CASCADE, related_name='rooms')
    name = models.CharField(max_length=100)
    room_type = models.CharField(max_length=50, choices=ROOM_TYPE_CHOICES, default='other', help_text="Type of room for lux calculation")
    
    # Dimensions
    length = models.FloatField(validators=[MinValueValidator(0.1)], help_text="Room length in meters", null=True, blank=True)
    width = models.FloatField(validators=[MinValueValidator(0.1)], help_text="Room width in meters", null=True, blank=True)
    area = models.FloatField(
        validators=[MinValueValidator(0.1), MaxValueValidator(10000.0)], 
        help_text="Area in square meters (0.1 - 10,000 m²)"
    )
    height = models.FloatField(validators=[MinValueValidator(0)], help_text="Height in meters", default=3.0)
    
    # Lux calculation - now dynamically calculated based on room type
    required_lux = models.FloatField(validators=[MinValueValidator(0)], default=300, help_text="Required illuminance in lux", blank=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = "Room"
        verbose_name_plural = "Rooms"

    def __str__(self):
        return f"{self.name} ({self.area}m²) - {self.get_room_type_display()}"
    
    def save(self, *args, **kwargs):
        """Override save to calculate area and required lux dynamically"""
        # Calculate area from length and width if provided
        if self.length and self.width:
            calculated_area = self.length * self.width
            # Update area only if not already set or significantly different
            if not self.area or abs(self.area - calculated_area) > 0.1:
                self.area = calculated_area
        
        # Set required lux based on room type if not explicitly set
        if not self.required_lux or self.required_lux == 300:  # 300 is default
            self.required_lux = self.LUX_STANDARDS.get(self.room_type, 300)
        
        super().save(*args, **kwargs)
    
    def clean(self):
        """Validate room data"""
        super().clean()
        if self.area < 0.1:
            raise ValidationError({'area': 'Room area must be at least 0.1 m²'})
        if self.area > 10000:
            raise ValidationError({'area': 'Room area cannot exceed 10,000 m²'})
        
        # Validate length and width if provided
        if self.length and self.width:
            calculated_area = self.length * self.width
            if abs(self.area - calculated_area) > 0.1 * calculated_area:
                self.area = calculated_area
    
    @classmethod
    def calculate_required_lux(cls, room_type):
        """Get recommended lux level for a room type"""
        return cls.LUX_STANDARDS.get(room_type, 300)
    
    def calculate_required_lumens(self):
        """Calculate total lumens required based on room dimensions and type"""
        # Formula: Required Lumens = Room Area (m²) × Required Lux Level
        # Apply room utilization factor and maintenance factor
        room_index = (self.length * self.width) / (self.height * (self.length + self.width)) if self.length and self.width else 1.0
        utilization_factor = 0.7  # Accounts for light absorption and reflection
        maintenance_factor = 0.8  # Accounts for lamp depreciation and dirt
        
        required_lumens = (self.area * self.required_lux) / (utilization_factor * maintenance_factor)
        return math.ceil(required_lumens)

    @property
    def total_lumens_required(self):
        """Calculate total lumens required for this room (considers efficiency factors)"""
        return self.calculate_required_lumens()

    @property
    def current_lux(self):
        """Calculate current lux based on installed fixtures"""
        # Guard against zero area
        if self.area <= 0:
            return 0.0
        
        # Calculate total lumens from all fixtures
        total_lumens = sum(fixture.total_lumens for fixture in self.fixtures.all())
        
        # Guard against no fixtures
        if total_lumens == 0:
            return 0.0
        
        # Apply lighting efficiency factor (accounting for losses, reflections, etc.)
        # Typical efficiency factor is 0.6-0.8 for indoor spaces
        efficiency_factor = 0.7
        effective_lumens = total_lumens * efficiency_factor
        
        # Calculate lux (lumens per square meter)
        lux = effective_lumens / self.area
        
        return round(lux, 2)

    @property
    def is_adequately_lit(self):
        """Check if room has adequate lighting"""
        return self.current_lux >= self.required_lux


class Fixture(models.Model):
    """Lighting fixtures in a room"""
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='fixtures')
    lighting_catalog = models.ForeignKey(LightingCatalog, on_delete=models.CASCADE, related_name='installations')
    quantity = models.IntegerField(validators=[MinValueValidator(1)], default=1)
    x_coordinate = models.FloatField(null=True, blank=True, help_text="X position from CAD")
    y_coordinate = models.FloatField(null=True, blank=True, help_text="Y position from CAD")
    
    class Meta:
        ordering = ['room', 'lighting_catalog']
        verbose_name = "Fixture"
        verbose_name_plural = "Fixtures"

    def __str__(self):
        return f"{self.lighting_catalog.symbol_name} x{self.quantity} in {self.room.name}"

    @property
    def total_lumens(self):
        """Total lumens from this fixture"""
        return self.lighting_catalog.lumens * self.quantity

    @property
    def total_cost(self):
        """Total cost for this fixture"""
        return self.lighting_catalog.unit_cost * self.quantity


class Report(models.Model):
    """Generated reports"""
    REPORT_TYPE_CHOICES = [
        ('pdf', 'PDF Report'),
        ('csv', 'CSV Report'),
    ]

    cad_file = models.ForeignKey(CADFile, on_delete=models.CASCADE, related_name='reports')
    report_type = models.CharField(max_length=10, choices=REPORT_TYPE_CHOICES)
    file_path = models.FileField(upload_to='reports/')
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-generated_at']
        verbose_name = "Report"
        verbose_name_plural = "Reports"

    def __str__(self):
        return f"{self.report_type.upper()} - {self.cad_file.project_name} - {self.generated_at.strftime('%Y-%m-%d')}"
