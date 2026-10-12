from django.db import migrations, models

# index_together -> Meta.indexes. Old Django created these indexes with the
# columns in a different order (prod has (dialect, language) and (year, author)),
# so RenameIndex can't find them. Drop whatever plain index covers the columns
# and create the named one.
INDEXES = [
    ('language', models.Index(fields=['language', 'dialect'], name='languages_languag_5ccb7a_idx')),
    ('source', models.Index(fields=['author', 'year'], name='sources_author_9ad4e0_idx')),
]


def forwards(apps, schema_editor):
    conn = schema_editor.connection
    for model_name, index in INDEXES:
        model = apps.get_model('core', model_name)
        table = model._meta.db_table
        columns = {model._meta.get_field(f).column for f in index.fields}
        with conn.cursor() as cursor:
            constraints = conn.introspection.get_constraints(cursor, table)
        for name, c in constraints.items():
            if c['index'] and not c['unique'] and not c['primary_key'] and set(c['columns']) == columns:
                schema_editor.execute(schema_editor._delete_index_sql(model, name))
        schema_editor.add_index(model, index)


def backwards(apps, schema_editor):
    for model_name, index in INDEXES:
        schema_editor.remove_index(apps.get_model('core', model_name), index)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_glottolog'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RenameIndex(
                    model_name='language',
                    new_name='languages_languag_5ccb7a_idx',
                    old_fields=('language', 'dialect'),
                ),
                migrations.RenameIndex(
                    model_name='source',
                    new_name='sources_author_9ad4e0_idx',
                    old_fields=('author', 'year'),
                ),
            ],
            database_operations=[
                migrations.RunPython(forwards, backwards),
            ],
        ),
    ]
