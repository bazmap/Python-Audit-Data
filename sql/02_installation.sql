CREATE OR REPLACE PROCEDURE "${schemaDataOfAudit}".ab_audit_data(
	schemas_audit text default 'all',
	schema_data_audit text default '${schemaDataOfAudit}',
	prefix_data_audit text default '',
	type_audit text default 'all',
	limite_nb_valeur_audit integer default 25
)
LANGUAGE plpgsql
AS
$corps$

/*
Ajouter
	Limitation des valeurs remontées si uniquement des valeurs uniques
	Si uniquement valeur unique mais moins de 10 valeurs alors on les affiches...

	Permettre un audit uniquement géométrique
*/

/*
Description
Cette fonction permet d'auditer un schéma et tout son contenu.


Paramètres
----------
schemas_audit text : 'schema_1,schema_2'
	Schéma à auditer
	En utilisant 'all' tous les schémas sont audités sauf les schémas "systèmes" et le schéma "public"

schema_data_audit text : 'audit_data'
	Schéma dans lequel créer les tables et vues d'audit
	Si le schéma n'éxiste pas, il sera créé automatiquement

prefix_data_audit text : ''
	Préfixe des tables et vues d'audit si besoin

type_audit text : 'all'
	Type d'audit
	L'audit peut être mené sur plusieurs éléments :
		'bdd'
		'role'
		'schema'
		'fonction'
		'vue'
		'vue matérialisée'
		'table'
		'index'
		'trigger'
		'colonne'
		'valeur' : analyse des valeurs présentes dans chaque colonne
		'geometrie' : analyse des colonnes géométriques
		'all' : tout auditer
	Il est possible de combiner plusieurs éléments pour les auditer d'un seul coup en les séparant par des virgules : 'table,colonne'

limite_nb_valeur_audit integer : 25
	Nombre maximum de valeurs distinctes à remonter par colonne


Retour
------
Table de données :
	audit_bdd
	audit_colonne
	audit_extension
	audit_fonction
	audit_geometrie
	audit_index
	audit_role
	audit_schema
	audit_sequence
	audit_table
	audit_trigger
	audit_valeur
	audit_vue
	audit_vue_materialisee
Vue de données :
	audit_table_colonne_valeur
	audit_geometrie


Utilisation
-----------
Le plus simple est d'utiliser la notation nommée plutot que la notation positionnée pour les arguments
CALL public.ab_audit_data(
	schemas_audit => 'schema_1,schema_2',
	schema_data_audit => 'audit_data',
	prefix_data_audit => '',
	type_audit => 'all',
	limite_nb_valeur_audit => 25
)
;

En version simple :
CALL public.ab_audit_data(
	'schema_1,schema_2', 'audit_data'
)
;


=> Intégrer l'audit géométrique dans l'audit de valeurs
=> Ajouter les colonnes qui vont bien


*/

DECLARE
	-- Paramètres internes, ne pas modifier

		-- Version de PostgreSQL
		pg_version int := current_setting('server_version_num')::int;


		-- Variables de boucle
		liste_sequence record;
		liste_table record;
		liste_colonne record;
		liste_valeur record;

		-- Calcul du nombre de lignes
		nb_ligne_table integer;
		nb_ligne_non_nulle integer;

		-- Calcul du poid des colonnes
		column_size text;

		-- Requête à exécuter
		var_requete text;



BEGIN

	RAISE NOTICE USING MESSAGE = 'Audit de base';



	-- Création du schéma de stockage de l'audit
	RAISE NOTICE USING MESSAGE = 'Schéma de stockage de l''audit : ' || quote_ident(schema_data_audit);

	EXECUTE
		$a$CREATE SCHEMA IF NOT EXISTS $a$ || quote_ident(schema_data_audit);



	-- Type d'audit
	type_audit =
		CASE
			WHEN type_audit LIKE '%all%' THEN 'bdd,role,schema,extension,fonction,sequence,vue,vue matérialisée,table,index,trigger,colonne,valeur,geometrie'
			ELSE type_audit
		END;

	RAISE NOTICE USING MESSAGE = 'Eléments audités : ' || type_audit;



	-- Schéma à auditer
	IF schemas_audit = 'all' THEN
		schemas_audit = (
			SELECT
				string_agg(nspname, ',')
			FROM
				pg_catalog.pg_namespace
			WHERE
				NOT nspname ~ 'information_schema|pg_catalog|public|pg_temp_.*|pg_toast.*'
			AND
				nspname <> schema_data_audit
		);
	END IF;

	RAISE NOTICE USING MESSAGE = 'Schémas audités : ' || schemas_audit;






	----------------------------------------------------
	----------------------------------------------------
	-- Audit
	----------------------------------------------------
	----------------------------------------------------


	-- BDD
	IF array['bdd'] && regexp_split_to_array(type_audit, ',') THEN

		RAISE NOTICE USING MESSAGE = 'Audit des BDD';

		-- Suppression de la table d'audit
		EXECUTE 
			$a$DROP TABLE IF EXISTS $a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_bdd') || $a$ CASCADE $a$
		;

		-- Création de la table d'audit
		EXECUTE
			$a$CREATE TABLE $a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_bdd') || $a$ ( 
				nom_bdd text,
				proprietaire text,
				taille text,
				encodage text,
				"collation" text,
				classification_caractere text,
				connectivite text,
				type_bdd text,
				droits text[]
			) $a$
		;


		EXECUTE
			$a$INSERT INTO $a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_bdd') || $a$ (
				nom_bdd,
				proprietaire,
				taille,
				encodage,
				"collation",
				classification_caractere,
				connectivite,
				type_bdd,
				droits
			)
			SELECT
				pgdb.datname AS nom_bdd,
				pga.rolname AS proprietaire,
				pg_size_pretty(pg_database_size(pgdb.datname)) AS taille,
				pg_encoding_to_char(pgdb.encoding) AS encodage,
				pgdb.datcollate AS "collation",
				pgdb.datctype AS "classification_caractere",
				CASE
					WHEN pgdb.datallowconn IS TRUE
						THEN
							CASE pgdb.datconnlimit
								WHEN -1 THEN 'Nombre illimité de connexion'
								WHEN 1 THEN '1 connexion max'
								ELSE pgdb.datconnlimit || ' connexions simultanées max'
							END
					ELSE 'Connexion non autorisée'
				END AS connectivite,
				CASE
					WHEN pgdb.datistemplate IS TRUE
						THEN 'Base template'
					ELSE 'Base standard'
				END AS "type",
				pgdb.datacl AS droits
			FROM
				pg_database pgdb
			LEFT JOIN
				pg_authid as pga
			ON
				pgdb.datdba = pga.oid
			ORDER BY
				pgdb.datname $a$
		;

	END IF;


	-- Rôle
	IF array['role'] && regexp_split_to_array(type_audit, ',') THEN

		RAISE NOTICE USING MESSAGE = 'Audit des Rôles';

		-- Suppression de la table d'audit
		EXECUTE 
			$a$DROP TABLE IF EXISTS $a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_role') || $a$ CASCADE $a$
		;

		-- Création de la table d'audit
		EXECUTE
			$a$CREATE TABLE $a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_role') || $a$ ( 
				nom_role text,
				superutilisateur text,
				creer_bdd text,
				creer_role text,
				peut_login text,
				limite_connexion text,
				valide_jusqua text,
				membre text,
				membre_de text
			) $a$
		;


		EXECUTE
			$a$INSERT INTO $a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_role') || $a$ (
				nom_role,
				superutilisateur,
				creer_bdd,
				creer_role,
				peut_login,
				limite_connexion,
				valide_jusqua,
				membre,
				membre_de
			)
			SELECT
				pgr.rolname AS nom_role,
				pgr.rolsuper AS superutilisateur,
				pgr.rolcreatedb AS creer_bdd,
				pgr.rolcreaterole AS creer_role,
				pgr.rolcanlogin AS peut_login,
				pgr.rolconnlimit AS limite_connexion,
				pgr.rolvaliduntil AS valide_jusqua,
				string_agg(pgram.rolname, ', ') AS "membre",
				string_agg(pgram2.rolname, ', ') AS "membre_de"
			FROM
				pg_roles AS pgr
			LEFT JOIN
				pg_auth_members AS pgam
				ON pgam.roleid = pgr.oid
			LEFT JOIN
				pg_roles AS pgram
				ON pgram.oid = pgam.member
			LEFT JOIN
				pg_auth_members AS pgam2
				ON pgam2.member = pgr.oid
			LEFT JOIN
				pg_roles AS pgram2
				ON pgram2.oid = pgam2.roleid
			WHERE
				pgr.rolname NOT LIKE 'pg_%'
			GROUP BY
				pgr.rolname,
				pgr.rolsuper,
				pgr.rolcreatedb,
				pgr.rolcreaterole,
				pgr.rolcanlogin,
				pgr.rolconnlimit,
				pgr.rolvaliduntil $a$
		;

	END IF;


	-- Schéma
	IF array['schema'] && regexp_split_to_array(type_audit, ',') THEN

		RAISE NOTICE USING MESSAGE = 'Audit des schémas';

		-- Suppression de la table d'audit
		EXECUTE 
			$a$DROP TABLE IF EXISTS $a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_schema') || $a$ CASCADE $a$
		;

		-- Création de la table d'audit
		EXECUTE
			$a$CREATE TABLE $a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_schema') || $a$ ( 
				nom_schema text,
				taille text,
				commentaire text,
				proprietaire text,
				droits text[]
			) $a$
		;


		EXECUTE
			$a$INSERT INTO $a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_schema') || $a$ (
				nom_schema,
				taille,
				commentaire,
				proprietaire,
				droits
			)
			SELECT
				pgn.nspname as "nom_schema",
				pg_size_pretty(sum(pg_relation_size(pgc.oid))) || ' (' || pg_size_pretty(sum(pg_total_relation_size(pgc.oid))) || ')' as "taille_totale",
				pgd.description as "commentaire",
				pga.rolname,
				pgn.nspacl
			FROM
				pg_catalog.pg_namespace AS pgn
			LEFT JOIN
				pg_catalog.pg_description AS pgd
			ON
				(pgn.oid = pgd.objoid AND 0 = pgd.objsubid)
			LEFT JOIN
				pg_catalog.pg_class AS pgc
			ON
				pgc.relnamespace = pgn.oid
			AND
				pgc.relkind IN ('r','m')
			LEFT JOIN
				pg_authid as pga
			ON
				pga.oid = pgn.nspowner
			WHERE
				pgn.nspname = ANY (regexp_split_to_array($a$ || quote_literal(schemas_audit) || $a$, ','))
			GROUP BY
				1,3,4,5
			ORDER BY
				pgn.nspname $a$
		;

	END IF;



	-- Extensions
	IF array['extension'] && regexp_split_to_array(type_audit, ',') THEN

		RAISE NOTICE USING MESSAGE = 'Audit des extensions';

		-- Suppression de la table d'audit
		EXECUTE 
			$a$DROP TABLE IF EXISTS $a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_extension') || $a$ CASCADE $a$
		;

		-- Création de la table d'audit
		EXECUTE
			$a$CREATE TABLE $a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_extension') || $a$ ( 
				nom_schema text,
				nom_extension text,
				version text,
				relocalisable text,
				table_config text,
				condition text,
				proprietaire text
			) $a$
		;


		EXECUTE
			$a$INSERT INTO $a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_extension') || $a$ (
				nom_schema,
				nom_extension,
				version,
				relocalisable,
				table_config,
				condition,
				proprietaire
			)
			SELECT
				pgn.nspname AS nom_schema,
				pge.extname AS nom_extension,
				pge.extversion AS "version",
				pge.extrelocatable AS relocalisable,
				pgc.relname AS table_config,
				extcondition AS condition,
				pga.rolname
			FROM
				pg_catalog.pg_extension pge
			LEFT JOIN
				pg_catalog.pg_namespace pgn
				ON pgn.oid = pge.extnamespace
			LEFT JOIN
				pg_catalog.pg_class pgc
				ON pgc.oid = ANY (pge.extconfig)
			LEFT JOIN
				pg_authid as pga
			ON
				pga.oid = pge.extowner
			WHERE
				pgn.nspname = ANY (regexp_split_to_array($a$ || quote_literal(schemas_audit) || $a$, ',')) $a$
		;

	END IF;



	-- Fonctions
	IF array['fonction'] && regexp_split_to_array(type_audit, ',') THEN

		RAISE NOTICE USING MESSAGE = 'Audit des fonctions';

		-- Suppression de la table d'audit
		EXECUTE 
			$a$DROP TABLE IF EXISTS $a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_fonction') || $a$ CASCADE $a$
		;

		-- Création de la table d'audit
		EXECUTE
			$a$CREATE TABLE $a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_fonction') || $a$ ( 
				nom_schema text,
				nom_fonction text,
				arguments text,
				retour text,
				language text,
				definition text,
				proprietaire text,
				droits text[]
			) $a$
		;


		IF pg_version < 110000 THEN

			EXECUTE
				$a$INSERT INTO $a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_fonction') || $a$ (
					nom_schema,
					nom_fonction,
					arguments,
					retour,
					language,
					definition,
					proprietaire,
					droits
				)
				SELECT
					pgn.nspname AS nom_schema,
					pgp.proname AS nom_fonction,
					pg_get_function_arguments(pgp.oid) AS arguments,
					pg_get_function_result(pgp.oid) AS retour,
					pgl.lanname AS LANGUAGE,
					pg_get_functiondef(pgp.oid) AS definition,
					pga.rolname,
					pgp.proacl
				FROM
					pg_catalog.pg_proc pgp
				LEFT JOIN
					pg_catalog.pg_namespace pgn
				ON
					pgn.oid = pgp.pronamespace
				LEFT JOIN
					pg_catalog.pg_language pgl
				ON
					pgl.oid = pgp.prolang
				LEFT JOIN
					pg_catalog.pg_depend pgd
				ON
					pgd.objid = pgp.oid
				AND
					pgd.deptype = 'e'
				LEFT JOIN
					pg_authid as pga
				ON
					pga.oid = pgp.proowner
				WHERE
					pgn.nspname = ANY (regexp_split_to_array($a$ || quote_literal(schemas_audit) || $a$, ','))
				AND
					pgd.deptype IS NULL
				AND
					NOT pgp.proisagg
				AND
					NOT pgp.proiswindow $a$
			;

		ELSE

			EXECUTE
				$a$INSERT INTO $a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_fonction') || $a$ (
					nom_schema,
					nom_fonction,
					arguments,
					retour,
					language,
					definition,
					proprietaire,
					droits
				)
				SELECT
					pgn.nspname AS nom_schema,
					pgp.proname AS nom_fonction,
					pg_get_function_arguments(pgp.oid) AS arguments,
					pg_get_function_result(pgp.oid) AS retour,
					pgl.lanname AS LANGUAGE,
					pg_get_functiondef(pgp.oid) AS definition,
					pga.rolname,
					pgp.proacl
				FROM
					pg_catalog.pg_proc pgp
				LEFT JOIN
					pg_catalog.pg_namespace pgn
				ON
					pgn.oid = pgp.pronamespace
				LEFT JOIN
					pg_catalog.pg_language pgl
				ON
					pgl.oid = pgp.prolang
				LEFT JOIN
					pg_catalog.pg_depend pgd
				ON
					pgd.objid = pgp.oid
				AND
					pgd.deptype = 'e'
				LEFT JOIN
					pg_authid as pga
				ON
					pga.oid = pgp.proowner
				WHERE
					pgn.nspname = ANY (regexp_split_to_array($a$ || quote_literal(schemas_audit) || $a$, ','))
				AND
					pgd.objid IS NULL
				AND
					pgp.prokind = 'f' $a$
			;

		END IF;

	END IF;



	-- Séquences
	IF array['sequence'] && regexp_split_to_array(type_audit, ',') THEN

		RAISE NOTICE USING MESSAGE = 'Audit des Séquences';

		-- Suppression de la table d'audit
		EXECUTE 
			$a$DROP TABLE IF EXISTS $a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_sequence') || $a$ CASCADE $a$
		;

		-- Création de la table d'audit
		EXECUTE
			$a$CREATE TABLE $a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_sequence') || $a$ ( 
				nom_schema text,
				nom_sequence text,
				valeur_demarage int8,
				valeur_actuelle int8,
				valeur_min int8,
				valeur_max int8,
				increment int8,
				taille_cache int8,
				cyclique boolean,
				proprietaire text,
				droits  text[]
			) $a$
		;


		IF pg_version < 100000 THEN

			FOR liste_sequence IN
				EXECUTE
					$a$SELECT
						pgn.nspname AS nom_schema,
						pgc.relname AS nom_sequence,
						pga.rolname AS proprietaire,
						pgc.relacl AS droits
					FROM
						pg_catalog.pg_class pgc
					LEFT JOIN
						pg_catalog.pg_namespace pgn
						ON pgn.oid = pgc.relnamespace
					LEFT JOIN
						pg_catalog.pg_depend pgd
					ON
						pgd.objid = pgc.oid
					AND
						pgd.deptype = 'e'
					LEFT JOIN
						pg_authid as pga
					ON
						pga.oid = pgc.relowner
					WHERE
						pgn.nspname = ANY (regexp_split_to_array($a$ || quote_literal(schemas_audit) || $a$, ','))
					AND
						pgc.relkind = 'S'
					AND
						pgd.deptype IS NULL $a$

			LOOP

				EXECUTE
					$a$INSERT INTO $a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_sequence') || $a$ (
						nom_schema,
						nom_sequence,
						valeur_demarage,
						valeur_actuelle,
						valeur_min,
						valeur_max,
						increment,
						taille_cache,
						cyclique,
						proprietaire,
						droits
					)
					SELECT
						$a$ || quote_literal(liste_sequence.nom_schema) || $a$,
						$a$ || quote_literal(liste_sequence.nom_sequence) || $a$,
						start_value,
						last_value,
						min_value,
						max_value,
						increment_by,
						cache_value,
						is_cycled,
						$a$ || quote_literal(liste_sequence.proprietaire) || $a$,
						$a$ || quote_literal(liste_sequence.droits) || $a$
					FROM
						$a$ || quote_ident(liste_sequence.nom_schema) || $a$.$a$ || quote_ident(liste_sequence.nom_sequence)
				;

			END LOOP;


		ELSE

			EXECUTE
				$a$INSERT INTO $a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_sequence') || $a$ (
					nom_schema,
					nom_sequence,
					valeur_demarage,
					valeur_actuelle,
					valeur_min,
					valeur_max,
					increment,
					taille_cache,
					cyclique,
					proprietaire,
					droits
				)
				SELECT
					pgn.nspname,
					pgc.relname,
					pgs.seqstart,
					pg_sequence_last_value(pgs.seqrelid),
					pgs.seqmin,
					pgs.seqmax,
					pgs.seqincrement,
					pgs.seqcache,
					pgs.seqcycle,
					pga.rolname AS proprietaire,
					pgc.relacl
				FROM
					pg_catalog.pg_sequence pgs
				LEFT JOIN
					pg_catalog.pg_class pgc
				ON
					pgc.oid = pgs.seqrelid
				LEFT JOIN
					pg_catalog.pg_namespace pgn
				ON
					pgn.oid = pgc.relnamespace
				LEFT JOIN
					pg_authid as pga
				ON
					pga.oid = pgc.relowner
				WHERE
					pgn.nspname = ANY (regexp_split_to_array($a$ || quote_literal(schemas_audit) || $a$, ',')) $a$
			;

		END IF ;

	END IF;



	-- Vue
	IF array['vue'] && regexp_split_to_array(type_audit, ',') THEN

		RAISE NOTICE USING MESSAGE = 'Audit des vues';

		-- Suppression de la table d'audit
		EXECUTE 
			$a$DROP TABLE IF EXISTS $a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_vue') || $a$ CASCADE $a$
		;

		-- Création de la table d'audit
		EXECUTE
			$a$CREATE TABLE $a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_vue') || $a$ ( 
				nom_schema text,
				nom_table text,
				definition text,
				proprietaire text,
				droits text[]
			) $a$
		;


		EXECUTE
			$a$INSERT INTO $a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_vue') || $a$ (
				nom_schema,
				nom_table,
				definition,
				proprietaire,
				droits
			)
			SELECT
				pgn.nspname AS nom_schema,
				pgc.relname AS nom_vue,
				pg_get_viewdef(pgc.oid) AS definition,
				pga.rolname AS proprietaire,
				pgc.relacl
			FROM
				pg_catalog.pg_class pgc
			LEFT JOIN
				pg_catalog.pg_namespace pgn
			ON
				pgn.oid = pgc.relnamespace
			LEFT JOIN
				pg_catalog.pg_depend pgd
			ON
				pgd.objid = pgc.oid
			AND
				pgd.deptype = 'e'
			LEFT JOIN
				pg_authid as pga
			ON
				pga.oid = pgc.relowner
			WHERE
				pgc.relkind = 'v'
			AND
				pgn.nspname = ANY (regexp_split_to_array($a$ || quote_literal(schemas_audit) || $a$, ','))
			AND
				pgd.deptype IS NULL$a$
		;

	END IF;



	-- Vue matérialisée
	IF array['vue matérialisée'] && regexp_split_to_array(type_audit, ',') THEN

		RAISE NOTICE USING MESSAGE = 'Audit des vues matérialisées';

		-- Suppression de la table d'audit
		EXECUTE 
			$a$DROP TABLE IF EXISTS $a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_vue_materialisee') || $a$ CASCADE $a$
		;

		-- Création de la table d'audit
		EXECUTE
			$a$CREATE TABLE $a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_vue_materialisee') || $a$ ( 
				nom_schema text,
				nom_table text,
				definition text,
				peuplee boolean,
				proprietaire text,
				droits text[]
			) $a$
		;


		EXECUTE
			$a$INSERT INTO $a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_vue_materialisee') || $a$ (
				nom_schema,
				nom_table,
				definition,
				peuplee,
				proprietaire,
				droits
			)
			SELECT
				pgn.nspname AS nom_schema,
				pgc.relname AS nom_vue,
				pg_get_viewdef(pgc.oid) AS definition,
				pgc.relispopulated AS peuplee,
				pga.rolname AS proprietaire,
				pgc.relacl
			FROM
				pg_catalog.pg_class pgc
			LEFT JOIN
				pg_catalog.pg_namespace pgn
			ON
				pgn.oid = pgc.relnamespace
			LEFT JOIN
				pg_catalog.pg_depend pgd
			ON
				pgd.objid = pgc.oid
			AND
				pgd.deptype = 'e'
			LEFT JOIN
				pg_authid as pga
			ON
				pga.oid = pgc.relowner
			WHERE
				pgc.relkind = 'm'
			AND
				pgn.nspname = ANY (regexp_split_to_array($a$ || quote_literal(schemas_audit) || $a$, ','))
			AND
				pgd.deptype IS NULL $a$
		;

	END IF;



	-- Index
	IF array['index','geometrie'] && regexp_split_to_array(type_audit, ',') THEN

		RAISE NOTICE USING MESSAGE = 'Audit des index';

		-- Suppression de la table d'audit
		EXECUTE 
			$a$DROP TABLE IF EXISTS $a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_index') || $a$ CASCADE $a$
		;

		-- Création de la table d'audit
		EXECUTE
			$a$CREATE TABLE $a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_index') || $a$ ( 
				nom_schema text,
				nom_table text,
				nom_colonne text,
				nom_index text,
				type text,
				definition text,
				proprietaire text,
				droits text[]
			) $a$
		;


		EXECUTE
			$a$INSERT INTO $a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_index') || $a$ (
				nom_schema,
				nom_table,
				nom_colonne,
				nom_index,
				type,
				definition,
				proprietaire,
				droits
			)
			SELECT
				pgn.nspname AS nom_schema,
				pgct.relname AS nom_table,
				string_agg(pgatt.attname, ', ') AS nom_colonne,
				pgc.relname AS nom_index,
				am.amname AS type,
				pg_get_indexdef(pgi.indexrelid) AS definition,
				pga.rolname AS proprietaire,
				pgc.relacl
			FROM
				pg_catalog.pg_index pgi
			LEFT JOIN
				pg_catalog.pg_class pgc
			ON
				pgc.oid = pgi.indexrelid
			LEFT JOIN
				pg_catalog.pg_class pgct
			ON
				pgct.oid = pgi.indrelid
			LEFT JOIN
				pg_catalog.pg_namespace pgn
			ON
				pgn.oid = pgct.relnamespace
			LEFT JOIN
				pg_catalog.pg_depend pgd
			ON
				pgd.objid = pgi.indrelid
			AND
				pgd.deptype = 'e'
			LEFT JOIN 
				pg_catalog.pg_am am 
			ON 
				am.oid = pgc.relam
			LEFT JOIN 
				pg_catalog.pg_attribute pgatt
			ON 
				pgatt.attnum = ANY (pgi.indkey)
			AND 
				pgatt.attrelid = pgct.oid
			LEFT JOIN
				pg_authid as pga
			ON
				pga.oid = pgc.relowner
			WHERE
				pgn.nspname = ANY (regexp_split_to_array($a$ || quote_literal(schemas_audit) || $a$, ','))
			AND
				pgd.deptype IS NULL
			GROUP BY 
				1,2,4,5,6,7,8 $a$
		;

	END IF;



	-- Trigger
	IF array['trigger'] && regexp_split_to_array(type_audit, ',') THEN

		RAISE NOTICE USING MESSAGE = 'Audit des triggers';

		-- Suppression de la table d'audit
		EXECUTE 
			$a$DROP TABLE IF EXISTS $a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_trigger') || $a$ CASCADE $a$
		;

		-- Création de la table d'audit
		EXECUTE
			$a$CREATE TABLE $a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_trigger') || $a$ ( 
				nom_schema text,
				nom_table text,
				nom_trigger text,
				definition text,
				even_declencheur text,
				condition_action text,
				action_menee text,
				niveau_action text,
				timing_action text
			) $a$
		;


		EXECUTE
			$a$INSERT INTO $a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_trigger') || $a$ (
				nom_schema,
				nom_table,
				nom_trigger,
				definition,
				even_declencheur,
				condition_action,
				action_menee,
				niveau_action,
				timing_action
			)
			SELECT
				pgn.nspname::text AS nom_schema,
				pgc.relname AS nom_table,
				pgt.tgname AS nom_trigger,
				pg_get_triggerdef(pgt.oid) AS definition,
				em.text AS even_declencheur,
				CASE
					WHEN pg_has_role(pgc.relowner, 'USAGE') THEN ( SELECT rm.m[1] AS m
						FROM regexp_matches(pg_get_triggerdef(pgt.oid), '.{35,} WHEN \((.+)\) EXECUTE PROCEDURE'::text) rm(m)
						LIMIT 1)
					ELSE NULL::text
				END AS condition_action,
				"substring"(pg_get_triggerdef(pgt.oid), "position"("substring"(pg_get_triggerdef(pgt.oid), 48), 'EXECUTE PROCEDURE') + 47) AS action_menee,
				CASE pgt.tgtype::integer & 1
					WHEN 1 THEN 'ROW'
					ELSE 'STATEMENT'
				END AS niveau_action,
				CASE pgt.tgtype::integer & 66
					WHEN 2 THEN 'BEFORE'
					WHEN 64 THEN 'INSTEAD OF'
					ELSE 'AFTER'
				END AS timing_action
			-- Liste des triggers
			FROM
				pg_catalog.pg_trigger AS pgt
			-- Liste des tables
			LEFT JOIN
				pg_catalog.pg_class AS pgc
			ON
				pgc.oid = pgt.tgrelid
			-- Liste des dépendances
			LEFT JOIN
				pg_catalog.pg_depend pgd
			ON
				pgd.objid = pgt.tgrelid
			AND
				pgd.deptype = 'e'
			-- Liste des schémas
			LEFT JOIN
				pg_catalog.pg_namespace AS pgn
			ON
				pgn.oid = pgc.relnamespace
			LEFT JOIN
				(
					VALUES
						(4,'INSERT'),
						(8,'DELETE'),
						(16,'UPDATE')
				) AS em (num, text)
			ON
				(pgt.tgtype::integer & em.num) <> 0
			-- Schéma spécifique
			WHERE
				pgn.nspname = ANY (regexp_split_to_array($a$ || quote_literal(schemas_audit) || $a$, ','))
			AND
				NOT pgt.tgisinternal
			AND
				NOT pg_is_other_temp_schema(pgn.oid)
			AND
				pgd.deptype IS NULL
			$a$
		;

	END IF;



	IF array['table','colonne','valeur','geometrie'] && regexp_split_to_array(type_audit, ',') THEN

		RAISE NOTICE USING MESSAGE = 'Audit des tables, colonnes et valeurs';

		-- Suppression de la table d'audit
		EXECUTE 
			$a$DROP TABLE IF EXISTS $a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_table') || $a$ CASCADE $a$
		;

		-- Création de la table d'audit
		EXECUTE
			$a$CREATE TABLE $a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_table') || $a$ ( 
				nom_schema text,
				nom_table text,
				taille text,
				nb_ligne integer,
				cle_primaire text,
				commentaire text,
				proprietaire text,
				droits text[]
			) $a$
		;


		-- Suppression de la table d'audit
		EXECUTE 
			$a$DROP TABLE IF EXISTS $a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_colonne') || $a$ CASCADE $a$
		;

		-- Création de la table d'audit
		EXECUTE
			$a$CREATE TABLE $a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_colonne') || $a$ ( 
				nom_schema text,
				nom_table text,
				nom_colonne text,
				type_donnees text,
				taille text,
				index text,
				cle_primaire text,
				cle_etrangere text,
				ct_check text,
				valeur_defaut text,
				nb_non_null integer,
				commentaire text
			) $a$
		;


		-- Suppression de la table d'audit
		EXECUTE 
			$a$DROP TABLE IF EXISTS $a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_valeur') || $a$ CASCADE $a$
		;

		-- Création de la table d'audit
		EXECUTE
			$a$CREATE TABLE $a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_valeur') || $a$ ( 
				nom_schema text,
				nom_table text,
				nom_colonne text,
				valeurs text,
				srid integer,
				dimension integer,
				validite boolean,
				non_validite text,
				nb integer,
				pourcentage text,
				commentaire text
			) $a$
		;


		-- Suppression vue d'audit
		EXECUTE
			$a$DROP VIEW IF EXISTS $a$ || quote_ident(schema_data_audit) || $b$.$b$ || quote_ident(prefix_data_audit || 'audit_table_colonne_valeur')
		;

		-- Création vue d'audit
		EXECUTE
			$a$CREATE OR REPLACE VIEW $a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_table_colonne_valeur') || $a$ AS
				WITH 
					audit AS (
						SELECT
							'Table' AS "type",
							nom_schema,
							nom_table,
							NULL AS nom_colonne,
							NULL AS type_donnees,
							taille,
							NULL AS valeurs,
							NULL::integer AS srid,
							NULL::integer AS dimension,
							NULL::boolean AS validite,
							NULL AS non_validite,
							nb_ligne,
							NULL AS pourcentage_occurence,
							NULL AS valeur_defaut,
							NULL AS index,
							NULL AS cle_primaire,
							NULL AS cle_etrangere,
							NULL AS ct_check,
							commentaire,
							proprietaire,
							droits
						FROM 
							$a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_table') || $a$
						UNION
						SELECT
							'Colonne' AS "type",
							nom_schema,
							nom_table,
							nom_colonne,
							type_donnees,
							taille,
							NULL AS valeurs,
							NULL::integer AS srid,
							NULL::integer AS dimension,
							NULL::boolean AS validite,
							NULL AS non_validite,
							nb_non_null AS nb_ligne,
							NULL AS pourcentage_occurence,
							valeur_defaut,
							index,
							cle_primaire,
							cle_etrangere,
							ct_check,
							commentaire,
							NULL AS proprietaire,
							NULL AS droits
						FROM 
							$a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_colonne') || $a$ 
						UNION
						SELECT
							'Valeur' AS "type",
							nom_schema,
							nom_table,
							nom_colonne,
							NULL AS type_donnees,
							NULL AS taille,
							valeurs,
							srid,
							dimension,
							validite,
							non_validite,
							nb AS nb_ligne,
							pourcentage as pourcentage_occurence,
							NULL AS valeur_defaut,
							NULL AS index,
							NULL AS cle_primaire,
							NULL AS cle_etrangere,
							NULL AS ct_check,
							commentaire,
							NULL AS proprietaire,
							NULL AS droits
						FROM 
							$a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_valeur') || $a$
					)
				SELECT 
					*
				FROM 
					audit
				ORDER BY
					nom_schema,
					nom_table,
					CASE
						WHEN "type" = 'Table' THEN 1
						ELSE 2
					END,
					nom_colonne,
					CASE
						WHEN "type" = 'Colonne' THEN 1
						WHEN "type" = 'Valeur' THEN 2
					END,
					CASE 
						WHEN valeurs = '[NULL]' THEN 1
						WHEN valeurs = '...Autres valeurs...' THEN 3
						ELSE 2
					END,
					nb_ligne DESC
				$a$
		;


		-- Suppression vue d'audit
		EXECUTE
			$a$DROP VIEW IF EXISTS $a$ || quote_ident(schema_data_audit) || $b$.$b$ || quote_ident(prefix_data_audit || 'audit_geometrie')
		;

		-- Création vue d'audit
		EXECUTE
			$a$CREATE OR REPLACE VIEW $a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_geometrie') || $a$ AS
				SELECT
					t1.nom_schema,
					t1.nom_table,
					t1.nom_colonne,
					t2.type_donnees,
					t1.valeurs,
					t1.srid,
					t1.dimension,
					t1.validite,
					t1.non_validite,
					t1.nb AS nb_ligne,
					t1.pourcentage as pourcentage_occurence,
					t2.index,
					t2.valeur_defaut,
					t2.ct_check,
					t1.commentaire
				FROM 
					$a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_valeur') || $a$ as t1
				LEFT JOIN 
					$a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_colonne') || $a$ as t2
					ON t2.nom_schema = t1.nom_schema
					AND t2.nom_table = t1.nom_table
					AND t2.nom_colonne = t1.nom_colonne
				WHERE 
					dimension IS NOT NULL
				ORDER BY
					t1.nom_schema,
					t1.nom_table,
					t1.nom_colonne,
					t1.nb DESC
				$a$
		;


		-- Boucle sur chaque table
		FOR liste_table IN
			-- Récupération de la liste des tables
			EXECUTE
				$a$SELECT
					pgn.nspname as "nom_schema",
					pgc.relname as "nom_table",
					pg_size_pretty(pg_relation_size(pgc.oid)) as "taille_data",
					pg_size_pretty(pg_total_relation_size(pgc.oid)) as "taille_totale",
					pgc_pk.conname || ' (' || string_agg(pgatt.attname, ', ') || ')' as nom_pk,
					pgd.description as "commentaire",
					pga.rolname AS proprietaire,
					pgc.relacl as droits
				FROM
					pg_catalog.pg_class AS pgc
				LEFT JOIN
					pg_catalog.pg_namespace AS pgn
				ON
					pgn.oid = pgc.relnamespace
				LEFT JOIN 
					pg_constraint pgc_pk 
				ON 
					pgc_pk.conrelid = pgc.oid 
				AND 
					pgc_pk.contype = 'p'::"char"
				LEFT JOIN 
					pg_catalog.pg_attribute pgatt
				ON 
					pgatt.attnum = ANY (pgc_pk.conkey)
				AND 
					pgatt.attrelid = pgc.oid
				LEFT JOIN
					pg_catalog.pg_description AS pgd
				ON
					(pgc.oid = pgd.objoid AND 0 = pgd.objsubid)
				LEFT JOIN
					pg_catalog.pg_depend pgdep
				ON
					pgdep.objid = pgc.oid
				AND
					pgdep.deptype = 'e'
				LEFT JOIN
					pg_authid as pga
				ON
					pga.oid = pgc.relowner
				WHERE
					pgc.relkind = 'r'
				AND
					pgn.nspname = ANY (regexp_split_to_array($a$ || quote_literal(schemas_audit) || $a$, ','))
				AND
					pgdep.deptype IS NULL
				GROUP BY 
					1,2,3,4,pgc_pk.conname,6,7,8
				ORDER BY
					1,2$a$

		LOOP

			-- Message d'information
			RAISE NOTICE USING MESSAGE = 'Table : ' || liste_table.nom_table;



			-- Récupération du nombre de lignes dans la table
			EXECUTE
				$a$SELECT
					count(*)
				FROM
					$a$ || quote_ident(liste_table.nom_schema) || $b$.$b$ || quote_ident(liste_table.nom_table)
			INTO nb_ligne_table
			;



			-- Insertion des résultats
			EXECUTE
				$a$INSERT INTO $a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_table') || $a$ (
					nom_schema,
					nom_table,
					taille,
					nb_ligne,
					cle_primaire,
					commentaire,
					proprietaire,
					droits
				)
				VALUES (
					$a$ || quote_literal(liste_table.nom_schema) || $a$,
					$a$ || quote_literal(liste_table.nom_table) || $a$,
					$a$ || quote_literal(liste_table.taille_data || ' (' || liste_table.taille_totale || ')') || $a$,
					$a$ || COALESCE(nb_ligne_table::text,'0')::integer || $a$,
					NULLIF($a$ || quote_literal(COALESCE(liste_table.nom_pk,'[@@NULL]')) || $a$,'[@@NULL]'),
					NULLIF($a$ || quote_literal(COALESCE(liste_table.commentaire,'[@@NULL]')) || $a$,'[@@NULL]'),
					NULLIF($a$ || quote_literal(COALESCE(liste_table.proprietaire,'[@@NULL]')) || $a$,'[@@NULL]'),
					NULLIF($a$ || quote_literal(COALESCE(liste_table.droits::text,'[@@NULL]')) || $a$,'[@@NULL]')::text[]
				) $a$
			;



			IF array['colonne','valeur','geometrie'] && regexp_split_to_array(type_audit, ',') THEN

				-- Boucle sur chaque colonne
				FOR liste_colonne IN
					EXECUTE
						$a$SELECT
							pgn.nspname::text AS "nom_schema",
							pgclass.relname::text AS "nom_table",
							pga.attname::text AS "nom_colonne",
							CASE
								WHEN pgt.typname = 'geometry' THEN 'Geometry : ' || public.postgis_typmod_type(pga.atttypmod)
								ELSE pgt.typname ||
								CASE
									WHEN pga.atttypid IN (1042, 1043) -- varchar
										THEN
											CASE
												WHEN pga.atttypmod > 0
													THEN ' (' || (pga.atttypmod - 4)::text || ')'
												ELSE ''
											END
									WHEN pga.atttypid IN (1560, 1562) -- bit
										THEN ' (' || (pga.atttypmod)::text || ')'
									WHEN pga.atttypid = 21 -- int2
										THEN ' (16)'
									WHEN pga.atttypid = 23 -- int4
										THEN ' (32)'
									WHEN pga.atttypid = 20 -- int8
										THEN ' (64)'
									WHEN pga.atttypid = 700 -- float4
										THEN ' (24)'
									WHEN pga.atttypid = 701 -- float8
										THEN ' (53)'
									WHEN pga.atttypid = 1700 -- numeric
										THEN
											' (' ||
											CASE
												WHEN pga.atttypmod = -1
													THEN ''
												ELSE (((pga.atttypmod - 4) >> 16) & 65535)::text
											END ||
											CASE
												WHEN pga.atttypmod = -1
													THEN ''
												ELSE ((pga.atttypmod - 4) & 65535)::text
											END
											|| ')'
									ELSE ''::text
								END
							END AS "type_donnees",
							string_agg(quote_ident(pgc_pgi.relname) || ' (' || am.amname || ')', ',' || CHR(10)) AS "index",
							string_agg(quote_ident(pgc_pk.conname), ',' || CHR(10)) AS "cle_primaire",
							string_agg(quote_ident(pgconst_fk.conname) || ' : ' || quote_ident(pgns_fk.nspname) || '.' || quote_ident(pgcla_fk.relname) || '.' || quote_ident(pga_fk.attname), ',' || CHR(10)) AS "cle_etrangere",
							string_agg(quote_ident(pgc_chk.conname) || ' : ' || pg_get_constraintdef(pgc_chk.oid), ',' || CHR(10)) AS "ct_check",
							pg_get_expr(pgdef.adbin, pgdef.adrelid) AS "valeur_defaut",
							rtrim(replace("substring"(pgd.description, 'Commentaire : [^@@]+'), 'Commentaire : ', '')) AS "commentaire"
						-- Liste des schémas
						FROM pg_catalog.pg_namespace pgn
						-- Liste des table
						LEFT JOIN pg_catalog.pg_class pgclass
							ON pgclass.relnamespace = pgn.oid
						-- Liste colonnes
						LEFT JOIN pg_catalog.pg_attribute pga
							ON pga.attrelid = pgclass.oid
						-- Liste des types
						LEFT JOIN pg_catalog.pg_type pgt
							ON pgt.oid = pga.atttypid
						-- Valeur par défaut
						LEFT JOIN pg_catalog.pg_attrdef pgdef
							ON pgdef.adrelid = pgclass.oid
							AND pgdef.adnum = pga.attnum
						-- Liste des commentaires
						LEFT JOIN pg_catalog.pg_description pgd
							ON pgd.objoid = pgclass.oid
							AND pgd.objsubid = pga.attnum
						-- Liste des contraintes de clé primaire
						LEFT JOIN pg_catalog.pg_constraint pgc_pk
							ON pgc_pk.conrelid = pgclass.oid
							AND pga.attnum = ANY (pgc_pk.conkey)
							AND pgc_pk.contype = 'p'
						-- Liste des contraintes de clé étrangère
						LEFT JOIN pg_catalog.pg_constraint pgconst_fk
							ON pgconst_fk.conrelid = pgclass.oid
							AND pga.attnum = ANY (pgconst_fk.conkey)
							AND pgconst_fk.contype = 'f'
						-- Liste des tables de référence pour les clés étrangères
						LEFT JOIN pg_catalog.pg_class pgcla_fk
							ON pgcla_fk.oid = pgconst_fk.confrelid
						-- Liste des schéma de référence pour les clés étrangères
						LEFT JOIN pg_catalog.pg_namespace pgns_fk
							ON pgns_fk.oid = pgcla_fk.relnamespace
						-- Liste des colonnes de référence pour les clés étrangères
						LEFT JOIN pg_catalog.pg_attribute pga_fk
							ON pga_fk.attnum = ANY (pgconst_fk.confkey)
							AND pga_fk.attrelid = pgconst_fk.confrelid
						-- Liste des contraintes check
						LEFT JOIN pg_catalog.pg_constraint pgc_chk
							ON pgc_chk.conrelid = pgclass.oid
							AND pga.attnum = ANY (pgc_chk.conkey)
							AND pgc_chk.contype = 'c'
						-- Liste des index 
						LEFT JOIN pg_catalog.pg_index pgi
							ON pgi.indrelid = pgclass.oid
							AND pga.attnum = ANY (pgi.indkey)
							AND NOT pgi.indisprimary 
						-- Nom des index 
						LEFT JOIN pg_catalog.pg_class pgc_pgi
							ON pgc_pgi.oid = pgi.indexrelid
						-- Type des index 
						LEFT JOIN pg_am am 
							ON am.oid = pgc_pgi.relam
						-- Schéma spécifique
						WHERE
							pgn.nspname = $a$ || quote_literal(liste_table.nom_schema) || $b$
						-- Table spécifique
						AND
							pgclass.relname = $b$ || quote_literal(liste_table.nom_table) || $c$
						-- Uniquement les colonnes utiles
						AND
							pga.attnum > 0
						-- Uniquement les colonnes réelles
						AND
							pga.atttypid <> 0
						GROUP BY
							pgn.nspname,pgclass.relname,pga.attname,4,9,10
						ORDER BY
							pgn.nspname, -- Nom schéma
							pgclass.relname, -- Nom table
							pga.attname -- Nom colonne
						$c$

				LOOP

					-- Message d'information
					RAISE NOTICE USING MESSAGE = '	Colonne : ' || liste_colonne.nom_colonne;



					-- Calcul de la taille de la colonne
					EXECUTE
						$a$SELECT
							pg_size_pretty(sum(pg_column_size($a$ || quote_ident(liste_colonne.nom_colonne) || $b$))::numeric)
						FROM
							$b$ || quote_ident(liste_table.nom_schema) || $c$.$c$ || quote_ident(liste_table.nom_table)
					INTO column_size
					;



					-- Récupération du nombre de lignes non nulles dans la colonne
					EXECUTE
						$a$SELECT
							count(1)
						FROM
							$a$ || quote_ident(liste_table.nom_schema) || $a$.$a$ || quote_ident(liste_table.nom_table) || $a$
						WHERE 
							$a$ || quote_ident(liste_colonne.nom_colonne) || $a$ IS NOT NULL $a$
					INTO nb_ligne_non_nulle
					;



					-- Insertion des résultats
					EXECUTE
						$a$INSERT INTO $a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_colonne') || $a$ (
							nom_schema,
							nom_table,
							nom_colonne,
							type_donnees,
							taille,
							index,
							cle_primaire,
							cle_etrangere,
							ct_check,
							valeur_defaut,
							nb_non_null,
							commentaire
						)
						VALUES (
							$a$ || quote_literal(liste_table.nom_schema) || $a$,
							$a$ || quote_literal(liste_table.nom_table) || $a$,
							$a$ || quote_literal(liste_colonne.nom_colonne) || $a$,
							NULLIF($a$ || quote_literal(COALESCE(liste_colonne.type_donnees,'[@@NULL]')) || $a$,'[@@NULL]'),
							NULLIF($a$ || quote_literal(COALESCE(column_size,'[@@NULL]')) || $a$,'[@@NULL]'),
							NULLIF($a$ || quote_literal(COALESCE(liste_colonne.index,'[@@NULL]')) || $a$,'[@@NULL]'),
							NULLIF($a$ || quote_literal(COALESCE(liste_colonne.cle_primaire,'[@@NULL]')) || $a$,'[@@NULL]'),
							NULLIF($a$ || quote_literal(COALESCE(liste_colonne.cle_etrangere,'[@@NULL]')) || $a$,'[@@NULL]'),
							NULLIF($a$ || quote_literal(COALESCE(liste_colonne.ct_check,'[@@NULL]')) || $a$,'[@@NULL]'),
							NULLIF($a$ || quote_literal(COALESCE(liste_colonne.valeur_defaut,'[@@NULL]')) || $a$,'[@@NULL]'),
							NULLIF($a$ || quote_literal(COALESCE(nb_ligne_non_nulle::text,'[@@NULL]')) || $a$,'[@@NULL]')::integer,
							NULLIF($a$ || quote_literal(COALESCE(liste_colonne.commentaire,'[@@NULL]')) || $a$,'[@@NULL]')
						) $a$
					;



					-- Récupération des valeurs distinctes
					IF array['valeur','geometrie'] && regexp_split_to_array(type_audit, ',') THEN

						-- Si la colonne est géométrique
						IF liste_colonne.type_donnees LIKE 'Geometry%' THEN 

							-- Insertion des données
							EXECUTE
								$a$INSERT INTO $a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_valeur') || $a$ ( 
									nom_schema,
									nom_table,
									nom_colonne,
									valeurs,
									srid,
									dimension,
									validite,
									non_validite,
									nb,
									pourcentage
								)
								SELECT 
									$a$ || quote_literal(liste_colonne.nom_schema) || $a$,
									$a$ || quote_literal(liste_colonne.nom_table) || $a$,
									$a$ || quote_literal(liste_colonne.nom_colonne) || $a$,
									GeometryType($a$ || quote_ident(liste_colonne.nom_colonne) || $a$),
									ST_srid($a$ || quote_ident(liste_colonne.nom_colonne) || $a$),
									ST_ndims($a$ || quote_ident(liste_colonne.nom_colonne) || $a$),
									ST_isvalid($a$ || quote_ident(liste_colonne.nom_colonne) || $a$),
									reason(ST_IsValidDetail($a$ || quote_ident(liste_colonne.nom_colonne) || $a$)),
									count(1),
									CASE 
										WHEN $a$ || nb_ligne_table || $a$ = 0 THEN '-'
										ELSE
											round(
												( (count(1)::numeric / $a$ || nb_ligne_table || $a$) * 100 )::numeric,
												2
											) || '%'
									END
								FROM 
									$a$ || quote_ident(liste_colonne.nom_schema) || $a$.$a$ || quote_ident(liste_colonne.nom_table) || $a$
								GROUP BY 
									1,2,3,4,5,6,7,8
								$a$
							;


						ELSE


							-- requête de récupération des valeurs
								-- On limite aux 25 premières valeurs
								-- On limite à 4 lignes avec le même nombre de valeur
									-- Ca permet d'éviter d'avoir 25 ligne avec des valeurs uniques
							var_requete = 
								$a$WITH 
									valeurs_origine AS (
										SELECT
											CASE
												WHEN $a$ || quote_ident(liste_colonne.nom_colonne) || $a$ IS NULL THEN '[NULL]'
												WHEN $a$ || quote_literal(liste_colonne.type_donnees) || $a$ LIKE 'Geometry%' THEN 'Donnée géométrique'
												WHEN $a$ || quote_literal(liste_colonne.type_donnees) || $a$ LIKE 'Bytea%' THEN 'Donnée Binaire'
												ELSE $a$ || quote_ident(liste_colonne.nom_colonne) || $a$::TEXT
											END AS valeur
										FROM
											$a$ || quote_ident(liste_table.nom_schema) || $a$.$a$ || quote_ident(liste_table.nom_table) || $a$
									),
									valeur_group AS (
										SELECT 
											valeur,
											sum(1) AS nb_ligne
										FROM 
											valeurs_origine
										GROUP BY
											valeur
									),
									valeur_filtre AS (
									SELECT
										CASE
											WHEN valeur = '[NULL]' THEN '[NULL]'
											WHEN row_number() over(ORDER BY nb_ligne DESC) <= 25 
											AND row_number() over(PARTITION BY nb_ligne ORDER BY nb_ligne DESC) <= 4
												THEN  valeur
											ELSE '...Autres valeurs...'
										END AS valeur,
										sum(nb_ligne) AS nb_ligne
									FROM 
										valeur_group
									GROUP BY 
										valeur,
										nb_ligne
									)
								SELECT 
									valeur,
									sum(nb_ligne) AS nb_ligne
								FROM 
									valeur_filtre
								GROUP BY 
									valeur
								ORDER BY 
									CASE
										WHEN "valeur" ='[NULL]' THEN 0
										WHEN "valeur" ='...Autres valeurs...' THEN 3
										ELSE 1
									END ASC,
									nb_ligne DESC
								$a$
							;

							--RAISE NOTICE USING MESSAGE = COALESCE(var_requete, '');

							-- Boucle sur chaque valeur
							FOR liste_valeur IN
								EXECUTE
									var_requete

							LOOP

								-- Insertion des résultats
								EXECUTE
									$a$INSERT INTO $a$ || quote_ident(schema_data_audit) || $a$.$a$ || quote_ident(prefix_data_audit || 'audit_valeur') || $a$ (
										nom_schema,
										nom_table,
										nom_colonne,
										valeurs,
										nb,
										pourcentage,
										commentaire
									)
									VALUES (
										$a$ || quote_literal(liste_table.nom_schema) || $a$,
										$a$ || quote_literal(liste_table.nom_table) || $a$,
										$a$ || quote_literal(liste_colonne.nom_colonne) || $a$,
										$a$ || quote_literal(COALESCE(liste_valeur.valeur, '[NULL]')) || $a$,
										NULLIF(
											$a$ || 
												quote_literal(COALESCE(liste_valeur.nb_ligne::TEXT, '[@@NULL]'))
											|| $a$,
											'[@@NULL]'
										)::integer,
										NULLIF(
											$a$ || 
												quote_literal(
													COALESCE(
														(
															round(
																(liste_valeur.nb_ligne/nb_ligne_table*100)::numeric,
																2
															)::text ||
															'%'::text
														)::text,
														'[@@NULL]'
													)
												)
											|| $a$,
											'[@@NULL]'
										),
										NULL
									) $a$
								;

							END LOOP ;

						END IF;

					END IF;

				END LOOP;

			END IF;

		END LOOP;

	END IF;

END
$corps$
;