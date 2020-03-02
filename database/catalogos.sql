
-- Catalogos de la Plaza --

INSERT INTO cat_continente(idcontinente, nombre) VALUES
			(1, 'Americano'),
			(2, 'Europa'),
			(3, 'Africa'),
			(4, 'Asia'),
			(5, 'Antartida');

INSERT INTO cat_pais(idpais,idcontinente, nombre) VALUES
			(1, 1, 'Mexico');

INSERT INTO cat_estados(idpais, idcontinente, idestado, nombre) VALUES
			(1,1,1,'Aguascalientes'),
			(1,1,2,'Baja California'),
			(1,1,3,'Baja California Sur'),
			(1,1,4,'Campeche'),
			(1,1,5,'Coahuila'),
			(1,1,6,'Colima'),
			(1,1,7,'Chiapas'),
			(1,1,8,'Chihuahua'),
			(1,1,9,'Ciudad de México'),
			(1,1,10,'Durango'),
			(1,1,11,'Guanajuato'),
			(1,1,12,'Guerrero'),
			(1,1,13,'Hidalgo'),
			(1,1,14,'Jalisco'),
			(1,1,15,'Estado de Mexico'),
			(1,1,16,'Michoacan'),
			(1,1,17,'Morelos'),
			(1,1,18,'Nayarit'),
			(1,1,19,'Nuevo Leon'),
			(1,1,20,'Oaxaca'),
			(1,1,21,'Puebla'),
			(1,1,22,'Queretaro'),
			(1,1,23,'Quintana Roo'),
			(1,1,24,'San Lius Potosi'),
			(1,1,25,'Sinaloa'),
			(1,1,26,'Sonora'),
			(1,1,27,'Tabasco'),
			(1,1,28,'Tamaulipas'),
			(1,1,29,'Tlaxcala'),
			(1,1,30,'Veracruz'),
			(1,1,31,'Yucatan'),
			(1,1,32,'Zacatecas');

INSERT INTO cat_plaza(idplaza, idestado, idpais, idcontinente, nombre, calle, colonia, delegacion, cp ,numexterior, numinterior, telefonolocal, extension, email, celular, politicaboleto) VALUES
			(1,15,1,1,'Heroes Tecamac', 'Calle x', 'colonia x', 'delegacion x', 1234,'no. 1', '12', '5566666666', '12345', 'atencionplaza@plaza.com', '5544444444', 'La empresa no se hace responsable por objetos|personales,fallas mecanicas  y/o  electricas,|siniestros ocasionados por derrumbes,temblores,|terremotos o fenomenos naturales,asi como ro-|bo de accesorios o vandalismo en su vehiculo.|Por robo total de acuerdo a los terminos  del|seguro contratado.Boleto Perdido.Se entregara|el  vehiculo  a quien acredite la  propiedad.|Costo del boleto perdido es de $100.00|Al recibir este boleto acepta las condiciones|del seguro contra robo total. PARKING TIP S.A|DE  C.V.  -R.F.C PTI120210571. Escobillera 13|Col.Paseos de Churubusco Iztapalapa CDMX C.P.|09030 Horario de Lunes-Domingo de 7 a 22 hrs |');

INSERT INTO cat_tipodescuento (idtipodescuento, nombre, descripcion) VALUES
			(0,'sin asignar', 'sin asignar '),
			(1, 'Walmart', '2 horas por cinco pesos'),
			(2, 'vips', '2 horas por cinco pesos'),
			(3, 'suburbia', '2 horas por cinco pesos'),
			(4,'cinemex', 'coho pesos por hora, las tres primeras horas');

INSERT INTO cat_tarifa (idcontinente,idpais,idestado,idplaza,idtipodescuento,intervaloinicial,intervalofinal,estado,prioridad,descripcion,monto) VALUES
				(1,1,15,1,0,0,1,1,1,'tarifa de 0 a 1 horas',10),
				(1,1,15,1,0,1,2,1,1,'tarifa de 1 a 2 horas',20),
				(1,1,15,1,0,2,3,1,1,'tarifa de 2 a 3 horas',30),
				(1,1,15,1,0,3,4,1,1,'tarifa de 3 a 4 horas',40),
				(1,1,15,1,0,4,5,1,1,'tarifa de 4 a 5 horas',50),
				(1,1,15,1,0,5,6,1,1,'tarifa de 5 a 6 horas',60),
				(1,1,15,1,0,6,7,1,1,'tarifa de 6 a 7 horas',70),
				(1,1,15,1,0,7,8,1,1,'tarifa de 7 a 8 horas',80),
				(1,1,15,1,0,8,9,1,1,'tarifa de 8 a 9 horas',90),
				(1,1,15,1,0,9,10,1,1,'tarifa de 9 a 10 horas',100),
				(1,1,15,1,0,10,11,1,1,'tarifa de 10 a 11 horas',110),
				(1,1,15,1,0,11,23,1,1,'tarifa maxima',120),
				(1,1,15,1,1,0,2,1,1,'descuento wallmart',5),
				(1,1,15,1,2,0,1,1,1,'descuento cinemex',8),
				(1,1,15,1,2,1,2,1,1,'descuento cinemex',16),
				(1,1,15,1,2,2,3,1,1,'descuento cinemex',24),
				(1,1,15,1,3,0,2,1,1,'descuento vips',5),
				(1,1,15,1,4,0,2,1,1,'descuento suburbia',5),
				(1,1,15,1,0,4,5,1,1,'DE RELLENO',50),
				(1,1,15,1,0,11,12,1,1,'tarifa de 11 a 12 horas',120),
				(1,1,15,1,0,12,13,1,1,'tarifa de 12 a 13 horas',130),
				(1,1,15,1,0,13,14,1,1,'tarifa de 13 a 14 horas',140),
				(1,1,15,1,0,14,15,1,1,'tarifa de 14 a 15 horas',150),
				(1,1,15,1,0,15,16,1,1,'tarifa de 15 a 16 horas',160);


-- Catalogos de Boleto --
INSERT INTO cat_estadosboleto (idestado, nombre, descripcion) VALUES 
			(1,'No Pagado', 'Boleto aun no pagado'),
			(2,'Pagado', 'Boleto ya pagado, pero aun no ha salido del estacionamiento'),
			(3,'Tiempo de Salida Excedido', 'Se agoto el tiempo de salida por lo tanto se debe proceder a pagar nuevamente'),
			(4,'Obsoleto', 'Boleto que ya cuncluyo el ciclo, por lo tanto ya no puede ser utilizado'),
			(5,'Boleto Perdido', 'Boleto que fur perdido, por tanto se le debe de aplicar una tarifa especial'),
			(6,'Boleto Perdido Pagado', 'Boleto perdido que ya cobrado con una tarifa especial'),
			(7,'Cobro Maximo', 'Boleto que no es perdido pero no fue pagado en el mismo dia de ingreso');

INSERT INTO cat_mediopago (mediopago,nombre, descripcion) VALUES
			(0,'sin asignar','sin asignar'),
			(1,'efectivo','este tipo de pago consta de monedas y billetes'),
			(2,'tarjeta debito','medio de pago electronico'),
			(3,'tarjeta credito','medio de pago electronico');


-- Catalogos de Caseta-Cajeto --
INSERT INTO cat_tipocaj (idtipocaja, tipo) VALUES
			(0,'noasig'),
			(1,'cajero'),
			(2,'caja'),
			(3,'kiosco');
			
INSERT INTO cat_casetacajero (idcaj, idtipocaja, idestado, idpais, idcontinente, idplaza, nombre , descripcion, ubicacion, direccion_ip, modelo, no_serie) VALUES
			(0,0,15,1,1,1,'Sin asignar', 'Sin Asignar','Sin asignar','localhost', 'cajero automatico mg diamante','0'),
			(1,1,15,1,1,1,'Cajero_1', 'descripcion...','Ubicado enfrente de Cinemex','200.10.10.3','cajero automatico mg diamante','1'),
			(2,1,15,1,1,1,'Cajero_2', 'descripcion...','Ubicado enfrente de SmartFit ','200.10.10.5', 'cajero automatico mg diamante','2'),
			(3,1,15,1,1,1,'Cajero_3', 'descripcion...','Ubicado enfrente de SmartFit ','200.10.10.7', 'cajero automatico mg diamante','3'),
			(4,1,15,1,1,1,'Cajero_4', 'descripcion...','Ubicado enfrente del Teatro ','200.10.10.9', 'cajero automatico mg diamante','4'),
			(5,1,15,1,1,1,'Cajero_5', 'descripcion...','Ubicado enfrente cd Walmart ','200.10.10.11', 'cajero automatico mg diamante','5'),
			(6,1,15,1,1,1,'Cajero_6', 'descripcion...','Ubicado enfrente de Walmart ','200.10.10.13', 'cajero automatico mg diamante','6'),
			(7,1,15,1,1,1,'Cajero_7', 'descripcion...','Ubicado atras del avion ','200.10.10.15', 'cajero automatico mg diamante','7'),
			(8,3,15,1,1,1,'kiosco_1', 'descripcion...','Por asignar','200.10.10.25', 'Por asignar','8');

INSERT INTO cat_rasppublicidad (iddispositivo, idcaj, nombre, descripcion, direccion_ip, modelo, no_serie) VALUES			
			(1,1,'Publicidad_1', 'descripcion...','200.10.10.4','cajero automatico mg diamante','1'),
			(2,2,'Publicidad_2', 'descripcion...','200.10.10.6','cajero automatico mg diamante','2'),
			(3,3,'Publicidad_3', 'descripcion...','200.10.10.8','cajero automatico mg diamante','3'),
			(4,4,'Publicidad_4', 'descripcion...','200.10.10.10','cajero automatico mg diamante','4'),
			(5,5,'Publicidad_5', 'descripcion...','200.10.10.12','cajero automatico mg diamante','5'),
			(6,6,'Publicidad_6', 'descripcion...','200.10.10.14','cajero automatico mg diamante','6'),
			(7,7,'Publicidad_7', 'descripcion...','200.10.10.16','cajero automatico mg diamante','7');

INSERT INTO cat_tipomantenimiento(idtipo, nombre, descripcion) VALUES
			(1, 'recoleccion de dinero', 'Se obtinen el dinero almacenado en el colector de monedas, en el deposito y en el colector de billetes'),
			(2, 'falla en dispositivos', 'correccion de fallas en los dispositivos que componen al cajero'),
			(3, 'ayuda', 'el usuario ha presionado el boton de ayuda'),
			(4, 'seguridad', 'sensores de seguridad del cajero han sido activados');

INSERT INTO cat_estado_operacion (idestado, nombre, descripcion ) VALUES
			(1,'finalizado sin intento de saqueo','no hubo intento de retirar dinero'),
			(2,'finalizado con intento de saqueo','si hubo intento de retirar dinero');

-- Catalogos de Barrera de Salida --
INSERT INTO cat_barrerasalida (idsalida, idestado, idpais, idcontinente, idplaza, nombre , descripcion, ubicacion, direccion_ip, modelo, no_serie) VALUES
			(0,15,1,1,1,'sin asignar', 'sin asignar','sin asignar','localhost', 'validadora eum 1000','0'),
			(1,15,1,1,1,'validadora_1', 'descripcion...','Ubicada en Isla 1','200.10.10.21', 'validadora eum 1000','1'),
			(2,15,1,1,1,'validadora_2', 'descripcion...','Ubicada en Isla 2','200.10.10.22', 'validadora eum 1000','2'),
			(3,15,1,1,1,'validadora_3', 'descripcion...','Ubicada en Isla 3','200.10.10.23', 'validadora eum 1000','3'),
			(4,15,1,1,1,'validadora_4', 'descripcion...','Ubicada en Isla 4','200.10.10.24', 'validadora eum 1000','4');			

INSERT INTO cat_tipo_mantenimiento_barrera (idtipo, nombre, descripcion ) VALUES
			(1,'ayuda','el usuario ha presionado el boton de ayuda');			

-- Catalogos de Expedidora --
INSERT INTO cat_expedidora (idexpedidora, idestado, idpais, idcontinente, idplaza, nombre , descripcion, ubicacion, direccion_ip, modelo, no_serie ) VALUES
			(1,15,1,1,1,'expedidora_1','descripcion...','ubicada en Isla 1','200.10.10.17', 'expedidora eum 1000','1'),
			(2,15,1,1,1,'expedidora_2','descripcion...','ubicada en Isla 2','200.10.10.18', 'expedidora eum 1000','2'),
			(3,15,1,1,1,'expedidora_3','descripcion...','ubicada en Isla 3','200.10.10.19', 'expedidora eum 1000','3'),
			(4,15,1,1,1,'expedidora_4','descripcion...','ubicada en Isla 4','200.10.10.20', 'expedidora eum 1000','4');			

INSERT INTO cat_tipo_mantenimiento_expedidora (idtipo, nombre, descripcion ) VALUES
			(1,'ayuda','el usuario ha presionado el boton de ayuda'),						
			(2,'papel de impresion agotado','el papel de impresion ha sido agotado'),
			(3,'papel de impresion por agotarse','el papel de impresion esta a punto de agotarse'),
			(4,'impresora apagada o desconectada','la expedidora no detecta la impresora esta apagada o desconectada');		

-- Catalogos de Pack usuarios
INSERT INTO persona (idpersona, idcontinente, idpais, idestado, idplaza, nombre , apellidopaterno, apellidomaterno, curp, sexo, estadicivil ) VALUES
			('turnom@gmail.com',1,1,15,1,'persona1','apellidoP1','apellidoM1','RAGJ820722HDFNNS01','M','C'),
			('roldan096@hotmail.com',1,1,15,1,'Roldan','apellidoP1','apellidoM1','RAGJ820722HDFNNS01','M','C'),
			('123@hotmail.com',1,1,15,1,'Alan','apellidoP1','apellidoM1','RAGJ820722HDFNNS01','M','C'),
			('124@hotmail.com',1,1,15,1,'Oscar','apellidoP1','apellidoM1','RAGJ820722HDFNNS01','M','C'),
			('125@hotmail.com',1,1,15,1,'Juan','apellidoP1','apellidoM1','RAGJ820722HDFNNS01','M','C'),
			('mora@hotmail.com',1,1,15,1,'mora','apellidoMora','apellidoMorita','MOR820722HDFNNS01','M','C'),			
			('ayuda@ayuda.com',1,1,15,1,'ayuda','apellidoPAyuda','apellidoMAyuda','AYU911722HDFNNS01','M','C'),			
			('turnov@gmail.com',1,1,15,1,'persona2','apellidoP2','apellidoM2','OORF950406HDFSNR05','H','S');

INSERT INTO contacto (celular, idpersona, telcasa, oficina, ext, idfacebook, correo) VALUES
			(55123,'turnom@gmail.com',NULL,NULL,NULL,'PersonaFB1',NULL),
			(55876,'turnov@gmail.com',NULL,NULL,NULL,'PersonaFB2',NULL);

INSERT INTO direccion (idpersona, calle, numeroexterior, colonia, delegacion, codigopostal) VALUES
			('turnom@gmail.com','escobilleras',13,'centro','iztapalapa',08070),
			('turnov@gmail.com','escobilleras',14,'centro','iztapalapa',08070);

INSERT INTO cat_roles(idrol, nombre, descripcion) VALUES
			(1, 'rolKiosco', 'Personal de atencion en el kiosko');

INSERT INTO usuario (idusuario, idrol,idpersona, password, turno) VALUES
			('1234',1,'turnom@gmail.com','1234', 'matutino'),
			('5678',1,'turnov@gmail.com','5678', 'vespertino');
