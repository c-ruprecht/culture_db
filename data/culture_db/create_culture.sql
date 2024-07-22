/* CREATE_CULTURE.SQL */

/* Description:  A schema for the database holding culture library information
/* Authors:      faith, vennaro
/* Date:  Thu Oct 13 07:39:51 EDT 2016


/* CREATE DATABASE CULTURE.DB

/*
*/
drop table if exists library;
create table library
(library_id integer PRIMARY KEY,
 sample_id integer NOT NULL,
 library_name text, 
 FOREIGN KEY(sample_id) REFERENCES sample(sample_id)
);
create index library_to_parent_a ON sample(sample_id);


drop table if exists culture;
create table culture
(culture_id integer PRIMARY KEY,
 library_id integer NOT NULL,
 culture_name text UNIQUE,
 culture_type text, /* intial, seed, no */
 culture_date integer NOT NULL,
 culture_vessel text, /* deep 96, etc... */
/* archived text, *//*ENUM('Y','N', '?'); is this a replicated, archived arrayed culture collection or the original culturing from one*/
/* grown_from_archive, *//* put culture name of where it was grown from!!!!!!!!! */
/* metagenomics text, *//*ENUM('Y','N', '?'); do we have metagenomics data from this sample? */
/* genome_sequence text, *//*ENUM('Y','N', '?'); do we have metagenomics data from this sample? */
/* rDNA_16S text,/ /*ENUM('Y','N', '?'); do we have metagenomics data from this sample? */
 FOREIGN KEY(library_id) REFERENCES library(library_id)
);
create index culture_to_parent_a ON library(library_id);

drop table if exists donor;
create table donor
(donor_id integer primary key,
 patient_id text UNIQUE, /* the mt sinai patient id */
 donor_species text, /* human, mouse, etc... */
 sex text, /* male, female, ? */
 age_at_sampling real
);


drop table if exists sample;
create table sample
(sample_id integer primary key,
 donor_id integer NOT NULL,
 sample_name text UNIQUE, /* patient ID + other information; sometimes just patient ID */
 sample_description text, /* more info about the sample */
 collection_date integer,
 health_status text, /* CDI, UC, CD, pouch, pouchitis, healthy */
 sample_type text, /* feces, cecal contents, etc... */
 sample_preservation text, /* shipped on cold packs; -80C long-term storage */
 FOREIGN KEY(donor_id) REFERENCES donor(donor_id)
);
create index sample_to_parent_a ON sample(donor_id);

drop table if exists isolate;
create table isolate
(isolate_id integer primary key,
 library_id integer NOT NULL,
 media_id integer NOT NULL,
 strain_id integer NOT NULL,
 seed_well text, /* P23 */
 archive_well text, /* A9 */
 diamond_well text, /* A9 */
 FOREIGN KEY(library_id) REFERENCES library(library_id)
);
create index sample_to_parent_b ON library(library_id);


drop table if exists strain;
create table strain
(strain_id integer primary key,
 genus text, /* Escherichia */
 species text, /* Escherichia coli */
 strain text, /* Escherichia coli MG1655 */
 unique(genus,species,strain)
);

drop table if exists media;
create table media
(media_id integer primary key,
 media_code text, /* the M number code */
 media_description text /* what kind of media is it */
);

drop table if exists genome;
create table genome
(genome_id integer primary key,
 isolate_id integer UNIQUE,
 length integer NOT NULL,
 N50 integer NOT NULL,
 sequence_file text, /* the filename of the genome */
 original_file text, /* the original filename of the genome (before it is renamed to build the database) */
 alternative_names text, /* placeholder for alternative genome names (not currently used) */
 FOREIGN KEY(isolate_id) REFERENCES isolate(strain_id)
);

drop table if exists metagenomics;
create table metagenomics
(metagenomic_id integer primary key,
 sample_id integer NOT NULL,
 strain_id integer NOT NULL,
 relative_abundance real, 
 FOREIGN KEY(strain_id) REFERENCES strain(strain_id),
 FOREIGN KEY(sample_id) REFERENCES sample(strain_id)
);
create index metagenomics_to_parent_a ON metagenomics(sample_id);
create index metagenomics_to_parent_b ON metagenomics(strain_id);

drop table if exists growth;
create table growth
(growth_id integer primary key,
 isolate_id integer NOT NULL,
 culture_id integer NOT NULL,
 OD600 real, /* optical density */
 OD600_no_bkgnd real, /* optical density background subtracted */
 bruker_name text, /* the MSP name */
 bruker_score real, /* the MSP score */
 FOREIGN KEY(isolate_id) REFERENCES isolate(isolate_id),
 FOREIGN KEY(culture_id) REFERENCES culture(culture_id)
);
create index growth_to_parent_b ON growth(isolate_id);
create index growth_to_parent_c ON growth(culture_id);

