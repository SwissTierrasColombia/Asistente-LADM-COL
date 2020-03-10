import qgis

from asistente_ladm_col.config.mapping_config import (QueryNames,
                                                      LADMNames)

def functionalTests():
    try:
        from qgistester.test import Test
    except:
        return []

    initial_models = None
    final_models = None

    def open_schema_import_dialog(models):
        plugin = qgis.utils.plugins['asistente_ladm_col']
        plugin.show_dlg_import_schema(**models)

    def open_schema_import_dialog_model1():
        open_schema_import_dialog({'selected_models': [LADMNames.SUPPORTED_SUPPLIES_MODEL]})

    def open_schema_import_dialog_model2():
        open_schema_import_dialog({'selected_models': [LADMNames.SUPPORTED_SNR_DATA_MODEL]})

    def get_initial_models_in_cache():
        global initial_models
        initial_models = get_models_in_cache()

    def get_models_in_cache():
        plugin = qgis.utils.plugins['asistente_ladm_col']
        models = [record[QueryNames.MODEL] for record in plugin.qgis_utils._layers]
        models = set(models)
        if None in models:
            models.remove(None)
        return models

    def get_final_models_in_cache():
        global final_models
        final_models = get_models_in_cache()

    def validate_initial_final_models():
        global initial_models
        global final_models
        assert len(final_models -initial_models) > 0, "Modelos iniciales: {}, Modelos finales: {}".format(initial_models, final_models)

    layer_relations_cache_test = Test(
        'CACHE DE CAPAS Y RELACIONES DEBE SER RECONSTRUIDO SI SE EJECUTÓ BIEN UN SCHEMA IMPORT.')
    layer_relations_cache_test.addStep("""INSTRUCCIONES:<br>
    1. Se abrirá por 1era vez el diálogo Schema Import automáticamente.<br> 
       1.a Selecciona una conexión nueva (se recomienda a GPKG).<br>
       1.b Dale click a Run para importar la estructura pre-seleccionada a la GPKG.<br>
       1.c Cierra el diálogo.<br>
    2. Se abrirá por 2da vez el diálogo Schema Import automáticamente.<br>
       2.a Dale click a Run para importar la estructura pre-seleccionada a la GPKG.<br>
       2.b Cierra el diálogo.<br><br>
    Luego de esto, el test evaluará automáticamente si el caché de capas y relaciones se reconstruyó.
      """)
    layer_relations_cache_test.addStep('Usar diálogo Schema Import (1era vez)...', open_schema_import_dialog_model1)
    layer_relations_cache_test.addStep('Obtener modelos en 1er Schema Import', get_initial_models_in_cache)
    layer_relations_cache_test.addStep('¿Todo va bien?', isVerifyStep=True)
    layer_relations_cache_test.addStep('Usar diálogo Schema Import (2da vez)...', open_schema_import_dialog_model2)
    layer_relations_cache_test.addStep('¿Hasta acá todo va bien?', isVerifyStep=True)
    layer_relations_cache_test.addStep('Obtener modelos en 2do Schema Import', get_final_models_in_cache)
    layer_relations_cache_test.addStep('Se reconstruyó el cache? Esto es, hay más modelos finales que iniciales?', validate_initial_final_models)

    return [layer_relations_cache_test]