create table boleto (
  idboleto        int4 not null, 
  idexpedidora    int4 not null, 
  fechaexpedicion timestamp not null, 
  idestado        int4 not null, 
  idtipodescuento int4 not null, 
  idsalida        int4 not null, 
  primary key (idboleto, 
  idexpedidora, 
  fechaexpedicion));
comment on table boleto is 'Esta tabla se encarga de recabar los datos que corresponden al manejo de un boleto de estacionamiento';
create table cat_estadosboleto (
  idestado    serial not null, 
  nombre      varchar(50) not null, 
  descripcion varchar(200), 
  primary key (idestado));
create table cat_expedidora (
  idexpedidora serial not null, 
  idcontinente int4 not null, 
  idpais       int4 not null, 
  idestado     int4 not null, 
  idplaza      int4 not null, 
  nombre       varchar(50) not null, 
  descripcion  varchar(500), 
  ubicacion    varchar(100) not null, 
  direccion_ip varchar(15) not null, 
  modelo       varchar(50) not null, 
  no_serie     varchar(50) not null, 
  primary key (idexpedidora));
create table cat_tipodescuento (
  idtipodescuento serial not null, 
  nombre          varchar(50) not null, 
  descripcion     varchar(100), 
  primary key (idtipodescuento));
create table cat_mediopago (
  mediopago   serial not null, 
  nombre      varchar(50) not null, 
  descripcion varchar(200), 
  primary key (mediopago));
create table cat_casetacajero (
  idcaj        serial not null, 
  idtipocaja   int4 not null, 
  idcontinente int4 not null, 
  idpais       int4 not null, 
  idestado     int4 not null, 
  idplaza      int4 not null, 
  nombre       varchar(50) not null, 
  descripcion  varchar(200), 
  ubicacion    varchar(100) not null, 
  direccion_ip varchar(15) not null, 
  modelo       varchar(50) not null, 
  no_serie     varchar(50) not null, 
  primary key (idcaj));
create table cat_barrerasalida (
  idsalida     serial not null, 
  idpais       int4 not null, 
  idcontinente int4 not null, 
  idestado     int4 not null, 
  idplaza      int4 not null, 
  nombre       varchar(50) not null, 
  descripcion  varchar(200), 
  ubicacion    varchar(100) not null, 
  direccion_ip varchar(15) not null, 
  modelo       varchar(50) not null, 
  no_serie     varchar(50) not null, 
  primary key (idsalida));
create table cat_tipocaj (
  idtipocaja serial not null, 
  tipo       varchar(6) not null, 
  primary key (idtipocaja));
create table persona (
  idpersona       varchar(50) not null, 
  idcontinente    int4 not null, 
  idpais          int4 not null, 
  idestado        int4 not null, 
  idplaza         int4 not null, 
  nombre          varchar(30) not null, 
  apellidopaterno varchar(30) not null, 
  apellidomaterno varchar(30) not null, 
  curp            varchar(18) not null, 
  sexo            varchar(1), 
  estadicivil     varchar(1), 
  primary key (idpersona));
create table usuario (
  idusuario varchar(50) not null, 
  idpersona varchar(50) not null, 
  idrol     int4 not null, 
  password  varchar(256) not null, 
  turno     varchar(10) not null, 
  primary key (idusuario));
create table cat_roles (
  idrol       serial not null, 
  nombre      varchar(30) not null, 
  descripcion varchar(50), 
  primary key (idrol));
create table contacto (
  celular    serial not null, 
  idpersona  varchar(50) not null, 
  telcasa    int4, 
  oficina    int4, 
  ext        int4, 
  idfacebook varchar(50) not null, 
  correo     varchar(50), 
  primary key (celular));
create table direccion (
  idpersona      varchar(50) not null, 
  calle          varchar(50) not null, 
  numerointerior int4, 
  numeroexterior int4 not null, 
  colonia        varchar(50) not null, 
  delegacion     varchar(50) not null, 
  codigopostal   int4 not null);
create table cat_tarifa (
  idtarifa         serial not null, 
  idcontinente     int4 not null, 
  idpais           int4 not null, 
  idestado         int4 not null, 
  idplaza          int4 not null, 
  idtipodescuento  int4 not null, 
  intervaloinicial int4 not null, 
  intervalofinal   int4 not null, 
  fechainicial     date, 
  fechafinal       date, 
  descripcion      varchar(100) not null, 
  diasaplica       int4, 
  monto            float4 not null, 
  estado           int4 not null, 
  prioridad        int4 not null, 
  primary key (idtarifa));
create table pagos (
  idpago          serial not null, 
  idboleto        int4 not null, 
  idexpedidora    int4 not null, 
  fechaexpedicion timestamp not null, 
  idcaj           int4 not null, 
  mediopago       int4 not null, 
  monto           float4 not null, 
  monedas         varchar(50), 
  billetes        varchar(50), 
  cambio          varchar(50), 
  fechapago       timestamp not null, 
  primary key (idpago));
create table cat_plaza (
  idplaza        int4 not null, 
  idestado       int4 not null, 
  idpais         int4 not null, 
  idcontinente   int4 not null, 
  nombre         varchar(100) not null, 
  calle          varchar(50) not null, 
  colonia        varchar(50) not null, 
  delegacion     varchar(50) not null, 
  cp             int4 not null, 
  numinterior    varchar(10), 
  numexterior    varchar(10) not null, 
  telefonolocal  varchar(10) not null, 
  extension      varchar(5), 
  email          varchar(50), 
  celular        varchar(10), 
  politicaboleto varchar(1000) not null, 
  primary key (idplaza, 
  idestado, 
  idpais, 
  idcontinente));
create table cat_pais (
  idpais       int4 not null unique, 
  idcontinente int4 not null, 
  nombre       varchar(100) not null, 
  primary key (idpais, 
  idcontinente));
create table cat_continente (
  idcontinente serial not null, 
  nombre       varchar(100) not null, 
  primary key (idcontinente));
create table cat_estados (
  idestado     int4 not null, 
  idpais       int4 not null, 
  idcontinente int4 not null, 
  nombre       varchar(100) not null, 
  primary key (idestado, 
  idpais, 
  idcontinente));
create table propaganda (
  idpropaganda serial not null, 
  idpersona    varchar(50) not null, 
  primary key (idpropaganda));
create table log_inicial (
  idmantenimiento    serial not null, 
  idcaj              int4 not null, 
  idpersona          varchar(50) not null, 
  idtipo             int4 not null, 
  fechamantenimiento timestamp not null, 
  monedas_previas    varchar(50) not null, 
  billetes_previas   varchar(50) not null, 
  primary key (idmantenimiento));
create table cat_tipomantenimiento (
  idtipo      serial not null, 
  nombre      varchar(50), 
  descripcion varchar(200), 
  primary key (idtipo));
create table tarifaaplicada (
  id       serial not null, 
  idpago   int4 not null, 
  idtarifa int4 not null, 
  primary key (id));
create table logs_expedidora (
  idlog            serial not null, 
  idexpedidora     int4 not null, 
  idtipo           int4 not null, 
  feha             date, 
  estado_operacion varchar(15), 
  descripcion      varchar(500), 
  primary key (idlog));
create table cat_tipo_mantenimiento_expedidora (
  idtipo      serial not null, 
  nombre      varchar(50) not null, 
  descripcion varchar(200), 
  primary key (idtipo));
create table logs_barrerasalida (
  idlog            serial not null, 
  idsalida         int4 not null, 
  idtipo           int4 not null, 
  fecha            date, 
  estado_operacion varchar(15), 
  descripcion      varchar(500), 
  primary key (idlog));
create table cat_tipo_mantenimiento_barrera (
  idtipo      serial not null, 
  nombre      varchar(50) not null, 
  descripcion varchar(200), 
  primary key (idtipo));
create table log_final (
  idmantenimiento    serial not null, 
  idestado           int4 not null, 
  idcaj              int4 not null, 
  idpersona          varchar(50) not null, 
  fechamantenimiento timestamp not null, 
  descripcion        varchar(500), 
  primary key (idmantenimiento));
create table cat_estado_operacion (
  idestado    serial not null, 
  nombre      varchar(50) not null, 
  descripcion varchar(200), 
  primary key (idestado));
create table cat_rasppublicidad (
  iddispositivo serial not null, 
  idcaj         int4 not null, 
  nombre        varchar(50) not null, 
  descripcion   varchar(200), 
  direccion_ip  varchar(15) not null, 
  modelo        varchar(50) not null, 
  no_serie      varchar(50) not null, 
  primary key (iddispositivo));
alter table boleto add constraint FKboleto879862 foreign key (idexpedidora) references cat_expedidora (idexpedidora);
alter table usuario add constraint FKusuario201440 foreign key (idpersona) references persona (idpersona);
alter table contacto add constraint FKcontacto594190 foreign key (idpersona) references persona (idpersona);
alter table direccion add constraint FKdireccion948067 foreign key (idpersona) references persona (idpersona);
alter table pagos add constraint FKpagos776926 foreign key (mediopago) references cat_mediopago (mediopago);
alter table pagos add constraint FKpagos480161 foreign key (idcaj) references cat_casetacajero (idcaj);
alter table tarifaaplicada add constraint FKtarifaapli688954 foreign key (idtarifa) references cat_tarifa (idtarifa);
alter table cat_casetacajero add constraint FKcat_caseta109927 foreign key (idtipocaja) references cat_tipocaj (idtipocaja);
alter table boleto add constraint FKboleto796209 foreign key (idestado) references cat_estadosboleto (idestado);
alter table persona add constraint FKpersona682061 foreign key (idplaza, idestado, idpais, idcontinente) references cat_plaza (idplaza, idestado, idpais, idcontinente);
alter table cat_tarifa add constraint FKcat_tarifa835937 foreign key (idplaza, idestado, idpais, idcontinente) references cat_plaza (idplaza, idestado, idpais, idcontinente);
alter table cat_pais add constraint FKcat_pais738728 foreign key (idcontinente) references cat_continente (idcontinente);
alter table cat_estados add constraint FKcat_estado697731 foreign key (idpais, idcontinente) references cat_pais (idpais, idcontinente);
alter table cat_plaza add constraint FKcat_plaza49732 foreign key (idestado, idpais, idcontinente) references cat_estados (idestado, idpais, idcontinente);
alter table cat_casetacajero add constraint FKcat_caseta877415 foreign key (idplaza, idestado, idpais, idcontinente) references cat_plaza (idplaza, idestado, idpais, idcontinente);
alter table cat_barrerasalida add constraint FKcat_barrer589934 foreign key (idplaza, idestado, idpais, idcontinente) references cat_plaza (idplaza, idestado, idpais, idcontinente);
alter table cat_expedidora add constraint FKcat_expedi227901 foreign key (idplaza, idestado, idpais, idcontinente) references cat_plaza (idplaza, idestado, idpais, idcontinente);
alter table propaganda add constraint FKpropaganda755598 foreign key (idpersona) references persona (idpersona);
alter table pagos add constraint FKpagos105187 foreign key (idboleto, idexpedidora, fechaexpedicion) references boleto (idboleto, idexpedidora, fechaexpedicion);
alter table boleto add constraint FKboleto86638 foreign key (idtipodescuento) references cat_tipodescuento (idtipodescuento);
alter table tarifaaplicada add constraint FKtarifaapli910266 foreign key (idpago) references pagos (idpago);
alter table cat_tarifa add constraint FKcat_tarifa108370 foreign key (idtipodescuento) references cat_tipodescuento (idtipodescuento);
alter table boleto add constraint FKboleto412672 foreign key (idsalida) references cat_barrerasalida (idsalida);
alter table usuario add constraint FKusuario502249 foreign key (idrol) references cat_roles (idrol);
alter table log_inicial add constraint FKlog_inicia28135 foreign key (idtipo) references cat_tipomantenimiento (idtipo);
alter table log_inicial add constraint FKlog_inicia460351 foreign key (idpersona) references persona (idpersona);
alter table log_inicial add constraint FKlog_inicia441973 foreign key (idcaj) references cat_casetacajero (idcaj);
alter table logs_expedidora add constraint FKlogs_exped579727 foreign key (idexpedidora) references cat_expedidora (idexpedidora);
alter table logs_expedidora add constraint FKlogs_exped703754 foreign key (idtipo) references cat_tipo_mantenimiento_expedidora (idtipo);
alter table logs_barrerasalida add constraint FKlogs_barre39312 foreign key (idsalida) references cat_barrerasalida (idsalida);
alter table logs_barrerasalida add constraint FKlogs_barre723506 foreign key (idtipo) references cat_tipo_mantenimiento_barrera (idtipo);
alter table log_final add constraint FKlog_final405600 foreign key (idestado) references cat_estado_operacion (idestado);
alter table log_final add constraint FKlog_final731871 foreign key (idcaj) references cat_casetacajero (idcaj);
alter table log_final add constraint FKlog_final286506 foreign key (idpersona) references persona (idpersona);
alter table cat_rasppublicidad add constraint FKcat_rasppu459149 foreign key (idcaj) references cat_casetacajero (idcaj);
