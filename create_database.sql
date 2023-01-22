/*create table surah*/
create table surah(surah_id int primary key, surah_name varchar(50) not null collate Arabic_CI_AI_KS_WS, type varchar(50) not null, nyah int not null, revolution_order int)

/* create table ayat */
create table ayat(ayat_id int primary key, ayat_text varchar(max)not null collate Arabic_CI_AI_KS_WS, fk_surah_id int foreign key references surah(surah_id))
