<?php
// func. displaying entry form:
function showform ()
{
?>
<FORM ACTION ="<?php echo $_SERVER['PHP_SELF']; ?>" method="GET">
<P>Please specify the operands:
<INPUT NAME = "m" SIZE = "5">
<INPUT NAME = "n" SIZE = "5">
<P>
<INPUT TYPE = "SUBMIT" VALUE = "ADD!">
</FORM>

<?php
}

// html header and body start:
?>

<html>
<head><title></title></head>
<body>

<?php
// main actions:
// getting in the values (if any), check and display the result
// or the entry form 
$m = $_GET["m"];
$n = $_GET["n"];

if ($m=="" || $n == "") showform();
	elseif (!is_numeric($n) || !is_numeric($m)) printf("<P>Error! Invalid data. Data must be numeric.");
		else 
			{
			// here php can call any program via function system() more at http://www.php.net/system or http://be2.php.net/system;
			printf("<P>The sum of %ld and %ld is %ld.", $m, $n, $m+$n);
			}
?>
</body>
</html>
