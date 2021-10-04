from django.shortcuts import render, HttpResponse
from .models import SimulateContentType, SimulatePermission


# Create your views here.
def index_view(request):
    simulate_content_type = SimulateContentType.objects.get(pk=1)

    # related_name='sp_set' 所以就不会有 simulatepermission_set 这个属性.
    # ['DoesNotExist', 'MultipleObjectsReturned', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__',
    #  '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__',
    #  '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__',
    #  '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__',
    #  '_check_column_name_clashes', '_check_constraints', '_check_field_name_clashes', '_check_fields',
    #  '_check_id_field', '_check_index_together', '_check_indexes', '_check_local_fields', '_check_long_column_names',
    #  '_check_m2m_through_same_relationship', '_check_managers', '_check_model', '_check_model_name_db_lookup_clashes',
    #  '_check_ordering', '_check_property_name_related_field_accessor_clashes', '_check_single_primary_key',
    #  '_check_swappable', '_check_unique_together', '_do_insert', '_do_update', '_get_FIELD_display',
    #  '_get_next_or_previous_by_FIELD', '_get_next_or_previous_in_order', '_get_pk_val', '_get_unique_checks',
    #  '_meta', '_perform_date_checks', '_perform_unique_checks', '_save_parents', '_save_table', '_set_pk_val',
    #  '_state', 'app_label', 'check', 'clean', 'clean_fields', 'date_error_message', 'delete', 'from_db', 'full_clean',
    #  'get_deferred_fields', 'id', 'model', 'objects', 'pk', 'prepare_database_save', 'refresh_from_db', 'save',
    #  'save_base', 'serializable_value', 'sp_set', 'unique_error_message', 'validate_unique']
    print(dir(simulate_content_type))

    # <QuerySet [<SimulatePermission: SimulatePermission object (1)>,
    #            <SimulatePermission: SimulatePermission object (2)>,
    #            <SimulatePermission: SimulatePermission object (3)>,
    #            <SimulatePermission: SimulatePermission object (4)>]>
    print(simulate_content_type.sp_set.all())
    return HttpResponse("hello world!")
