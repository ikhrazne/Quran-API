/*create table surah*/
create table surah(surah_id int primary key, surah_name nvarchar(50) not null collate Arabic_CI_AI_KS_WS, type varchar(50) not null, nyah int not null, revolution_order int)

/* create table ayat */
create table ayat(ayat_id int primary key, ayat_text nvarchar(max)not null collate Arabic_CI_AI_KS_WS,
fk_surah_id int foreign key references surah(surah_id),
fk_hizb_id int foreign key references ahzab(hizb_id),
fk_juz_id int foreign key references juz(juz_id));

/* create table juz */
create table juz(juz_id int primary key, juz_number int);

/* create ahzab */
create table ahzab(hizb_id int primary key, hizb_number int);

/* create files*/
create table files(file_id uniqueidentifier identity primary key, lang varchar(5), pdf_file varbinary(max) filestream)

