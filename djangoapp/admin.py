from django.contrib import admin
from .models import CarMake, CarModel, CarDealer, DealerReview

# Define an inline admin class for CarModel
# This allows us to edit CarModel instances directly from the CarMake admin page
class CarModelInline(admin.StackedInline):
    model = CarModel  # The model to use
    extra = 0  # The number of extra forms to show in the inline formset

# Define an admin class for CarMake
# This includes the CarModelInline, allowing us to edit CarModel instances on the CarMake admin page
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]  # The inlines to include

# Register the models with the admin site
# CarMake is registered with the custom CarMakeAdmin, which includes CarModelInline
admin.site.register(CarMake, CarMakeAdmin)
# CarModel, CarDealer, and DealerReview are registered with the default admin
admin.site.register(CarModel)
admin.site.register(CarDealer)
admin.site.register(DealerReview)