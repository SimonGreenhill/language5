-- Run once at cut-over, after `manage.py migrate`, then `manage.py remove_stale_contenttypes --noinput`.
-- Drops tables no code uses any more: the removed pronouns app (all empty in the
-- 2026-10-12 dump), South's history table, and an unused database cache table.
BEGIN;
DROP TABLE pronoun_rules_relationships, pronoun_relationships, pronoun_rules,
           pronouns_entries, pronouns, pronouns_pronountype, paradigms,
           south_migrationhistory, cache;
DELETE FROM django_migrations WHERE app = 'pronouns';
COMMIT;
