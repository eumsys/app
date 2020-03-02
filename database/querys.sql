select * from boleto;
select * from pagos;
select * from tarifaaplicada;

select * from tarifa;

SELECT boleto.fechaexpedicion, boleto.idtipodescuento, boleto.idestado, pagos.fechapago, MAX(pagos.idpago) FROM boleto, pagos WHERE boleto.idboleto = 1 and boleto.idexpedidora = 1 and boleto.fechaexpedicion = '2017-07-25 00:00:00';

--Query para obtner los datos del boleto
SELECT  B.idboleto, B.idtipodescuento, B.idestado, B.fechaexpedicion, CASE COUNT(B.idboleto) 
    WHEN NULL THEN 0 ELSE COUNT(B.idboleto) END 
    FROM boleto B WHERE B.idboleto = 1 and B.idexpedidora = 1 and B.fechaexpedicion = '2017-07-26 14:01:58';

--Query para obtener el ultimo registro del pago del boleto indicado. ESTA OPCION ES LA MEJOR SEGUN LA TEORIA
    SELECT B.fechaexpedicion, B.idestado, P.fechapago,idpago
    FROM boleto B INNER JOIN pagos P ON  B.idboleto = P.idboleto and B.idexpedidora = P.idexpedidora and B.fechaexpedicion = P.fechaexpedicion
    AND idpago IN (SELECT MAX(idpago) from pagos WHERE pagos.idboleto = 1 and pagos.idexpedidora = 1 and pagos.fechaexpedicion = '2017-07-27 01:08:11')


--Query para exportar los datos de una tabla
COPY "TARIFA"("idTarifa", "plaza",  "fec_ini", "fec_fin","descuento", "hor_fin", "dia_sem", "des_tar", "costo", "int_1", "int_2", "estado", "prioridad", "descuento") TO '/home/pi/Desktop/tablaTarifa.csv' delimiters ',' WITH CSV HEADER;

idTarifa,plaza,fec_ini,fec_fin,hor_ini,hor_fin,dia_sem,des_tar,costo,int_1,int_2,estado,prioridad,descuento
48,1,,,,,,tarifa de 0 a 1 horas,10,0,1,1,1,1
49,1,,,,,,tarifa de 1 a 2 horas,20,1,2,1,1,1
50,1,,,,,,tarifa de 2 a 3 horas,30,2,3,1,1,1
51,1,,,,,,tarifa de 3 a 4 horas,40,3,4,1,1,1
52,1,,,,,,tarifa de 4 a 5 horas,50,4,5,1,1,1
53,1,,,,,,tarifa de 5 a 6 horas,60,5,6,1,1,1
54,1,,,,,,tarifa de 6 a 7 horas,70,6,7,1,1,1
55,1,,,,,,tarifa de 7 a 8 horas,80,7,8,1,1,1
56,1,,,,,,tarifa de 8 a 9 horas,90,8,9,1,1,1
57,1,,,,,,tarifa de 9 a 10 horas,100,9,10,1,1,1
58,1,,,,,,tarifa de 10 a 11 horas,110,10,11,1,1,1
59,1,,,,,,tarifa maxima,120,11,23,1,1,1
60,1,,,,,,descuento wallmart,5,0,2,1,1,2
61,1,,,,,,descuento cinemex,8,0,1,1,1,3
62,1,,,,,,descuento cinemex,16,1,2,1,1,3
63,1,,,,,,descuento cinemex,24,2,3,1,1,3
64,1,,,,,,descuento vips,5,0,2,1,1,4
65,1,,,,,,descuento suburbia,5,0,2,1,1,5

<<<<<<< HEAD
SELECT * FROM usuario;
SELECT P.nombre, P.apellidopaterno, P.apellidomaterno, U.turno FROM usuario AS U JOIN persona AS P ON U.idpersona=P.idpersona WHERE U.idusuario='1234' AND U.password='1234';
=======

CREATE TABLE "TARIFA"
(
  "idTarifa" integer NOT NULL,
  plaza integer,
  fec_ini date,
  fec_fin date,
  des_tar character varying,
  costo integer,
  int_1 integer,
  int_2 integer,
  estado integer,
  prioridad integer,
  descuento integer,
  hor_ini time without time zone,
  hor_fin time without time zone,
  dia_sem character varying,
  CONSTRAINT "TARIFA_pkey" PRIMARY KEY ("idTarifa")
)
WITH (
  OIDS=FALSE
);
ALTER TABLE """TARIFA"""
  OWNER TO postgres;
>>>>>>> 7fdcca580443bece70e63a7a18307663898b7696

INSERT INTO logs (idpersona, idcaj, idtipo, monedas_previas, billetes_previas, monedas_posteriores, billetes_posteriores, fechamantenimiento) VALUES
			('turnom@gmail.com',1,1,'0:0', '0:0','ok', 'ok', '31-12-2017 11:37:35');

SELECT P.nombre, P.apellidopaterno, P.apellidomaterno, U.turno FROM usuario AS U JOIN persona AS P ON U.idpersona=P.idpersona WHERE U.idusuario='1234' AND U.password='1234';			
SELECT * FROM cat_plaza AS cpa JOIN cat_pais AS cpla ON cpa.idpais = cpla.idpais JOIN cat_continente AS ccon ON ccon.idcontinente = cpla.idcontinente JOIN cat_estados AS cest ON cest.idestado = cpa.idestado;
