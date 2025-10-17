-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 01-06-2022 a las 22:40:03
-- Versión del servidor: 10.4.22-MariaDB
-- Versión de PHP: 7.4.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `intersalud_prueba`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `agendas`
--

CREATE TABLE `agendas` (
  `id_Agenda` int(11) NOT NULL,
  `Medico_id` int(11) DEFAULT NULL,
  `Consultorio_id` int(11) DEFAULT NULL,
  `Especialidad_Medica` int(11) DEFAULT NULL,
  `Horario_Cita_id` int(11) DEFAULT NULL,
  `Domicilio_id` int(11) DEFAULT NULL,
  `Max_pacientes` int(11) DEFAULT NULL,
  `Status_id` int(11) DEFAULT NULL,
  `Status_Medico_id` int(11) DEFAULT NULL,
  `Nota` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `agendas`
--

INSERT INTO `agendas` (`id_Agenda`, `Medico_id`, `Consultorio_id`, `Especialidad_Medica`, `Horario_Cita_id`, `Domicilio_id`, `Max_pacientes`, `Status_id`, `Status_Medico_id`, `Nota`) VALUES
(1, 1, 1, 1, 1, NULL, 10, 1, NULL, 'Asistir a la consulta acompañado'),
(2, 1, 1, 1, 2, NULL, 20, 1, NULL, 'beber 2 litros de agua si viene por eco'),
(3, 3, 2, 2, 3, NULL, 10, 1, NULL, 'llegar a la consulta acompañado');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `anamnesis`
--

CREATE TABLE `anamnesis` (
  `id_anamnesis` int(11) NOT NULL,
  `Paciente_Id` int(11) NOT NULL,
  `Paciente_Especial_id` int(11) NOT NULL,
  `Medico_id` int(11) NOT NULL,
  `Fecha` datetime NOT NULL,
  `Control_Historia_Medico_id` int(11) DEFAULT NULL,
  `Enfermedad_Actual` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `Origen` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `Hallazgo` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `Plan_Tratamiento` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `Diagnostico_Definitivo` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `Pronostico` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `id_Status` int(11) NOT NULL,
  `Peso` float(10,2) NOT NULL,
  `Talla` float(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `anamnesis`
--

INSERT INTO `anamnesis` (`id_anamnesis`, `Paciente_Id`, `Paciente_Especial_id`, `Medico_id`, `Fecha`, `Control_Historia_Medico_id`, `Enfermedad_Actual`, `Origen`, `Hallazgo`, `Plan_Tratamiento`, `Diagnostico_Definitivo`, `Pronostico`, `id_Status`, `Peso`, `Talla`) VALUES
(1, 1, 0, 1, '2022-03-30 00:00:00', 1, 'test', 'test', 'test', 'test', 'test', 'test', 1, 60.00, 1.50),
(2, 1, 0, 1, '2022-04-19 00:00:00', 5, 'test', 'test', 'test', 'test', 'test', 'tset', 1, 50.00, 1.60),
(3, 1, 0, 1, '2022-04-25 00:00:00', 12, 'test', 'test', 'testtest', 'tset', 'tset', 'test', 1, 70.00, 1.68),
(5, 1, 0, 1, '2022-04-25 00:00:00', 19, 'cierre', 'cierre', 'cierre', 'cierre', 'cierre', 'cierre', 1, 80.00, 2.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `antecedentes`
--

CREATE TABLE `antecedentes` (
  `id_antecedente` int(11) NOT NULL,
  `Paciente_Id` int(11) NOT NULL,
  `Paciente_Especial_id` int(11) DEFAULT NULL,
  `Medico_id` int(11) NOT NULL,
  `Fecha` date NOT NULL,
  `Control_Historia_Medico_id` int(11) DEFAULT NULL,
  `id_Status` int(11) NOT NULL,
  `Personal` text NOT NULL,
  `Familiar` text NOT NULL,
  `Farmacologico` text NOT NULL,
  `Examen_Fisico` text NOT NULL,
  `Imprecion_Diagnostica` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `antecedentes`
--

INSERT INTO `antecedentes` (`id_antecedente`, `Paciente_Id`, `Paciente_Especial_id`, `Medico_id`, `Fecha`, `Control_Historia_Medico_id`, `id_Status`, `Personal`, `Familiar`, `Farmacologico`, `Examen_Fisico`, `Imprecion_Diagnostica`) VALUES
(1, 1, 0, 1, '2022-03-30', 1, 1, 'test', 'test', 'test', 'test', 'test');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `bancos_bs`
--

CREATE TABLE `bancos_bs` (
  `id_Bancos_Bs` int(11) NOT NULL,
  `Bancos` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Status_Id` int(11) DEFAULT 1,
  `Codigo_Bancario` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `bancos_bs`
--

INSERT INTO `bancos_bs` (`id_Bancos_Bs`, `Bancos`, `Status_Id`, `Codigo_Bancario`) VALUES
(1, '100%BANCO', 1, 156),
(2, 'ABN AMRO BANK', 1, 196),
(3, 'BANCAMIGA BANCO MICROFINANCIERO, C.A.', 1, 172),
(4, 'BANCO ACTIVO BANCO COMERCIAL, C.A.', 1, 171),
(5, 'BANCO AGRICOLA', 1, 166),
(6, 'BANCO AGRICOLA DE LOS TRABAJADORES', 1, 175),
(7, 'BANCO CARONI C.A. BANCO UNIVERSAL', 1, 128),
(8, 'BANCO DE DESARROLLO DEL MICROEMPRESARIO', 1, 164),
(9, 'BANCO DE VENEZUELA S.A.I.C.A.', 1, 102),
(10, 'BANCO DEL CARIBE C.A.', 1, 114),
(11, 'BANCO DEL PUEBLO SOBERANO C.A.', 1, 149),
(12, 'BANCO DEL TESORO', 1, 163),
(13, 'BANCO ESPIRITO SANTO S.A.', 1, 176),
(14, 'BANCO EXTERIOR C.A.', 1, 115),
(15, 'BANCO INDUSTRIAL DE VENEZUELA.', 1, 3),
(16, 'BANCO INTERNACIONAL DE DESARROLLO C.A.', 1, 173),
(17, 'BANCO MERCANTIL C.A.', 1, 105),
(18, 'BANCO NACIONAL DE CREDITO', 1, 191),
(19, 'BANCO OCCIDENTAL DE DESCUENTO.', 1, 116),
(20, 'BANCO PLAZA', 1, 138),
(21, 'BANCO PROVINCIAL BBVA', 1, 108),
(22, 'BANCO VENEZOLANO DE CREDITO S.A.', 1, 104),
(23, 'BANCRECER S.A. BANCO DE DESARROLLO', 1, 168),
(24, 'BANESCO BANCO UNIVERSAL', 1, 134),
(25, 'BANFANB', 1, 177),
(26, 'BANGENTE', 1, 146),
(27, 'BANPLUS BANCO COMERCIAL C.A', 1, 174),
(28, 'CITIBANK', 1, 190),
(29, 'CORP BANCA', 1, 121),
(30, 'DELSUR BANCO UNIVERSAL', 1, 157),
(31, 'FONDO COMUN', 1, 151),
(32, 'INSTITUTO MUNICIPAL DE CRÃ‰DITO POPULAR', 1, 601),
(33, 'MIBANCO BANCO DE DESARROLLO C.A.', 1, 169),
(34, 'SOFITASA', 1, 137);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `billeteras_cripto`
--

CREATE TABLE `billeteras_cripto` (
  `id_Billetera_Cripto` int(11) NOT NULL,
  `Billetera` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Status_id` int(11) DEFAULT 1,
  `Medicos_id` int(11) DEFAULT NULL,
  `Cripto_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `citas_consultas`
--

CREATE TABLE `citas_consultas` (
  `id_Cita_Consulta` int(11) NOT NULL,
  `Agenda_id` int(11) DEFAULT NULL,
  `Paciente_id` int(11) DEFAULT NULL,
  `Paciente_Especial_id` int(11) DEFAULT NULL,
  `Medico_id` int(11) DEFAULT NULL,
  `Asistente_id` int(11) DEFAULT NULL,
  `Horario_Cita_Paciente` int(11) DEFAULT NULL,
  `Max_paciente` int(11) DEFAULT NULL,
  `Costo` float(20,2) DEFAULT NULL,
  `Nota` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Status_Consulta_id` int(11) DEFAULT 1,
  `title` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `start` datetime NOT NULL,
  `end` datetime NOT NULL,
  `color` varchar(20) COLLATE utf8_unicode_ci NOT NULL DEFAULT '#378006',
  `confirmado` tinyint(1) NOT NULL DEFAULT 0,
  `disponibilidad` int(100) DEFAULT 0,
  `id_servicio` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `citas_consultas`
--

INSERT INTO `citas_consultas` (`id_Cita_Consulta`, `Agenda_id`, `Paciente_id`, `Paciente_Especial_id`, `Medico_id`, `Asistente_id`, `Horario_Cita_Paciente`, `Max_paciente`, `Costo`, `Nota`, `Status_Consulta_id`, `title`, `start`, `end`, `color`, `confirmado`, `disponibilidad`, `id_servicio`) VALUES
(1, 1, 1, NULL, 1, NULL, 1, 10, 5.00, 'no tengo con quien ir', 1, 'Usuario Paciente - test', '2022-03-30 19:00:00', '2022-03-30 19:30:00', '#378006', 1, 0, 1),
(2, 1, 1, NULL, 1, NULL, 1, 10, 5.00, 'test', 1, 'Usuario Paciente - test', '2022-04-07 12:05:00', '2022-04-07 12:35:00', '#378006', 1, 0, 1),
(3, 1, 1, NULL, 1, NULL, 1, 10, 5.00, 'test test', 1, 'Usuario Paciente - test', '2022-04-07 14:00:00', '2022-04-07 14:30:00', '#378006', 1, 0, 1),
(4, 1, 1, NULL, 1, NULL, 1, 10, 5.00, 'test whatsapp', 1, 'Usuario Paciente - test', '2022-04-07 16:00:00', '2022-04-07 16:30:00', '#378006', 1, 0, 1),
(5, 2, 1, NULL, 1, NULL, 2, 20, 5.00, 'test', 1, 'Usuario Paciente - test', '2022-04-19 10:00:00', '2022-04-19 10:30:00', '#378006', 1, 0, 1),
(6, 2, 1, NULL, 1, NULL, 2, 20, 10.00, 'no puedo beber mucha agua', 1, 'Usuario Paciente - test', '2022-04-19 10:30:00', '2022-04-19 11:00:00', '#378006', 1, 0, 2),
(11, 2, 1, NULL, 1, NULL, 2, 20, 5.00, 'tst', 1, 'Usuario test Paciente - tst', '2022-04-25 08:30:00', '2022-04-25 09:00:00', '#378006', 1, 0, 1),
(18, 2, 1, NULL, 1, NULL, 2, 20, 5.00, 'test new', 1, 'Usuario test Paciente - test', '2022-04-25 11:00:00', '2022-04-25 11:59:00', '#378006', 1, 0, 1),
(19, 1, 1, NULL, 1, NULL, 1, 10, 7.00, 'test cierre', 1, 'Usuario test Paciente - cierre', '2022-04-25 17:30:00', '2022-04-25 18:45:00', '#378006', 1, 0, 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ciudades`
--

CREATE TABLE `ciudades` (
  `id_Ciudad` int(11) NOT NULL,
  `Estado_id` int(11) DEFAULT NULL,
  `Ciudad` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Capital` tinyint(4) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `ciudades`
--

INSERT INTO `ciudades` (`id_Ciudad`, `Estado_id`, `Ciudad`, `Capital`) VALUES
(1, 1, 'Maroa', 0),
(2, 1, 'Puerto Ayacucho', 1),
(3, 1, 'San Fernando de Atabapo', 0),
(4, 2, 'Anaco', 0),
(5, 2, 'Aragua de Barcelona', 0),
(6, 2, 'Barcelona', 1),
(7, 2, 'Boca de Uchire', 0),
(8, 2, 'Cantaura', 0),
(9, 2, 'Clarines', 0),
(10, 2, 'El Chaparro', 0),
(11, 2, 'El Pao Anzoátegui', 0),
(12, 2, 'El Tigre', 0),
(13, 2, 'El Tigrito', 0),
(14, 2, 'Guanape', 0),
(15, 2, 'Guanta', 0),
(16, 2, 'Lechería', 0),
(17, 2, 'Onoto', 0),
(18, 2, 'Pariaguán', 0),
(19, 2, 'Píritu', 0),
(20, 2, 'Puerto La Cruz', 0),
(21, 2, 'Puerto Píritu', 0),
(22, 2, 'Sabana de Uchire', 0),
(23, 2, 'San Mateo Anzoátegui', 0),
(24, 2, 'San Pablo Anzoátegui', 0),
(25, 2, 'San Tomé', 0),
(26, 2, 'Santa Ana de Anzoátegui', 0),
(27, 2, 'Santa Fe Anzoátegui', 0),
(28, 2, 'Santa Rosa', 0),
(29, 2, 'Soledad', 0),
(30, 2, 'Urica', 0),
(31, 2, 'Valle de Guanape', 0),
(43, 3, 'Achaguas', 0),
(44, 3, 'Biruaca', 0),
(45, 3, 'Bruzual', 0),
(46, 3, 'El Amparo', 0),
(47, 3, 'El Nula', 0),
(48, 3, 'Elorza', 0),
(49, 3, 'Guasdualito', 0),
(50, 3, 'Mantecal', 0),
(51, 3, 'Puerto Páez', 0),
(52, 3, 'San Fernando de Apure', 1),
(53, 3, 'San Juan de Payara', 0),
(54, 4, 'Barbacoas', 0),
(55, 4, 'Cagua', 0),
(56, 4, 'Camatagua', 0),
(58, 4, 'Choroní', 0),
(59, 4, 'Colonia Tovar', 0),
(60, 4, 'El Consejo', 0),
(61, 4, 'La Victoria', 0),
(62, 4, 'Las Tejerías', 0),
(63, 4, 'Magdaleno', 0),
(64, 4, 'Maracay', 1),
(65, 4, 'Ocumare de La Costa', 0),
(66, 4, 'Palo Negro', 0),
(67, 4, 'San Casimiro', 0),
(68, 4, 'San Mateo', 0),
(69, 4, 'San Sebastián', 0),
(70, 4, 'Santa Cruz de Aragua', 0),
(71, 4, 'Tocorón', 0),
(72, 4, 'Turmero', 0),
(73, 4, 'Villa de Cura', 0),
(74, 4, 'Zuata', 0),
(75, 5, 'Barinas', 1),
(76, 5, 'Barinitas', 0),
(77, 5, 'Barrancas', 0),
(78, 5, 'Calderas', 0),
(79, 5, 'Capitanejo', 0),
(80, 5, 'Ciudad Bolivia', 0),
(81, 5, 'El Cantón', 0),
(82, 5, 'Las Veguitas', 0),
(83, 5, 'Libertad de Barinas', 0),
(84, 5, 'Sabaneta', 0),
(85, 5, 'Santa Bárbara de Barinas', 0),
(86, 5, 'Socopó', 0),
(87, 6, 'Caicara del Orinoco', 0),
(88, 6, 'Canaima', 0),
(89, 6, 'Ciudad Bolívar', 1),
(90, 6, 'Ciudad Piar', 0),
(91, 6, 'El Callao', 0),
(92, 6, 'El Dorado', 0),
(93, 6, 'El Manteco', 0),
(94, 6, 'El Palmar', 0),
(95, 6, 'El Pao', 0),
(96, 6, 'Guasipati', 0),
(97, 6, 'Guri', 0),
(98, 6, 'La Paragua', 0),
(99, 6, 'Matanzas', 0),
(100, 6, 'Puerto Ordaz', 0),
(101, 6, 'San Félix', 0),
(102, 6, 'Santa Elena de Uairén', 0),
(103, 6, 'Tumeremo', 0),
(104, 6, 'Unare', 0),
(105, 6, 'Upata', 0),
(106, 7, 'Bejuma', 0),
(107, 7, 'Belén', 0),
(108, 7, 'Campo de Carabobo', 0),
(109, 7, 'Canoabo', 0),
(110, 7, 'Central Tacarigua', 0),
(111, 7, 'Chirgua', 0),
(112, 7, 'Ciudad Alianza', 0),
(113, 7, 'El Palito', 0),
(114, 7, 'Guacara', 0),
(115, 7, 'Guigue', 0),
(116, 7, 'Las Trincheras', 0),
(117, 7, 'Los Guayos', 0),
(118, 7, 'Mariara', 0),
(119, 7, 'Miranda', 0),
(120, 7, 'Montalbán', 0),
(121, 7, 'Morón', 0),
(122, 7, 'Naguanagua', 0),
(123, 7, 'Puerto Cabello', 0),
(124, 7, 'San Joaquín', 0),
(125, 7, 'Tocuyito', 0),
(126, 7, 'Urama', 0),
(127, 7, 'Valencia', 1),
(128, 7, 'Vigirimita', 0),
(129, 8, 'Aguirre', 0),
(130, 8, 'Apartaderos Cojedes', 0),
(131, 8, 'Arismendi', 0),
(132, 8, 'Camuriquito', 0),
(133, 8, 'El Baúl', 0),
(134, 8, 'El Limón', 0),
(135, 8, 'El Pao Cojedes', 0),
(136, 8, 'El Socorro', 0),
(137, 8, 'La Aguadita', 0),
(138, 8, 'Las Vegas', 0),
(139, 8, 'Libertad de Cojedes', 0),
(140, 8, 'Mapuey', 0),
(141, 8, 'Piñedo', 0),
(142, 8, 'Samancito', 0),
(143, 8, 'San Carlos', 1),
(144, 8, 'Sucre', 0),
(145, 8, 'Tinaco', 0),
(146, 8, 'Tinaquillo', 0),
(147, 8, 'Vallecito', 0),
(148, 9, 'Tucupita', 1),
(149, 24, 'Caracas', 1),
(150, 24, 'El Junquito', 0),
(151, 10, 'Adícora', 0),
(152, 10, 'Boca de Aroa', 0),
(153, 10, 'Cabure', 0),
(154, 10, 'Capadare', 0),
(155, 10, 'Capatárida', 0),
(156, 10, 'Chichiriviche', 0),
(157, 10, 'Churuguara', 0),
(158, 10, 'Coro', 1),
(159, 10, 'Cumarebo', 0),
(160, 10, 'Dabajuro', 0),
(161, 10, 'Judibana', 0),
(162, 10, 'La Cruz de Taratara', 0),
(163, 10, 'La Vela de Coro', 0),
(164, 10, 'Los Taques', 0),
(165, 10, 'Maparari', 0),
(166, 10, 'Mene de Mauroa', 0),
(167, 10, 'Mirimire', 0),
(168, 10, 'Pedregal', 0),
(169, 10, 'Píritu Falcón', 0),
(170, 10, 'Pueblo Nuevo Falcón', 0),
(171, 10, 'Puerto Cumarebo', 0),
(172, 10, 'Punta Cardón', 0),
(173, 10, 'Punto Fijo', 0),
(174, 10, 'San Juan de Los Cayos', 0),
(175, 10, 'San Luis', 0),
(176, 10, 'Santa Ana Falcón', 0),
(177, 10, 'Santa Cruz De Bucaral', 0),
(178, 10, 'Tocopero', 0),
(179, 10, 'Tocuyo de La Costa', 0),
(180, 10, 'Tucacas', 0),
(181, 10, 'Yaracal', 0),
(182, 11, 'Altagracia de Orituco', 0),
(183, 11, 'Cabruta', 0),
(184, 11, 'Calabozo', 0),
(185, 11, 'Camaguán', 0),
(196, 11, 'Chaguaramas Guárico', 0),
(197, 11, 'El Socorro', 0),
(198, 11, 'El Sombrero', 0),
(199, 11, 'Las Mercedes de Los Llanos', 0),
(200, 11, 'Lezama', 0),
(201, 11, 'Onoto', 0),
(202, 11, 'Ortíz', 0),
(203, 11, 'San José de Guaribe', 0),
(204, 11, 'San Juan de Los Morros', 1),
(205, 11, 'San Rafael de Laya', 0),
(206, 11, 'Santa María de Ipire', 0),
(207, 11, 'Tucupido', 0),
(208, 11, 'Valle de La Pascua', 0),
(209, 11, 'Zaraza', 0),
(210, 12, 'Aguada Grande', 0),
(211, 12, 'Atarigua', 0),
(212, 12, 'Barquisimeto', 1),
(213, 12, 'Bobare', 0),
(214, 12, 'Cabudare', 0),
(215, 12, 'Carora', 0),
(216, 12, 'Cubiro', 0),
(217, 12, 'Cují', 0),
(218, 12, 'Duaca', 0),
(219, 12, 'El Manzano', 0),
(220, 12, 'El Tocuyo', 0),
(221, 12, 'Guaríco', 0),
(222, 12, 'Humocaro Alto', 0),
(223, 12, 'Humocaro Bajo', 0),
(224, 12, 'La Miel', 0),
(225, 12, 'Moroturo', 0),
(226, 12, 'Quíbor', 0),
(227, 12, 'Río Claro', 0),
(228, 12, 'Sanare', 0),
(229, 12, 'Santa Inés', 0),
(230, 12, 'Sarare', 0),
(231, 12, 'Siquisique', 0),
(232, 12, 'Tintorero', 0),
(233, 13, 'Apartaderos Mérida', 0),
(234, 13, 'Arapuey', 0),
(235, 13, 'Bailadores', 0),
(236, 13, 'Caja Seca', 0),
(237, 13, 'Canaguá', 0),
(238, 13, 'Chachopo', 0),
(239, 13, 'Chiguara', 0),
(240, 13, 'Ejido', 0),
(241, 13, 'El Vigía', 0),
(242, 13, 'La Azulita', 0),
(243, 13, 'La Playa', 0),
(244, 13, 'Lagunillas Mérida', 0),
(245, 13, 'Mérida', 1),
(246, 13, 'Mesa de Bolívar', 0),
(247, 13, 'Mucuchíes', 0),
(248, 13, 'Mucujepe', 0),
(249, 13, 'Mucuruba', 0),
(250, 13, 'Nueva Bolivia', 0),
(251, 13, 'Palmarito', 0),
(252, 13, 'Pueblo Llano', 0),
(253, 13, 'Santa Cruz de Mora', 0),
(254, 13, 'Santa Elena de Arenales', 0),
(255, 13, 'Santo Domingo', 0),
(256, 13, 'Tabáy', 0),
(257, 13, 'Timotes', 0),
(258, 13, 'Torondoy', 0),
(259, 13, 'Tovar', 0),
(260, 13, 'Tucani', 0),
(261, 13, 'Zea', 0),
(262, 14, 'Araguita', 0),
(263, 14, 'Carrizal', 0),
(264, 14, 'Caucagua', 0),
(265, 14, 'Chaguaramas Miranda', 0),
(266, 14, 'Charallave', 0),
(267, 14, 'Chirimena', 0),
(268, 14, 'Chuspa', 0),
(269, 14, 'Cúa', 0),
(270, 14, 'Cupira', 0),
(271, 14, 'Curiepe', 0),
(272, 14, 'El Guapo', 0),
(273, 14, 'El Jarillo', 0),
(274, 14, 'Filas de Mariche', 0),
(275, 14, 'Guarenas', 0),
(276, 14, 'Guatire', 0),
(277, 14, 'Higuerote', 0),
(278, 14, 'Los Anaucos', 0),
(279, 14, 'Los Teques', 1),
(280, 14, 'Ocumare del Tuy', 0),
(281, 14, 'Panaquire', 0),
(282, 14, 'Paracotos', 0),
(283, 14, 'Río Chico', 0),
(284, 14, 'San Antonio de Los Altos', 0),
(285, 14, 'San Diego de Los Altos', 0),
(286, 14, 'San Fernando del Guapo', 0),
(287, 14, 'San Francisco de Yare', 0),
(288, 14, 'San José de Los Altos', 0),
(289, 14, 'San José de Río Chico', 0),
(290, 14, 'San Pedro de Los Altos', 0),
(291, 14, 'Santa Lucía', 0),
(292, 14, 'Santa Teresa', 0),
(293, 14, 'Tacarigua de La Laguna', 0),
(294, 14, 'Tacarigua de Mamporal', 0),
(295, 14, 'Tácata', 0),
(296, 14, 'Turumo', 0),
(297, 15, 'Aguasay', 0),
(298, 15, 'Aragua de Maturín', 0),
(299, 15, 'Barrancas del Orinoco', 0),
(300, 15, 'Caicara de Maturín', 0),
(301, 15, 'Caripe', 0),
(302, 15, 'Caripito', 0),
(303, 15, 'Chaguaramal', 0),
(305, 15, 'Chaguaramas Monagas', 0),
(307, 15, 'El Furrial', 0),
(308, 15, 'El Tejero', 0),
(309, 15, 'Jusepín', 0),
(310, 15, 'La Toscana', 0),
(311, 15, 'Maturín', 1),
(312, 15, 'Miraflores', 0),
(313, 15, 'Punta de Mata', 0),
(314, 15, 'Quiriquire', 0),
(315, 15, 'San Antonio de Maturín', 0),
(316, 15, 'San Vicente Monagas', 0),
(317, 15, 'Santa Bárbara', 0),
(318, 15, 'Temblador', 0),
(319, 15, 'Teresen', 0),
(320, 15, 'Uracoa', 0),
(321, 16, 'Altagracia', 0),
(322, 16, 'Boca de Pozo', 0),
(323, 16, 'Boca de Río', 0),
(324, 16, 'El Espinal', 0),
(325, 16, 'El Valle del Espíritu Santo', 0),
(326, 16, 'El Yaque', 0),
(327, 16, 'Juangriego', 0),
(328, 16, 'La Asunción', 1),
(329, 16, 'La Guardia', 0),
(330, 16, 'Pampatar', 0),
(331, 16, 'Porlamar', 0),
(332, 16, 'Puerto Fermín', 0),
(333, 16, 'Punta de Piedras', 0),
(334, 16, 'San Francisco de Macanao', 0),
(335, 16, 'San Juan Bautista', 0),
(336, 16, 'San Pedro de Coche', 0),
(337, 16, 'Santa Ana de Nueva Esparta', 0),
(338, 16, 'Villa Rosa', 0),
(339, 17, 'Acarigua', 0),
(340, 17, 'Agua Blanca', 0),
(341, 17, 'Araure', 0),
(342, 17, 'Biscucuy', 0),
(343, 17, 'Boconoito', 0),
(344, 17, 'Campo Elías', 0),
(345, 17, 'Chabasquén', 0),
(346, 17, 'Guanare', 1),
(347, 17, 'Guanarito', 0),
(348, 17, 'La Aparición', 0),
(349, 17, 'La Misión', 0),
(350, 17, 'Mesa de Cavacas', 0),
(351, 17, 'Ospino', 0),
(352, 17, 'Papelón', 0),
(353, 17, 'Payara', 0),
(354, 17, 'Pimpinela', 0),
(355, 17, 'Píritu de Portuguesa', 0),
(356, 17, 'San Rafael de Onoto', 0),
(357, 17, 'Santa Rosalía', 0),
(358, 17, 'Turén', 0),
(359, 18, 'Altos de Sucre', 0),
(360, 18, 'Araya', 0),
(361, 18, 'Cariaco', 0),
(362, 18, 'Carúpano', 0),
(363, 18, 'Casanay', 0),
(364, 18, 'Cumaná', 1),
(365, 18, 'Cumanacoa', 0),
(366, 18, 'El Morro Puerto Santo', 0),
(367, 18, 'El Pilar', 0),
(368, 18, 'El Poblado', 0),
(369, 18, 'Guaca', 0),
(370, 18, 'Guiria', 0),
(371, 18, 'Irapa', 0),
(372, 18, 'Manicuare', 0),
(373, 18, 'Mariguitar', 0),
(374, 18, 'Río Caribe', 0),
(375, 18, 'San Antonio del Golfo', 0),
(376, 18, 'San José de Aerocuar', 0),
(377, 18, 'San Vicente de Sucre', 0),
(378, 18, 'Santa Fe de Sucre', 0),
(379, 18, 'Tunapuy', 0),
(380, 18, 'Yaguaraparo', 0),
(381, 18, 'Yoco', 0),
(382, 19, 'Abejales', 0),
(383, 19, 'Borota', 0),
(384, 19, 'Bramon', 0),
(385, 19, 'Capacho', 0),
(386, 19, 'Colón', 0),
(387, 19, 'Coloncito', 0),
(388, 19, 'Cordero', 0),
(389, 19, 'El Cobre', 0),
(390, 19, 'El Pinal', 0),
(391, 19, 'Independencia', 0),
(392, 19, 'La Fría', 0),
(393, 19, 'La Grita', 0),
(394, 19, 'La Pedrera', 0),
(395, 19, 'La Tendida', 0),
(396, 19, 'Las Delicias', 0),
(397, 19, 'Las Hernández', 0),
(398, 19, 'Lobatera', 0),
(399, 19, 'Michelena', 0),
(400, 19, 'Palmira', 0),
(401, 19, 'Pregonero', 0),
(402, 19, 'Queniquea', 0),
(403, 19, 'Rubio', 0),
(404, 19, 'San Antonio del Tachira', 0),
(405, 19, 'San Cristobal', 1),
(406, 19, 'San José de Bolívar', 0),
(407, 19, 'San Josecito', 0),
(408, 19, 'San Pedro del Río', 0),
(409, 19, 'Santa Ana Táchira', 0),
(410, 19, 'Seboruco', 0),
(411, 19, 'Táriba', 0),
(412, 19, 'Umuquena', 0),
(413, 19, 'Ureña', 0),
(414, 20, 'Batatal', 0),
(415, 20, 'Betijoque', 0),
(416, 20, 'Boconó', 0),
(417, 20, 'Carache', 0),
(418, 20, 'Chejende', 0),
(419, 20, 'Cuicas', 0),
(420, 20, 'El Dividive', 0),
(421, 20, 'El Jaguito', 0),
(422, 20, 'Escuque', 0),
(423, 20, 'Isnotú', 0),
(424, 20, 'Jajó', 0),
(425, 20, 'La Ceiba', 0),
(426, 20, 'La Concepción de Trujllo', 0),
(427, 20, 'La Mesa de Esnujaque', 0),
(428, 20, 'La Puerta', 0),
(429, 20, 'La Quebrada', 0),
(430, 20, 'Mendoza Fría', 0),
(431, 20, 'Meseta de Chimpire', 0),
(432, 20, 'Monay', 0),
(433, 20, 'Motatán', 0),
(434, 20, 'Pampán', 0),
(435, 20, 'Pampanito', 0),
(436, 20, 'Sabana de Mendoza', 0),
(437, 20, 'San Lázaro', 0),
(438, 20, 'Santa Ana de Trujillo', 0),
(439, 20, 'Tostós', 0),
(440, 20, 'Trujillo', 1),
(441, 20, 'Valera', 0),
(442, 21, 'Carayaca', 0),
(443, 21, 'Litoral', 0),
(444, 25, 'Archipiélago Los Roques', 0),
(445, 22, 'Aroa', 0),
(446, 22, 'Boraure', 0),
(447, 22, 'Campo Elías de Yaracuy', 0),
(448, 22, 'Chivacoa', 0),
(449, 22, 'Cocorote', 0),
(450, 22, 'Farriar', 0),
(451, 22, 'Guama', 0),
(452, 22, 'Marín', 0),
(453, 22, 'Nirgua', 0),
(454, 22, 'Sabana de Parra', 0),
(455, 22, 'Salom', 0),
(456, 22, 'San Felipe', 1),
(457, 22, 'San Pablo de Yaracuy', 0),
(458, 22, 'Urachiche', 0),
(459, 22, 'Yaritagua', 0),
(460, 22, 'Yumare', 0),
(461, 23, 'Bachaquero', 0),
(462, 23, 'Bobures', 0),
(463, 23, 'Cabimas', 0),
(464, 23, 'Campo Concepción', 0),
(465, 23, 'Campo Mara', 0),
(466, 23, 'Campo Rojo', 0),
(467, 23, 'Carrasquero', 0),
(468, 23, 'Casigua', 0),
(469, 23, 'Chiquinquirá', 0),
(470, 23, 'Ciudad Ojeda', 0),
(471, 23, 'El Batey', 0),
(472, 23, 'El Carmelo', 0),
(473, 23, 'El Chivo', 0),
(474, 23, 'El Guayabo', 0),
(475, 23, 'El Mene', 0),
(476, 23, 'El Venado', 0),
(477, 23, 'Encontrados', 0),
(478, 23, 'Gibraltar', 0),
(479, 23, 'Isla de Toas', 0),
(480, 23, 'La Concepción del Zulia', 0),
(481, 23, 'La Paz', 0),
(482, 23, 'La Sierrita', 0),
(483, 23, 'Lagunillas del Zulia', 0),
(484, 23, 'Las Piedras de Perijá', 0),
(485, 23, 'Los Cortijos', 0),
(486, 23, 'Machiques', 0),
(487, 23, 'Maracaibo', 1),
(488, 23, 'Mene Grande', 0),
(489, 23, 'Palmarejo', 0),
(490, 23, 'Paraguaipoa', 0),
(491, 23, 'Potrerito', 0),
(492, 23, 'Pueblo Nuevo del Zulia', 0),
(493, 23, 'Puertos de Altagracia', 0),
(494, 23, 'Punta Gorda', 0),
(495, 23, 'Sabaneta de Palma', 0),
(496, 23, 'San Francisco', 0),
(497, 23, 'San José de Perijá', 0),
(498, 23, 'San Rafael del Moján', 0),
(499, 23, 'San Timoteo', 0),
(500, 23, 'Santa Bárbara Del Zulia', 0),
(501, 23, 'Santa Cruz de Mara', 0),
(502, 23, 'Santa Cruz del Zulia', 0),
(503, 23, 'Santa Rita', 0),
(504, 23, 'Sinamaica', 0),
(505, 23, 'Tamare', 0),
(506, 23, 'Tía Juana', 0),
(507, 23, 'Villa del Rosario', 0),
(508, 21, 'La Guaira', 1),
(509, 21, 'Catia La Mar', 0),
(510, 21, 'Macuto', 0),
(511, 21, 'Naiguatá', 0),
(512, 25, 'Archipiélago Los Monjes', 0),
(513, 25, 'Isla La Tortuga y Cayos adyacentes', 0),
(514, 25, 'Isla La Sola', 0),
(515, 25, 'Islas Los Testigos', 0),
(516, 25, 'Islas Los Frailes', 0),
(517, 25, 'Isla La Orchila', 0),
(518, 25, 'Archipiélago Las Aves', 0),
(519, 25, 'Isla de Aves', 0),
(520, 25, 'Isla La Blanquilla', 0),
(521, 25, 'Isla de Patos', 0),
(522, 25, 'Islas Los Hermanos', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `consultorios`
--

CREATE TABLE `consultorios` (
  `id_Consultorio` int(11) NOT NULL,
  `Direccion` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
-- cambio con respecto a la original para identificar el numero del consultorio
  `numero_consultorio` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL, 
  `Telefono` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Celular` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Correo` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Especialidad_Medica_id` int(11) DEFAULT NULL,
  `Ciudad_id` int(11) DEFAULT NULL,
  `Estado_id` int(11) DEFAULT NULL,
  `Municipio_id` int(11) DEFAULT NULL,
  `Parroquia_id` int(11) DEFAULT NULL,
  `Status_id` int(11) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `consultorios`
--

INSERT INTO `consultorios` (`id_Consultorio`, `Direccion`, `Local`, `Telefono`, `Celular`, `Correo`, `Especialidad_Medica_id`, `Ciudad_id`, `Estado_id`, `Municipio_id`, `Parroquia_id`, `Status_id`) VALUES
(1, 'Simon rodriguez', 'L-32', '02514468334', '04129977546', 'local32@test.com', 1, 212, 12, 146, 462, 1),
(2, 'Dirección de desarrollo', 'L-ps1', '02514447788', '04245163222', 'local_psicologia@test.com', 2, 210, 12, 145, 460, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `control_especialidades`
--

CREATE TABLE `control_especialidades` (
  `id_Control_Especialidad` int(11) NOT NULL,
  `Medico_id` int(11) DEFAULT NULL,
  `Especialidades_Medicas_id` int(11) DEFAULT NULL,
  `Status_Medico_id` int(11) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `control_especialidades`
--

INSERT INTO `control_especialidades` (`id_Control_Especialidad`, `Medico_id`, `Especialidades_Medicas_id`, `Status_Medico_id`) VALUES
(1, 1, 1, 1),
(2, 2, 1, 1),
(3, 3, 2, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `control_historia_medicas`
--

CREATE TABLE `control_historia_medicas` (
  `id_Control_Historia_Medica` int(11) NOT NULL,
  `Especialidad_Medica_id` int(11) DEFAULT NULL,
  `Control_Especialidad_id` int(11) DEFAULT NULL,
  `Medico_id` int(11) DEFAULT NULL,
  `Paciente_id` int(11) DEFAULT NULL,
  `Paciente_Especial_id` int(11) DEFAULT NULL,
  `Cita_Consulta_id` int(11) DEFAULT NULL,
  `Fecha` datetime DEFAULT NULL,
  `id_servicio` int(11) DEFAULT NULL,
  `cerrado` tinyint(1) NOT NULL DEFAULT 0,
  `factura_generada` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `control_historia_medicas`
--

INSERT INTO `control_historia_medicas` (`id_Control_Historia_Medica`, `Especialidad_Medica_id`, `Control_Especialidad_id`, `Medico_id`, `Paciente_id`, `Paciente_Especial_id`, `Cita_Consulta_id`, `Fecha`, `id_servicio`, `cerrado`, `factura_generada`) VALUES
(1, 1, NULL, 1, 1, NULL, 1, '2022-03-30 00:00:00', 1, 1, 0),
(2, 1, NULL, 1, 1, NULL, 2, '2022-04-07 00:00:00', 1, 0, 0),
(3, 1, NULL, 1, 1, NULL, 3, '2022-04-07 00:00:00', 1, 0, 0),
(4, 1, NULL, 1, 1, NULL, 4, '2022-04-07 00:00:00', 1, 0, 0),
(5, 1, NULL, 1, 1, NULL, 5, '2022-04-19 00:00:00', 1, 1, 0),
(6, 1, NULL, 1, 1, NULL, 6, '2022-04-19 00:00:00', 2, 0, 0),
(12, 1, NULL, 1, 1, NULL, 11, '2022-04-25 00:00:00', 1, 1, 1),
(18, 1, NULL, 1, 1, NULL, 18, '2022-04-25 00:00:00', 1, 1, 1),
(19, 1, NULL, 1, 1, NULL, 19, '2022-04-25 00:00:00', 3, 1, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `criptos`
--

CREATE TABLE `criptos` (
  `id_Cripto` int(11) NOT NULL,
  `Criptop` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Status_id` int(11) DEFAULT 1,
  `Siglas` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cuenta_bancaria_bs`
--

CREATE TABLE `cuenta_bancaria_bs` (
  `id_Cuenta_Bancaria_BS` int(11) NOT NULL,
  `Banco_id` int(11) DEFAULT NULL,
  `Medico_id` int(11) DEFAULT NULL,
  `Status_id` int(11) DEFAULT NULL,
  `Numero_Cuenta` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Tipo` int(11) NOT NULL,
  `Fecha` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `cuenta_bancaria_bs`
--

INSERT INTO `cuenta_bancaria_bs` (`id_Cuenta_Bancaria_BS`, `Banco_id`, `Medico_id`, `Status_id`, `Numero_Cuenta`, `Tipo`, `Fecha`) VALUES
(1, 21, 1, 1, '01081000120045847856', 2, '2022-05-20 00:00:00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cuenta_usd`
--

CREATE TABLE `cuenta_usd` (
  `id_Cuenta_USD` int(11) NOT NULL,
  `Entidad_USD_id` int(11) DEFAULT NULL,
  `Medico_id` int(11) DEFAULT NULL,
  `Status_Pago` int(11) DEFAULT NULL,
  `Numero_Cuenta` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Tipo` int(11) DEFAULT NULL,
  `Fecha` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `datos_seniat`
--

CREATE TABLE `datos_seniat` (
  `id_Datos_SENIAT` int(11) NOT NULL,
  `RIF` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Direccion` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Medico_id` int(11) DEFAULT NULL,
  `Fecha` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `datos_seniat`
--

INSERT INTO `datos_seniat` (`id_Datos_SENIAT`, `RIF`, `Direccion`, `Medico_id`, `Fecha`) VALUES
(1, '18105604-1', 'dirección del usuario medico para el rif', 1, '2022-03-29 00:00:00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `direcciones_pacientes`
--

CREATE TABLE `direcciones_pacientes` (
  `id_Direccion_Paciente` int(11) NOT NULL,
  `Paciente_id` int(11) DEFAULT NULL,
  `Direccion` mediumtext COLLATE utf8_unicode_ci DEFAULT NULL,
  `Numero_Casa` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Telefono` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Celular` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Correo` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Cuidad_id` int(11) DEFAULT NULL,
  `Estado_id` int(11) DEFAULT NULL,
  `Municipio_id` int(11) DEFAULT NULL,
  `Parroquia_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `direcciones_pacientes`
--

INSERT INTO `direcciones_pacientes` (`id_Direccion_Paciente`, `Paciente_id`, `Direccion`, `Numero_Casa`, `Telefono`, `Celular`, `Correo`, `Cuidad_id`, `Estado_id`, `Municipio_id`, `Parroquia_id`) VALUES
(1, 1, 'Dirección paciente', '10-15', '02515555555', '584244145944', 'usuariop@test.com', NULL, 12, NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `entidades_usd`
--

CREATE TABLE `entidades_usd` (
  `id_Entidad_USD` int(11) NOT NULL,
  `Entidad_USD` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Status_id` int(11) DEFAULT NULL,
  `Referencia` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `especialidades_medicas`
--

CREATE TABLE `especialidades_medicas` (
  `id_Especialidad_Medica` int(11) NOT NULL,
  `Espacialiadad_Medica` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `especialidades_medicas`
--

INSERT INTO `especialidades_medicas` (`id_Especialidad_Medica`, `Espacialiadad_Medica`) VALUES
(1, 'Medico general'),
(2, 'Psicología');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estados`
--

CREATE TABLE `estados` (
  `id_Estado` int(11) NOT NULL,
  `Estado` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `estados`
--

INSERT INTO `estados` (`id_Estado`, `Estado`) VALUES
(1, 'Amazonas'),
(2, 'Anzoátegui'),
(3, 'Apure'),
(4, 'Aragua'),
(5, 'Barinas'),
(6, 'Bolívar'),
(7, 'Carabobo'),
(8, 'Cojedes'),
(9, 'Delta Amacuro'),
(10, 'Falcón'),
(11, 'Guárico'),
(12, 'Lara'),
(13, 'Mérida'),
(14, 'Miranda'),
(15, 'Monagas'),
(16, 'Nueva Esparta'),
(17, 'Portuguesa'),
(18, 'Sucre'),
(19, 'Táchira'),
(20, 'Trujillo'),
(21, 'Vargas'),
(22, 'Yaracuy'),
(23, 'Zulia'),
(24, 'Distrito Capital'),
(25, 'Dependencias Federales');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estados_civiles`
--

CREATE TABLE `estados_civiles` (
  `id_Civil` int(11) NOT NULL,
  `Civil` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `estados_civiles`
--

INSERT INTO `estados_civiles` (`id_Civil`, `Civil`) VALUES
(1, 'Soltero(a)'),
(2, 'Casado(a)');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `facturas`
--

CREATE TABLE `facturas` (
  `id_Factura` int(11) NOT NULL,
  `Cita_Consulta_id` int(11) DEFAULT NULL,
  `Fecha` datetime DEFAULT NULL,
  `Datos_SENIAT_id` int(11) DEFAULT NULL,
  `Pacientes_id` int(11) DEFAULT NULL,
  `Status_Factura_id` int(11) DEFAULT NULL,
  `Relacion_Medico` int(11) DEFAULT NULL,
  `Medico_id` int(11) DEFAULT NULL,
  `Asistente_id` int(11) DEFAULT NULL,
  `Nombre` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Apellido` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `CIDNI` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Status_no_paciente` int(11) DEFAULT NULL,
  `moneda_cancela` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `facturas`
--

INSERT INTO `facturas` (`id_Factura`, `Cita_Consulta_id`, `Fecha`, `Datos_SENIAT_id`, `Pacientes_id`, `Status_Factura_id`, `Relacion_Medico`, `Medico_id`, `Asistente_id`, `Nombre`, `Apellido`, `CIDNI`, `Status_no_paciente`, `moneda_cancela`) VALUES
(14, 11, '2022-05-03 00:00:00', 1, 1, NULL, NULL, 1, 4, 'Usuario test', 'Paciente', 'V - 11999664', 1, NULL),
(17, 11, '2022-05-03 00:00:00', 1, 1, NULL, NULL, 1, 4, 'Usuario test', 'Paciente', 'V - 11999664', 1, NULL),
(18, 11, '2022-05-03 00:00:00', 1, 1, NULL, NULL, 1, 4, 'Usuario test', 'Paciente', 'V - 11999664', 1, NULL),
(19, 11, '2022-05-03 00:00:00', 1, 1, NULL, NULL, 1, 4, 'Usuario test', 'Paciente', 'V - 11999664', 1, 'Bs'),
(20, 11, '2022-05-07 00:00:00', 1, 1, NULL, NULL, 1, 4, 'Usuario test', 'Paciente', 'V - 11999664', 1, 'Bs'),
(21, 11, '2022-05-24 00:00:00', 1, 1, NULL, NULL, 1, 4, 'Usuario test', 'Paciente', 'V - 11999664', 1, 'Bs'),
(22, 11, '2022-05-24 00:00:00', 1, 1, NULL, NULL, 1, 4, 'Usuario test', 'Paciente', 'V - 11999664', 1, 'Bs'),
(23, 11, '2022-05-24 00:00:00', 1, 1, NULL, NULL, 1, 4, 'Usuario test', 'Paciente', 'V - 11999664', 1, 'Bs'),
(24, 11, '2022-05-24 00:00:00', 1, 1, 1, NULL, 1, 4, 'Usuario test', 'Paciente', 'V - 11999664', 1, 'Bs');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `factura_detalle`
--

CREATE TABLE `factura_detalle` (
  `id_Factura_Detalle` int(11) NOT NULL,
  `Factura_id` int(11) DEFAULT NULL,
  `Servicio_id` int(11) DEFAULT NULL,
  `Cantidad` int(11) DEFAULT NULL,
  `Costo_Servicio` decimal(10,2) DEFAULT NULL,
  `moneda` varchar(11) COLLATE utf8_unicode_ci DEFAULT NULL,
  `iva` decimal(10,2) DEFAULT NULL,
  `Status_Factura_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `factura_detalle`
--

INSERT INTO `factura_detalle` (`id_Factura_Detalle`, `Factura_id`, `Servicio_id`, `Cantidad`, `Costo_Servicio`, `moneda`, `iva`, `Status_Factura_id`) VALUES
(12, 14, 1, 1, '5.00', 'USD', '0.60', NULL),
(13, 14, 2, 1, '10.00', 'USD', '0.60', NULL),
(14, 14, 3, 1, '7.00', 'USD', '0.60', NULL),
(21, 17, 1, 1, '5.00', 'USD', '0.60', NULL),
(22, 17, 2, 1, '10.00', 'USD', '0.60', NULL),
(23, 17, 3, 1, '7.00', 'USD', '0.60', NULL),
(24, 18, 1, 1, '5.00', 'USD', '0.60', NULL),
(25, 18, 2, 1, '10.00', 'USD', '0.60', NULL),
(26, 18, 3, 1, '7.00', 'USD', '0.60', NULL),
(27, 19, 1, 1, '5.00', 'USD', '0.60', NULL),
(28, 19, 2, 1, '10.00', 'USD', '0.60', NULL),
(29, 19, 3, 1, '7.00', 'USD', '0.60', NULL),
(30, 20, 1, 1, '5.00', 'USD', '0.60', NULL),
(31, 20, 2, 1, '10.00', 'USD', '0.60', NULL),
(32, 20, 3, 1, '7.00', 'USD', '0.60', NULL),
(33, 21, 1, 1, '5.00', 'USD', '0.60', NULL),
(34, 21, 2, 1, '10.00', 'USD', '0.60', NULL),
(35, 21, 3, 1, '7.00', 'USD', '0.60', NULL),
(36, 22, 1, 1, '5.00', 'USD', '0.60', NULL),
(37, 22, 2, 1, '10.00', 'USD', '0.60', NULL),
(38, 22, 3, 1, '7.00', 'USD', '0.60', NULL),
(39, 23, 1, 1, '5.00', 'USD', '0.60', NULL),
(40, 23, 2, 1, '10.00', 'USD', '0.60', NULL),
(41, 23, 3, 1, '7.00', 'USD', '0.60', NULL),
(42, 24, 1, 1, '5.00', 'USD', '0.60', 1),
(43, 24, 2, 1, '10.00', 'USD', '0.60', 1),
(44, 24, 3, 1, '7.00', 'USD', '0.60', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `factura_total_bs`
--

CREATE TABLE `factura_total_bs` (
  `id_Factura_BS` int(11) NOT NULL,
  `Factura_Id` int(11) DEFAULT NULL,
  `Status_Tasa_id` int(11) DEFAULT NULL,
  `Status_Pago` int(11) DEFAULT NULL,
  `Cuenta_Bancaria_BS_id` int(11) DEFAULT NULL,
  `Efectivo` decimal(10,2) DEFAULT NULL,
  `Total_Cancelado` decimal(10,2) DEFAULT NULL,
  `Referencia_Bancaria` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Tipo_Pago_id` int(11) DEFAULT NULL,
  `comprobante` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `banco_emisor` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `factura_total_bs`
--

INSERT INTO `factura_total_bs` (`id_Factura_BS`, `Factura_Id`, `Status_Tasa_id`, `Status_Pago`, `Cuenta_Bancaria_BS_id`, `Efectivo`, `Total_Cancelado`, `Referencia_Bancaria`, `Tipo_Pago_id`, `comprobante`, `banco_emisor`) VALUES
(1, 17, 1, NULL, NULL, NULL, '104.41', NULL, 2, NULL, NULL),
(2, 18, 1, NULL, NULL, NULL, '104.41', NULL, 2, NULL, NULL),
(3, 19, 1, NULL, NULL, NULL, '104.41', NULL, 2, NULL, NULL),
(4, 20, 1, NULL, NULL, NULL, '104.41', NULL, 2, NULL, NULL),
(5, 21, 1, NULL, 1, NULL, '24.60', '5412369874125', 1, NULL, NULL),
(6, 22, 1, NULL, 1, NULL, '24.60', '5412369874125', 1, NULL, NULL),
(7, 23, 1, NULL, 1, NULL, '24.60', '5412369874125', 1, NULL, NULL),
(8, 24, 1, 1, 1, NULL, '24.60', '5412369874125', 1, NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `factura_total_cripto`
--

CREATE TABLE `factura_total_cripto` (
  `Id_Factura_Cripto` int(11) NOT NULL,
  `Factura_id` int(11) DEFAULT NULL,
  `Status_Tasa_id` int(11) DEFAULT NULL,
  `Status_Pago` int(11) DEFAULT NULL,
  `Billetera_Cripto_id` int(11) DEFAULT NULL,
  `Total_Cancelado` int(11) DEFAULT NULL,
  `Referencia` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Gas` decimal(10,0) DEFAULT NULL,
  `Nota` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Tipo_Pago_id` int(11) DEFAULT NULL,
  `comprobante` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `billetera_emisora` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `factura_total_usd`
--

CREATE TABLE `factura_total_usd` (
  `id_Factura_USD` int(11) NOT NULL,
  `Factura_id` int(11) DEFAULT NULL,
  `Status_Tasa_id` int(11) DEFAULT NULL,
  `Status_Pago` int(11) DEFAULT NULL,
  `Cuenta_USD_id` int(11) DEFAULT NULL,
  `Efectivo` int(11) DEFAULT NULL,
  `Total_Cancelado` decimal(10,2) DEFAULT NULL,
  `Referencia` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Tipo_Pago_id` int(11) DEFAULT NULL,
  `impuesto` decimal(10,2) DEFAULT NULL,
  `comprobante` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `entidad_emisora` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `historico_login_pacientes`
--

CREATE TABLE `historico_login_pacientes` (
  `id_Login_Pacientes` int(11) NOT NULL,
  `Login_Pacientes_id` int(11) DEFAULT NULL,
  `Old_contrasena` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Fecha` datetime DEFAULT NULL,
  `Paciente_id` int(11) DEFAULT NULL,
  `Correo` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Nota` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `historico_login_pacientes`
--

INSERT INTO `historico_login_pacientes` (`id_Login_Pacientes`, `Login_Pacientes_id`, `Old_contrasena`, `Fecha`, `Paciente_id`, `Correo`, `Nota`) VALUES
(1, 1, '$2y$10$UVBGDoECJF8Ghr4fgHqrAO1n4NiaXzikX4F6oaZ8z/6uFFrgqgm1W', '2022-04-19 00:00:00', 1, NULL, ''),
(2, 1, '$2y$10$KqAgMa73HHGFmSLcXCy/DeEc3gMSBviDna9cqZtyWhjDbIoA3huNa', '2022-04-19 00:00:00', 1, NULL, ''),
(3, 1, '$2y$10$3JJMQJ5zlfiX5p/Ykcwau.do8E.WYkJ.RfhCz6f5t9VTRrJVDzPoa', '2022-04-19 00:00:00', 1, NULL, ''),
(4, 1, '$2y$10$V5Ru2szRCJDPLvhficI5MuGI49PWSSunzXdkTAI6DS6kgy5FCpSgu', '2022-04-19 00:00:00', 1, NULL, ''),
(5, 1, '$2y$10$WO8hduanFA3pHWoE2anMpOlUHLJCp3cNLGxoBUrTxSsezStr9hwJ2', '2022-04-19 00:00:00', 1, NULL, ''),
(6, 1, '$2y$10$PqxaykqiRy5lvSlLJQHvm.OQBajk9J4knYt7UsYflELU8h5M/QR7m', '2022-04-19 00:00:00', 1, NULL, ''),
(7, 1, '$2y$10$9ny.tKWPvAVOjZzvmDb1cOopo/zIfRChIsZp..EhtWTCP7SfI9agu', '2022-04-19 00:00:00', 1, NULL, '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `historico_login_trabajadores`
--

CREATE TABLE `historico_login_trabajadores` (
  `id_Login_Trabajadores` int(11) NOT NULL,
  `Login_Tranajador_id` int(11) DEFAULT NULL,
  `Old_Constrasena` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Fecha` datetime DEFAULT NULL,
  `Medico_id` int(11) DEFAULT NULL,
  `Asistente_id` int(11) DEFAULT NULL,
  `Correo` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Nota` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `historico_login_trabajadores`
--

INSERT INTO `historico_login_trabajadores` (`id_Login_Trabajadores`, `Login_Tranajador_id`, `Old_Constrasena`, `Fecha`, `Medico_id`, `Asistente_id`, `Correo`, `Nota`) VALUES
(1, 2, '$2y$10$06FQ2k7FEGnwAlbXL4dN6umeAMgreQs69M5c8D95aMwS6up6HM3uC', '2022-03-30 00:00:00', 1, NULL, 'usuariom@test.com', ''),
(2, 2, '$2y$10$6E..uu.rgrQl1FJQtPGJ1uzJsnQDc08vVSgntNFDv8AJ2qtvFv4Vq', '2022-03-30 00:00:00', 1, NULL, 'usuariom@test.com', ''),
(3, 5, '$2y$10$aaxIWecA1i8pQkv3CqDXVuFhNy/xqPrg2qxxN48MnKs4eBmIU5S3C', '2022-04-19 00:00:00', 2, NULL, 'elvirateran58@gmail.com', ''),
(4, 5, '$2y$10$xYWcMQqZFsrQFiOUQCGRj.wR46H7fVXtWWETMhNUB58Cnzuz/Oo6G', '2022-04-19 00:00:00', 2, NULL, 'elvirateran158@gmail.com', ''),
(5, 5, '$2y$10$wG4eakAdtbvP0vj.p3sGD.H804J3C79XUC4YsdvRpS.cumG.c.fxO', '2022-04-19 00:00:00', 2, NULL, 'elvirateran58@gmail.com', ''),
(6, 5, '$2y$10$IHWiza2tm8hQreEvEogwFOj.adEiFOo1CckENYmUqPAvvqBJDUm6u', '2022-04-19 00:00:00', 2, NULL, 'elvirateran58@gmail.com', ''),
(7, 5, '$2y$10$cSU6K/2u9fXq3hyTjK5fEeTjkwHM0p2BRnb.wWyLoIv2BaXDMNRRW', '2022-04-19 00:00:00', 2, NULL, 'elvirateran158@gmail.com', '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `historico_pediatria`
--

CREATE TABLE `historico_pediatria` (
  `id_Historico_Pediatria` int(11) NOT NULL,
  `Fecha` datetime DEFAULT NULL,
  `Dato1` int(11) DEFAULT NULL,
  `Dato2` int(11) DEFAULT NULL,
  `Dato3` int(11) DEFAULT NULL,
  `Paciente_id` int(11) DEFAULT NULL,
  `Medico_id` int(11) DEFAULT NULL,
  `Paciente_pediatrico_Id` int(11) DEFAULT NULL,
  `Cita_Consulta_id` int(11) DEFAULT NULL,
  `Pediatria_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `horarios_citas`
--

CREATE TABLE `horarios_citas` (
  `id_Horario_Cita` int(11) NOT NULL,
  `Medico_id` int(11) NOT NULL,
  `Especialidad_id` int(11) NOT NULL,
  `turno_id` int(11) NOT NULL,
  `Domicilio` int(11) DEFAULT NULL,
  `Hora_Inicio_Lunes` time DEFAULT NULL,
  `Hora_Fin_Lunes` time DEFAULT NULL,
  `Lunes` int(11) DEFAULT NULL,
  `Hora_Inicio_Martes` time DEFAULT NULL,
  `Hora_Fin_Martes` time DEFAULT NULL,
  `Martes` int(11) DEFAULT NULL,
  `Horario_Inicio_Miercoles` time DEFAULT NULL,
  `Horario_Fin_Miercoles` time DEFAULT NULL,
  `Miercoles` int(11) DEFAULT NULL,
  `Horario_Inicio_Jueves` time DEFAULT NULL,
  `Horario_Fin_Jueves` time DEFAULT NULL,
  `Jueves` int(11) DEFAULT NULL,
  `Horario_Inicio_Viernes` time DEFAULT NULL,
  `Horario_Fin_Viernes` time DEFAULT NULL,
  `Viernes` int(11) DEFAULT NULL,
  `Horario_Inicio_Sabado` time DEFAULT NULL,
  `Horario_Fin_Sabado` time DEFAULT NULL,
  `Sabado` int(11) DEFAULT NULL,
  `Horario_inicio_Domingo` time DEFAULT NULL,
  `Horario_Fin_Domingo` time DEFAULT NULL,
  `Domingo` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `horarios_citas`
--

INSERT INTO `horarios_citas` (`id_Horario_Cita`, `Medico_id`, `Especialidad_id`, `turno_id`, `Domicilio`, `Hora_Inicio_Lunes`, `Hora_Fin_Lunes`, `Lunes`, `Hora_Inicio_Martes`, `Hora_Fin_Martes`, `Martes`, `Horario_Inicio_Miercoles`, `Horario_Fin_Miercoles`, `Miercoles`, `Horario_Inicio_Jueves`, `Horario_Fin_Jueves`, `Jueves`, `Horario_Inicio_Viernes`, `Horario_Fin_Viernes`, `Viernes`, `Horario_Inicio_Sabado`, `Horario_Fin_Sabado`, `Sabado`, `Horario_inicio_Domingo`, `Horario_Fin_Domingo`, `Domingo`) VALUES
(1, 1, 1, 2, 0, '12:05:00', '21:00:00', 1, NULL, NULL, 0, '12:05:00', '20:00:00', 1, '12:05:00', '20:00:00', 1, NULL, NULL, 0, NULL, NULL, 0, NULL, NULL, 0),
(2, 1, 1, 1, 0, '07:00:00', '11:59:00', 1, '07:00:00', '11:59:00', 1, NULL, NULL, 0, NULL, NULL, 0, NULL, NULL, 0, NULL, NULL, 0, NULL, NULL, 0),
(3, 3, 2, 2, 0, NULL, NULL, 0, NULL, NULL, 0, NULL, NULL, 0, NULL, NULL, 0, '12:05:00', '20:00:00', 1, NULL, NULL, 0, NULL, NULL, 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `limite_usuarios`
--

CREATE TABLE `limite_usuarios` (
  `id` int(11) NOT NULL,
  `administrativo` int(11) NOT NULL,
  `medico` int(11) NOT NULL,
  `asistente` int(11) NOT NULL,
  `paciente` int(11) NOT NULL,
  `status` int(11) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `limite_usuarios`
--

INSERT INTO `limite_usuarios` (`id`, `administrativo`, `medico`, `asistente`, `paciente`, `status`, `created_at`, `updated_at`) VALUES
(1, 70, 2, 5, 100, 2, '2022-05-17 17:14:00', '2022-05-17 18:03:33'),
(2, 20, 4, 1, 100, 1, '2022-05-17 17:15:59', '2022-05-17 18:03:33'),
(3, 50, 2, 5, 100, 2, '2022-05-17 17:17:18', '2022-05-17 18:03:33'),
(4, 50, 3, 50, 150, 2, '2022-05-17 17:47:13', '2022-05-17 18:03:33');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `login_pacientes`
--

CREATE TABLE `login_pacientes` (
  `id_login_Pacientes` int(11) NOT NULL,
  `Paciente_id` int(11) DEFAULT NULL,
  `Usuario` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Correo` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Status_id` int(11) DEFAULT NULL,
  `Contrasena` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `login_pacientes`
--

INSERT INTO `login_pacientes` (`id_login_Pacientes`, `Paciente_id`, `Usuario`, `Correo`, `Status_id`, `Contrasena`) VALUES
(1, 1, 'Usuario test Paciente', 'usuariop@test.com', 1, '$2y$10$30u.g2qLEvwj4HVgC3Ndxux8Ybke3lp/qn2tSgDwkaXhrkprUAjpi');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `login_trabajadores`
--

CREATE TABLE `login_trabajadores` (
  `id_Login_Trabajador` int(11) NOT NULL,
  `Usuario` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Correo` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Status_Medico_id` int(11) DEFAULT NULL,
  `Contrasena` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `Medico_id` int(11) DEFAULT NULL,
  `Asistente_id` int(11) DEFAULT NULL,
  `general_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `login_trabajadores`
--

INSERT INTO `login_trabajadores` (`id_Login_Trabajador`, `Usuario`, `Correo`, `Status_Medico_id`, `Contrasena`, `Medico_id`, `Asistente_id`, `general_id`) VALUES
(1, 'John Doe', 'johndoe@test.com', 1, '$2y$10$3uRb7zlfRwtJFdSy/vZ/5.D3O36.BudZbgxVLF2e4N3v/vVFkl9kG', NULL, NULL, 1),
(2, 'Usuario Medico', 'usuariom@test.com', 1, '$2y$10$rojj7L0mXw6zo23e82BLwOwFwGkfFlmEhPQWqHNtVcnnhx5mfkXDK', 1, NULL, NULL),
(5, 'Elvira Terán', 'elvirateran58@gmail.com', 1, '$2y$10$HLJoo.d3Klq.08tyK/kq/.PyFBdNBi.gGts6pN00cRUhttq7GWXUu', 2, NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `medicoxasistente`
--

CREATE TABLE `medicoxasistente` (
  `id` int(11) NOT NULL,
  `id_Medico` int(11) NOT NULL,
  `id_Asistente` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `medicoxasistente`
--

INSERT INTO `medicoxasistente` (`id`, `id_Medico`, `id_Asistente`) VALUES
(2, 1, 4);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `meetings`
--

CREATE TABLE `meetings` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `uuid` char(36) COLLATE utf8_unicode_ci NOT NULL,
  `topic` varchar(125) COLLATE utf8_unicode_ci NOT NULL,
  `start_time` datetime NOT NULL,
  `duration` int(11) NOT NULL,
  `started_at` datetime DEFAULT NULL,
  `ended_at` datetime DEFAULT NULL,
  `provider` varchar(125) COLLATE utf8_unicode_ci NOT NULL,
  `scheduler_type` varchar(125) COLLATE utf8_unicode_ci NOT NULL,
  `scheduler_id` bigint(20) UNSIGNED NOT NULL,
  `presenter_type` varchar(125) COLLATE utf8_unicode_ci NOT NULL,
  `presenter_id` bigint(20) UNSIGNED NOT NULL,
  `host_type` varchar(125) COLLATE utf8_unicode_ci NOT NULL,
  `host_id` bigint(20) UNSIGNED NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `deleted_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `meeting_participants`
--

CREATE TABLE `meeting_participants` (
  `uuid` char(36) COLLATE utf8_unicode_ci NOT NULL,
  `started_at` datetime DEFAULT NULL,
  `ended_at` datetime DEFAULT NULL,
  `participant_type` varchar(125) COLLATE utf8_unicode_ci NOT NULL,
  `participant_id` bigint(20) UNSIGNED NOT NULL,
  `meeting_id` bigint(20) UNSIGNED NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `deleted_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `meeting_rooms`
--

CREATE TABLE `meeting_rooms` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `uuid` char(36) COLLATE utf8_unicode_ci NOT NULL,
  `name` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `email` varchar(125) COLLATE utf8_unicode_ci NOT NULL,
  `type` tinyint(4) NOT NULL,
  `group` varchar(125) COLLATE utf8_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `deleted_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `meta_attributes`
--

CREATE TABLE `meta_attributes` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `key` varchar(125) COLLATE utf8_unicode_ci NOT NULL,
  `value` text COLLATE utf8_unicode_ci NOT NULL,
  `type` varchar(125) COLLATE utf8_unicode_ci NOT NULL,
  `model_type` varchar(125) COLLATE utf8_unicode_ci NOT NULL,
  `model_id` char(36) COLLATE utf8_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `migrations`
--

CREATE TABLE `migrations` (
  `id` int(10) UNSIGNED NOT NULL,
  `migration` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `batch` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `migrations`
--

INSERT INTO `migrations` (`id`, `migration`, `batch`) VALUES
(3, '2022_04_02_155432_create_meetings_table', 1),
(4, '2022_04_02_155432_create_meta_attributes_table', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `model_has_permissions`
--

CREATE TABLE `model_has_permissions` (
  `permission_id` bigint(20) UNSIGNED NOT NULL,
  `model_type` varchar(125) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model_id` bigint(20) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `model_has_roles`
--

CREATE TABLE `model_has_roles` (
  `role_id` bigint(20) UNSIGNED NOT NULL,
  `model_type` varchar(125) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model_id` bigint(20) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `model_has_roles`
--

INSERT INTO `model_has_roles` (`role_id`, `model_type`, `model_id`) VALUES
(1, 'App\\User', 1),
(1, 'App\\User', 25),
(2, 'App\\User', 2),
(2, 'App\\User', 4),
(2, 'App\\User', 5),
(3, 'App\\User', 3),
(3, 'App\\User', 7),
(4, 'App\\User', 6);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `municipios`
--

CREATE TABLE `municipios` (
  `id_Municipio` int(11) NOT NULL,
  `Estado_id` int(11) DEFAULT NULL,
  `Municipio` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `municipios`
--

INSERT INTO `municipios` (`id_Municipio`, `Estado_id`, `Municipio`) VALUES
(1, 1, 'Alto Orinoco'),
(2, 1, 'Atabapo'),
(3, 1, 'Atures'),
(4, 1, 'Autana'),
(5, 1, 'Manapiare'),
(6, 1, 'Maroa'),
(7, 1, 'Río Negro'),
(8, 2, 'Anaco'),
(9, 2, 'Aragua'),
(10, 2, 'Manuel Ezequiel Bruzual'),
(11, 2, 'Diego Bautista Urbaneja'),
(12, 2, 'Fernando Peñalver'),
(13, 2, 'Francisco Del Carmen Carvajal'),
(14, 2, 'General Sir Arthur McGregor'),
(15, 2, 'Guanta'),
(16, 2, 'Independencia'),
(17, 2, 'José Gregorio Monagas'),
(18, 2, 'Juan Antonio Sotillo'),
(19, 2, 'Juan Manuel Cajigal'),
(20, 2, 'Libertad'),
(21, 2, 'Francisco de Miranda'),
(22, 2, 'Pedro María Freites'),
(23, 2, 'Píritu'),
(24, 2, 'San José de Guanipa'),
(25, 2, 'San Juan de Capistrano'),
(26, 2, 'Santa Ana'),
(27, 2, 'Simón Bolívar'),
(28, 2, 'Simón Rodríguez'),
(29, 3, 'Achaguas'),
(30, 3, 'Biruaca'),
(31, 3, 'Muñóz'),
(32, 3, 'Páez'),
(33, 3, 'Pedro Camejo'),
(34, 3, 'Rómulo Gallegos'),
(35, 3, 'San Fernando'),
(36, 4, 'Atanasio Girardot'),
(37, 4, 'Bolívar'),
(38, 4, 'Camatagua'),
(39, 4, 'Francisco Linares Alcántara'),
(40, 4, 'José Ángel Lamas'),
(41, 4, 'José Félix Ribas'),
(42, 4, 'José Rafael Revenga'),
(43, 4, 'Libertador'),
(44, 4, 'Mario Briceño Iragorry'),
(45, 4, 'Ocumare de la Costa de Oro'),
(46, 4, 'San Casimiro'),
(47, 4, 'San Sebastián'),
(48, 4, 'Santiago Mariño'),
(49, 4, 'Santos Michelena'),
(50, 4, 'Sucre'),
(51, 4, 'Tovar'),
(52, 4, 'Urdaneta'),
(53, 4, 'Zamora'),
(54, 5, 'Alberto Arvelo Torrealba'),
(55, 5, 'Andrés Eloy Blanco'),
(56, 5, 'Antonio José de Sucre'),
(57, 5, 'Arismendi'),
(58, 5, 'Barinas'),
(59, 5, 'Bolívar'),
(60, 5, 'Cruz Paredes'),
(61, 5, 'Ezequiel Zamora'),
(62, 5, 'Obispos'),
(63, 5, 'Pedraza'),
(64, 5, 'Rojas'),
(65, 5, 'Sosa'),
(66, 6, 'Caroní'),
(67, 6, 'Cedeño'),
(68, 6, 'El Callao'),
(69, 6, 'Gran Sabana'),
(70, 6, 'Heres'),
(71, 6, 'Piar'),
(72, 6, 'Angostura (Raúl Leoni)'),
(73, 6, 'Roscio'),
(74, 6, 'Sifontes'),
(75, 6, 'Sucre'),
(76, 6, 'Padre Pedro Chien'),
(77, 7, 'Bejuma'),
(78, 7, 'Carlos Arvelo'),
(79, 7, 'Diego Ibarra'),
(80, 7, 'Guacara'),
(81, 7, 'Juan José Mora'),
(82, 7, 'Libertador'),
(83, 7, 'Los Guayos'),
(84, 7, 'Miranda'),
(85, 7, 'Montalbán'),
(86, 7, 'Naguanagua'),
(87, 7, 'Puerto Cabello'),
(88, 7, 'San Diego'),
(89, 7, 'San Joaquín'),
(90, 7, 'Valencia'),
(91, 8, 'Anzoátegui'),
(92, 8, 'Tinaquillo'),
(93, 8, 'Girardot'),
(94, 8, 'Lima Blanco'),
(95, 8, 'Pao de San Juan Bautista'),
(96, 8, 'Ricaurte'),
(97, 8, 'Rómulo Gallegos'),
(98, 8, 'San Carlos'),
(99, 8, 'Tinaco'),
(100, 9, 'Antonio Díaz'),
(101, 9, 'Casacoima'),
(102, 9, 'Pedernales'),
(103, 9, 'Tucupita'),
(104, 10, 'Acosta'),
(105, 10, 'Bolívar'),
(106, 10, 'Buchivacoa'),
(107, 10, 'Cacique Manaure'),
(108, 10, 'Carirubana'),
(109, 10, 'Colina'),
(110, 10, 'Dabajuro'),
(111, 10, 'Democracia'),
(112, 10, 'Falcón'),
(113, 10, 'Federación'),
(114, 10, 'Jacura'),
(115, 10, 'José Laurencio Silva'),
(116, 10, 'Los Taques'),
(117, 10, 'Mauroa'),
(118, 10, 'Miranda'),
(119, 10, 'Monseñor Iturriza'),
(120, 10, 'Palmasola'),
(121, 10, 'Petit'),
(122, 10, 'Píritu'),
(123, 10, 'San Francisco'),
(124, 10, 'Sucre'),
(125, 10, 'Tocópero'),
(126, 10, 'Unión'),
(127, 10, 'Urumaco'),
(128, 10, 'Zamora'),
(129, 11, 'Camaguán'),
(130, 11, 'Chaguaramas'),
(131, 11, 'El Socorro'),
(132, 11, 'José Félix Ribas'),
(133, 11, 'José Tadeo Monagas'),
(134, 11, 'Juan Germán Roscio'),
(135, 11, 'Julián Mellado'),
(136, 11, 'Las Mercedes'),
(137, 11, 'Leonardo Infante'),
(138, 11, 'Pedro Zaraza'),
(139, 11, 'Ortíz'),
(140, 11, 'San Gerónimo de Guayabal'),
(141, 11, 'San José de Guaribe'),
(142, 11, 'Santa María de Ipire'),
(143, 11, 'Sebastián Francisco de Miranda'),
(144, 12, 'Andrés Eloy Blanco'),
(145, 12, 'Crespo'),
(146, 12, 'Iribarren'),
(147, 12, 'Jiménez'),
(148, 12, 'Morán'),
(149, 12, 'Palavecino'),
(150, 12, 'Simón Planas'),
(151, 12, 'Torres'),
(152, 12, 'Urdaneta'),
(179, 13, 'Alberto Adriani'),
(180, 13, 'Andrés Bello'),
(181, 13, 'Antonio Pinto Salinas'),
(182, 13, 'Aricagua'),
(183, 13, 'Arzobispo Chacón'),
(184, 13, 'Campo Elías'),
(185, 13, 'Caracciolo Parra Olmedo'),
(186, 13, 'Cardenal Quintero'),
(187, 13, 'Guaraque'),
(188, 13, 'Julio César Salas'),
(189, 13, 'Justo Briceño'),
(190, 13, 'Libertador'),
(191, 13, 'Miranda'),
(192, 13, 'Obispo Ramos de Lora'),
(193, 13, 'Padre Noguera'),
(194, 13, 'Pueblo Llano'),
(195, 13, 'Rangel'),
(196, 13, 'Rivas Dávila'),
(197, 13, 'Santos Marquina'),
(198, 13, 'Sucre'),
(199, 13, 'Tovar'),
(200, 13, 'Tulio Febres Cordero'),
(201, 13, 'Zea'),
(223, 14, 'Acevedo'),
(224, 14, 'Andrés Bello'),
(225, 14, 'Baruta'),
(226, 14, 'Brión'),
(227, 14, 'Buroz'),
(228, 14, 'Carrizal'),
(229, 14, 'Chacao'),
(230, 14, 'Cristóbal Rojas'),
(231, 14, 'El Hatillo'),
(232, 14, 'Guaicaipuro'),
(233, 14, 'Independencia'),
(234, 14, 'Lander'),
(235, 14, 'Los Salias'),
(236, 14, 'Páez'),
(237, 14, 'Paz Castillo'),
(238, 14, 'Pedro Gual'),
(239, 14, 'Plaza'),
(240, 14, 'Simón Bolívar'),
(241, 14, 'Sucre'),
(242, 14, 'Urdaneta'),
(243, 14, 'Zamora'),
(258, 15, 'Acosta'),
(259, 15, 'Aguasay'),
(260, 15, 'Bolívar'),
(261, 15, 'Caripe'),
(262, 15, 'Cedeño'),
(263, 15, 'Ezequiel Zamora'),
(264, 15, 'Libertador'),
(265, 15, 'Maturín'),
(266, 15, 'Piar'),
(267, 15, 'Punceres'),
(268, 15, 'Santa Bárbara'),
(269, 15, 'Sotillo'),
(270, 15, 'Uracoa'),
(271, 16, 'Antolín del Campo'),
(272, 16, 'Arismendi'),
(273, 16, 'García'),
(274, 16, 'Gómez'),
(275, 16, 'Maneiro'),
(276, 16, 'Marcano'),
(277, 16, 'Mariño'),
(278, 16, 'Península de Macanao'),
(279, 16, 'Tubores'),
(280, 16, 'Villalba'),
(281, 16, 'Díaz'),
(282, 17, 'Agua Blanca'),
(283, 17, 'Araure'),
(284, 17, 'Esteller'),
(285, 17, 'Guanare'),
(286, 17, 'Guanarito'),
(287, 17, 'Monseñor José Vicente de Unda'),
(288, 17, 'Ospino'),
(289, 17, 'Páez'),
(290, 17, 'Papelón'),
(291, 17, 'San Genaro de Boconoíto'),
(292, 17, 'San Rafael de Onoto'),
(293, 17, 'Santa Rosalía'),
(294, 17, 'Sucre'),
(295, 17, 'Turén'),
(296, 18, 'Andrés Eloy Blanco'),
(297, 18, 'Andrés Mata'),
(298, 18, 'Arismendi'),
(299, 18, 'Benítez'),
(300, 18, 'Bermúdez'),
(301, 18, 'Bolívar'),
(302, 18, 'Cajigal'),
(303, 18, 'Cruz Salmerón Acosta'),
(304, 18, 'Libertador'),
(305, 18, 'Mariño'),
(306, 18, 'Mejía'),
(307, 18, 'Montes'),
(308, 18, 'Ribero'),
(309, 18, 'Sucre'),
(310, 18, 'Valdéz'),
(341, 19, 'Andrés Bello'),
(342, 19, 'Antonio Rómulo Costa'),
(343, 19, 'Ayacucho'),
(344, 19, 'Bolívar'),
(345, 19, 'Cárdenas'),
(346, 19, 'Córdoba'),
(347, 19, 'Fernández Feo'),
(348, 19, 'Francisco de Miranda'),
(349, 19, 'García de Hevia'),
(350, 19, 'Guásimos'),
(351, 19, 'Independencia'),
(352, 19, 'Jáuregui'),
(353, 19, 'José María Vargas'),
(354, 19, 'Junín'),
(355, 19, 'Libertad'),
(356, 19, 'Libertador'),
(357, 19, 'Lobatera'),
(358, 19, 'Michelena'),
(359, 19, 'Panamericano'),
(360, 19, 'Pedro María Ureña'),
(361, 19, 'Rafael Urdaneta'),
(362, 19, 'Samuel Darío Maldonado'),
(363, 19, 'San Cristóbal'),
(364, 19, 'Seboruco'),
(365, 19, 'Simón Rodríguez'),
(366, 19, 'Sucre'),
(367, 19, 'Torbes'),
(368, 19, 'Uribante'),
(369, 19, 'San Judas Tadeo'),
(370, 20, 'Andrés Bello'),
(371, 20, 'Boconó'),
(372, 20, 'Bolívar'),
(373, 20, 'Candelaria'),
(374, 20, 'Carache'),
(375, 20, 'Escuque'),
(376, 20, 'José Felipe Márquez Cañizalez'),
(377, 20, 'Juan Vicente Campos Elías'),
(378, 20, 'La Ceiba'),
(379, 20, 'Miranda'),
(380, 20, 'Monte Carmelo'),
(381, 20, 'Motatán'),
(382, 20, 'Pampán'),
(383, 20, 'Pampanito'),
(384, 20, 'Rafael Rangel'),
(385, 20, 'San Rafael de Carvajal'),
(386, 20, 'Sucre'),
(387, 20, 'Trujillo'),
(388, 20, 'Urdaneta'),
(389, 20, 'Valera'),
(390, 21, 'Vargas'),
(391, 22, 'Arístides Bastidas'),
(392, 22, 'Bolívar'),
(407, 22, 'Bruzual'),
(408, 22, 'Cocorote'),
(409, 22, 'Independencia'),
(410, 22, 'José Antonio Páez'),
(411, 22, 'La Trinidad'),
(412, 22, 'Manuel Monge'),
(413, 22, 'Nirgua'),
(414, 22, 'Peña'),
(415, 22, 'San Felipe'),
(416, 22, 'Sucre'),
(417, 22, 'Urachiche'),
(418, 22, 'José Joaquín Veroes'),
(441, 23, 'Almirante Padilla'),
(442, 23, 'Baralt'),
(443, 23, 'Cabimas'),
(444, 23, 'Catatumbo'),
(445, 23, 'Colón'),
(446, 23, 'Francisco Javier Pulgar'),
(447, 23, 'Páez'),
(448, 23, 'Jesús Enrique Losada'),
(449, 23, 'Jesús María Semprún'),
(450, 23, 'La Cañada de Urdaneta'),
(451, 23, 'Lagunillas'),
(452, 23, 'Machiques de Perijá'),
(453, 23, 'Mara'),
(454, 23, 'Maracaibo'),
(455, 23, 'Miranda'),
(456, 23, 'Rosario de Perijá'),
(457, 23, 'San Francisco'),
(458, 23, 'Santa Rita'),
(459, 23, 'Simón Bolívar'),
(460, 23, 'Sucre'),
(461, 23, 'Valmore Rodríguez'),
(462, 24, 'Libertador');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pacientes_especiales`
--

CREATE TABLE `pacientes_especiales` (
  `id_Pacientes_Especiales` int(11) NOT NULL,
  `Paciente_id` int(11) DEFAULT NULL,
  `Nombre_Paciente_Especial` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Apellido_Paciente_Especial` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Fecha_Nacimiento_Paciente_Especial` date DEFAULT NULL,
  `Sexo_id` int(11) DEFAULT NULL,
  `Parentesco_Familiar` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Prefijo_CIDNI_id` int(11) DEFAULT NULL,
  `CIDNI` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Status_id` int(11) DEFAULT NULL,
  `Paciente_Infantil` char(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Paciente_Mayor` char(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Paciente_Discapacidad` char(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Nota` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Civil_id` int(11) DEFAULT NULL,
  `Pais_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pagos_confirmar`
--

CREATE TABLE `pagos_confirmar` (
  `id_pago` int(11) NOT NULL,
  `Paciente_id` int(11) NOT NULL,
  `moneda_id` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  `monto` decimal(10,2) NOT NULL,
  `referencia` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `fecha_pago` date NOT NULL,
  `tipo_pago` int(11) NOT NULL,
  `cuenta_bs` int(11) DEFAULT NULL,
  `cuenta_usd` int(11) DEFAULT NULL,
  `banco_emisor` int(11) DEFAULT NULL,
  `entidad_emisora` int(11) DEFAULT NULL,
  `billetera_emisora` int(11) DEFAULT NULL,
  `comprobante` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `impuesto_dolar` double(10,2) DEFAULT NULL,
  `confirmado` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `pagos_confirmar`
--

INSERT INTO `pagos_confirmar` (`id_pago`, `Paciente_id`, `moneda_id`, `monto`, `referencia`, `fecha_pago`, `tipo_pago`, `cuenta_bs`, `cuenta_usd`, `banco_emisor`, `entidad_emisora`, `billetera_emisora`, `comprobante`, `impuesto_dolar`, `confirmado`) VALUES
(3, 1, 'Bs', '24.60', '5412369874125', '2022-05-20', 1, 1, NULL, 21, NULL, NULL, 'comprobante\\comprobante_1_2022-05-20.png', NULL, 1),
(4, 1, 'Bs', '142.23', '521478963', '2022-05-28', 1, 1, NULL, 4, NULL, NULL, 'comprobante\\comprobante_1_2022-05-28.png', 0.00, 0),
(5, 1, 'Bs', '142.23', '521478963', '2022-05-28', 1, 1, NULL, 4, NULL, NULL, 'comprobante\\comprobante_1_2022-05-28.png', 0.00, 0),
(6, 1, 'Bs', '142.23', '521478963', '2022-05-28', 1, 1, NULL, 4, NULL, NULL, 'comprobante\\comprobante_1_2022-05-28.png', 0.00, 0),
(7, 1, 'Bs', '142.23', '521478963', '2022-05-28', 1, 1, NULL, 4, NULL, NULL, 'comprobante\\comprobante_1_2022-05-28.png', 0.00, 0),
(8, 1, 'Bs', '142.23', '521478963', '2022-05-28', 1, 1, NULL, 4, NULL, NULL, 'comprobante\\comprobante_1_2022-05-28.png', 0.00, 0),
(9, 1, 'Bs', '142.23', '521478963', '2022-05-28', 1, 1, NULL, 4, NULL, NULL, 'comprobante\\comprobante_1_2022-05-28.png', 0.00, 0),
(10, 1, 'Bs', '126.36', '789632145', '2022-05-27', 1, 1, NULL, 3, NULL, NULL, 'comprobante\\comprobante_1_2022-05-27.png', 0.00, 0),
(11, 1, 'Bs', '200.32', '521478963', '2022-05-19', 1, 1, NULL, 3, NULL, NULL, 'comprobante\\comprobante_1_2022-05-19.png', 0.00, 0),
(12, 1, 'Bs', '129.36', '12365478996', '2022-05-17', 1, 1, NULL, 3, NULL, NULL, 'comprobante\\comprobante_1_2022-05-17.png', 0.00, 0),
(13, 1, 'Bs', '120.36', '52145630789', '2022-05-27', 1, 1, NULL, 4, NULL, NULL, 'comprobante\\comprobante_1_2022-05-27.png', 0.00, 0),
(14, 1, 'Bs', '136.25', '521478963201254', '2022-05-20', 1, 1, NULL, 3, NULL, NULL, 'comprobante\\comprobante_1_2022-05-20.png', 0.00, 0),
(15, 1, 'Bs', '126.32', '32145698745632100', '2022-05-27', 1, 1, NULL, 3, NULL, NULL, 'comprobante\\comprobante_1_2022-05-27.png', 0.00, 0),
(16, 1, 'Bs', '126.32', '32145698745632100', '2022-05-27', 1, 1, NULL, 3, NULL, NULL, 'comprobante\\comprobante_1_2022-05-27.png', 0.00, 0),
(17, 1, 'Bs', '100.23', '12300', '2022-05-26', 1, 1, NULL, 4, NULL, NULL, 'comprobante\\comprobante_1_2022-05-26.png', 0.00, 0),
(18, 1, 'Bs', '100.25', '1000', '2022-05-28', 1, 1, NULL, 4, NULL, NULL, 'comprobante\\comprobante_1_2022-05-28.png', 0.00, 0),
(19, 1, 'Bs', '100.25', '1000', '2022-05-28', 1, 1, NULL, 4, NULL, NULL, 'comprobante\\comprobante_1_2022-05-28.png', 0.00, 0),
(20, 1, 'Bs', '200.12', '21365478', '2022-05-28', 1, 1, NULL, 3, NULL, NULL, 'comprobante\\comprobante_1_2022-05-28.png', 0.00, 0),
(21, 1, 'Bs', '200.05', '563214789', '2022-05-27', 1, 1, NULL, 4, NULL, NULL, 'comprobante\\comprobante_1_2022-05-27.png', 0.00, 0),
(22, 1, 'Bs', '250.23', '521478963', '2022-05-20', 1, 1, NULL, 3, NULL, NULL, 'comprobante\\comprobante_1_2022-05-20.png', 0.00, 0),
(23, 1, 'Bs', '300.50', '52147896523', '2022-05-26', 1, 1, NULL, 3, NULL, NULL, 'comprobante\\comprobante_1_2022-05-26.png', 0.00, 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `paises`
--

CREATE TABLE `paises` (
  `id_Pais` int(11) NOT NULL,
  `Codigo` int(11) DEFAULT NULL,
  `iso3166a1` char(2) COLLATE utf8_unicode_ci DEFAULT NULL,
  `iso3166a2` char(5) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Pais` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `paises`
--

INSERT INTO `paises` (`id_Pais`, `Codigo`, `iso3166a1`, `iso3166a2`, `Pais`) VALUES
(1, 58, 'VE', 'Vzla', 'Venezuela'),
(2, 57, 'CO', 'COL', 'Colombia'),
(3, 56, 'PE', 'Per', 'Perú');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `parroquias`
--

CREATE TABLE `parroquias` (
  `id_Parroquia` int(11) NOT NULL,
  `Municipio_id` int(11) DEFAULT NULL,
  `Parroquia` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `parroquias`
--

INSERT INTO `parroquias` (`id_Parroquia`, `Municipio_id`, `Parroquia`) VALUES
(1, 1, 'Alto Orinoco'),
(2, 1, 'Huachamacare Acanaña'),
(3, 1, 'Marawaka Toky Shamanaña'),
(4, 1, 'Mavaka Mavaka'),
(5, 1, 'Sierra Parima Parimabé'),
(6, 2, 'Ucata Laja Lisa'),
(7, 2, 'Yapacana Macuruco'),
(8, 2, 'Caname Guarinuma'),
(9, 3, 'Fernando Girón Tovar'),
(10, 3, 'Luis Alberto Gómez'),
(11, 3, 'Pahueña Limón de Parhueña'),
(12, 3, 'Platanillal Platanillal'),
(13, 4, 'Samariapo'),
(14, 4, 'Sipapo'),
(15, 4, 'Munduapo'),
(16, 4, 'Guayapo'),
(17, 5, 'Alto Ventuari'),
(18, 5, 'Medio Ventuari'),
(19, 5, 'Bajo Ventuari'),
(20, 6, 'Victorino'),
(21, 6, 'Comunidad'),
(22, 7, 'Casiquiare'),
(23, 7, 'Cocuy'),
(24, 7, 'San Carlos de Río Negro'),
(25, 7, 'Solano'),
(26, 8, 'Anaco'),
(27, 8, 'San Joaquín'),
(28, 9, 'Cachipo'),
(29, 9, 'Aragua de Barcelona'),
(30, 11, 'Lechería'),
(31, 11, 'El Morro'),
(32, 12, 'Puerto Píritu'),
(33, 12, 'San Miguel'),
(34, 12, 'Sucre'),
(35, 13, 'Valle de Guanape'),
(36, 13, 'Santa Bárbara'),
(37, 14, 'El Chaparro'),
(38, 14, 'Tomás Alfaro'),
(39, 14, 'Calatrava'),
(40, 15, 'Guanta'),
(41, 15, 'Chorrerón'),
(42, 16, 'Mamo'),
(43, 16, 'Soledad'),
(44, 17, 'Mapire'),
(45, 17, 'Piar'),
(46, 17, 'Santa Clara'),
(47, 17, 'San Diego de Cabrutica'),
(48, 17, 'Uverito'),
(49, 17, 'Zuata'),
(50, 18, 'Puerto La Cruz'),
(51, 18, 'Pozuelos'),
(52, 19, 'Onoto'),
(53, 19, 'San Pablo'),
(54, 20, 'San Mateo'),
(55, 20, 'El Carito'),
(56, 20, 'Santa Inés'),
(57, 20, 'La Romereña'),
(58, 21, 'Atapirire'),
(59, 21, 'Boca del Pao'),
(60, 21, 'El Pao'),
(61, 21, 'Pariaguán'),
(62, 22, 'Cantaura'),
(63, 22, 'Libertador'),
(64, 22, 'Santa Rosa'),
(65, 22, 'Urica'),
(66, 23, 'Píritu'),
(67, 23, 'San Francisco'),
(68, 24, 'San José de Guanipa'),
(69, 25, 'Boca de Uchire'),
(70, 25, 'Boca de Chávez'),
(71, 26, 'Pueblo Nuevo'),
(72, 26, 'Santa Ana'),
(73, 27, 'Bergatín'),
(74, 27, 'Caigua'),
(75, 27, 'El Carmen'),
(76, 27, 'El Pilar'),
(77, 27, 'Naricual'),
(78, 27, 'San Crsitóbal'),
(79, 28, 'Edmundo Barrios'),
(80, 28, 'Miguel Otero Silva'),
(81, 29, 'Achaguas'),
(82, 29, 'Apurito'),
(83, 29, 'El Yagual'),
(84, 29, 'Guachara'),
(85, 29, 'Mucuritas'),
(86, 29, 'Queseras del medio'),
(87, 30, 'Biruaca'),
(88, 31, 'Bruzual'),
(89, 31, 'Mantecal'),
(90, 31, 'Quintero'),
(91, 31, 'Rincón Hondo'),
(92, 31, 'San Vicente'),
(93, 32, 'Guasdualito'),
(94, 32, 'Aramendi'),
(95, 32, 'El Amparo'),
(96, 32, 'San Camilo'),
(97, 32, 'Urdaneta'),
(98, 33, 'San Juan de Payara'),
(99, 33, 'Codazzi'),
(100, 33, 'Cunaviche'),
(101, 34, 'Elorza'),
(102, 34, 'La Trinidad'),
(103, 35, 'San Fernando'),
(104, 35, 'El Recreo'),
(105, 35, 'Peñalver'),
(106, 35, 'San Rafael de Atamaica'),
(107, 36, 'Pedro José Ovalles'),
(108, 36, 'Joaquín Crespo'),
(109, 36, 'José Casanova Godoy'),
(110, 36, 'Madre María de San José'),
(111, 36, 'Andrés Eloy Blanco'),
(112, 36, 'Los Tacarigua'),
(113, 36, 'Las Delicias'),
(114, 36, 'Choroní'),
(115, 37, 'Bolívar'),
(116, 38, 'Camatagua'),
(117, 38, 'Carmen de Cura'),
(118, 39, 'Santa Rita'),
(119, 39, 'Francisco de Miranda'),
(120, 39, 'Moseñor Feliciano González'),
(121, 40, 'Santa Cruz'),
(122, 41, 'José Félix Ribas'),
(123, 41, 'Castor Nieves Ríos'),
(124, 41, 'Las Guacamayas'),
(125, 41, 'Pao de Zárate'),
(126, 41, 'Zuata'),
(127, 42, 'José Rafael Revenga'),
(128, 43, 'Palo Negro'),
(129, 43, 'San Martín de Porres'),
(130, 44, 'El Limón'),
(131, 44, 'Caña de Azúcar'),
(132, 45, 'Ocumare de la Costa'),
(133, 46, 'San Casimiro'),
(134, 46, 'Güiripa'),
(135, 46, 'Ollas de Caramacate'),
(136, 46, 'Valle Morín'),
(137, 47, 'San Sebastían'),
(138, 48, 'Turmero'),
(139, 48, 'Arevalo Aponte'),
(140, 48, 'Chuao'),
(141, 48, 'Samán de Güere'),
(142, 48, 'Alfredo Pacheco Miranda'),
(143, 49, 'Santos Michelena'),
(144, 49, 'Tiara'),
(145, 50, 'Cagua'),
(146, 50, 'Bella Vista'),
(147, 51, 'Tovar'),
(148, 52, 'Urdaneta'),
(149, 52, 'Las Peñitas'),
(150, 52, 'San Francisco de Cara'),
(151, 52, 'Taguay'),
(152, 53, 'Zamora'),
(153, 53, 'Magdaleno'),
(154, 53, 'San Francisco de Asís'),
(155, 53, 'Valles de Tucutunemo'),
(156, 53, 'Augusto Mijares'),
(157, 54, 'Sabaneta'),
(158, 54, 'Juan Antonio Rodríguez Domínguez'),
(159, 55, 'El Cantón'),
(160, 55, 'Santa Cruz de Guacas'),
(161, 55, 'Puerto Vivas'),
(162, 56, 'Ticoporo'),
(163, 56, 'Nicolás Pulido'),
(164, 56, 'Andrés Bello'),
(165, 57, 'Arismendi'),
(166, 57, 'Guadarrama'),
(167, 57, 'La Unión'),
(168, 57, 'San Antonio'),
(169, 58, 'Barinas'),
(170, 58, 'Alberto Arvelo Larriva'),
(171, 58, 'San Silvestre'),
(172, 58, 'Santa Inés'),
(173, 58, 'Santa Lucía'),
(174, 58, 'Torumos'),
(175, 58, 'El Carmen'),
(176, 58, 'Rómulo Betancourt'),
(177, 58, 'Corazón de Jesús'),
(178, 58, 'Ramón Ignacio Méndez'),
(179, 58, 'Alto Barinas'),
(180, 58, 'Manuel Palacio Fajardo'),
(181, 58, 'Juan Antonio Rodríguez Domínguez'),
(182, 58, 'Dominga Ortiz de Páez'),
(183, 59, 'Barinitas'),
(184, 59, 'Altamira de Cáceres'),
(185, 59, 'Calderas'),
(186, 60, 'Barrancas'),
(187, 60, 'El Socorro'),
(188, 60, 'Mazparrito'),
(189, 61, 'Santa Bárbara'),
(190, 61, 'Pedro Briceño Méndez'),
(191, 61, 'Ramón Ignacio Méndez'),
(192, 61, 'José Ignacio del Pumar'),
(193, 62, 'Obispos'),
(194, 62, 'Guasimitos'),
(195, 62, 'El Real'),
(196, 62, 'La Luz'),
(197, 63, 'Ciudad Bolívia'),
(198, 63, 'José Ignacio Briceño'),
(199, 63, 'José Félix Ribas'),
(200, 63, 'Páez'),
(201, 64, 'Libertad'),
(202, 64, 'Dolores'),
(203, 64, 'Santa Rosa'),
(204, 64, 'Palacio Fajardo'),
(205, 65, 'Ciudad de Nutrias'),
(206, 65, 'El Regalo'),
(207, 65, 'Puerto Nutrias'),
(208, 65, 'Santa Catalina'),
(209, 66, 'Cachamay'),
(210, 66, 'Chirica'),
(211, 66, 'Dalla Costa'),
(212, 66, 'Once de Abril'),
(213, 66, 'Simón Bolívar'),
(214, 66, 'Unare'),
(215, 66, 'Universidad'),
(216, 66, 'Vista al Sol'),
(217, 66, 'Pozo Verde'),
(218, 66, 'Yocoima'),
(219, 66, '5 de Julio'),
(220, 67, 'Cedeño'),
(221, 67, 'Altagracia'),
(222, 67, 'Ascensión Farreras'),
(223, 67, 'Guaniamo'),
(224, 67, 'La Urbana'),
(225, 67, 'Pijiguaos'),
(226, 68, 'El Callao'),
(227, 69, 'Gran Sabana'),
(228, 69, 'Ikabarú'),
(229, 70, 'Catedral'),
(230, 70, 'Zea'),
(231, 70, 'Orinoco'),
(232, 70, 'José Antonio Páez'),
(233, 70, 'Marhuanta'),
(234, 70, 'Agua Salada'),
(235, 70, 'Vista Hermosa'),
(236, 70, 'La Sabanita'),
(237, 70, 'Panapana'),
(238, 71, 'Andrés Eloy Blanco'),
(239, 71, 'Pedro Cova'),
(240, 72, 'Raúl Leoni'),
(241, 72, 'Barceloneta'),
(242, 72, 'Santa Bárbara'),
(243, 72, 'San Francisco'),
(244, 73, 'Roscio'),
(245, 73, 'Salóm'),
(246, 74, 'Sifontes'),
(247, 74, 'Dalla Costa'),
(248, 74, 'San Isidro'),
(249, 75, 'Sucre'),
(250, 75, 'Aripao'),
(251, 75, 'Guarataro'),
(252, 75, 'Las Majadas'),
(253, 75, 'Moitaco'),
(254, 76, 'Padre Pedro Chien'),
(255, 76, 'Río Grande'),
(256, 77, 'Bejuma'),
(257, 77, 'Canoabo'),
(258, 77, 'Simón Bolívar'),
(259, 78, 'Güigüe'),
(260, 78, 'Carabobo'),
(261, 78, 'Tacarigua'),
(262, 79, 'Mariara'),
(263, 79, 'Aguas Calientes'),
(264, 80, 'Ciudad Alianza'),
(265, 80, 'Guacara'),
(266, 80, 'Yagua'),
(267, 81, 'Morón'),
(268, 81, 'Yagua'),
(269, 82, 'Tocuyito'),
(270, 82, 'Independencia'),
(271, 83, 'Los Guayos'),
(272, 84, 'Miranda'),
(273, 85, 'Montalbán'),
(274, 86, 'Naguanagua'),
(275, 87, 'Bartolomé Salóm'),
(276, 87, 'Democracia'),
(277, 87, 'Fraternidad'),
(278, 87, 'Goaigoaza'),
(279, 87, 'Juan José Flores'),
(280, 87, 'Unión'),
(281, 87, 'Borburata'),
(282, 87, 'Patanemo'),
(283, 88, 'San Diego'),
(284, 89, 'San Joaquín'),
(285, 90, 'Candelaria'),
(286, 90, 'Catedral'),
(287, 90, 'El Socorro'),
(288, 90, 'Miguel Peña'),
(289, 90, 'Rafael Urdaneta'),
(290, 90, 'San Blas'),
(291, 90, 'San José'),
(292, 90, 'Santa Rosa'),
(293, 90, 'Negro Primero'),
(294, 91, 'Cojedes'),
(295, 91, 'Juan de Mata Suárez'),
(296, 92, 'Tinaquillo'),
(297, 93, 'El Baúl'),
(298, 93, 'Sucre'),
(299, 94, 'La Aguadita'),
(300, 94, 'Macapo'),
(301, 95, 'El Pao'),
(302, 96, 'El Amparo'),
(303, 96, 'Libertad de Cojedes'),
(304, 97, 'Rómulo Gallegos'),
(305, 98, 'San Carlos de Austria'),
(306, 98, 'Juan Ángel Bravo'),
(307, 98, 'Manuel Manrique'),
(308, 99, 'General en Jefe José Laurencio Silva'),
(309, 100, 'Curiapo'),
(310, 100, 'Almirante Luis Brión'),
(311, 100, 'Francisco Aniceto Lugo'),
(312, 100, 'Manuel Renaud'),
(313, 100, 'Padre Barral'),
(314, 100, 'Santos de Abelgas'),
(315, 101, 'Imataca'),
(316, 101, 'Cinco de Julio'),
(317, 101, 'Juan Bautista Arismendi'),
(318, 101, 'Manuel Piar'),
(319, 101, 'Rómulo Gallegos'),
(320, 102, 'Pedernales'),
(321, 102, 'Luis Beltrán Prieto Figueroa'),
(322, 103, 'San José (Delta Amacuro)'),
(323, 103, 'José Vidal Marcano'),
(324, 103, 'Juan Millán'),
(325, 103, 'Leonardo Ruíz Pineda'),
(326, 103, 'Mariscal Antonio José de Sucre'),
(327, 103, 'Monseñor Argimiro García'),
(328, 103, 'San Rafael (Delta Amacuro)'),
(329, 103, 'Virgen del Valle'),
(330, 10, 'Clarines'),
(331, 10, 'Guanape'),
(332, 10, 'Sabana de Uchire'),
(333, 104, 'Capadare'),
(334, 104, 'La Pastora'),
(335, 104, 'Libertador'),
(336, 104, 'San Juan de los Cayos'),
(337, 105, 'Aracua'),
(338, 105, 'La Peña'),
(339, 105, 'San Luis'),
(340, 106, 'Bariro'),
(341, 106, 'Borojó'),
(342, 106, 'Capatárida'),
(343, 106, 'Guajiro'),
(344, 106, 'Seque'),
(345, 106, 'Zazárida'),
(346, 106, 'Valle de Eroa'),
(347, 107, 'Cacique Manaure'),
(348, 108, 'Norte'),
(349, 108, 'Carirubana'),
(350, 108, 'Santa Ana'),
(351, 108, 'Urbana Punta Cardón'),
(352, 109, 'La Vela de Coro'),
(353, 109, 'Acurigua'),
(354, 109, 'Guaibacoa'),
(355, 109, 'Las Calderas'),
(356, 109, 'Macoruca'),
(357, 110, 'Dabajuro'),
(358, 111, 'Agua Clara'),
(359, 111, 'Avaria'),
(360, 111, 'Pedregal'),
(361, 111, 'Piedra Grande'),
(362, 111, 'Purureche'),
(363, 112, 'Adaure'),
(364, 112, 'Adícora'),
(365, 112, 'Baraived'),
(366, 112, 'Buena Vista'),
(367, 112, 'Jadacaquiva'),
(368, 112, 'El Vínculo'),
(369, 112, 'El Hato'),
(370, 112, 'Moruy'),
(371, 112, 'Pueblo Nuevo'),
(372, 113, 'Agua Larga'),
(373, 113, 'El Paují'),
(374, 113, 'Independencia'),
(375, 113, 'Mapararí'),
(376, 114, 'Agua Linda'),
(377, 114, 'Araurima'),
(378, 114, 'Jacura'),
(379, 115, 'Tucacas'),
(380, 115, 'Boca de Aroa'),
(381, 116, 'Los Taques'),
(382, 116, 'Judibana'),
(383, 117, 'Mene de Mauroa'),
(384, 117, 'San Félix'),
(385, 117, 'Casigua'),
(386, 118, 'Guzmán Guillermo'),
(387, 118, 'Mitare'),
(388, 118, 'Río Seco'),
(389, 118, 'Sabaneta'),
(390, 118, 'San Antonio'),
(391, 118, 'San Gabriel'),
(392, 118, 'Santa Ana'),
(393, 119, 'Boca del Tocuyo'),
(394, 119, 'Chichiriviche'),
(395, 119, 'Tocuyo de la Costa'),
(396, 120, 'Palmasola'),
(397, 121, 'Cabure'),
(398, 121, 'Colina'),
(399, 121, 'Curimagua'),
(400, 122, 'San José de la Costa'),
(401, 122, 'Píritu'),
(402, 123, 'San Francisco'),
(403, 124, 'Sucre'),
(404, 124, 'Pecaya'),
(405, 125, 'Tocópero'),
(406, 126, 'El Charal'),
(407, 126, 'Las Vegas del Tuy'),
(408, 126, 'Santa Cruz de Bucaral'),
(409, 127, 'Bruzual'),
(410, 127, 'Urumaco'),
(411, 128, 'Puerto Cumarebo'),
(412, 128, 'La Ciénaga'),
(413, 128, 'La Soledad'),
(414, 128, 'Pueblo Cumarebo'),
(415, 128, 'Zazárida'),
(416, 113, 'Churuguara'),
(417, 129, 'Camaguán'),
(418, 129, 'Puerto Miranda'),
(419, 129, 'Uverito'),
(420, 130, 'Chaguaramas'),
(421, 131, 'El Socorro'),
(422, 132, 'Tucupido'),
(423, 132, 'San Rafael de Laya'),
(424, 133, 'Altagracia de Orituco'),
(425, 133, 'San Rafael de Orituco'),
(426, 133, 'San Francisco Javier de Lezama'),
(427, 133, 'Paso Real de Macaira'),
(428, 133, 'Carlos Soublette'),
(429, 133, 'San Francisco de Macaira'),
(430, 133, 'Libertad de Orituco'),
(431, 134, 'Cantaclaro'),
(432, 134, 'San Juan de los Morros'),
(433, 134, 'Parapara'),
(434, 135, 'El Sombrero'),
(435, 135, 'Sosa'),
(436, 136, 'Las Mercedes'),
(437, 136, 'Cabruta'),
(438, 136, 'Santa Rita de Manapire'),
(439, 137, 'Valle de la Pascua'),
(440, 137, 'Espino'),
(441, 138, 'San José de Unare'),
(442, 138, 'Zaraza'),
(443, 139, 'San José de Tiznados'),
(444, 139, 'San Francisco de Tiznados'),
(445, 139, 'San Lorenzo de Tiznados'),
(446, 139, 'Ortiz'),
(447, 140, 'Guayabal'),
(448, 140, 'Cazorla'),
(449, 141, 'San José de Guaribe'),
(450, 141, 'Uveral'),
(451, 142, 'Santa María de Ipire'),
(452, 142, 'Altamira'),
(453, 143, 'El Calvario'),
(454, 143, 'El Rastro'),
(455, 143, 'Guardatinajas'),
(456, 143, 'Capital Urbana Calabozo'),
(457, 144, 'Quebrada Honda de Guache'),
(458, 144, 'Pío Tamayo'),
(459, 144, 'Yacambú'),
(460, 145, 'Fréitez'),
(461, 145, 'José María Blanco'),
(462, 146, 'Catedral'),
(463, 146, 'Concepción'),
(464, 146, 'El Cují'),
(465, 146, 'Juan de Villegas'),
(466, 146, 'Santa Rosa'),
(467, 146, 'Tamaca'),
(468, 146, 'Unión'),
(469, 146, 'Aguedo Felipe Alvarado'),
(470, 146, 'Buena Vista'),
(471, 146, 'Juárez'),
(472, 147, 'Juan Bautista Rodríguez'),
(473, 147, 'Cuara'),
(474, 147, 'Diego de Lozada'),
(475, 147, 'Paraíso de San José'),
(476, 147, 'San Miguel'),
(477, 147, 'Tintorero'),
(478, 147, 'José Bernardo Dorante'),
(479, 147, 'Coronel Mariano Peraza '),
(480, 148, 'Bolívar'),
(481, 148, 'Anzoátegui'),
(482, 148, 'Guarico'),
(483, 148, 'Hilario Luna y Luna'),
(484, 148, 'Humocaro Alto'),
(485, 148, 'Humocaro Bajo'),
(486, 148, 'La Candelaria'),
(487, 148, 'Morán'),
(488, 149, 'Cabudare'),
(489, 149, 'José Gregorio Bastidas'),
(490, 149, 'Agua Viva'),
(491, 150, 'Sarare'),
(492, 150, 'Buría'),
(493, 150, 'Gustavo Vegas León'),
(494, 151, 'Trinidad Samuel'),
(495, 151, 'Antonio Díaz'),
(496, 151, 'Camacaro'),
(497, 151, 'Castañeda'),
(498, 151, 'Cecilio Zubillaga'),
(499, 151, 'Chiquinquirá'),
(500, 151, 'El Blanco'),
(501, 151, 'Espinoza de los Monteros'),
(502, 151, 'Lara'),
(503, 151, 'Las Mercedes'),
(504, 151, 'Manuel Morillo'),
(505, 151, 'Montaña Verde'),
(506, 151, 'Montes de Oca'),
(507, 151, 'Torres'),
(508, 151, 'Heriberto Arroyo'),
(509, 151, 'Reyes Vargas'),
(510, 151, 'Altagracia'),
(511, 152, 'Siquisique'),
(512, 152, 'Moroturo'),
(513, 152, 'San Miguel'),
(514, 152, 'Xaguas'),
(515, 179, 'Presidente Betancourt'),
(516, 179, 'Presidente Páez'),
(517, 179, 'Presidente Rómulo Gallegos'),
(518, 179, 'Gabriel Picón González'),
(519, 179, 'Héctor Amable Mora'),
(520, 179, 'José Nucete Sardi'),
(521, 179, 'Pulido Méndez'),
(522, 180, 'La Azulita'),
(523, 181, 'Santa Cruz de Mora'),
(524, 181, 'Mesa Bolívar'),
(525, 181, 'Mesa de Las Palmas'),
(526, 182, 'Aricagua'),
(527, 182, 'San Antonio'),
(528, 183, 'Canagua'),
(529, 183, 'Capurí'),
(530, 183, 'Chacantá'),
(531, 183, 'El Molino'),
(532, 183, 'Guaimaral'),
(533, 183, 'Mucutuy'),
(534, 183, 'Mucuchachí'),
(535, 184, 'Fernández Peña'),
(536, 184, 'Matriz'),
(537, 184, 'Montalbán'),
(538, 184, 'Acequias'),
(539, 184, 'Jají'),
(540, 184, 'La Mesa'),
(541, 184, 'San José del Sur'),
(542, 185, 'Tucaní'),
(543, 185, 'Florencio Ramírez'),
(544, 186, 'Santo Domingo'),
(545, 186, 'Las Piedras'),
(546, 187, 'Guaraque'),
(547, 187, 'Mesa de Quintero'),
(548, 187, 'Río Negro'),
(549, 188, 'Arapuey'),
(550, 188, 'Palmira'),
(551, 189, 'San Cristóbal de Torondoy'),
(552, 189, 'Torondoy'),
(553, 190, 'Antonio Spinetti Dini'),
(554, 190, 'Arias'),
(555, 190, 'Caracciolo Parra Pérez'),
(556, 190, 'Domingo Peña'),
(557, 190, 'El Llano'),
(558, 190, 'Gonzalo Picón Febres'),
(559, 190, 'Jacinto Plaza'),
(560, 190, 'Juan Rodríguez Suárez'),
(561, 190, 'Lasso de la Vega'),
(562, 190, 'Mariano Picón Salas'),
(563, 190, 'Milla'),
(564, 190, 'Osuna Rodríguez'),
(565, 190, 'Sagrario'),
(566, 190, 'El Morro'),
(567, 190, 'Los Nevados'),
(568, 191, 'Andrés Eloy Blanco'),
(569, 191, 'La Venta'),
(570, 191, 'Piñango'),
(571, 191, 'Timotes'),
(572, 192, 'Eloy Paredes'),
(573, 192, 'San Rafael de Alcázar'),
(574, 192, 'Santa Elena de Arenales'),
(575, 193, 'Santa María de Caparo'),
(576, 194, 'Pueblo Llano'),
(577, 195, 'Cacute'),
(578, 195, 'La Toma'),
(579, 195, 'Mucuchíes'),
(580, 195, 'Mucurubá'),
(581, 195, 'San Rafael'),
(582, 196, 'Gerónimo Maldonado'),
(583, 196, 'Bailadores'),
(584, 197, 'Tabay'),
(585, 198, 'Chiguará'),
(586, 198, 'Estánquez'),
(587, 198, 'Lagunillas'),
(588, 198, 'La Trampa'),
(589, 198, 'Pueblo Nuevo del Sur'),
(590, 198, 'San Juan'),
(591, 199, 'El Amparo'),
(592, 199, 'El Llano'),
(593, 199, 'San Francisco'),
(594, 199, 'Tovar'),
(595, 200, 'Independencia'),
(596, 200, 'María de la Concepción Palacios Blanco'),
(597, 200, 'Nueva Bolivia'),
(598, 200, 'Santa Apolonia'),
(599, 201, 'Caño El Tigre'),
(600, 201, 'Zea'),
(601, 223, 'Aragüita'),
(602, 223, 'Arévalo González'),
(603, 223, 'Capaya'),
(604, 223, 'Caucagua'),
(605, 223, 'Panaquire'),
(606, 223, 'Ribas'),
(607, 223, 'El Café'),
(608, 223, 'Marizapa'),
(609, 224, 'Cumbo'),
(610, 224, 'San José de Barlovento'),
(611, 225, 'El Cafetal'),
(612, 225, 'Las Minas'),
(613, 225, 'Nuestra Señora del Rosario'),
(614, 226, 'Higuerote'),
(615, 226, 'Curiepe'),
(616, 226, 'Tacarigua de Brión'),
(617, 227, 'Mamporal'),
(618, 228, 'Carrizal'),
(619, 229, 'Chacao'),
(620, 230, 'Charallave'),
(621, 230, 'Las Brisas'),
(622, 231, 'El Hatillo'),
(623, 232, 'Altagracia de la Montaña'),
(624, 232, 'Cecilio Acosta'),
(625, 232, 'Los Teques'),
(626, 232, 'El Jarillo'),
(627, 232, 'San Pedro'),
(628, 232, 'Tácata'),
(629, 232, 'Paracotos'),
(630, 233, 'Cartanal'),
(631, 233, 'Santa Teresa del Tuy'),
(632, 234, 'La Democracia'),
(633, 234, 'Ocumare del Tuy'),
(634, 234, 'Santa Bárbara'),
(635, 235, 'San Antonio de los Altos'),
(636, 236, 'Río Chico'),
(637, 236, 'El Guapo'),
(638, 236, 'Tacarigua de la Laguna'),
(639, 236, 'Paparo'),
(640, 236, 'San Fernando del Guapo'),
(641, 237, 'Santa Lucía del Tuy'),
(642, 238, 'Cúpira'),
(643, 238, 'Machurucuto'),
(644, 239, 'Guarenas'),
(645, 240, 'San Antonio de Yare'),
(646, 240, 'San Francisco de Yare'),
(647, 241, 'Leoncio Martínez'),
(648, 241, 'Petare'),
(649, 241, 'Caucagüita'),
(650, 241, 'Filas de Mariche'),
(651, 241, 'La Dolorita'),
(652, 242, 'Cúa'),
(653, 242, 'Nueva Cúa'),
(654, 243, 'Guatire'),
(655, 243, 'Bolívar'),
(656, 258, 'San Antonio de Maturín'),
(657, 258, 'San Francisco de Maturín'),
(658, 259, 'Aguasay'),
(659, 260, 'Caripito'),
(660, 261, 'El Guácharo'),
(661, 261, 'La Guanota'),
(662, 261, 'Sabana de Piedra'),
(663, 261, 'San Agustín'),
(664, 261, 'Teresen'),
(665, 261, 'Caripe'),
(666, 262, 'Areo'),
(667, 262, 'Capital Cedeño'),
(668, 262, 'San Félix de Cantalicio'),
(669, 262, 'Viento Fresco'),
(670, 263, 'El Tejero'),
(671, 263, 'Punta de Mata'),
(672, 264, 'Chaguaramas'),
(673, 264, 'Las Alhuacas'),
(674, 264, 'Tabasca'),
(675, 264, 'Temblador'),
(676, 265, 'Alto de los Godos'),
(677, 265, 'Boquerón'),
(678, 265, 'Las Cocuizas'),
(679, 265, 'La Cruz'),
(680, 265, 'San Simón'),
(681, 265, 'El Corozo'),
(682, 265, 'El Furrial'),
(683, 265, 'Jusepín'),
(684, 265, 'La Pica'),
(685, 265, 'San Vicente'),
(686, 266, 'Aparicio'),
(687, 266, 'Aragua de Maturín'),
(688, 266, 'Chaguamal'),
(689, 266, 'El Pinto'),
(690, 266, 'Guanaguana'),
(691, 266, 'La Toscana'),
(692, 266, 'Taguaya'),
(693, 267, 'Cachipo'),
(694, 267, 'Quiriquire'),
(695, 268, 'Santa Bárbara'),
(696, 269, 'Barrancas'),
(697, 269, 'Los Barrancos de Fajardo'),
(698, 270, 'Uracoa'),
(699, 271, 'Antolín del Campo'),
(700, 272, 'Arismendi'),
(701, 273, 'García'),
(702, 273, 'Francisco Fajardo'),
(703, 274, 'Bolívar'),
(704, 274, 'Guevara'),
(705, 274, 'Matasiete'),
(706, 274, 'Santa Ana'),
(707, 274, 'Sucre'),
(708, 275, 'Aguirre'),
(709, 275, 'Maneiro'),
(710, 276, 'Adrián'),
(711, 276, 'Juan Griego'),
(712, 276, 'Yaguaraparo'),
(713, 277, 'Porlamar'),
(714, 278, 'San Francisco de Macanao'),
(715, 278, 'Boca de Río'),
(716, 279, 'Tubores'),
(717, 279, 'Los Baleales'),
(718, 280, 'Vicente Fuentes'),
(719, 280, 'Villalba'),
(720, 281, 'San Juan Bautista'),
(721, 281, 'Zabala'),
(722, 283, 'Capital Araure'),
(723, 283, 'Río Acarigua'),
(724, 284, 'Capital Esteller'),
(725, 284, 'Uveral'),
(726, 285, 'Guanare'),
(727, 285, 'Córdoba'),
(728, 285, 'San José de la Montaña'),
(729, 285, 'San Juan de Guanaguanare'),
(730, 285, 'Virgen de la Coromoto'),
(731, 286, 'Guanarito'),
(732, 286, 'Trinidad de la Capilla'),
(733, 286, 'Divina Pastora'),
(734, 287, 'Monseñor José Vicente de Unda'),
(735, 287, 'Peña Blanca'),
(736, 288, 'Capital Ospino'),
(737, 288, 'Aparición'),
(738, 288, 'La Estación'),
(739, 289, 'Páez'),
(740, 289, 'Payara'),
(741, 289, 'Pimpinela'),
(742, 289, 'Ramón Peraza'),
(743, 290, 'Papelón'),
(744, 290, 'Caño Delgadito'),
(745, 291, 'San Genaro de Boconoito'),
(746, 291, 'Antolín Tovar'),
(747, 292, 'San Rafael de Onoto'),
(748, 292, 'Santa Fe'),
(749, 292, 'Thermo Morles'),
(750, 293, 'Santa Rosalía'),
(751, 293, 'Florida'),
(752, 294, 'Sucre'),
(753, 294, 'Concepción'),
(754, 294, 'San Rafael de Palo Alzado'),
(755, 294, 'Uvencio Antonio Velásquez'),
(756, 294, 'San José de Saguaz'),
(757, 294, 'Villa Rosa'),
(758, 295, 'Turén'),
(759, 295, 'Canelones'),
(760, 295, 'Santa Cruz'),
(761, 295, 'San Isidro Labrador'),
(762, 296, 'Mariño'),
(763, 296, 'Rómulo Gallegos'),
(764, 297, 'San José de Aerocuar'),
(765, 297, 'Tavera Acosta'),
(766, 298, 'Río Caribe'),
(767, 298, 'Antonio José de Sucre'),
(768, 298, 'El Morro de Puerto Santo'),
(769, 298, 'Puerto Santo'),
(770, 298, 'San Juan de las Galdonas'),
(771, 299, 'El Pilar'),
(772, 299, 'El Rincón'),
(773, 299, 'General Francisco Antonio Váquez'),
(774, 299, 'Guaraúnos'),
(775, 299, 'Tunapuicito'),
(776, 299, 'Unión'),
(777, 300, 'Santa Catalina'),
(778, 300, 'Santa Rosa'),
(779, 300, 'Santa Teresa'),
(780, 300, 'Bolívar'),
(781, 300, 'Maracapana'),
(782, 302, 'Libertad'),
(783, 302, 'El Paujil'),
(784, 302, 'Yaguaraparo'),
(785, 303, 'Cruz Salmerón Acosta'),
(786, 303, 'Chacopata'),
(787, 303, 'Manicuare'),
(788, 304, 'Tunapuy'),
(789, 304, 'Campo Elías'),
(790, 305, 'Irapa'),
(791, 305, 'Campo Claro'),
(792, 305, 'Maraval'),
(793, 305, 'San Antonio de Irapa'),
(794, 305, 'Soro'),
(795, 306, 'Mejía'),
(796, 307, 'Cumanacoa'),
(797, 307, 'Arenas'),
(798, 307, 'Aricagua'),
(799, 307, 'Cogollar'),
(800, 307, 'San Fernando'),
(801, 307, 'San Lorenzo'),
(802, 308, 'Villa Frontado (Muelle de Cariaco)'),
(803, 308, 'Catuaro'),
(804, 308, 'Rendón'),
(805, 308, 'San Cruz'),
(806, 308, 'Santa María'),
(807, 309, 'Altagracia'),
(808, 309, 'Santa Inés'),
(809, 309, 'Valentín Valiente'),
(810, 309, 'Ayacucho'),
(811, 309, 'San Juan'),
(812, 309, 'Raúl Leoni'),
(813, 309, 'Gran Mariscal'),
(814, 310, 'Cristóbal Colón'),
(815, 310, 'Bideau'),
(816, 310, 'Punta de Piedras'),
(817, 310, 'Güiria'),
(818, 341, 'Andrés Bello'),
(819, 342, 'Antonio Rómulo Costa'),
(820, 343, 'Ayacucho'),
(821, 343, 'Rivas Berti'),
(822, 343, 'San Pedro del Río'),
(823, 344, 'Bolívar'),
(824, 344, 'Palotal'),
(825, 344, 'General Juan Vicente Gómez'),
(826, 344, 'Isaías Medina Angarita'),
(827, 345, 'Cárdenas'),
(828, 345, 'Amenodoro Ángel Lamus'),
(829, 345, 'La Florida'),
(830, 346, 'Córdoba'),
(831, 347, 'Fernández Feo'),
(832, 347, 'Alberto Adriani'),
(833, 347, 'Santo Domingo'),
(834, 348, 'Francisco de Miranda'),
(835, 349, 'García de Hevia'),
(836, 349, 'Boca de Grita'),
(837, 349, 'José Antonio Páez'),
(838, 350, 'Guásimos'),
(839, 351, 'Independencia'),
(840, 351, 'Juan Germán Roscio'),
(841, 351, 'Román Cárdenas'),
(842, 352, 'Jáuregui'),
(843, 352, 'Emilio Constantino Guerrero'),
(844, 352, 'Monseñor Miguel Antonio Salas'),
(845, 353, 'José María Vargas'),
(846, 354, 'Junín'),
(847, 354, 'La Petrólea'),
(848, 354, 'Quinimarí'),
(849, 354, 'Bramón'),
(850, 355, 'Libertad'),
(851, 355, 'Cipriano Castro'),
(852, 355, 'Manuel Felipe Rugeles'),
(853, 356, 'Libertador'),
(854, 356, 'Doradas'),
(855, 356, 'Emeterio Ochoa'),
(856, 356, 'San Joaquín de Navay'),
(857, 357, 'Lobatera'),
(858, 357, 'Constitución'),
(859, 358, 'Michelena'),
(860, 359, 'Panamericano'),
(861, 359, 'La Palmita'),
(862, 360, 'Pedro María Ureña'),
(863, 360, 'Nueva Arcadia'),
(864, 361, 'Delicias'),
(865, 361, 'Pecaya'),
(866, 362, 'Samuel Darío Maldonado'),
(867, 362, 'Boconó'),
(868, 362, 'Hernández'),
(869, 363, 'La Concordia'),
(870, 363, 'San Juan Bautista'),
(871, 363, 'Pedro María Morantes'),
(872, 363, 'San Sebastián'),
(873, 363, 'Dr. Francisco Romero Lobo'),
(874, 364, 'Seboruco'),
(875, 365, 'Simón Rodríguez'),
(876, 366, 'Sucre'),
(877, 366, 'Eleazar López Contreras'),
(878, 366, 'San Pablo'),
(879, 367, 'Torbes'),
(880, 368, 'Uribante'),
(881, 368, 'Cárdenas'),
(882, 368, 'Juan Pablo Peñalosa'),
(883, 368, 'Potosí'),
(884, 369, 'San Judas Tadeo'),
(885, 370, 'Araguaney'),
(886, 370, 'El Jaguito'),
(887, 370, 'La Esperanza'),
(888, 370, 'Santa Isabel'),
(889, 371, 'Boconó'),
(890, 371, 'El Carmen'),
(891, 371, 'Mosquey'),
(892, 371, 'Ayacucho'),
(893, 371, 'Burbusay'),
(894, 371, 'General Ribas'),
(895, 371, 'Guaramacal'),
(896, 371, 'Vega de Guaramacal'),
(897, 371, 'Monseñor Jáuregui'),
(898, 371, 'Rafael Rangel'),
(899, 371, 'San Miguel'),
(900, 371, 'San José'),
(901, 372, 'Sabana Grande'),
(902, 372, 'Cheregüé'),
(903, 372, 'Granados'),
(904, 373, 'Arnoldo Gabaldón'),
(905, 373, 'Bolivia'),
(906, 373, 'Carrillo'),
(907, 373, 'Cegarra'),
(908, 373, 'Chejendé'),
(909, 373, 'Manuel Salvador Ulloa'),
(910, 373, 'San José'),
(911, 374, 'Carache'),
(912, 374, 'La Concepción'),
(913, 374, 'Cuicas'),
(914, 374, 'Panamericana'),
(915, 374, 'Santa Cruz'),
(916, 375, 'Escuque'),
(917, 375, 'La Unión'),
(918, 375, 'Santa Rita'),
(919, 375, 'Sabana Libre'),
(920, 376, 'El Socorro'),
(921, 376, 'Los Caprichos'),
(922, 376, 'Antonio José de Sucre'),
(923, 377, 'Campo Elías'),
(924, 377, 'Arnoldo Gabaldón'),
(925, 378, 'Santa Apolonia'),
(926, 378, 'El Progreso'),
(927, 378, 'La Ceiba'),
(928, 378, 'Tres de Febrero'),
(929, 379, 'El Dividive'),
(930, 379, 'Agua Santa'),
(931, 379, 'Agua Caliente'),
(932, 379, 'El Cenizo'),
(933, 379, 'Valerita'),
(934, 380, 'Monte Carmelo'),
(935, 380, 'Buena Vista'),
(936, 380, 'Santa María del Horcón'),
(937, 381, 'Motatán'),
(938, 381, 'El Baño'),
(939, 381, 'Jalisco'),
(940, 382, 'Pampán'),
(941, 382, 'Flor de Patria'),
(942, 382, 'La Paz'),
(943, 382, 'Santa Ana'),
(944, 383, 'Pampanito'),
(945, 383, 'La Concepción'),
(946, 383, 'Pampanito II'),
(947, 384, 'Betijoque'),
(948, 384, 'José Gregorio Hernández'),
(949, 384, 'La Pueblita'),
(950, 384, 'Los Cedros'),
(951, 385, 'Carvajal'),
(952, 385, 'Campo Alegre'),
(953, 385, 'Antonio Nicolás Briceño'),
(954, 385, 'José Leonardo Suárez'),
(955, 386, 'Sabana de Mendoza'),
(956, 386, 'Junín'),
(957, 386, 'Valmore Rodríguez'),
(958, 386, 'El Paraíso'),
(959, 387, 'Andrés Linares'),
(960, 387, 'Chiquinquirá'),
(961, 387, 'Cristóbal Mendoza'),
(962, 387, 'Cruz Carrillo'),
(963, 387, 'Matriz'),
(964, 387, 'Monseñor Carrillo'),
(965, 387, 'Tres Esquinas'),
(966, 388, 'Cabimbú'),
(967, 388, 'Jajó'),
(968, 388, 'La Mesa de Esnujaque'),
(969, 388, 'Santiago'),
(970, 388, 'Tuñame'),
(971, 388, 'La Quebrada'),
(972, 389, 'Juan Ignacio Montilla'),
(973, 389, 'La Beatriz'),
(974, 389, 'La Puerta'),
(975, 389, 'Mendoza del Valle de Momboy'),
(976, 389, 'Mercedes Díaz'),
(977, 389, 'San Luis'),
(978, 390, 'Caraballeda'),
(979, 390, 'Carayaca'),
(980, 390, 'Carlos Soublette'),
(981, 390, 'Caruao Chuspa'),
(982, 390, 'Catia La Mar'),
(983, 390, 'El Junko'),
(984, 390, 'La Guaira'),
(985, 390, 'Macuto'),
(986, 390, 'Maiquetía'),
(987, 390, 'Naiguatá'),
(988, 390, 'Urimare'),
(989, 391, 'Arístides Bastidas'),
(990, 392, 'Bolívar'),
(991, 407, 'Chivacoa'),
(992, 407, 'Campo Elías'),
(993, 408, 'Cocorote'),
(994, 409, 'Independencia'),
(995, 410, 'José Antonio Páez'),
(996, 411, 'La Trinidad'),
(997, 412, 'Manuel Monge'),
(998, 413, 'Salóm'),
(999, 413, 'Temerla'),
(1000, 413, 'Nirgua'),
(1001, 414, 'San Andrés'),
(1002, 414, 'Yaritagua'),
(1003, 415, 'San Javier'),
(1004, 415, 'Albarico'),
(1005, 415, 'San Felipe'),
(1006, 416, 'Sucre'),
(1007, 417, 'Urachiche'),
(1008, 418, 'El Guayabo'),
(1009, 418, 'Farriar'),
(1010, 441, 'Isla de Toas'),
(1011, 441, 'Monagas'),
(1012, 442, 'San Timoteo'),
(1013, 442, 'General Urdaneta'),
(1014, 442, 'Libertador'),
(1015, 442, 'Marcelino Briceño'),
(1016, 442, 'Pueblo Nuevo'),
(1017, 442, 'Manuel Guanipa Matos'),
(1018, 443, 'Ambrosio'),
(1019, 443, 'Carmen Herrera'),
(1020, 443, 'La Rosa'),
(1021, 443, 'Germán Ríos Linares'),
(1022, 443, 'San Benito'),
(1023, 443, 'Rómulo Betancourt'),
(1024, 443, 'Jorge Hernández'),
(1025, 443, 'Punta Gorda'),
(1026, 443, 'Arístides Calvani'),
(1027, 444, 'Encontrados'),
(1028, 444, 'Udón Pérez'),
(1029, 445, 'Moralito'),
(1030, 445, 'San Carlos del Zulia'),
(1031, 445, 'Santa Cruz del Zulia'),
(1032, 445, 'Santa Bárbara'),
(1033, 445, 'Urribarrí'),
(1034, 446, 'Carlos Quevedo'),
(1035, 446, 'Francisco Javier Pulgar'),
(1036, 446, 'Simón Rodríguez'),
(1037, 446, 'Guamo-Gavilanes'),
(1038, 448, 'La Concepción'),
(1039, 448, 'San José'),
(1040, 448, 'Mariano Parra León'),
(1041, 448, 'José Ramón Yépez'),
(1042, 449, 'Jesús María Semprún'),
(1043, 449, 'Barí'),
(1044, 450, 'Concepción'),
(1045, 450, 'Andrés Bello'),
(1046, 450, 'Chiquinquirá'),
(1047, 450, 'El Carmelo'),
(1048, 450, 'Potreritos'),
(1049, 451, 'Libertad'),
(1050, 451, 'Alonso de Ojeda'),
(1051, 451, 'Venezuela'),
(1052, 451, 'Eleazar López Contreras'),
(1053, 451, 'Campo Lara'),
(1054, 452, 'Bartolomé de las Casas'),
(1055, 452, 'Libertad'),
(1056, 452, 'Río Negro'),
(1057, 452, 'San José de Perijá'),
(1058, 453, 'San Rafael'),
(1059, 453, 'La Sierrita'),
(1060, 453, 'Las Parcelas'),
(1061, 453, 'Luis de Vicente'),
(1062, 453, 'Monseñor Marcos Sergio Godoy'),
(1063, 453, 'Ricaurte'),
(1064, 453, 'Tamare'),
(1065, 454, 'Antonio Borjas Romero'),
(1066, 454, 'Bolívar'),
(1067, 454, 'Cacique Mara'),
(1068, 454, 'Carracciolo Parra Pérez'),
(1069, 454, 'Cecilio Acosta'),
(1070, 454, 'Cristo de Aranza'),
(1071, 454, 'Coquivacoa'),
(1072, 454, 'Chiquinquirá'),
(1073, 454, 'Francisco Eugenio Bustamante'),
(1074, 454, 'Idelfonzo Vásquez'),
(1075, 454, 'Juana de Ávila'),
(1076, 454, 'Luis Hurtado Higuera'),
(1077, 454, 'Manuel Dagnino'),
(1078, 454, 'Olegario Villalobos'),
(1079, 454, 'Raúl Leoni'),
(1080, 454, 'Santa Lucía'),
(1081, 454, 'Venancio Pulgar'),
(1082, 454, 'San Isidro'),
(1083, 455, 'Altagracia'),
(1084, 455, 'Faría'),
(1085, 455, 'Ana María Campos'),
(1086, 455, 'San Antonio'),
(1087, 455, 'San José'),
(1088, 456, 'Donaldo García'),
(1089, 456, 'El Rosario'),
(1090, 456, 'Sixto Zambrano'),
(1091, 457, 'San Francisco'),
(1092, 457, 'El Bajo'),
(1093, 457, 'Domitila Flores'),
(1094, 457, 'Francisco Ochoa'),
(1095, 457, 'Los Cortijos'),
(1096, 457, 'Marcial Hernández'),
(1097, 458, 'Santa Rita'),
(1098, 458, 'El Mene'),
(1099, 458, 'Pedro Lucas Urribarrí'),
(1100, 458, 'José Cenobio Urribarrí'),
(1101, 459, 'Rafael Maria Baralt'),
(1102, 459, 'Manuel Manrique'),
(1103, 459, 'Rafael Urdaneta'),
(1104, 460, 'Bobures'),
(1105, 460, 'Gibraltar'),
(1106, 460, 'Heras'),
(1107, 460, 'Monseñor Arturo Álvarez'),
(1108, 460, 'Rómulo Gallegos'),
(1109, 460, 'El Batey'),
(1110, 461, 'Rafael Urdaneta'),
(1111, 461, 'La Victoria'),
(1112, 461, 'Raúl Cuenca'),
(1113, 447, 'Sinamaica'),
(1114, 447, 'Alta Guajira'),
(1115, 447, 'Elías Sánchez Rubio'),
(1116, 447, 'Guajira'),
(1117, 462, 'Altagracia'),
(1118, 462, 'Antímano'),
(1119, 462, 'Caricuao'),
(1120, 462, 'Catedral'),
(1121, 462, 'Coche'),
(1122, 462, 'El Junquito'),
(1123, 462, 'El Paraíso'),
(1124, 462, 'El Recreo'),
(1125, 462, 'El Valle'),
(1126, 462, 'La Candelaria'),
(1127, 462, 'La Pastora'),
(1128, 462, 'La Vega'),
(1129, 462, 'Macarao'),
(1130, 462, 'San Agustín'),
(1131, 462, 'San Bernardino'),
(1132, 462, 'San José'),
(1133, 462, 'San Juan'),
(1134, 462, 'San Pedro'),
(1135, 462, 'Santa Rosalía'),
(1136, 462, 'Santa Teresa'),
(1137, 462, 'Sucre (Catia)'),
(1138, 462, '23 de enero');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `password_resets`
--

CREATE TABLE `password_resets` (
  `email` varchar(125) COLLATE utf8mb4_unicode_ci NOT NULL,
  `token` varchar(125) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pediatria`
--

CREATE TABLE `pediatria` (
  `id_Pediatria` int(11) NOT NULL,
  `Paciente_Id` int(11) DEFAULT NULL,
  `Paciente_Infantil_id` int(11) DEFAULT NULL,
  `Medico_id` int(11) DEFAULT NULL,
  `Fecha` datetime DEFAULT NULL,
  `Pediatrico` int(11) DEFAULT NULL,
  `Control_Historia_Medico_id` int(11) DEFAULT NULL,
  `Dato1` int(11) DEFAULT NULL,
  `Dato2` int(11) DEFAULT NULL,
  `Dato3` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `permissions`
--

CREATE TABLE `permissions` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `name` varchar(125) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `guard_name` varchar(125) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `permissions`
--

INSERT INTO `permissions` (`id`, `name`, `description`, `guard_name`, `created_at`, `updated_at`) VALUES
(1, 'home', 'Ver dashboard', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(2, 'rol', 'Inicio roles', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(3, 'rol.add', 'Agregar rol', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(4, 'rol.destroy', 'Eliminar rol', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(5, 'pais', 'Inicio de paises', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(6, 'pais.add', 'Agregar pais', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(7, 'pais.edit', 'Editar pais', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(8, 'pais.destroy', 'Eliminar pais', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(9, 'estado', 'Inicio de estados', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(10, 'estado.add', 'Agregar estado', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(11, 'estado.edit', 'Editar estado', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(12, 'estado.destroy', 'Eliminar estado', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(13, 'ciudad', 'Inicio de ciudades', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(14, 'ciudad.add', 'Agregar ciudad', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(15, 'ciudad.edit', 'Editar ciudad', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(16, 'ciudad.destroy', 'Eliminar ciudad', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(17, 'municipio', 'Inicio de municipios', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(18, 'municipio.add', 'Agregar municipio', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(19, 'municipio.edit', 'Editar municipio', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(20, 'municipio.destroy', 'Eliminar municipio', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(21, 'parroquia', 'Inicio de parroquias', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(22, 'parroquia.add', 'Agregar parroquia', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(23, 'parroquia.edit', 'Editar parroquia', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(24, 'parroquia.destroy', 'Eliminar parroquia', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(25, 'prefijo', 'Inicio de prefijos DNI', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(26, 'prefijo.add', 'Agregar prefijo DNI', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(27, 'prefijo.edit', 'Editar prefijo DNI', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(28, 'prefijo.destroy', 'Eliminar prefijo DNI', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(29, 'sexo', 'Inicio de sexos', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(30, 'sexo.add', 'Agregar sexo', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(31, 'sexo.edit', 'Editar sexo', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(32, 'sexo.destroy', 'Eliminar sexo', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(33, 'civil', 'Inicio de estado civiles', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(34, 'civil.add', 'Agregar estado civil', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(35, 'civil.edit', 'Editar estado civil', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(36, 'civil.destroy', 'Eliminar estado civil', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(37, 'status_m', 'Inicio de status medico', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(38, 'status_m.add', 'Agregar status medico', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(39, 'status_m.edit', 'Editar status medico', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(40, 'status_m.destroy', 'Eliminar status medico', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(41, 'status_c', 'Inicio de status consulta', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(42, 'status_c.add', 'Agregar status consulta', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(43, 'status_c.edit', 'Editar status consulta', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(44, 'status_c.destroy', 'Eliminar status consulta', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(45, 'status_f', 'Inicio de status factura', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(46, 'status_f.add', 'Agregar status factura', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(47, 'status_f.edit', 'Editar status factura', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(48, 'status_f.destroy', 'Eliminar status factura', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(49, 'status_t', 'Inicio de status tasa', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(50, 'status_t.add', 'Agregar status tasa', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(51, 'status_t.edit', 'Editar status tasa', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(52, 'status_t.destroy', 'Eliminar status tasa', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(53, 'status', 'Inicio de status', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(54, 'status.add', 'Agregar status', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(55, 'status.edit', 'Editar status', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(56, 'status.destroy', 'Eliminar status', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(57, 'usuario_m', 'Inicio de usuario medico', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(58, 'usuario_m.create', 'vista crear usuario medico', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(59, 'usuario_m.add', 'Agregar usuario medico', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(60, 'usuario_m.edit', 'Editar usuario medico', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(61, 'usuario_m.destroy', 'Eliminar usuario medico', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(62, 'usuario_m.seniat', 'agregar datos del seniat usuario medico', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(63, 'usuario_m.login', 'agregar datos login usuario medico', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(64, 'urologia', 'Inicio de Historia urologia', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(65, 'urologia.create', 'vista Historia urologia', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(66, 'urologia.add', 'Agregar Historia urologia', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(67, 'urologia.edit', 'Editar Historia urologia', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(68, 'urologia.destroy', 'Eliminar Historia urologia', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(69, 'rol.create', 'crear rol', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(70, 'rol.edit', 'editar rol', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(71, 'usuario_a.add', 'Agregar Asistente', 'web', '2021-10-29 02:41:02', '2021-10-29 02:41:02'),
(72, 'usuario_a', 'listado de Asistente', 'web', '2021-10-29 02:41:02', '2021-10-29 02:41:02'),
(73, 'usuario_a.edit', 'Editar datos Asistente', 'web', '2021-10-29 02:41:02', '2021-10-29 02:41:02'),
(74, 'usuario_a.destroy', 'Eliminar Asistente', 'web', '2021-10-29 02:41:02', '2021-10-29 02:41:02'),
(75, 'usuario_p', 'listado de usuarios pacientes', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(76, 'usuario_p.create', 'vista agregar usuarios pacientes', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(77, 'usuario_p.edit', 'vista editar usuarios pacientes', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(78, 'usuario_p.destroy', 'Eliminar usuarios pacientes', 'web', '2021-10-28 08:00:00', '2021-10-28 08:00:00'),
(79, 'usuario_p.add', 'agregar usuario paciente', 'web', '2021-10-29 02:41:02', '2021-10-29 02:41:02'),
(80, 'usuario_p.update', 'actualizar usuario paciente', 'web', '2021-10-29 02:41:02', '2021-10-29 02:41:02'),
(81, 'cripto.add', 'Agregar Cripto', 'web', '2021-10-29 06:41:02', '2021-10-29 06:41:02'),
(82, 'cripto', 'listado de Cripto', 'web', '2021-10-29 06:41:02', '2021-10-29 06:41:02'),
(83, 'cripto.edit', 'Editar datos Cripto', 'web', '2021-10-29 06:41:02', '2021-10-29 06:41:02'),
(84, 'cripto.destroy', 'Eliminar Cripto', 'web', '2021-10-29 06:41:02', '2021-10-29 06:41:02'),
(85, 'banco', 'Listado de bancos', 'web', '2021-10-28 12:00:00', '2021-10-28 12:00:00'),
(86, 'banco.add', 'Agregar bancos', 'web', '2021-10-28 12:00:00', '2021-10-28 12:00:00'),
(87, 'banco.edit', 'Editar bancos', 'web', '2021-10-28 12:00:00', '2021-10-28 12:00:00'),
(88, 'banco.destroy', 'Eliminar bancos', 'web', '2021-10-28 12:00:00', '2021-10-28 12:00:00'),
(89, 'billetera', 'Listado de billeteras criptos', 'web', '2021-10-28 12:00:00', '2021-10-28 12:00:00'),
(90, 'billetera.add', 'Agregar billeteras criptos', 'web', '2021-10-28 12:00:00', '2021-10-28 12:00:00'),
(91, 'billetera.edit', 'Editar billeteras criptos', 'web', '2021-10-28 12:00:00', '2021-10-28 12:00:00'),
(92, 'billetera.destroy', 'Eliminar billeteras criptos', 'web', '2021-10-28 12:00:00', '2021-10-28 12:00:00'),
(93, 'cuenta_banco', 'Listado de Cuenta de Banco', 'web', '2021-10-28 12:00:00', '2021-10-28 12:00:00'),
(94, 'cuenta_banco.add', 'Agregar Cuenta de Banco', 'web', '2021-10-28 12:00:00', '2021-10-28 12:00:00'),
(95, 'cuenta_banco.edit', 'Editar Cuenta de Banco', 'web', '2021-10-28 12:00:00', '2021-10-28 12:00:00'),
(96, 'cuenta_banco.destroy', 'Eliminar Cuenta de Banco', 'web', '2021-10-28 12:00:00', '2021-10-28 12:00:00'),
(97, 'especialidad', 'Listado de especialidad medica', 'web', '2021-11-17 12:30:00', '2021-11-17 12:30:00'),
(98, 'especialidad.add', 'Agregar especialidad medica', 'web', '2021-11-17 12:30:00', '2021-11-17 12:30:00'),
(99, 'especialidad.edit', 'Editar especialidad medica', 'web', '2021-11-17 12:30:00', '2021-11-17 12:30:00'),
(100, 'especialidad.destroy', 'Eliminar especialidad medica', 'web', '2021-11-17 12:30:00', '2021-11-17 12:30:00'),
(101, 'consultorio', 'Listado de Consultorios', 'web', '2021-11-17 12:30:00', '2021-11-17 12:30:00'),
(102, 'consultorio.add', 'Agregar Consultorios', 'web', '2021-11-17 12:30:00', '2021-11-17 12:30:00'),
(103, 'consultorio.edit', 'Editar Consultorios', 'web', '2021-11-17 12:30:00', '2021-11-17 12:30:00'),
(104, 'consultorio.destroy', 'Eliminar Consultorios', 'web', '2021-11-17 12:30:00', '2021-11-17 12:30:00'),
(105, 'entidad', 'Listado de Entidad USD', 'web', '2021-11-24 12:00:00', '2021-11-24 12:00:00'),
(106, 'entidad.add', 'Agregar Entidad USD', 'web', '2021-11-24 12:00:00', '2021-11-24 12:00:00'),
(107, 'entidad.edit', 'Editar Entidad USD', 'web', '2021-11-24 12:00:00', '2021-11-24 12:00:00'),
(108, 'entidad.destroy', 'Eliminar Entidad USD', 'web', '2021-11-24 12:00:00', '2021-11-24 12:00:00'),
(109, 'tipoC', 'Listado de Tipos de Cuenta', 'web', '2021-11-24 12:00:00', '2021-11-24 12:00:00'),
(110, 'tipoC.add', 'Agregar Tipos de Cuenta', 'web', '2021-11-24 12:00:00', '2021-11-24 12:00:00'),
(111, 'tipoC.edit', 'Editar Tipos de Cuenta', 'web', '2021-11-24 12:00:00', '2021-11-24 12:00:00'),
(112, 'tipoC.destroy', 'Eliminar Tipos de Cuenta', 'web', '2021-11-24 12:00:00', '2021-11-24 12:00:00'),
(113, 'cuentaUSD', 'Listado de cuentas USD', 'web', '2021-11-25 12:00:00', '2021-11-25 12:00:00'),
(114, 'cuentaUSD.add', 'Agregar cuentas USD', 'web', '2021-11-25 12:00:00', '2021-11-25 12:00:00'),
(115, 'cuentaUSD.edit', 'Editar cuentas USD', 'web', '2021-11-25 12:00:00', '2021-11-25 12:00:00'),
(116, 'cuentaUSD.destroy', 'Eliminar cuentas USD', 'web', '2021-11-25 12:00:00', '2021-11-25 12:00:00'),
(117, 'controlE', 'Listado de Control de Especialidades', 'web', '2021-11-26 12:00:00', '2021-11-26 12:00:00'),
(118, 'controlE.add', 'Agregar Control de Especialidades', 'web', '2021-11-26 12:00:00', '2021-11-26 12:00:00'),
(119, 'controlE.edit', 'Editar Control de Especialidades', 'web', '2021-11-26 12:00:00', '2021-11-26 12:00:00'),
(120, 'controlE.destroy', 'Eliminar Control de Especialidades', 'web', '2021-11-26 12:00:00', '2021-11-26 12:00:00'),
(121, 'usuario_pe', 'Listado de Paciente Especial', 'web', '2021-12-01 12:00:00', '2021-12-01 12:00:00'),
(122, 'usuario_pe.add', 'Agregar Paciente Especial', 'web', '2021-12-01 12:00:00', '2021-12-01 12:00:00'),
(123, 'usuario_pe.edit', 'Editar Paciente Especial', 'web', '2021-12-01 12:00:00', '2021-12-01 12:00:00'),
(124, 'usuario_pe.destroy', 'Eliminar Paciente Especial', 'web', '2021-12-01 12:00:00', '2021-12-01 12:00:00'),
(125, 'tpago', 'Listado de Tipo de Pago', 'web', '2021-12-09 12:30:00', '2021-12-09 12:30:00'),
(126, 'tpago.add', 'Agregar Tipo de Pago', 'web', '2021-12-09 12:30:00', '2021-12-09 12:30:00'),
(127, 'tpago.edit', 'Editar Tipo de Pago', 'web', '2021-12-09 12:30:00', '2021-12-09 12:30:00'),
(128, 'tpago.destroy', 'Eliminar Tipo de Pago', 'web', '2021-12-09 12:30:00', '2021-12-09 12:30:00'),
(129, 'tcambio', 'Listado de Tipo de Cambio', 'web', '2021-12-09 12:30:00', '2021-12-09 12:30:00'),
(130, 'tcambio.add', 'Agregar Tipo de Cambio', 'web', '2021-12-09 12:30:00', '2021-12-09 12:30:00'),
(131, 'tcambio.edit', 'Editar Tipo de Cambio', 'web', '2021-12-09 12:30:00', '2021-12-09 12:30:00'),
(132, 'tcambio.destroy', 'Eliminar Tipo de Cambio', 'web', '2021-12-09 12:30:00', '2021-12-09 12:30:00'),
(133, 'servicio', 'Listado de Servicio', 'web', '2021-12-09 12:30:00', '2021-12-09 12:30:00'),
(134, 'servicio.add', 'Agregar Servicio', 'web', '2021-12-09 12:30:00', '2021-12-09 12:30:00'),
(135, 'servicio.edit', 'Editar Servicio', 'web', '2021-12-09 12:30:00', '2021-12-09 12:30:00'),
(136, 'servicio.destroy', 'Eliminar Servicio', 'web', '2021-12-09 12:30:00', '2021-12-09 12:30:00'),
(137, 'horario', 'Listado de horario', 'web', '2012-12-21 12:30:00', '2012-12-21 12:30:00'),
(138, 'horario.add', 'Agregar horario', 'web', '2012-12-21 12:30:00', '2012-12-21 12:30:00'),
(139, 'horario.edit', 'Editar horario', 'web', '2012-12-21 12:30:00', '2012-12-21 12:30:00'),
(140, 'horario.destroy', 'Eliminar horario', 'web', '2012-12-21 12:30:00', '2012-12-21 12:30:00'),
(141, 'agendas', 'Listado de agendas', 'web', '2022-02-22 10:30:00', '2022-02-22 10:30:00'),
(142, 'agendas.add', 'agregar agendas', 'web', '2022-02-22 10:30:00', '2022-02-22 10:30:00'),
(143, 'agendas.edit', 'editar agendas', 'web', '2022-02-22 10:30:00', '2022-02-22 10:30:00'),
(144, 'agendas.update', 'actualizar agendas', 'web', '2022-02-22 10:30:00', '2022-02-22 10:30:00'),
(145, 'agendas.destroy', 'eliminar agendas', 'web', '2022-02-22 10:30:00', '2022-02-22 10:30:00'),
(146, 'citas', 'listar citas', 'web', '2022-02-22 10:30:00', '2022-02-22 10:30:00'),
(147, 'citas.add', 'agregar citas', 'web', '2022-02-22 10:30:00', '2022-02-22 10:30:00'),
(148, 'citas.edit', 'editar citas', 'web', '2022-02-22 10:30:00', '2022-02-22 10:30:00'),
(149, 'citas.update', 'actualizar citas', 'web', '2022-02-22 10:30:00', '2022-02-22 10:30:00'),
(150, 'citas.destroy', 'eliminar citas', 'web', '2022-02-22 10:30:00', '2022-02-22 10:30:00'),
(151, 'consultao', 'listar consulta online', 'web', '2022-03-03 19:30:00', '2022-03-03 19:30:00'),
(152, 'consultao.add', 'agregar consulta online', 'web', '2022-03-03 19:30:00', '2022-03-03 19:30:00'),
(153, 'consultao.edit', 'editar consulta online', 'web', '2022-03-03 19:30:00', '2022-03-03 19:30:00'),
(154, 'consultao.update', 'actualizar consulta online', 'web', '2022-03-03 19:30:00', '2022-03-03 19:30:00'),
(155, 'consultao.delete', 'eliminar consulta online', 'web', '2022-03-03 19:30:00', '2022-03-03 19:30:00'),
(156, 'consulta', 'listar consulta', 'web', '2022-03-21 19:30:00', '2022-03-21 19:30:00'),
(157, 'consulta.add', 'agregar consulta', 'web', '2022-03-21 19:30:00', '2022-03-21 19:30:00'),
(158, 'consulta.edit', 'editar consulta', 'web', '2022-03-21 19:30:00', '2022-03-21 19:30:00'),
(159, 'consulta.update', 'actualizar consulta', 'web', '2022-03-21 19:30:00', '2022-03-21 19:30:00'),
(160, 'consulta.delete', 'eliminar consulta', 'web', '2022-03-21 19:30:00', '2022-03-21 19:30:00'),
(161, 'reporte_consulta', 'listar reporte consulta', 'web', '2022-03-25 19:30:00', '2022-03-25 19:30:00'),
(167, 'usuario_g', 'listar usuario general', 'web', '2022-03-28 15:00:00', '2022-03-28 15:00:00'),
(168, 'usuario_g.add', 'agregar usuario general', 'web', '2022-03-28 15:00:00', '2022-03-28 15:00:00'),
(169, 'usuario_g.edit', 'editar usuario general', 'web', '2022-03-28 15:00:00', '2022-03-28 15:00:00'),
(170, 'usuario_g.update', 'actualizar usuario general', 'web', '2022-03-28 15:00:00', '2022-03-28 15:00:00'),
(171, 'usuario_g.delete', 'eliminar usuario general', 'web', '2022-03-28 15:00:00', '2022-03-28 15:00:00'),
(172, 'factura', 'listar factura', 'web', '2022-05-05 15:00:00', '2022-05-05 15:00:00'),
(173, 'factura.add', 'agregar factura', 'web', '2022-05-05 15:00:00', '2022-05-05 15:00:00'),
(174, 'factura.edit', 'editar factura', 'web', '2022-05-05 15:00:00', '2022-05-05 15:00:00'),
(175, 'factura.update', 'actualizar factura', 'web', '2022-05-05 15:00:00', '2022-05-05 15:00:00'),
(176, 'factura.delete', 'eliminar factura', 'web', '2022-05-05 15:00:00', '2022-05-05 15:00:00'),
(177, 'facturaH', 'listar facturas', 'web', '2022-05-10 15:00:00', '2022-05-10 15:00:00'),
(178, 'facturaH.add', 'descargar factura', 'web', '2022-05-10 15:00:00', '2022-05-10 15:00:00'),
(179, 'pago', 'listar pago', 'web', '2022-05-11 15:00:00', '2022-05-11 15:00:00'),
(180, 'pago.add', 'agregar pago', 'web', '2022-05-11 15:00:00', '2022-05-11 15:00:00'),
(181, 'pago.edit', 'editar pago', 'web', '2022-05-11 15:00:00', '2022-05-11 15:00:00'),
(182, 'pago.update', 'actualizar pago', 'web', '2022-05-11 15:00:00', '2022-05-11 15:00:00'),
(183, 'pago.delete', 'eliminar pago', 'web', '2022-05-11 15:00:00', '2022-05-11 15:00:00'),
(184, 'confirmar_pago', 'listar confirmar pago', 'web', '2022-05-19 15:00:00', '2022-05-19 15:00:00'),
(185, 'confirmar_pago.add', 'agregar confirmar pago', 'web', '2022-05-19 15:00:00', '2022-05-19 15:00:00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `prefijos_cidni`
--

CREATE TABLE `prefijos_cidni` (
  `id_Prefijo_CIDNI` int(11) NOT NULL,
  `Prefijo_CIDNI` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `prefijos_cidni`
--

INSERT INTO `prefijos_cidni` (`id_Prefijo_CIDNI`, `Prefijo_CIDNI`) VALUES
(1, 'V -');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `roles`
--

CREATE TABLE `roles` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `name` varchar(125) COLLATE utf8mb4_unicode_ci NOT NULL,
  `guard_name` varchar(125) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `roles`
--

INSERT INTO `roles` (`id`, `name`, `guard_name`, `created_at`, `updated_at`) VALUES
(1, 'Admin', 'web', '2021-10-29 02:13:12', '2021-10-29 02:13:12'),
(2, 'Administrativo', 'web', '2022-03-30 13:44:30', '2022-03-30 13:44:30'),
(3, 'Medico', 'web', '2022-03-30 19:56:51', '2022-03-30 19:56:51'),
(4, 'Paciente', 'web', '2022-03-30 21:01:01', '2022-03-30 21:01:01');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `role_has_permissions`
--

CREATE TABLE `role_has_permissions` (
  `permission_id` bigint(20) UNSIGNED NOT NULL,
  `role_id` bigint(20) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `role_has_permissions`
--

INSERT INTO `role_has_permissions` (`permission_id`, `role_id`) VALUES
(1, 1),
(1, 2),
(1, 3),
(1, 4),
(2, 1),
(3, 1),
(4, 1),
(5, 1),
(6, 1),
(7, 1),
(8, 1),
(9, 1),
(10, 1),
(11, 1),
(12, 1),
(13, 1),
(14, 1),
(15, 1),
(16, 1),
(17, 1),
(18, 1),
(19, 1),
(20, 1),
(21, 1),
(22, 1),
(23, 1),
(24, 1),
(25, 1),
(25, 2),
(26, 1),
(26, 2),
(27, 1),
(27, 2),
(28, 1),
(28, 2),
(29, 1),
(29, 2),
(30, 1),
(30, 2),
(31, 1),
(31, 2),
(32, 1),
(32, 2),
(33, 1),
(33, 2),
(34, 1),
(34, 2),
(35, 1),
(35, 2),
(36, 1),
(36, 2),
(37, 1),
(38, 1),
(39, 1),
(40, 1),
(41, 1),
(42, 1),
(43, 1),
(44, 1),
(45, 1),
(46, 1),
(47, 1),
(48, 1),
(49, 1),
(50, 1),
(51, 1),
(52, 1),
(53, 1),
(54, 1),
(55, 1),
(56, 1),
(57, 1),
(57, 3),
(58, 1),
(58, 3),
(59, 1),
(59, 3),
(60, 1),
(60, 3),
(61, 1),
(61, 3),
(62, 1),
(62, 3),
(63, 1),
(63, 3),
(64, 1),
(65, 1),
(66, 1),
(67, 1),
(68, 1),
(69, 1),
(70, 1),
(71, 1),
(71, 3),
(72, 1),
(72, 3),
(73, 1),
(73, 3),
(74, 1),
(74, 3),
(75, 1),
(75, 4),
(76, 1),
(76, 4),
(77, 1),
(77, 4),
(78, 1),
(78, 4),
(79, 1),
(79, 4),
(80, 1),
(80, 4),
(81, 1),
(82, 1),
(83, 1),
(84, 1),
(85, 1),
(86, 1),
(87, 1),
(88, 1),
(89, 1),
(90, 1),
(91, 1),
(92, 1),
(93, 1),
(94, 1),
(95, 1),
(96, 1),
(97, 1),
(97, 3),
(98, 1),
(98, 3),
(99, 1),
(99, 3),
(100, 1),
(100, 3),
(101, 1),
(101, 3),
(102, 1),
(102, 3),
(103, 1),
(103, 3),
(104, 1),
(104, 3),
(105, 1),
(106, 1),
(107, 1),
(108, 1),
(109, 1),
(110, 1),
(111, 1),
(112, 1),
(113, 1),
(114, 1),
(115, 1),
(116, 1),
(117, 1),
(117, 3),
(118, 1),
(118, 3),
(119, 1),
(119, 3),
(120, 1),
(120, 3),
(121, 1),
(121, 3),
(121, 4),
(122, 1),
(122, 3),
(122, 4),
(123, 1),
(123, 3),
(123, 4),
(124, 1),
(124, 3),
(124, 4),
(125, 1),
(126, 1),
(127, 1),
(128, 1),
(129, 1),
(130, 1),
(131, 1),
(132, 1),
(133, 1),
(133, 3),
(134, 1),
(134, 3),
(135, 1),
(135, 3),
(136, 1),
(136, 3),
(137, 1),
(137, 3),
(138, 1),
(138, 3),
(139, 1),
(139, 3),
(140, 1),
(140, 3),
(141, 1),
(141, 3),
(142, 1),
(142, 3),
(143, 1),
(143, 3),
(144, 1),
(144, 3),
(145, 1),
(145, 3),
(146, 1),
(146, 3),
(146, 4),
(147, 1),
(147, 3),
(147, 4),
(148, 1),
(148, 3),
(148, 4),
(149, 1),
(149, 3),
(149, 4),
(150, 1),
(150, 3),
(150, 4),
(151, 3),
(152, 3),
(153, 3),
(154, 3),
(155, 3),
(156, 3),
(157, 3),
(158, 3),
(159, 3),
(160, 3),
(161, 1),
(167, 1),
(167, 2),
(168, 1),
(169, 1),
(169, 2),
(170, 1),
(170, 2),
(171, 1),
(171, 2),
(172, 1),
(173, 1),
(174, 1),
(175, 1),
(176, 1),
(177, 1),
(178, 1),
(179, 1),
(179, 4),
(180, 1),
(180, 4),
(181, 1),
(181, 4),
(182, 1),
(184, 1),
(185, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `servicios`
--

CREATE TABLE `servicios` (
  `id_Servicio` int(11) NOT NULL,
  `Servicio` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Costos` decimal(10,2) DEFAULT NULL,
  `simbolo` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Especialidad_Medica_id` int(11) DEFAULT NULL,
  `Medico_id` int(11) DEFAULT NULL,
  `Status_id` int(11) DEFAULT NULL,
  `duracion` time DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `servicios`
--

INSERT INTO `servicios` (`id_Servicio`, `Servicio`, `Costos`, `simbolo`, `Especialidad_Medica_id`, `Medico_id`, `Status_id`, `duracion`) VALUES
(1, 'consulta', '5.00', 'USD', 1, 1, 1, '00:30:00'),
(2, 'eco pelvico', '10.00', 'USD', 1, 1, 1, '00:30:00'),
(3, 'citologia', '7.00', 'USD', 1, 1, 1, '00:15:00'),
(4, 'consulata psicologica', '10.00', 'USD', 2, 3, 1, '00:45:00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `servicios_adicionales`
--

CREATE TABLE `servicios_adicionales` (
  `id` int(11) NOT NULL,
  `Cita_Consulta_id` int(11) NOT NULL,
  `id_servicio` int(11) NOT NULL,
  `nota` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `servicios_adicionales`
--

INSERT INTO `servicios_adicionales` (`id`, `Cita_Consulta_id`, `id_servicio`, `nota`) VALUES
(1, 3, 1, NULL),
(2, 3, 1, NULL),
(3, 3, 1, NULL),
(4, 3, 1, NULL),
(5, 3, 1, NULL),
(6, 3, 1, NULL),
(7, 3, 1, NULL),
(8, 5, 3, NULL),
(9, 11, 1, NULL),
(13, 18, 1, NULL),
(14, 18, 3, NULL),
(15, 18, 2, NULL),
(16, 19, 3, NULL),
(17, 19, 1, NULL),
(18, 19, 2, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sexos`
--

CREATE TABLE `sexos` (
  `id_Sexo` int(11) NOT NULL,
  `Sexo` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `sexos`
--

INSERT INTO `sexos` (`id_Sexo`, `Sexo`) VALUES
(1, 'Femenino'),
(2, 'Masculino');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `status`
--

CREATE TABLE `status` (
  `id_Status` int(11) NOT NULL,
  `Status` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `color` varchar(20) COLLATE utf8_unicode_ci NOT NULL DEFAULT '#FFFFFF',
  `Nota` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `status`
--

INSERT INTO `status` (`id_Status`, `Status`, `color`, `Nota`) VALUES
(1, 'Activo', '#47eb81', NULL),
(2, 'Inactivo', '#e82c2c', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `status_consultas`
--

CREATE TABLE `status_consultas` (
  `id_Consulta` int(11) NOT NULL,
  `Consulta` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `color` varchar(20) COLLATE utf8_unicode_ci NOT NULL DEFAULT '#FFFFFF',
  `Nota` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `status_consultas`
--

INSERT INTO `status_consultas` (`id_Consulta`, `Consulta`, `color`, `Nota`) VALUES
(1, 'Activo', '#3ae965', NULL),
(2, 'Inactivo', '#fb2d2d', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `status_factura`
--

CREATE TABLE `status_factura` (
  `id_Status_Factura` int(11) NOT NULL,
  `Status_Factura` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `color` varchar(20) COLLATE utf8_unicode_ci NOT NULL DEFAULT '#FFFFFF',
  `Nota` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `status_factura`
--

INSERT INTO `status_factura` (`id_Status_Factura`, `Status_Factura`, `color`, `Nota`) VALUES
(1, 'Activo', '#47f069', NULL),
(2, 'Inactivo', '#ec2222', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `status_medicos`
--

CREATE TABLE `status_medicos` (
  `id_Status_Medico` int(11) NOT NULL,
  `Status_Medico` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `color` varchar(10) COLLATE utf8_unicode_ci NOT NULL DEFAULT '#FFFFFF',
  `Nota` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `status_medicos`
--

INSERT INTO `status_medicos` (`id_Status_Medico`, `Status_Medico`, `color`, `Nota`) VALUES
(1, 'Activo', '#3df061', NULL),
(2, 'Inactivo', '#eb1414', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `status_tasas`
--

CREATE TABLE `status_tasas` (
  `id_Status_Tasa` int(11) NOT NULL,
  `Tasa` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `color` varchar(20) COLLATE utf8_unicode_ci NOT NULL DEFAULT '#FFFFFF',
  `Nota` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `status_tasas`
--

INSERT INTO `status_tasas` (`id_Status_Tasa`, `Tasa`, `color`, `Nota`) VALUES
(1, 'Activo', '#53e93f', NULL),
(2, 'Inactivo', '#ec2222', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tasa_cambio`
--

CREATE TABLE `tasa_cambio` (
  `id_Tasa_Cambio` int(11) NOT NULL,
  `BS` decimal(10,2) DEFAULT NULL,
  `USD` decimal(10,2) DEFAULT NULL,
  `BitCoins` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Ethereum` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Fecha` date DEFAULT NULL,
  `Status_Tasa_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `tasa_cambio`
--

INSERT INTO `tasa_cambio` (`id_Tasa_Cambio`, `BS`, `USD`, `BitCoins`, `Ethereum`, `Fecha`, `Status_Tasa_id`) VALUES
(1, '4.62', '1.00', '0,000336823952', '0,000336823952', '2022-04-27', 2),
(2, '5.26', '1.00', '0.000078541', '0.000078541', '2022-05-19', 2),
(3, '5.28', '1.00', '0.000000045213', '0.000000045213', '2022-05-19', 2),
(4, '5.28', '1.00', '0.000000045213', '0.000000045213', '2022-05-19', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipos_cuentas`
--

CREATE TABLE `tipos_cuentas` (
  `id_Cuenta` int(11) NOT NULL,
  `descripcion` varchar(150) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `tipos_cuentas`
--

INSERT INTO `tipos_cuentas` (`id_Cuenta`, `descripcion`) VALUES
(1, 'Ahorro'),
(2, 'Corriente');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_pagos`
--

CREATE TABLE `tipo_pagos` (
  `id_Tipos_Pago` int(11) NOT NULL,
  `Tipo_Pago` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `tipo_pagos`
--

INSERT INTO `tipo_pagos` (`id_Tipos_Pago`, `Tipo_Pago`) VALUES
(1, 'Transferencia'),
(2, 'Efectivo');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `turnos`
--

CREATE TABLE `turnos` (
  `id_turno` int(11) NOT NULL,
  `nombre` varchar(150) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `turnos`
--

INSERT INTO `turnos` (`id_turno`, `nombre`) VALUES
(1, 'Mañana'),
(2, 'Tarde');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

CREATE TABLE `users` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email_verified_at` timestamp NULL DEFAULT NULL,
  `password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `remember_token` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` char(1) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '1',
  `id_usuario` int(11) DEFAULT 0,
  `id_usuarioA` int(11) DEFAULT NULL,
  `id_usuarioP` int(11) DEFAULT NULL,
  `id_usuarioG` int(11) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `email_verified_at`, `password`, `remember_token`, `status`, `id_usuario`, `id_usuarioA`, `id_usuarioP`, `id_usuarioG`, `created_at`, `updated_at`) VALUES
(1, 'Admin', 'admin@admin.com', NULL, '$2y$10$ttkSHl10aTrTbySWYrHGUeSWNgUP6aC/TNt/mJehGCKxc2HKoY5Qu', 'nKKHvaGexww59iPmUhIVxFMl9JFN7nx94r4bvoxBM0XZ38l0w99LM0IYcND2', '1', 0, NULL, NULL, NULL, '2022-03-29 23:55:24', '2022-03-29 23:55:24'),
(2, 'John Doe', 'johndoe@test.com', NULL, '$2y$10$cHi.dAkyqQ0Yd5k6Nh8mJu5AB3NA1buh2KTAvw.qmkF6Jt7cL8tSa', NULL, '1', 0, NULL, NULL, 1, '2022-03-30 13:53:02', '2022-03-30 13:53:02'),
(3, 'Usuario Medico', 'usuariom@test.com', NULL, '$2y$10$wWl9FZ47zlkvijOhhpwyK.rd2qx0p9fwbHl/1IjTrmxVhyzeNxI6u', 'kg8JIsvjW5VZYz3qAWLdIEut546Mys9qfe1hol43hz5ANklsXAObld2YMLgh', '1', 1, NULL, NULL, NULL, '2022-03-30 19:52:19', '2022-05-18 19:57:27'),
(6, 'Usuario test Paciente', 'usuariop@test.com', '2022-05-28 14:48:40', '$2y$10$X7wiz75ckHxJiJDxukAbC.zxee9QLfRZ5dhYIG..8dDBj32jfzNYu', 'xneqWOu6vJZlJf3yzX8scbNXLz9veJFXVxp8ngN3LX0Km28sIJpg9TYUzQjd', '1', 0, NULL, 1, NULL, '2022-03-30 21:01:31', '2022-04-19 20:49:26'),
(7, 'Elvira Terán', 'elvirateran58@gmail.com', '2022-05-28 14:48:40', '$2y$10$1TdvPfpOUyM7l1XfxpFBtu/9zI3nOYxaI321/p8ssJXC8VekOUmRq', NULL, '1', 2, NULL, NULL, NULL, '2022-04-07 14:45:34', '2022-05-28 14:48:40');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios_asistentes`
--

CREATE TABLE `usuarios_asistentes` (
  `id_asistente` int(11) NOT NULL,
  `Nombre_Asistente` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Prefijo_CIDNI_id` int(11) DEFAULT NULL,
  `Apellidos_Asistente` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `CIDNI` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Sexo_id` int(11) DEFAULT NULL,
  `Fecha_Nacimiento_Asistente` date DEFAULT NULL,
  `Status_id` int(11) DEFAULT 1,
  `Civil_id` int(11) DEFAULT NULL,
  `Pais_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `usuarios_asistentes`
--

INSERT INTO `usuarios_asistentes` (`id_asistente`, `Nombre_Asistente`, `Prefijo_CIDNI_id`, `Apellidos_Asistente`, `CIDNI`, `Sexo_id`, `Fecha_Nacimiento_Asistente`, `Status_id`, `Civil_id`, `Pais_id`) VALUES
(4, 'Usuario', 1, 'Asistente', '11555888', 1, '2004-03-09', 1, 1, 1),
(5, 'Test', 1, 'Test', '11444777', 1, '2004-05-18', 1, 2, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios_general`
--

CREATE TABLE `usuarios_general` (
  `id` int(11) NOT NULL,
  `nombre` varchar(150) COLLATE utf8_unicode_ci NOT NULL,
  `id_prefijo_dni` int(11) NOT NULL,
  `cedula` int(20) NOT NULL,
  `id_sexo` int(11) NOT NULL,
  `fecha_nac` date NOT NULL,
  `telefono` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `id_status` int(11) NOT NULL,
  `direccion` varchar(250) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `usuarios_general`
--

INSERT INTO `usuarios_general` (`id`, `nombre`, `id_prefijo_dni`, `cedula`, `id_sexo`, `fecha_nac`, `telefono`, `id_status`, `direccion`) VALUES
(1, 'John Doe', 1, 11222333, 2, '2004-03-30', '04245163222', 1, 'dirección de John Doe');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios_medicos`
--

CREATE TABLE `usuarios_medicos` (
  `id_Medico` int(11) NOT NULL,
  `Nombres_Medico` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Prefijo_CIDNI_id` int(11) DEFAULT NULL,
  `Foto_Medico` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Apellidos_Medicos` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `CIDNI` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Fecha_Nacimiento_Medico` date DEFAULT NULL,
  `Sexo_id` int(11) DEFAULT NULL,
  `Registro_MPPS` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Numero_Colegio_de_Medico` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Status_Medico_id` int(11) DEFAULT 1,
  `Civil_id` int(11) DEFAULT NULL,
  `Pais_id` int(11) DEFAULT NULL,
  `id_Estado` int(11) DEFAULT NULL,
  `id_Ciudad` int(11) DEFAULT NULL,
  `id_Municipio` int(11) DEFAULT NULL,
  `id_Parroquia` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `usuarios_medicos`
--

INSERT INTO `usuarios_medicos` (`id_Medico`, `Nombres_Medico`, `Prefijo_CIDNI_id`, `Foto_Medico`, `Apellidos_Medicos`, `CIDNI`, `Fecha_Nacimiento_Medico`, `Sexo_id`, `Registro_MPPS`, `Numero_Colegio_de_Medico`, `Status_Medico_id`, `Civil_id`, `Pais_id`, `id_Estado`, `id_Ciudad`, `id_Municipio`, `id_Parroquia`) VALUES
(1, 'Usuario', 1, 'medico\\medico_1_11444555.png', 'Medico', '11444555', '2004-03-03', 1, '123654789', '987456321', 1, 2, 1, 12, NULL, NULL, NULL),
(2, 'Elvira', 1, NULL, 'Terán', '18105604', '1986-05-08', 1, '123654789', '987456321', 1, 1, 1, 12, NULL, NULL, NULL),
(3, 'Usuario II', 1, NULL, 'Medico', '17504275', '2004-04-01', 1, '147896325', '123654789', 1, 1, 1, 12, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios_pacientes`
--

CREATE TABLE `usuarios_pacientes` (
  `id_Paciente` int(11) NOT NULL,
  `Nombres_Paciente` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Apellidos_Paciente` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Prefijo_CIDNI_id` int(11) DEFAULT NULL,
  `CIDNI` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Fecha_Nacimiento_Paciente` date DEFAULT NULL,
  `Sexo_id` int(11) DEFAULT NULL,
  `Status_id` int(11) DEFAULT 1,
  `Civil_id` int(11) DEFAULT NULL,
  `Pais_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `usuarios_pacientes`
--

INSERT INTO `usuarios_pacientes` (`id_Paciente`, `Nombres_Paciente`, `Apellidos_Paciente`, `Prefijo_CIDNI_id`, `CIDNI`, `Fecha_Nacimiento_Paciente`, `Sexo_id`, `Status_id`, `Civil_id`, `Pais_id`) VALUES
(1, 'Usuario test', 'Paciente', 1, '11999664', '2004-03-03', 2, 1, 1, 1);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `agendas`
--
ALTER TABLE `agendas`
  ADD PRIMARY KEY (`id_Agenda`),
  ADD KEY `Max_pacientes` (`Max_pacientes`),
  ADD KEY `Medico_id` (`Medico_id`),
  ADD KEY `Consultorio_id` (`Consultorio_id`),
  ADD KEY `Especialidad_Medica` (`Especialidad_Medica`),
  ADD KEY `Horario_Cita_id` (`Horario_Cita_id`),
  ADD KEY `Status_id` (`Status_id`),
  ADD KEY `Status_Medico_id` (`Status_Medico_id`);

--
-- Indices de la tabla `anamnesis`
--
ALTER TABLE `anamnesis`
  ADD PRIMARY KEY (`id_anamnesis`),
  ADD KEY `Medico_id` (`Medico_id`),
  ADD KEY `Paciente_Id` (`Paciente_Id`),
  ADD KEY `Control_Historia_Medico_id` (`Control_Historia_Medico_id`),
  ADD KEY `id_Status` (`id_Status`);

--
-- Indices de la tabla `antecedentes`
--
ALTER TABLE `antecedentes`
  ADD PRIMARY KEY (`id_antecedente`),
  ADD KEY `Control_Historia_Medico_id` (`Control_Historia_Medico_id`),
  ADD KEY `id_Status` (`id_Status`),
  ADD KEY `Medico_id` (`Medico_id`),
  ADD KEY `Paciente_Id` (`Paciente_Id`);

--
-- Indices de la tabla `bancos_bs`
--
ALTER TABLE `bancos_bs`
  ADD PRIMARY KEY (`id_Bancos_Bs`),
  ADD KEY `Status_Id` (`Status_Id`);

--
-- Indices de la tabla `billeteras_cripto`
--
ALTER TABLE `billeteras_cripto`
  ADD PRIMARY KEY (`id_Billetera_Cripto`),
  ADD KEY `Status_id` (`Status_id`),
  ADD KEY `Medicos_id` (`Medicos_id`),
  ADD KEY `Cripto_id` (`Cripto_id`);

--
-- Indices de la tabla `citas_consultas`
--
ALTER TABLE `citas_consultas`
  ADD PRIMARY KEY (`id_Cita_Consulta`),
  ADD KEY `Agenda_id` (`Agenda_id`),
  ADD KEY `Paciente_id` (`Paciente_id`),
  ADD KEY `Paciente_Especial_id` (`Paciente_Especial_id`),
  ADD KEY `Medico_id` (`Medico_id`),
  ADD KEY `Asistente_id` (`Asistente_id`),
  ADD KEY `Status_Consulta_id` (`Status_Consulta_id`),
  ADD KEY `citas_consultas_ibfk_7` (`id_servicio`);

--
-- Indices de la tabla `ciudades`
--
ALTER TABLE `ciudades`
  ADD PRIMARY KEY (`id_Ciudad`),
  ADD KEY `id_Estado` (`Estado_id`) USING BTREE;

--
-- Indices de la tabla `consultorios`
--
ALTER TABLE `consultorios`
  ADD PRIMARY KEY (`id_Consultorio`),
  ADD KEY `Especialidad_Medica_id` (`Especialidad_Medica_id`),
  ADD KEY `Ciudad_id` (`Ciudad_id`),
  ADD KEY `Estado_id` (`Estado_id`),
  ADD KEY `Municipio_id` (`Municipio_id`),
  ADD KEY `Parroquia_id` (`Parroquia_id`),
  ADD KEY `Status_id` (`Status_id`);

--
-- Indices de la tabla `control_especialidades`
--
ALTER TABLE `control_especialidades`
  ADD PRIMARY KEY (`id_Control_Especialidad`),
  ADD KEY `Medico_id` (`Medico_id`),
  ADD KEY `Especialidades_Medicas_id` (`Especialidades_Medicas_id`),
  ADD KEY `Status_Medico_id` (`Status_Medico_id`);

--
-- Indices de la tabla `control_historia_medicas`
--
ALTER TABLE `control_historia_medicas`
  ADD PRIMARY KEY (`id_Control_Historia_Medica`),
  ADD KEY `Especialidad_Medica_id` (`Especialidad_Medica_id`),
  ADD KEY `Control_Especialidad_id` (`Control_Especialidad_id`),
  ADD KEY `Medico_id` (`Medico_id`),
  ADD KEY `Paciente_id` (`Paciente_id`),
  ADD KEY `Paciente_Especial_id` (`Paciente_Especial_id`),
  ADD KEY `Cita_Consulta_id` (`Cita_Consulta_id`),
  ADD KEY `control_historia_medicas_ibfk_7` (`id_servicio`);

--
-- Indices de la tabla `criptos`
--
ALTER TABLE `criptos`
  ADD PRIMARY KEY (`id_Cripto`),
  ADD KEY `Status_id` (`Status_id`);

--
-- Indices de la tabla `cuenta_bancaria_bs`
--
ALTER TABLE `cuenta_bancaria_bs`
  ADD PRIMARY KEY (`id_Cuenta_Bancaria_BS`),
  ADD KEY `Banco_id` (`Banco_id`),
  ADD KEY `Medico_id` (`Medico_id`),
  ADD KEY `Status_id` (`Status_id`),
  ADD KEY `Tipo` (`Tipo`) USING BTREE;

--
-- Indices de la tabla `cuenta_usd`
--
ALTER TABLE `cuenta_usd`
  ADD PRIMARY KEY (`id_Cuenta_USD`),
  ADD KEY `Entidad_USD_id` (`Entidad_USD_id`),
  ADD KEY `Medico_id` (`Medico_id`),
  ADD KEY `cuenta_usd_ibfk_5` (`Status_Pago`),
  ADD KEY `Tipo` (`Tipo`) USING BTREE;

--
-- Indices de la tabla `datos_seniat`
--
ALTER TABLE `datos_seniat`
  ADD PRIMARY KEY (`id_Datos_SENIAT`),
  ADD KEY `Medico_id` (`Medico_id`);

--
-- Indices de la tabla `direcciones_pacientes`
--
ALTER TABLE `direcciones_pacientes`
  ADD PRIMARY KEY (`id_Direccion_Paciente`),
  ADD UNIQUE KEY `Paciente_id_2` (`Paciente_id`),
  ADD KEY `Paciente_id` (`Paciente_id`),
  ADD KEY `Cuidad_id` (`Cuidad_id`),
  ADD KEY `Estado_id` (`Estado_id`),
  ADD KEY `Municipio_id` (`Municipio_id`),
  ADD KEY `Parroquia_id` (`Parroquia_id`);

--
-- Indices de la tabla `entidades_usd`
--
ALTER TABLE `entidades_usd`
  ADD PRIMARY KEY (`id_Entidad_USD`),
  ADD KEY `Status_id` (`Status_id`);

--
-- Indices de la tabla `especialidades_medicas`
--
ALTER TABLE `especialidades_medicas`
  ADD PRIMARY KEY (`id_Especialidad_Medica`);

--
-- Indices de la tabla `estados`
--
ALTER TABLE `estados`
  ADD PRIMARY KEY (`id_Estado`);

--
-- Indices de la tabla `estados_civiles`
--
ALTER TABLE `estados_civiles`
  ADD PRIMARY KEY (`id_Civil`);

--
-- Indices de la tabla `facturas`
--
ALTER TABLE `facturas`
  ADD PRIMARY KEY (`id_Factura`),
  ADD KEY `Cita_Consulta_id` (`Cita_Consulta_id`),
  ADD KEY `Datos_SENIAT_id` (`Datos_SENIAT_id`),
  ADD KEY `Pacientes_id` (`Pacientes_id`),
  ADD KEY `Status_Factura_id` (`Status_Factura_id`),
  ADD KEY `Medico_id` (`Medico_id`),
  ADD KEY `Asistente_id` (`Asistente_id`);

--
-- Indices de la tabla `factura_detalle`
--
ALTER TABLE `factura_detalle`
  ADD PRIMARY KEY (`id_Factura_Detalle`),
  ADD KEY `Factura_id` (`Factura_id`),
  ADD KEY `Servicio_id` (`Servicio_id`),
  ADD KEY `Status_Factura_id` (`Status_Factura_id`);

--
-- Indices de la tabla `factura_total_bs`
--
ALTER TABLE `factura_total_bs`
  ADD PRIMARY KEY (`id_Factura_BS`),
  ADD KEY `Factura_Id` (`Factura_Id`),
  ADD KEY `Status_Tasa_id` (`Status_Tasa_id`),
  ADD KEY `Cuenta_Bancaria_BS_id` (`Cuenta_Bancaria_BS_id`),
  ADD KEY `Tipo_Pago_id` (`Tipo_Pago_id`),
  ADD KEY `factura_total_bs_ibfk_5` (`banco_emisor`);

--
-- Indices de la tabla `factura_total_cripto`
--
ALTER TABLE `factura_total_cripto`
  ADD PRIMARY KEY (`Id_Factura_Cripto`),
  ADD KEY `Factura_id` (`Factura_id`),
  ADD KEY `Status_Tasa_id` (`Status_Tasa_id`),
  ADD KEY `Billetera_Cripto_id` (`Billetera_Cripto_id`),
  ADD KEY `Tipo_Pago_id` (`Tipo_Pago_id`),
  ADD KEY `factura_total_cripto_ibfk_5` (`billetera_emisora`);

--
-- Indices de la tabla `factura_total_usd`
--
ALTER TABLE `factura_total_usd`
  ADD PRIMARY KEY (`id_Factura_USD`),
  ADD KEY `Factura_id` (`Factura_id`),
  ADD KEY `Status_Tasa_id` (`Status_Tasa_id`),
  ADD KEY `Cuenta_USD_id` (`Cuenta_USD_id`),
  ADD KEY `Tipo_Pago_id` (`Tipo_Pago_id`),
  ADD KEY `factura_total_usd_ibfk_5` (`entidad_emisora`);

--
-- Indices de la tabla `historico_login_pacientes`
--
ALTER TABLE `historico_login_pacientes`
  ADD PRIMARY KEY (`id_Login_Pacientes`),
  ADD KEY `Login_Pacientes_id` (`Login_Pacientes_id`);

--
-- Indices de la tabla `historico_login_trabajadores`
--
ALTER TABLE `historico_login_trabajadores`
  ADD PRIMARY KEY (`id_Login_Trabajadores`),
  ADD KEY `Login_Tranajador_id` (`Login_Tranajador_id`),
  ADD KEY `Medico_id` (`Medico_id`),
  ADD KEY `Asistente_id` (`Asistente_id`);

--
-- Indices de la tabla `historico_pediatria`
--
ALTER TABLE `historico_pediatria`
  ADD PRIMARY KEY (`id_Historico_Pediatria`),
  ADD KEY `Paciente_id` (`Paciente_id`),
  ADD KEY `Medico_id` (`Medico_id`),
  ADD KEY `Paciente_pediatrico_Id` (`Paciente_pediatrico_Id`),
  ADD KEY `Cita_Consulta_id` (`Cita_Consulta_id`),
  ADD KEY `Pediatria_id` (`Pediatria_id`);

--
-- Indices de la tabla `horarios_citas`
--
ALTER TABLE `horarios_citas`
  ADD PRIMARY KEY (`id_Horario_Cita`),
  ADD KEY `horarios_ibfk_1` (`Medico_id`),
  ADD KEY `horarios_ibfk_2` (`Especialidad_id`),
  ADD KEY `horarios_ibfk_3` (`turno_id`);

--
-- Indices de la tabla `limite_usuarios`
--
ALTER TABLE `limite_usuarios`
  ADD PRIMARY KEY (`id`),
  ADD KEY `limites_ibfk_1` (`status`);

--
-- Indices de la tabla `login_pacientes`
--
ALTER TABLE `login_pacientes`
  ADD PRIMARY KEY (`id_login_Pacientes`),
  ADD KEY `Paciente_id` (`Paciente_id`),
  ADD KEY `Status_id` (`Status_id`);

--
-- Indices de la tabla `login_trabajadores`
--
ALTER TABLE `login_trabajadores`
  ADD PRIMARY KEY (`id_Login_Trabajador`),
  ADD UNIQUE KEY `Medico_id` (`Medico_id`),
  ADD KEY `Status_Medico_id` (`Status_Medico_id`),
  ADD KEY `Asistente_id` (`Asistente_id`),
  ADD KEY `login_trabajadores_ibfk_4` (`general_id`);

--
-- Indices de la tabla `medicoxasistente`
--
ALTER TABLE `medicoxasistente`
  ADD PRIMARY KEY (`id`),
  ADD KEY `medicoxasistente_ibfk_1` (`id_Medico`),
  ADD KEY `medicoxasistente_ibfk_2` (`id_Asistente`);

--
-- Indices de la tabla `meetings`
--
ALTER TABLE `meetings`
  ADD PRIMARY KEY (`id`),
  ADD KEY `meetings_scheduler_type_scheduler_id_index` (`scheduler_type`,`scheduler_id`),
  ADD KEY `meetings_presenter_type_presenter_id_index` (`presenter_type`,`presenter_id`),
  ADD KEY `meetings_host_type_host_id_index` (`host_type`,`host_id`);

--
-- Indices de la tabla `meeting_participants`
--
ALTER TABLE `meeting_participants`
  ADD PRIMARY KEY (`participant_id`,`participant_type`,`meeting_id`),
  ADD KEY `meeting_participants_participant_type_participant_id_index` (`participant_type`,`participant_id`),
  ADD KEY `meeting_participants_meeting_id_foreign` (`meeting_id`);

--
-- Indices de la tabla `meeting_rooms`
--
ALTER TABLE `meeting_rooms`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `meta_attributes`
--
ALTER TABLE `meta_attributes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `meta_attributes_model_type_model_id_index` (`model_type`,`model_id`);

--
-- Indices de la tabla `migrations`
--
ALTER TABLE `migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `model_has_permissions`
--
ALTER TABLE `model_has_permissions`
  ADD PRIMARY KEY (`permission_id`,`model_id`,`model_type`),
  ADD KEY `model_has_permissions_model_id_model_type_index` (`model_id`,`model_type`);

--
-- Indices de la tabla `model_has_roles`
--
ALTER TABLE `model_has_roles`
  ADD PRIMARY KEY (`role_id`,`model_id`,`model_type`),
  ADD KEY `model_has_roles_model_id_model_type_index` (`model_id`,`model_type`);

--
-- Indices de la tabla `municipios`
--
ALTER TABLE `municipios`
  ADD PRIMARY KEY (`id_Municipio`),
  ADD KEY `Estado_id` (`Estado_id`);

--
-- Indices de la tabla `pacientes_especiales`
--
ALTER TABLE `pacientes_especiales`
  ADD PRIMARY KEY (`id_Pacientes_Especiales`),
  ADD KEY `Paciente_id` (`Paciente_id`),
  ADD KEY `Sexo_id` (`Sexo_id`),
  ADD KEY `Prefijo_CIDNI_id` (`Prefijo_CIDNI_id`),
  ADD KEY `Status_id` (`Status_id`),
  ADD KEY `Civil_id` (`Civil_id`),
  ADD KEY `Pais_id` (`Pais_id`);

--
-- Indices de la tabla `pagos_confirmar`
--
ALTER TABLE `pagos_confirmar`
  ADD PRIMARY KEY (`id_pago`);

--
-- Indices de la tabla `paises`
--
ALTER TABLE `paises`
  ADD PRIMARY KEY (`id_Pais`);

--
-- Indices de la tabla `parroquias`
--
ALTER TABLE `parroquias`
  ADD PRIMARY KEY (`id_Parroquia`),
  ADD KEY `Municipio_id` (`Municipio_id`);

--
-- Indices de la tabla `password_resets`
--
ALTER TABLE `password_resets`
  ADD KEY `password_resets_email_index` (`email`);

--
-- Indices de la tabla `pediatria`
--
ALTER TABLE `pediatria`
  ADD PRIMARY KEY (`id_Pediatria`),
  ADD KEY `Paciente_Id` (`Paciente_Id`),
  ADD KEY `Paciente_Infantil_id` (`Paciente_Infantil_id`),
  ADD KEY `Medico_id` (`Medico_id`),
  ADD KEY `Control_Historia_Medico_id` (`Control_Historia_Medico_id`);

--
-- Indices de la tabla `permissions`
--
ALTER TABLE `permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `permissions_name_guard_name_unique` (`name`,`guard_name`);

--
-- Indices de la tabla `prefijos_cidni`
--
ALTER TABLE `prefijos_cidni`
  ADD PRIMARY KEY (`id_Prefijo_CIDNI`);

--
-- Indices de la tabla `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `roles_name_guard_name_unique` (`name`,`guard_name`);

--
-- Indices de la tabla `role_has_permissions`
--
ALTER TABLE `role_has_permissions`
  ADD PRIMARY KEY (`permission_id`,`role_id`),
  ADD KEY `role_has_permissions_role_id_foreign` (`role_id`);

--
-- Indices de la tabla `servicios`
--
ALTER TABLE `servicios`
  ADD PRIMARY KEY (`id_Servicio`),
  ADD KEY `Especialidad_Medica_id` (`Especialidad_Medica_id`),
  ADD KEY `Medico_id` (`Medico_id`),
  ADD KEY `Status_id` (`Status_id`);

--
-- Indices de la tabla `servicios_adicionales`
--
ALTER TABLE `servicios_adicionales`
  ADD PRIMARY KEY (`id`),
  ADD KEY `servicioa_ibfk_2` (`id_servicio`),
  ADD KEY `servicioa_ibfk_1` (`Cita_Consulta_id`);

--
-- Indices de la tabla `sexos`
--
ALTER TABLE `sexos`
  ADD PRIMARY KEY (`id_Sexo`);

--
-- Indices de la tabla `status`
--
ALTER TABLE `status`
  ADD PRIMARY KEY (`id_Status`);

--
-- Indices de la tabla `status_consultas`
--
ALTER TABLE `status_consultas`
  ADD PRIMARY KEY (`id_Consulta`);

--
-- Indices de la tabla `status_factura`
--
ALTER TABLE `status_factura`
  ADD PRIMARY KEY (`id_Status_Factura`);

--
-- Indices de la tabla `status_medicos`
--
ALTER TABLE `status_medicos`
  ADD PRIMARY KEY (`id_Status_Medico`);

--
-- Indices de la tabla `status_tasas`
--
ALTER TABLE `status_tasas`
  ADD PRIMARY KEY (`id_Status_Tasa`);

--
-- Indices de la tabla `tasa_cambio`
--
ALTER TABLE `tasa_cambio`
  ADD PRIMARY KEY (`id_Tasa_Cambio`),
  ADD KEY `Status_Tasa_id` (`Status_Tasa_id`);

--
-- Indices de la tabla `tipos_cuentas`
--
ALTER TABLE `tipos_cuentas`
  ADD PRIMARY KEY (`id_Cuenta`);

--
-- Indices de la tabla `tipo_pagos`
--
ALTER TABLE `tipo_pagos`
  ADD PRIMARY KEY (`id_Tipos_Pago`);

--
-- Indices de la tabla `turnos`
--
ALTER TABLE `turnos`
  ADD PRIMARY KEY (`id_turno`);

--
-- Indices de la tabla `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indices de la tabla `usuarios_asistentes`
--
ALTER TABLE `usuarios_asistentes`
  ADD PRIMARY KEY (`id_asistente`),
  ADD KEY `Prefijo_CIDNI_id` (`Prefijo_CIDNI_id`),
  ADD KEY `Sexo_id` (`Sexo_id`),
  ADD KEY `Status_id` (`Status_id`),
  ADD KEY `Civil_id` (`Civil_id`),
  ADD KEY `Pais_id` (`Pais_id`);

--
-- Indices de la tabla `usuarios_general`
--
ALTER TABLE `usuarios_general`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `cedula` (`cedula`),
  ADD KEY `usuarios_general_ibfk_1` (`id_sexo`),
  ADD KEY `usuarios_general_ibfk_2` (`id_status`),
  ADD KEY `usuarios_general_ibfk_3` (`id_prefijo_dni`);

--
-- Indices de la tabla `usuarios_medicos`
--
ALTER TABLE `usuarios_medicos`
  ADD PRIMARY KEY (`id_Medico`),
  ADD KEY `Prefijo_CIDNI_id` (`Prefijo_CIDNI_id`),
  ADD KEY `Sexo_id` (`Sexo_id`),
  ADD KEY `Status_Medico_id` (`Status_Medico_id`),
  ADD KEY `Civil_id` (`Civil_id`),
  ADD KEY `Pais_id` (`Pais_id`),
  ADD KEY `usuarios_medicos_ibfk_6` (`id_Estado`),
  ADD KEY `usuarios_medicos_ibfk_7` (`id_Ciudad`),
  ADD KEY `usuarios_medicos_ibfk_8` (`id_Parroquia`),
  ADD KEY `usuarios_medicos_ibfk_9` (`id_Municipio`);

--
-- Indices de la tabla `usuarios_pacientes`
--
ALTER TABLE `usuarios_pacientes`
  ADD PRIMARY KEY (`id_Paciente`),
  ADD KEY `Prefijo_CIDNI_id` (`Prefijo_CIDNI_id`),
  ADD KEY `Sexo_id` (`Sexo_id`),
  ADD KEY `Status_id` (`Status_id`),
  ADD KEY `Civil_id` (`Civil_id`),
  ADD KEY `Pais_id` (`Pais_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `agendas`
--
ALTER TABLE `agendas`
  MODIFY `id_Agenda` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `anamnesis`
--
ALTER TABLE `anamnesis`
  MODIFY `id_anamnesis` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `antecedentes`
--
ALTER TABLE `antecedentes`
  MODIFY `id_antecedente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `bancos_bs`
--
ALTER TABLE `bancos_bs`
  MODIFY `id_Bancos_Bs` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT de la tabla `billeteras_cripto`
--
ALTER TABLE `billeteras_cripto`
  MODIFY `id_Billetera_Cripto` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `citas_consultas`
--
ALTER TABLE `citas_consultas`
  MODIFY `id_Cita_Consulta` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT de la tabla `ciudades`
--
ALTER TABLE `ciudades`
  MODIFY `id_Ciudad` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=523;

--
-- AUTO_INCREMENT de la tabla `consultorios`
--
ALTER TABLE `consultorios`
  MODIFY `id_Consultorio` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `control_especialidades`
--
ALTER TABLE `control_especialidades`
  MODIFY `id_Control_Especialidad` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `control_historia_medicas`
--
ALTER TABLE `control_historia_medicas`
  MODIFY `id_Control_Historia_Medica` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT de la tabla `criptos`
--
ALTER TABLE `criptos`
  MODIFY `id_Cripto` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `cuenta_bancaria_bs`
--
ALTER TABLE `cuenta_bancaria_bs`
  MODIFY `id_Cuenta_Bancaria_BS` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `cuenta_usd`
--
ALTER TABLE `cuenta_usd`
  MODIFY `id_Cuenta_USD` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `datos_seniat`
--
ALTER TABLE `datos_seniat`
  MODIFY `id_Datos_SENIAT` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `direcciones_pacientes`
--
ALTER TABLE `direcciones_pacientes`
  MODIFY `id_Direccion_Paciente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `entidades_usd`
--
ALTER TABLE `entidades_usd`
  MODIFY `id_Entidad_USD` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `especialidades_medicas`
--
ALTER TABLE `especialidades_medicas`
  MODIFY `id_Especialidad_Medica` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `estados`
--
ALTER TABLE `estados`
  MODIFY `id_Estado` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT de la tabla `estados_civiles`
--
ALTER TABLE `estados_civiles`
  MODIFY `id_Civil` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `facturas`
--
ALTER TABLE `facturas`
  MODIFY `id_Factura` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT de la tabla `factura_detalle`
--
ALTER TABLE `factura_detalle`
  MODIFY `id_Factura_Detalle` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=45;

--
-- AUTO_INCREMENT de la tabla `factura_total_bs`
--
ALTER TABLE `factura_total_bs`
  MODIFY `id_Factura_BS` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `factura_total_usd`
--
ALTER TABLE `factura_total_usd`
  MODIFY `id_Factura_USD` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `historico_login_pacientes`
--
ALTER TABLE `historico_login_pacientes`
  MODIFY `id_Login_Pacientes` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `historico_login_trabajadores`
--
ALTER TABLE `historico_login_trabajadores`
  MODIFY `id_Login_Trabajadores` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `historico_pediatria`
--
ALTER TABLE `historico_pediatria`
  MODIFY `id_Historico_Pediatria` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `horarios_citas`
--
ALTER TABLE `horarios_citas`
  MODIFY `id_Horario_Cita` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `limite_usuarios`
--
ALTER TABLE `limite_usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `login_pacientes`
--
ALTER TABLE `login_pacientes`
  MODIFY `id_login_Pacientes` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `login_trabajadores`
--
ALTER TABLE `login_trabajadores`
  MODIFY `id_Login_Trabajador` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `medicoxasistente`
--
ALTER TABLE `medicoxasistente`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `meetings`
--
ALTER TABLE `meetings`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `meeting_rooms`
--
ALTER TABLE `meeting_rooms`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `meta_attributes`
--
ALTER TABLE `meta_attributes`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `migrations`
--
ALTER TABLE `migrations`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `municipios`
--
ALTER TABLE `municipios`
  MODIFY `id_Municipio` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=463;

--
-- AUTO_INCREMENT de la tabla `pacientes_especiales`
--
ALTER TABLE `pacientes_especiales`
  MODIFY `id_Pacientes_Especiales` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `pagos_confirmar`
--
ALTER TABLE `pagos_confirmar`
  MODIFY `id_pago` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT de la tabla `paises`
--
ALTER TABLE `paises`
  MODIFY `id_Pais` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `parroquias`
--
ALTER TABLE `parroquias`
  MODIFY `id_Parroquia` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1139;

--
-- AUTO_INCREMENT de la tabla `pediatria`
--
ALTER TABLE `pediatria`
  MODIFY `id_Pediatria` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `permissions`
--
ALTER TABLE `permissions`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=189;

--
-- AUTO_INCREMENT de la tabla `prefijos_cidni`
--
ALTER TABLE `prefijos_cidni`
  MODIFY `id_Prefijo_CIDNI` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `roles`
--
ALTER TABLE `roles`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `servicios`
--
ALTER TABLE `servicios`
  MODIFY `id_Servicio` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `servicios_adicionales`
--
ALTER TABLE `servicios_adicionales`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT de la tabla `sexos`
--
ALTER TABLE `sexos`
  MODIFY `id_Sexo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `status`
--
ALTER TABLE `status`
  MODIFY `id_Status` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `status_consultas`
--
ALTER TABLE `status_consultas`
  MODIFY `id_Consulta` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `status_factura`
--
ALTER TABLE `status_factura`
  MODIFY `id_Status_Factura` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `status_medicos`
--
ALTER TABLE `status_medicos`
  MODIFY `id_Status_Medico` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `status_tasas`
--
ALTER TABLE `status_tasas`
  MODIFY `id_Status_Tasa` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `tasa_cambio`
--
ALTER TABLE `tasa_cambio`
  MODIFY `id_Tasa_Cambio` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `tipos_cuentas`
--
ALTER TABLE `tipos_cuentas`
  MODIFY `id_Cuenta` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `tipo_pagos`
--
ALTER TABLE `tipo_pagos`
  MODIFY `id_Tipos_Pago` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `turnos`
--
ALTER TABLE `turnos`
  MODIFY `id_turno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `users`
--
ALTER TABLE `users`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `usuarios_asistentes`
--
ALTER TABLE `usuarios_asistentes`
  MODIFY `id_asistente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `usuarios_general`
--
ALTER TABLE `usuarios_general`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `usuarios_medicos`
--
ALTER TABLE `usuarios_medicos`
  MODIFY `id_Medico` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `usuarios_pacientes`
--
ALTER TABLE `usuarios_pacientes`
  MODIFY `id_Paciente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `agendas`
--
ALTER TABLE `agendas`
  ADD CONSTRAINT `agendas_ibfk_1` FOREIGN KEY (`Medico_id`) REFERENCES `usuarios_medicos` (`id_Medico`),
  ADD CONSTRAINT `agendas_ibfk_2` FOREIGN KEY (`Consultorio_id`) REFERENCES `consultorios` (`id_Consultorio`),
  ADD CONSTRAINT `agendas_ibfk_3` FOREIGN KEY (`Especialidad_Medica`) REFERENCES `especialidades_medicas` (`id_Especialidad_Medica`),
  ADD CONSTRAINT `agendas_ibfk_4` FOREIGN KEY (`Horario_Cita_id`) REFERENCES `horarios_citas` (`id_Horario_Cita`),
  ADD CONSTRAINT `agendas_ibfk_5` FOREIGN KEY (`Status_id`) REFERENCES `status` (`id_Status`),
  ADD CONSTRAINT `agendas_ibfk_6` FOREIGN KEY (`Status_Medico_id`) REFERENCES `status_medicos` (`id_Status_Medico`);

--
-- Filtros para la tabla `anamnesis`
--
ALTER TABLE `anamnesis`
  ADD CONSTRAINT `anamnesis_ibfk_1` FOREIGN KEY (`Medico_id`) REFERENCES `usuarios_medicos` (`id_Medico`),
  ADD CONSTRAINT `anamnesis_ibfk_2` FOREIGN KEY (`Paciente_Id`) REFERENCES `usuarios_pacientes` (`id_Paciente`),
  ADD CONSTRAINT `anamnesis_ibfk_3` FOREIGN KEY (`Control_Historia_Medico_id`) REFERENCES `control_historia_medicas` (`id_Control_Historia_Medica`),
  ADD CONSTRAINT `anamnesis_ibfk_4` FOREIGN KEY (`id_Status`) REFERENCES `status` (`id_Status`);

--
-- Filtros para la tabla `antecedentes`
--
ALTER TABLE `antecedentes`
  ADD CONSTRAINT `antecedentes_ibfk_1` FOREIGN KEY (`Control_Historia_Medico_id`) REFERENCES `control_historia_medicas` (`id_Control_Historia_Medica`),
  ADD CONSTRAINT `antecedentes_ibfk_2` FOREIGN KEY (`id_Status`) REFERENCES `status` (`id_Status`),
  ADD CONSTRAINT `antecedentes_ibfk_3` FOREIGN KEY (`Medico_id`) REFERENCES `usuarios_medicos` (`id_Medico`),
  ADD CONSTRAINT `antecedentes_ibfk_4` FOREIGN KEY (`Paciente_Id`) REFERENCES `usuarios_pacientes` (`id_Paciente`);

--
-- Filtros para la tabla `bancos_bs`
--
ALTER TABLE `bancos_bs`
  ADD CONSTRAINT `bancos_bs_ibfk_1` FOREIGN KEY (`Status_Id`) REFERENCES `status` (`id_Status`);

--
-- Filtros para la tabla `billeteras_cripto`
--
ALTER TABLE `billeteras_cripto`
  ADD CONSTRAINT `billeteras_cripto_ibfk_1` FOREIGN KEY (`Status_id`) REFERENCES `status` (`id_Status`),
  ADD CONSTRAINT `billeteras_cripto_ibfk_2` FOREIGN KEY (`Medicos_id`) REFERENCES `usuarios_medicos` (`id_Medico`),
  ADD CONSTRAINT `billeteras_cripto_ibfk_3` FOREIGN KEY (`Cripto_id`) REFERENCES `criptos` (`id_Cripto`);

--
-- Filtros para la tabla `citas_consultas`
--
ALTER TABLE `citas_consultas`
  ADD CONSTRAINT `citas_consultas_ibfk_1` FOREIGN KEY (`Agenda_id`) REFERENCES `agendas` (`id_Agenda`),
  ADD CONSTRAINT `citas_consultas_ibfk_2` FOREIGN KEY (`Paciente_id`) REFERENCES `usuarios_pacientes` (`id_Paciente`),
  ADD CONSTRAINT `citas_consultas_ibfk_3` FOREIGN KEY (`Paciente_Especial_id`) REFERENCES `pacientes_especiales` (`id_Pacientes_Especiales`),
  ADD CONSTRAINT `citas_consultas_ibfk_4` FOREIGN KEY (`Medico_id`) REFERENCES `usuarios_medicos` (`id_Medico`),
  ADD CONSTRAINT `citas_consultas_ibfk_5` FOREIGN KEY (`Asistente_id`) REFERENCES `usuarios_asistentes` (`id_asistente`),
  ADD CONSTRAINT `citas_consultas_ibfk_6` FOREIGN KEY (`Status_Consulta_id`) REFERENCES `status_consultas` (`id_Consulta`),
  ADD CONSTRAINT `citas_consultas_ibfk_7` FOREIGN KEY (`id_servicio`) REFERENCES `servicios` (`id_Servicio`);

--
-- Filtros para la tabla `ciudades`
--
ALTER TABLE `ciudades`
  ADD CONSTRAINT `ciudades_ibfk_1` FOREIGN KEY (`Estado_id`) REFERENCES `estados` (`id_Estado`);

--
-- Filtros para la tabla `consultorios`
--
ALTER TABLE `consultorios`
  ADD CONSTRAINT `consultorios_ibfk_1` FOREIGN KEY (`Especialidad_Medica_id`) REFERENCES `especialidades_medicas` (`id_Especialidad_Medica`),
  ADD CONSTRAINT `consultorios_ibfk_2` FOREIGN KEY (`Ciudad_id`) REFERENCES `ciudades` (`id_Ciudad`),
  ADD CONSTRAINT `consultorios_ibfk_3` FOREIGN KEY (`Estado_id`) REFERENCES `estados` (`id_Estado`),
  ADD CONSTRAINT `consultorios_ibfk_4` FOREIGN KEY (`Municipio_id`) REFERENCES `municipios` (`id_Municipio`),
  ADD CONSTRAINT `consultorios_ibfk_5` FOREIGN KEY (`Parroquia_id`) REFERENCES `parroquias` (`id_Parroquia`),
  ADD CONSTRAINT `consultorios_ibfk_6` FOREIGN KEY (`Status_id`) REFERENCES `status` (`id_Status`);

--
-- Filtros para la tabla `control_especialidades`
--
ALTER TABLE `control_especialidades`
  ADD CONSTRAINT `control_especialidades_ibfk_1` FOREIGN KEY (`Medico_id`) REFERENCES `usuarios_medicos` (`id_Medico`),
  ADD CONSTRAINT `control_especialidades_ibfk_2` FOREIGN KEY (`Especialidades_Medicas_id`) REFERENCES `especialidades_medicas` (`id_Especialidad_Medica`),
  ADD CONSTRAINT `control_especialidades_ibfk_3` FOREIGN KEY (`Status_Medico_id`) REFERENCES `status_medicos` (`id_Status_Medico`);

--
-- Filtros para la tabla `control_historia_medicas`
--
ALTER TABLE `control_historia_medicas`
  ADD CONSTRAINT `control_historia_medicas_ibfk_1` FOREIGN KEY (`Especialidad_Medica_id`) REFERENCES `especialidades_medicas` (`id_Especialidad_Medica`),
  ADD CONSTRAINT `control_historia_medicas_ibfk_2` FOREIGN KEY (`Control_Especialidad_id`) REFERENCES `control_especialidades` (`id_Control_Especialidad`),
  ADD CONSTRAINT `control_historia_medicas_ibfk_3` FOREIGN KEY (`Medico_id`) REFERENCES `usuarios_medicos` (`id_Medico`),
  ADD CONSTRAINT `control_historia_medicas_ibfk_4` FOREIGN KEY (`Paciente_id`) REFERENCES `usuarios_pacientes` (`id_Paciente`),
  ADD CONSTRAINT `control_historia_medicas_ibfk_5` FOREIGN KEY (`Paciente_Especial_id`) REFERENCES `pacientes_especiales` (`id_Pacientes_Especiales`),
  ADD CONSTRAINT `control_historia_medicas_ibfk_6` FOREIGN KEY (`Cita_Consulta_id`) REFERENCES `citas_consultas` (`id_Cita_Consulta`),
  ADD CONSTRAINT `control_historia_medicas_ibfk_7` FOREIGN KEY (`id_servicio`) REFERENCES `servicios` (`id_Servicio`);

--
-- Filtros para la tabla `criptos`
--
ALTER TABLE `criptos`
  ADD CONSTRAINT `criptos_ibfk_1` FOREIGN KEY (`Status_id`) REFERENCES `status` (`id_Status`);

--
-- Filtros para la tabla `cuenta_bancaria_bs`
--
ALTER TABLE `cuenta_bancaria_bs`
  ADD CONSTRAINT `cuenta_bancaria_bs_ibfk_1` FOREIGN KEY (`Banco_id`) REFERENCES `bancos_bs` (`id_Bancos_Bs`),
  ADD CONSTRAINT `cuenta_bancaria_bs_ibfk_2` FOREIGN KEY (`Medico_id`) REFERENCES `usuarios_medicos` (`id_Medico`),
  ADD CONSTRAINT `cuenta_bancaria_bs_ibfk_3` FOREIGN KEY (`Status_id`) REFERENCES `status` (`id_Status`),
  ADD CONSTRAINT `cuenta_bancaria_bs_ibfk_4` FOREIGN KEY (`Tipo`) REFERENCES `tipos_cuentas` (`id_Cuenta`);

--
-- Filtros para la tabla `cuenta_usd`
--
ALTER TABLE `cuenta_usd`
  ADD CONSTRAINT `cuenta_usd_ibfk_1` FOREIGN KEY (`Entidad_USD_id`) REFERENCES `entidades_usd` (`id_Entidad_USD`),
  ADD CONSTRAINT `cuenta_usd_ibfk_2` FOREIGN KEY (`Medico_id`) REFERENCES `usuarios_medicos` (`id_Medico`),
  ADD CONSTRAINT `cuenta_usd_ibfk_3` FOREIGN KEY (`Medico_id`) REFERENCES `usuarios_medicos` (`id_Medico`),
  ADD CONSTRAINT `cuenta_usd_ibfk_4` FOREIGN KEY (`Tipo`) REFERENCES `tipos_cuentas` (`id_Cuenta`),
  ADD CONSTRAINT `cuenta_usd_ibfk_5` FOREIGN KEY (`Status_Pago`) REFERENCES `status` (`id_Status`);

--
-- Filtros para la tabla `datos_seniat`
--
ALTER TABLE `datos_seniat`
  ADD CONSTRAINT `datos_seniat_ibfk_1` FOREIGN KEY (`Medico_id`) REFERENCES `usuarios_medicos` (`id_Medico`);

--
-- Filtros para la tabla `direcciones_pacientes`
--
ALTER TABLE `direcciones_pacientes`
  ADD CONSTRAINT `direcciones_pacientes_ibfk_1` FOREIGN KEY (`Paciente_id`) REFERENCES `usuarios_pacientes` (`id_Paciente`),
  ADD CONSTRAINT `direcciones_pacientes_ibfk_2` FOREIGN KEY (`Cuidad_id`) REFERENCES `ciudades` (`id_Ciudad`),
  ADD CONSTRAINT `direcciones_pacientes_ibfk_3` FOREIGN KEY (`Estado_id`) REFERENCES `estados` (`id_Estado`),
  ADD CONSTRAINT `direcciones_pacientes_ibfk_4` FOREIGN KEY (`Municipio_id`) REFERENCES `municipios` (`id_Municipio`),
  ADD CONSTRAINT `direcciones_pacientes_ibfk_5` FOREIGN KEY (`Parroquia_id`) REFERENCES `parroquias` (`id_Parroquia`);

--
-- Filtros para la tabla `entidades_usd`
--
ALTER TABLE `entidades_usd`
  ADD CONSTRAINT `entidades_usd_ibfk_1` FOREIGN KEY (`Status_id`) REFERENCES `status` (`id_Status`),
  ADD CONSTRAINT `status_ibfk_1` FOREIGN KEY (`Status_id`) REFERENCES `status` (`id_Status`);

--
-- Filtros para la tabla `facturas`
--
ALTER TABLE `facturas`
  ADD CONSTRAINT `facturas_ibfk_1` FOREIGN KEY (`Cita_Consulta_id`) REFERENCES `citas_consultas` (`id_Cita_Consulta`),
  ADD CONSTRAINT `facturas_ibfk_2` FOREIGN KEY (`Datos_SENIAT_id`) REFERENCES `datos_seniat` (`id_Datos_SENIAT`),
  ADD CONSTRAINT `facturas_ibfk_3` FOREIGN KEY (`Pacientes_id`) REFERENCES `usuarios_pacientes` (`id_Paciente`),
  ADD CONSTRAINT `facturas_ibfk_4` FOREIGN KEY (`Status_Factura_id`) REFERENCES `status_factura` (`id_Status_Factura`),
  ADD CONSTRAINT `facturas_ibfk_5` FOREIGN KEY (`Medico_id`) REFERENCES `usuarios_medicos` (`id_Medico`),
  ADD CONSTRAINT `facturas_ibfk_6` FOREIGN KEY (`Asistente_id`) REFERENCES `usuarios_asistentes` (`id_asistente`);

--
-- Filtros para la tabla `factura_detalle`
--
ALTER TABLE `factura_detalle`
  ADD CONSTRAINT `factura_detalle_ibfk_1` FOREIGN KEY (`Factura_id`) REFERENCES `facturas` (`id_Factura`),
  ADD CONSTRAINT `factura_detalle_ibfk_2` FOREIGN KEY (`Servicio_id`) REFERENCES `servicios` (`id_Servicio`),
  ADD CONSTRAINT `factura_detalle_ibfk_3` FOREIGN KEY (`Status_Factura_id`) REFERENCES `status_factura` (`id_Status_Factura`);

--
-- Filtros para la tabla `factura_total_bs`
--
ALTER TABLE `factura_total_bs`
  ADD CONSTRAINT `factura_total_bs_ibfk_1` FOREIGN KEY (`Factura_Id`) REFERENCES `facturas` (`id_Factura`),
  ADD CONSTRAINT `factura_total_bs_ibfk_2` FOREIGN KEY (`Status_Tasa_id`) REFERENCES `status_tasas` (`id_Status_Tasa`),
  ADD CONSTRAINT `factura_total_bs_ibfk_3` FOREIGN KEY (`Cuenta_Bancaria_BS_id`) REFERENCES `cuenta_bancaria_bs` (`id_Cuenta_Bancaria_BS`),
  ADD CONSTRAINT `factura_total_bs_ibfk_4` FOREIGN KEY (`Tipo_Pago_id`) REFERENCES `tipo_pagos` (`id_Tipos_Pago`),
  ADD CONSTRAINT `factura_total_bs_ibfk_5` FOREIGN KEY (`banco_emisor`) REFERENCES `bancos_bs` (`id_Bancos_Bs`);

--
-- Filtros para la tabla `factura_total_cripto`
--
ALTER TABLE `factura_total_cripto`
  ADD CONSTRAINT `factura_total_cripto_ibfk_1` FOREIGN KEY (`Factura_id`) REFERENCES `facturas` (`id_Factura`),
  ADD CONSTRAINT `factura_total_cripto_ibfk_2` FOREIGN KEY (`Status_Tasa_id`) REFERENCES `status_tasas` (`id_Status_Tasa`),
  ADD CONSTRAINT `factura_total_cripto_ibfk_3` FOREIGN KEY (`Billetera_Cripto_id`) REFERENCES `billeteras_cripto` (`id_Billetera_Cripto`),
  ADD CONSTRAINT `factura_total_cripto_ibfk_4` FOREIGN KEY (`Tipo_Pago_id`) REFERENCES `tipo_pagos` (`id_Tipos_Pago`),
  ADD CONSTRAINT `factura_total_cripto_ibfk_5` FOREIGN KEY (`billetera_emisora`) REFERENCES `billeteras_cripto` (`id_Billetera_Cripto`);

--
-- Filtros para la tabla `factura_total_usd`
--
ALTER TABLE `factura_total_usd`
  ADD CONSTRAINT `factura_total_usd_ibfk_1` FOREIGN KEY (`Factura_id`) REFERENCES `facturas` (`id_Factura`),
  ADD CONSTRAINT `factura_total_usd_ibfk_2` FOREIGN KEY (`Status_Tasa_id`) REFERENCES `status_tasas` (`id_Status_Tasa`),
  ADD CONSTRAINT `factura_total_usd_ibfk_3` FOREIGN KEY (`Cuenta_USD_id`) REFERENCES `cuenta_usd` (`id_Cuenta_USD`),
  ADD CONSTRAINT `factura_total_usd_ibfk_4` FOREIGN KEY (`Tipo_Pago_id`) REFERENCES `tipo_pagos` (`id_Tipos_Pago`),
  ADD CONSTRAINT `factura_total_usd_ibfk_5` FOREIGN KEY (`entidad_emisora`) REFERENCES `entidades_usd` (`id_Entidad_USD`);

--
-- Filtros para la tabla `historico_login_pacientes`
--
ALTER TABLE `historico_login_pacientes`
  ADD CONSTRAINT `historico_login_pacientes_ibfk_1` FOREIGN KEY (`Login_Pacientes_id`) REFERENCES `login_pacientes` (`id_login_Pacientes`);

--
-- Filtros para la tabla `historico_login_trabajadores`
--
ALTER TABLE `historico_login_trabajadores`
  ADD CONSTRAINT `historico_login_trabajadores_ibfk_1` FOREIGN KEY (`Login_Tranajador_id`) REFERENCES `login_trabajadores` (`id_Login_Trabajador`),
  ADD CONSTRAINT `historico_login_trabajadores_ibfk_2` FOREIGN KEY (`Medico_id`) REFERENCES `usuarios_medicos` (`id_Medico`),
  ADD CONSTRAINT `historico_login_trabajadores_ibfk_3` FOREIGN KEY (`Asistente_id`) REFERENCES `usuarios_asistentes` (`id_asistente`);

--
-- Filtros para la tabla `historico_pediatria`
--
ALTER TABLE `historico_pediatria`
  ADD CONSTRAINT `historico_pediatria_ibfk_1` FOREIGN KEY (`Paciente_id`) REFERENCES `usuarios_pacientes` (`id_Paciente`),
  ADD CONSTRAINT `historico_pediatria_ibfk_2` FOREIGN KEY (`Medico_id`) REFERENCES `usuarios_medicos` (`id_Medico`),
  ADD CONSTRAINT `historico_pediatria_ibfk_3` FOREIGN KEY (`Paciente_pediatrico_Id`) REFERENCES `pacientes_especiales` (`id_Pacientes_Especiales`),
  ADD CONSTRAINT `historico_pediatria_ibfk_4` FOREIGN KEY (`Cita_Consulta_id`) REFERENCES `citas_consultas` (`id_Cita_Consulta`),
  ADD CONSTRAINT `historico_pediatria_ibfk_5` FOREIGN KEY (`Pediatria_id`) REFERENCES `pediatria` (`id_Pediatria`);

--
-- Filtros para la tabla `horarios_citas`
--
ALTER TABLE `horarios_citas`
  ADD CONSTRAINT `horarios_ibfk_1` FOREIGN KEY (`Medico_id`) REFERENCES `usuarios_medicos` (`id_Medico`),
  ADD CONSTRAINT `horarios_ibfk_2` FOREIGN KEY (`Especialidad_id`) REFERENCES `especialidades_medicas` (`id_Especialidad_Medica`),
  ADD CONSTRAINT `horarios_ibfk_3` FOREIGN KEY (`turno_id`) REFERENCES `turnos` (`id_turno`);

--
-- Filtros para la tabla `limite_usuarios`
--
ALTER TABLE `limite_usuarios`
  ADD CONSTRAINT `limites_ibfk_1` FOREIGN KEY (`status`) REFERENCES `status` (`id_Status`);

--
-- Filtros para la tabla `login_pacientes`
--
ALTER TABLE `login_pacientes`
  ADD CONSTRAINT `login_pacientes_ibfk_1` FOREIGN KEY (`Paciente_id`) REFERENCES `usuarios_pacientes` (`id_Paciente`),
  ADD CONSTRAINT `login_pacientes_ibfk_2` FOREIGN KEY (`Status_id`) REFERENCES `status` (`id_Status`);

--
-- Filtros para la tabla `login_trabajadores`
--
ALTER TABLE `login_trabajadores`
  ADD CONSTRAINT `login_trabajadores_ibfk_1` FOREIGN KEY (`Status_Medico_id`) REFERENCES `status_medicos` (`id_Status_Medico`),
  ADD CONSTRAINT `login_trabajadores_ibfk_2` FOREIGN KEY (`Asistente_id`) REFERENCES `usuarios_asistentes` (`id_asistente`),
  ADD CONSTRAINT `login_trabajadores_ibfk_3` FOREIGN KEY (`Medico_id`) REFERENCES `usuarios_medicos` (`id_Medico`),
  ADD CONSTRAINT `login_trabajadores_ibfk_4` FOREIGN KEY (`general_id`) REFERENCES `usuarios_general` (`id`);

--
-- Filtros para la tabla `medicoxasistente`
--
ALTER TABLE `medicoxasistente`
  ADD CONSTRAINT `medicoxasistente_ibfk_1` FOREIGN KEY (`id_Medico`) REFERENCES `usuarios_medicos` (`id_Medico`),
  ADD CONSTRAINT `medicoxasistente_ibfk_2` FOREIGN KEY (`id_Asistente`) REFERENCES `usuarios_asistentes` (`id_asistente`);

--
-- Filtros para la tabla `meeting_participants`
--
ALTER TABLE `meeting_participants`
  ADD CONSTRAINT `meeting_participants_meeting_id_foreign` FOREIGN KEY (`meeting_id`) REFERENCES `meetings` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `servicios_adicionales`
--
ALTER TABLE `servicios_adicionales`
  ADD CONSTRAINT `servicioa_ibfk_1` FOREIGN KEY (`Cita_Consulta_id`) REFERENCES `citas_consultas` (`id_Cita_Consulta`),
  ADD CONSTRAINT `servicioa_ibfk_2` FOREIGN KEY (`id_servicio`) REFERENCES `servicios` (`id_Servicio`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
