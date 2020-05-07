<?php
//error_reporting(E_ALL);
//ini_set('display_errors', '1');

session_start();
include_once('../include/extras.php');
include_once('../clases/conexion.php');
?>
<!DOCTYPE html>
<html lang="es">
<head>
	<title>Sistema de Transcripci&oacute;n MC-BOLIVIA</title>
	<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
	<link href="../css/imc.css" rel="stylesheet" type="text/css">
	<style type="text/css">
		<!--
		.Estilo3 {font-size: 18px}
	-->
</style>
</head>
<?php
if( ! isset($_POST['save_archivo'])) {
	die;
}

if (! file_exists($_FILES['csv']['tmp_name'])) {
	die ('El archivo no existe '. $_FILES['csv']['tmp_name']);
}


$error_csv = 0;
$html = '';

$canales         = canales_cod();
$productos_all   = producto_cod_all();
$fecha_unicas    = array();


$nro_registros = 0;
$fecha_registro = date("Y-m-d");

/*****
 Primero validar el archivo CSV y verificar que podemos
 tener código de todos los Rubro, Anunciante, Producto, etc

 El archivo CSV debe tener el siguiente orden:
		  dia/mes/año: datos[0]  = 03
        medio: datos[1]  = ATB, 
       ciudad: datos[2]  = LA PAZ,
        rubro: datos[3] = COSMETICOS, PRODUCTOS DE LIMPIEZA PERSONAL Y TRATAMIENTOS CORPORALES,
   anunciante: datos[4] = BEIERSDORF BOLIVIA,
     producto: datos[5] = NIVEA POWDER COMFORT,
  observacion: datos[6]   =
     duración: datos[7] = 24,
 hora emision: datos[8] = 06:18:47,
	   nombre: datos[9]   = 
	   *****/
	   $encabezado_index = -1;
	   $encabezado = array(
	   	"N",
	   	"FECHA DE EMISION",
	   	"MEDIO",
	   	"CIUDAD",
	   	"RUBRO",	
	   	"ANUNCIANTE",	
	   	"PRODUCTO",	
	   	"OBSERVACION",	
	   	"DURACION SEG.",	
	   	"HORA EMISION",	
	   	"NOMBRE"
	   	);
	   $file = fopen($_FILES['csv']['tmp_name'], "r");
	   $a1 = "";
	   $a2 = "";
	   $a3 = "";
	   $pop=Array();
	   $error_tvprograma = 0;	
	   $etp = "";
	   while ( !feof($file) ) {
	   	$datos = fgetcsv($file, 0, ";", '"');
	   	if (sizeof($datos) < 3 ){
	   		continue;
	   	}

	   	$datos        = array_map('trim', $datos);
	   	$fecha_emision= $datos[1] ? $datos[1] : '';
	   	$medio        = strtoupper($datos[2]);  
	   	$ciudad       = strtoupper($datos[3]); 
		$rubro        = (str_replace(" ","",trim(strtoupper($datos[4]))));//no es espacio q sera, caracter raro
		$anunciante   = strtoupper($datos[5]);
	  	$producto     = (str_replace(" ","",(strtoupper(trim($datos[6])))));//no es espacio q sera,caracter raro
		$observacion  = strtoupper($datos[7]); //str_replace(,"",utf8_decode(strtoupper($datos[12])));
		$duracion     = $datos[8] ? $datos[8] : '';
		$hora_emision = $datos[9] ? $datos[9] : ''; 
		$nombre       = $datos[10] ? $datos[10] : '';
		
		
		//Iteramos hasta encontrar el encabezado 
		if(strtoupper($datos[0]) == $encabezado[0] && $encabezado_index == -1){
			//verificamos q tenga el mismo orden q el esperado
			for ($i=0; $i <sizeof($encabezado); $i++) { 
				if($datos[$i] != $encabezado[$i]){
					echo "<h2><center>Error fatal el csv no esta con el orden convenido </h2></center><br>";
					echo "<h2>El orden esperado es este : <br>";
					echo "<br> || ".implode($encabezado, " || ")." || </h2>";
					die();
				}
			}
			$encabezado_index = 1;
			continue; 	// el encabezado esta OK, volvemos a iterar y scamos los datos
		}

		// no encontramos el encabezado seguimos iterando hasta encontrar
		if($encabezado_index == -1) continue;
		
		//Ignoramos campos vacio 
		if(  $datos[1] =='' && $datos[2] =='' && $datos[3] =='' && $datos[4] =='' && $datos[5] =='' && $datos[6] == '' && $datos[7] == '' && $datos[8] =='' && $datos[9] =='' && $datos[10] =='' ){
			continue;
		}
		$nro_registros++;
		$sw_error  = 0;
		for ($i=0; $i <11 ; $i++) { 
			
			if(empty($datos[$i])){
				$error_csv = 1;
				$html .= '<tr>'.tagRow('Campo Vacio').
				tagRow($nro_registros).tagRow($fecha_emision).tagRow(_htmlrev($medio)). 
				tagRow($ciudad).tagRow(_htmlrev($rubro)).
				tagRow($anunciante).tagRow(_htmlrev($producto)).
				tagRow($observacion).tagRow(_htmlrev($duracion)).
				tagRow($hora_emision) .tagRow(($nombre)).'</tr>';
				$sw_error = 1;
			}
		}

		if($sw_error){
			continue;
		}

		/**
		 * Procedemos a verificar  q todo este en orden
		 */
		
		if(sizeof(explode("/",$fecha_emision)) != 3){
			$error_csv = 1;
			$html .= '<tr>'.tagRow('Error fecha emision').
			tagRow($nro_registros).tagRow($fecha_emision).tagRow(_htmlrev($medio)). 
			tagRow($ciudad).tagRow(_htmlrev($rubro)).
			tagRow($anunciante).tagRow(_htmlrev($producto)).
			tagRow($observacion).tagRow(_htmlrev($duracion)).
			tagRow($hora_emision) .tagRow(($nombre)).'</tr>';
		}


		/**
		 * Verificamos ciudad y canal
		 */	
		
		if(!empty($canales[$ciudad][$medio]) ){
			$cod_canal  = $canales[$ciudad][$medio]["cod_canal"];
			$cod_ciudad = $canales[$ciudad][$medio]["cod_ciudad"];
		}else{
			$error_csv = 1;
			$html .= '<tr>'.tagRow('Error ciudad o canal').
			tagRow($nro_registros).tagRow($fecha_emision).tagRow(_htmlrev($medio)). 
			tagRow($ciudad).tagRow(_htmlrev($rubro)).
			tagRow($anunciante).tagRow(_htmlrev($producto)).
			tagRow($observacion).tagRow(_htmlrev($duracion)).
			tagRow($hora_emision) .tagRow(($nombre)).'</tr>';
			continue;
		}
		
		
		if(empty($productos_all[$producto])){
			$error_csv = 1;
			$html .= '<tr>'.tagRow("No se encontro el producto <b>".$producto."</b><br>Revise que este bien escrito").
			tagRow($nro_registros).tagRow($fecha_emision).tagRow(_htmlrev($medio)). 
			tagRow($ciudad).tagRow(_htmlrev($rubro)).
			tagRow($anunciante).tagRow(_htmlrev($producto)).
			tagRow($observacion).tagRow(_htmlrev($duracion)).
			tagRow($hora_emision) .tagRow(($nombre)).'</tr>';
			continue;
		}

		if(empty($productos_all[$producto][$anunciante])){
			$error_csv = 1;
			$html .= '<tr>'.tagRow("Anunciante: <b>$anunciante</b>no pertenece al producto: <b>$producto</b><br> <a target='_blank' href='"."../admtv/cproducto.php?producto=".$producto."&anunciante=&buscar=Buscar'>Mas detalles</a>").
			tagRow($nro_registros).tagRow($fecha_emision).tagRow(_htmlrev($medio)). 
			tagRow($ciudad).tagRow(_htmlrev($rubro)).
			tagRow($anunciante).tagRow(_htmlrev($producto)).
			tagRow($observacion).tagRow(_htmlrev($duracion)).
			tagRow($hora_emision) .tagRow(($nombre)).'</tr>';
			continue;
		}

		$cod_anunciante = $productos_all[$producto][$anunciante];

		if(empty($productos_all[$producto][$anunciante][$rubro]) ){
			$error_csv = 1;
			$html .= '<tr>'.tagRow('No se encontro el rubro: <b>'.$rubro."</b><br><br>Producto:<b>$producto</b><br>Anunciante:<b>$anunciante</b><br><a target='_blank' href=../admtv/cproducto.php?producto=$producto&anunciante=&buscar=Buscar>Mas detalles</a>").
			tagRow($nro_registros).tagRow($fecha_emision).tagRow(_htmlrev($medio)). 
			tagRow($ciudad).tagRow(_htmlrev($rubro)).
			tagRow($anunciante).tagRow(_htmlrev($producto)).
			tagRow($observacion).tagRow(_htmlrev($duracion)).
			tagRow($hora_emision) .tagRow(($nombre)).'</tr>';
			continue;
		}

		if($productos_all[$producto][$anunciante][$rubro]['rep'] > 1){
			$error_csv = 1;
			$cod_anu = $productos_all[$producto][$anunciante][$rubro]['cod_anunciante'];
			$html .= '<tr>'.tagRow("ERROR FATAL anunciante <b>$anunciante</b>, producto <b>$producto</b>estan duplicados, depure el sistema <a target='_blank'  href='"."../admtv/cproducto.php?producto=".$producto."&anunciante=$cod_anu&buscar=Buscar'>Mas detalles</a>").
			tagRow($nro_registros).tagRow($fecha_emision).tagRow(_htmlrev($medio)). 
			tagRow($ciudad).tagRow(_htmlrev($rubro)).
			tagRow($anunciante).tagRow(_htmlrev($producto)).
			tagRow($observacion).tagRow(_htmlrev($duracion)).
			tagRow($hora_emision) .tagRow(($nombre)).'</tr>';
			continue;	
		}


		$programa = programa($cod_canal,$cod_ciudad,$fecha_emision,$duracion,$hora_emision);

		if($programa == -1){
			$error_csv = 1;
			$cod_anu = $productos_all[$producto][$anunciante][$rubro]['cod_anunciante'];
			$html .= '<tr>'.tagRow("Tv Tarifario no establecido <br>, horario no establecido ultimamente, revise tvhorarios").
			tagRow($nro_registros).tagRow($fecha_emision).tagRow(_htmlrev($medio)). 
			tagRow($ciudad).tagRow(_htmlrev($rubro)).
			tagRow($anunciante).tagRow(_htmlrev($producto)).
			tagRow($observacion).tagRow(_htmlrev($duracion)).
			tagRow($hora_emision) .tagRow(($nombre)).'</tr>';
			continue;
		}
		
		if($programa == -2){
			$sms = "No se encontro ningun programa el dia <b>$fecha_emision</b> dentro el intervalo de tiempo hora inicio : $hora_emision
			, con duracion de $duracion segundos o no tiene tarifa establecida<br>";
			$error_csv = 1;
			$cod_anu = $productos_all[$producto][$anunciante][$rubro]['cod_anunciante'];
			$html .= '<tr>'.tagRow($sms).
			tagRow($nro_registros).tagRow($fecha_emision).tagRow(_htmlrev($medio)). 
			tagRow($ciudad).tagRow(_htmlrev($rubro)).
			tagRow($anunciante).tagRow(_htmlrev($producto)).
			tagRow($observacion).tagRow(_htmlrev($duracion)).
			tagRow($hora_emision) .tagRow(($nombre)).'</tr>';
			continue;
		}

		$fecha_unicas[$programa["fecha_emision"]]=$programa["fecha_emision"];

	}	
	fclose($file);
	$file = fopen($_FILES['csv']['tmp_name'], "r");

//si todo ok volvemos a importar
	if($error_csv == 0){
		$nro_registros = 0;
		$fecha_actual = date("Y")."-".date("m")."-".date("d");
		$html = '';
		$encabezado_index = -1;
	}
	while ( !feof($file) && $error_csv == 0 ) {
		$datos = fgetcsv($file, 0, ";", '"');
		if (sizeof($datos) < 3 ){
			continue;
		}

		$datos        = array_map('trim', $datos);
		$fecha_emision= $datos[1] ? $datos[1] : '';
		$medio        = strtoupper($datos[2]);  
		$ciudad       = strtoupper($datos[3]); 
		$rubro        = (str_replace(" ","",trim(strtoupper($datos[4]))));//no es espacio q sera, caracter raro
		$anunciante   = strtoupper($datos[5]);
	  	$producto     = (str_replace(" ","",(strtoupper(trim($datos[6])))));//no es espacio q sera,caracter raro
		$observacion  = strtoupper($datos[7]); //str_replace(,"",utf8_decode(strtoupper($datos[12])));
		$duracion     = $datos[8] ? $datos[8] : '';
		$hora_emision = $datos[9] ? $datos[9] : ''; 
		$nombre       = $datos[10] ? $datos[10] : '';
		
		
		//Iteramos hasta encontrar el encabezado 
		if(strtoupper($datos[0]) == $encabezado[0] && $encabezado_index == -1){
			//verificamos q tenga el mismo orden q el esperado
			for ($i=0; $i <sizeof($encabezado); $i++) { 
				if($datos[$i] != $encabezado[$i]){
					echo "<h2><center>Error fatal el csv no esta con el orden convenido </h2></center><br>";
					echo "<h2>El orden esperado es este : <br>";
					echo "<br> || ".implode($encabezado, " || ")." || </h2>";
					die();
				}
			}
			$encabezado_index = 1;
			continue; 	// el encabezado esta OK, volvemos a iterar y scamos los datos

		}

		// no encontramos el encabezado seguimos iterando hasta encontrar
		if($encabezado_index == -1) continue;
		
		//Ignoramos campos vacio 
		if(  $datos[1] =='' && $datos[2] =='' && $datos[3] =='' && $datos[4] =='' && $datos[5] =='' && $datos[6] == '' && $datos[7] == '' && $datos[8] =='' && $datos[9] =='' && $datos[10] =='' ){
			continue;
		}
		$nro_registros++;

		$cod_canal = $canales[$ciudad][$medio]["cod_canal"];
		$cod_ciu   = $canales[$ciudad][$medio]["cod_ciudad"];

		$cod_tmp = $productos_all[$producto][$anunciante][$rubro];
		$cod_rubro = $cod_tmp["cod_rubro"];
		$cod_anu  = $cod_tmp["cod_anunciante"];
		$cod_prod = $cod_tmp["cod_producto"];


		$programa = programa($cod_canal,$cod_ciu,$fecha_emision,$duracion,$hora_emision);
		$cod_programa  = $programa["cod_programa"];
		$fecha_emision = $programa["fecha_emision"];

		if(empty($cod_programa) || empty($fecha_emision)){
			echo "Error fatal, Envie el CSV que estaba subiendo para inciar la depuracion";
			echo "<br>";
			echo "Modo Debug <br>";
			echo "<pre>";
			echo "------PROGRAMA-------";
			print_r($programa);
			echo "---------------------";
			echo "----PARAMETROS PROGRAMA----";
			echo "cod_canal $cod_canal <br>";
			echo "cod_ciudad $cod_ciudad <br>";
			echo "fecha_emision $fecha_emision <br>";
			echo "hora_emision $hora_emision <br>";
			echo "------PROGRAMA-------";
			print_r($productos_all);
			echo "</pre>";
			exit();
		}


		$qry = sprintf("SELECT * FROM  tvmencion WHERE cod_mencion=%d 
		  AND fecha_registro = '%s'
			AND fecha_emision = '%s'
			AND cod_canal =%d
			AND cod_ciu=%d
			AND cod_rubro=%d
			AND cod_anunciante=%d
			AND cod_producto=%d
			AND nombre_spot='%s'
			AND duracion=%d
			AND hora_emision='%s'
			AND cod_programa=%d",
			$cod_mencion, $fecha_actual, $fecha_emision, $cod_canal, $cod_ciu,$cod_rubro, $cod_anu, $cod_prod, $nombre, $duracion, $hora_emision,
			$cod_programa);
		$cn->query = $qry;
		$cn->Ejecutar(__LINE__, __FILE__);
		$sw = 0;
		while ($row = mysql_fetch_assoc($cn->result)) {
			$sw = 1;
		}

		if($sw == 0){
			$cod_mencion = traemax('tvmencion','cod_mencion','');
			$qry = sprintf("INSERT INTO tvmencion (cod_mencion, fecha_registro, fecha_emision, cod_canal, cod_ciu,
				cod_rubro, cod_anunciante, cod_producto, nombre_spot, duracion, hora_emision,
				cod_programa, observacion)				        
				VALUES (%d, '%s', '%s', %d, %d, %d, %d, %d, '%s', %d, '%s', %d, '%s')",
				$cod_mencion, $fecha_actual, $fecha_emision, $cod_canal, $cod_ciu, 
				$cod_rubro, $cod_anu, $cod_prod, $nombre, $duracion, $hora_emision,
				$cod_programa, $observacion);
			$cn->query = $qry;
			$cn->Ejecutar(__LINE__, __FILE__);
	    }


		$html .= '<tr>'. tagRow($nro_registros).tagRow($fecha_emision) . tagRow(_htmlrev($medio)) . 
		tagRow($ciudad) . tagRow(_htmlrev($rubro)) . tagRow(_htmlrev($anunciante)) . 
		tagRow(_htmlrev($producto)) . tagRow(_htmlrev($observacion)) . 
		tagRow($duracion) . tagRow($hora_emision) .tagRow($programa["nombre_programa"]).
		tagRow(_htmlrev($nombre)).'</tr>';


	}
	fclose($file);

	if($encabezado_index == -1){
		echo "<h2><center>Error fatal el csv no esta con el orden convenido </h2></center><br>";
		echo "<h2>El orden esperado es este : <br>";
		echo "<br> || ".implode($encabezado, " || ")." || </h2>";
		die();
	}

	function tagRow($content) {
		return '<td>' . $content . '</td>';
	}

	function canales_cod() {
	// Obtenemos nombre de ciudad, canal y sus respectivos codigos
		$result = mysql_query('select cod_ciudad,nom_ciu, cod_canal, nombre  from tvcanal, tciudad where estado = 1 and tciudad.cod_ciu = tvcanal.cod_ciudad order by cod_ciudad, cod_canal');
		if ( ! $result ) {
			die('Consulta no válida: ' . mysql_error());
		}
		if (mysql_num_rows($result) == 0) {
			die('No hay nombres de ciudad y canales');
		}
		$canales = array();
		while ( $fila = mysql_fetch_assoc($result) ) {		
			$cod_ciu   = trim($fila['cod_ciudad']);
			$nom_ciu   = trim($fila['nom_ciu']);
			$cod_canal = trim($fila['cod_canal']);
			$canal     = trim($fila['nombre']);

			$canales[$nom_ciu][$canal]= array('cod_ciudad' =>$cod_ciu,"cod_canal"=>$cod_canal) ;
		}

		mysql_free_result($result);
		return $canales;
	}


	function producto_cod_all(){
		$query = "SELECT tvproducto.cod_producto,tvproducto.nombre as producto,tvanunciante.cod_anu,
		tvanunciante.anunciante,tvrubro.cod_rubro,tvrubro.nom_rubro, count(*) as rep
		FROM tvproducto, tvanunciante, tvrubro 
		WHERE tvproducto.cod_anu = tvanunciante.cod_anu AND
		tvproducto.cod_rubro = tvrubro.cod_rubro AND
		tvproducto.estado = 1 AND
		tvanunciante.estado = 1 AND
		tvrubro.estado = 1
		GROUP by tvproducto.nombre, tvproducto.cod_anu, tvproducto.cod_rubro
		order by rep desc";

		$result = mysql_query($query);
		if ( ! $result ) {
			die('Consulta no válida: ' . mysql_error());
		}
		if (mysql_num_rows($result) == 0) {
			die('No hay nombres de producto, anunciantes, rubros');
		}
		$producto_all = array();
		while ( $fila = mysql_fetch_assoc($result) ) {
			$producto       = trim($fila['producto']);
			$anunciante     = trim($fila['anunciante']);
			$rubro          = trim($fila['nom_rubro']);

			$cod_producto   = trim($fila['cod_producto']);
			$cod_anunciante = trim($fila['cod_anu']);
			$cod_rubro      = trim($fila['cod_rubro']);

			$producto_all[$producto][$anunciante][$rubro]= array(
				'cod_producto'  =>$cod_producto,
				'cod_anunciante'=>$cod_anunciante,
				'cod_rubro'     =>$cod_rubro,
				'rep'           =>$fila['rep']) ;
		}

		mysql_free_result($result);
		return $producto_all;
	}

	function programa($cod_canal,$cod_ciudad,$fecha_publicacion,$duracion,$hora_inicio){
		$semana  = array('','--LMIJV','--LMIJV','--LMIJV','--LMIJV','--LMIJV','S------','-D-----');
		$f_tmp = explode("/",$fecha_publicacion);
		$fecha_publicacion_ = $f_tmp[2]."-".$f_tmp[1]."-".$f_tmp[0];
		$fecha_publicacion  =  $fecha_publicacion_;
		$dia = $semana[date('N', strtotime($fecha_publicacion))];
	/*
		Obtener nombre, codigo del programa
		y al tarifario que pertenecia en esa epoca
	*/	

		//si el programa no esta en el rango que indica el tarifario
		//quiere decir que es tarifario nuevo 
		//volvemos a consultar buscando desde el tarifario mas actual a la fecha de ese programa
		//hasta la ultima fecha actual del tarifario 
		//para evitar bucles infinitos se puede hacer hasta un maximo de 1000 repeticiones

		$orden         = " desc";
		$discriminante = "<=";
		$inde = 0;
		$tarifario_fatal = 1;
		
		while($inde < 30){
			$sql  =" SELECT distinct(fecha) as fecha FROM tvtarifario 
			WHERE cod_canal  = $cod_canal 
			AND   cod_ciudad = $cod_ciudad 
			AND   fecha $discriminante '$fecha_publicacion' 
			AND   fecha is not null order by fecha ".$orden;

			$ans = mysql_query($sql);
			$cambio_tarifa = "";
			if(mysql_num_rows($ans) > 0){
				$cambio_tarifa = mysql_result($ans,$inde, 'fecha');
				$tarifario_fatal = 0;
			}
			
			
			if(!empty($cambio_tarifa)){
				$sql_tmp = $sql;
				$sql = "select tvprograma.* , tvtipoprograma.tipo, tvtarifario.cod_programa, tvtarifario.fecha, 
				tvtarifario.dia, tvtarifario.precio
				from tvprograma, tvtipoprograma, tvtarifario 
				where tvprograma.id_tipoprograma = tvtipoprograma.id_tipoprograma 
				and tvprograma.cod_canal = $cod_canal 
				and tvprograma.estado = 1
				and tvtarifario.cod_programa = tvprograma.cod_programa
				and tvprograma.id_tarifa is not null
				and tvtarifario.fecha is not null
				and tvtarifario.dia = '$dia'
				and tvtarifario.fecha = '$cambio_tarifa'
				and tvtarifario.precio > 0
				order by tvprograma.cod_programa";	
				$resp = mysql_query($sql);

				if(mysql_num_rows($resp) > 0) break;
			}
			if($orden != " desc") $inde++;
			$orden = "asc";
			$discriminante = ">=";
		}

		if($tarifario_fatal == 1){
			return -1;
		}

		$ini_deteccion = strtotime($hora_inicio);
		$ini_deteccion_= date('H:i:s',strtotime($hora_inicio));

		$tim           = $hora_inicio." +$duracion seconds";
		$fin_deteccion = strtotime(date('H:i:s', strtotime($tim)));

		$fin_deteccion_= strtotime(date('H:i:s',$fin_deteccion));

		$cod_programa    = "";
		$nombre_programa = "";
		$dia_programa    = "";
		//Obtenermos cod_programa, nombre_programa deacuerdo al horario
		for ($i=0; $i <mysql_num_rows($resp) ; $i++) { 
			$ini_prog  = strtotime(mysql_result($resp, $i,'hora_inicio'));
			$sum_horas = sumahoras(parse_hora(mysql_result($resp,$i, 'duracion')),date('H:i:s',$ini_prog));
			$fin_prog  = strtotime($sum_horas); 

			$ini_prog_ = date('H:i:s', $ini_prog);
			$fin_prog_ = date('H:i:s', $fin_prog);
			$dia_programa = mysql_result($resp, $i,'dia');
			if( dentro_de_horario($ini_prog_,$fin_prog_,$ini_deteccion_) && $dia_programa == $dia){
				$cod_programa    = mysql_result($resp, $i,'cod_programa');
				$nombre_programa = mysql_result($resp, $i,'nombre');
				
				break;		
			}
		}
		$ini_deteccion = date("H:i:s",$ini_deteccion);
		$fin_deteccion = date("H:i:s",$fin_deteccion);

		if(empty($cod_programa) or empty($nombre_programa)){
			return -2; 
		}
		return array("cod_programa"=>$cod_programa,"nombre_programa" => $nombre_programa,"fecha_emision"=>$fecha_publicacion);
	}

function dentro_de_horario($hms_inicio, $hms_fin, $hms_referencia=NULL){ // v2011-06-21
	if( is_null($hms_referencia) ){
		$hms_referencia = date('G:i:s');
	}

	list($h, $m, $s) = array_pad(preg_split('/[^\d]+/', $hms_inicio), 3, 0);
	$s_inicio = 3600*$h + 60*$m + $s;

	list($h, $m, $s) = array_pad(preg_split('/[^\d]+/', $hms_fin), 3, 0);
	$s_fin = 3600*$h + 60*$m + $s;

	list($h, $m, $s) = array_pad(preg_split('/[^\d]+/', $hms_referencia), 3, 0);
	$s_referencia = 3600*$h + 60*$m + $s;

	if($s_inicio<=$s_fin){
		return $s_referencia>=$s_inicio && $s_referencia<=$s_fin;
	}else{
		return $s_referencia>=$s_inicio || $s_referencia<=$s_fin;
	}
}


function stripAccents($String){
	$char_find    		  = array('Á','É', 'Í', 'Ó', 'Ú', 'á', 'é', 'í', 'ó', 'ú','ñ','Ñ','ó');
	$char_replace 		  = array('A','E', 'I', 'O', 'U', 'a', 'e', 'i', 'o', 'u','n','N','o');
	$word_clean = str_replace($char_find, $char_replace, $String);
    return $word_clean;
}
?>
<body>
	<h1 align="center"><span class="unnamed1 Estilo3">Menciones TV importadas desde CSV</span></h1>

	<h3>Se importaron correctamente las siguientes Menciones de televisi&oacute;n</h3>

	<?php if ($error_csv == 1) { ?>
	<p align="left"><font color="red">Las siguientes l&iacute;neas del archivo CSV, no coinciden con Rubro o Anunciante
		o Producto conocido. Abortando operaci&oacute;n.</font></p>

		<table border="1">
			<tr>
				<th>DESCRIPCION ERROR</th>
				<th>N</th>
				<th>FECHA DE EMISION</th>
				<th>MEDIO</th>
				<th>CIUDAD</th>
				<th>RUBRO</th>
				<th>ANUNCIANTE</th>
				<th>PRODUCTO</th>
				<th>OBSERVACION</th>
				<th>DUR. SEG</th>
				<th>HORA EMISION</th>
				<th>NOMBRE</th>
			</tr>
			<?php } else { ?>

			<table border="1">
				<tr>
					<th>N</th>
					<th>FECHA DE EMISION</th>
					<th>MEDIO</th>
					<th>CIUDAD</th>
					<th>RUBRO</th>
					<th>ANUNCIANTE</th>
					<th>PRODUCTO</th>
					<th>OBSERVACION</th>
					<th>DUR. SEG</th>
					<th>HORA EMISION</th>
					<th>PROGRAMA</th>
					<th>NOMBRE</th>
				</tr>
				<?php } ?>
				<?php print $html; ?>

			</table>
		</body>

