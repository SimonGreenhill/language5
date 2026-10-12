-- Cut-over, run once in this order:
--   1. manage.py migrate
--   2. psql -f deploy/cutover.sql            (this file)
--   3. manage.py remove_stale_contenttypes --noinput
--   4. PG_STATEMENT_TIMEOUT=0 manage.py buildwatson
--      (~2 min; drops stale search entries; local.py's statement_timeout would cancel it)
-- Drops tables no code uses any more: the removed pronouns app (all empty in the
-- 2026-10-12 dump), South's history table, and an unused database cache table.
BEGIN;
DROP TABLE pronoun_rules_relationships, pronoun_relationships, pronoun_rules,
           pronouns_entries, pronouns, pronouns_pronountype, paradigms,
           south_migrationhistory, cache;
DELETE FROM django_migrations WHERE app = 'pronouns';
COMMIT;
