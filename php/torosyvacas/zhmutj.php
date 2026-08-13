<?php
$outfile = "torosyvacas.txt";

// checking whether to pick a new word
if (isset($_POST["begin"]))
	{
	// the input part, only in the beginning
	$nr_l=$_POST["nr_l"];
	$lang = $_POST["lang"];
	$list="list_" . $lang . "_" . $nr_l . ".clean.txt";
	$thewords = file($list);
	$num=count($thewords)-1;
	$theword = trim($thewords[rand(0,$num)]);

	// truncate to 0 old file if we came the first time:
	$handle = fopen($outfile, "w+");
	ftruncate($handle,0);
	fclose($handle);
	}
	else 
		{
			$theword = $_POST["theword"];
			$list="list_en_" . strlen($theword) . ".clean.txt";
			$thewords = file($list);
		}
			
// func. displaying entry form:
function showform()
{
global $theword;
?>
<FORM ACTION ="<?php echo $_SERVER['PHP_SELF']; ?>" method="POST" name="f">
<P>Enter your guess:&nbsp;&nbsp;&nbsp;
<INPUT NAME = "inword" SIZE = "8" maxsize="6" id="inword">
<INPUT TYPE = "hidden" NAME="theword" VALUE="<? echo $theword; ?>">
&nbsp;and&nbsp;&nbsp;
<INPUT TYPE = "SUBMIT" NAME= "submit" VALUE = "CHECK!">
</FORM>

<?php
}

// html header and body start:
?>

<html>
<head><title>Bulls and Cows</title>
<style>
body {font-family:Tahoma;color:#aa6666;background:#000000;background-image:url('ab.jpg')}
h3 {font-family:Tahoma;color:#ffffff;}
</style>
<script>
<!--
function sf()
{
document.f.inword.focus();
}
// -->
</script>
</head>

<body OnLoad="sf()">
<table align="center" width="600" border="0" cellspacing="0" cellpadding="1">
<tr><td bgcolor="#cc8888" align="center" valign="bottom">
<table align="center" width="599" border="0" cellspacing="0" cellpadding="20">
<tr><td bgcolor="#000000" align="center">
<h3> OK, GOOD LUCK WITH GUESSING MY WORD OF <?php echo strlen($theword); ?> LETTERS!</h3>

<table border="0" width="350" align="center">
<tr><td align="left">

<?php
// getting in the guessed word, check and display the result
if (!isset($_POST["begin"])) {
		
		$inword = trim($_POST["inword"]);
		$out = "<BR><span style='color:white;font-weight:bold'>" . $inword . ":</span>&nbsp;&nbsp;&nbsp;";
		// here goes the comparing algorithm:
		if ($inword==$theword) {
			$out = "<P>BINGO! It is <span style='color:white;font-weight:bold'>" . $theword . "</span>!!!" .
				"<P><a href='index.php'><span style='color:white'>One more time?</span></a>";
			}
	
		// two (obsolete, but saving the scanning through the dictionary) pre-checks:
		// number of letters
		elseif (strlen($inword)!=strlen($theword)) $out .= "Oops! Must be " . strlen($theword) . " letters.";
		// alphabetic characters
		elseif (!(ctype_alpha($inword))) $out .= " does not seem like a valid word!";

		else {
			// check for existence:
			$exists = FALSE;
			foreach ($thewords as $aword) {	if ($inword == strtolower(trim($aword))) $exists = TRUE; }
			if ($exists===FALSE) $out .= " Sorry, the word should be an existing single noun with no repeating letters!";
			
			else {
			// letter by letter comparing algorithm
			$thearray = preg_split('//',$theword,-1,PREG_SPLIT_NO_EMPTY);
			$inarray = preg_split('//',$inword,-1,PREG_SPLIT_NO_EMPTY);
			$nb = 0; // counter for bulls
			$nc = 0; // counter for cows
			foreach ($thearray as $pos => $letr)
				{
				foreach ($inarray as $inpos => $inletr)
					{
					if ($letr == $inletr)
						{
						if ($pos == $inpos) $nb=$nb+1;
							else $nc=$nc+1;
						}
					}
				}
			if ($nb>=1)
				{
				for ($i=1;$i<=$nb;$i++)
					{
					$out .= "<img src='toro.jpg' border='0'>&nbsp;";
					}
				}
			if ($nc>=1)
				{
				for ($j=1;$j<=$nc;$j++)
					{
					$out .= " <img src='vaca.jpg' border='0'>&nbsp;";
					}
				}
			if ($nb==0 AND $nc==0) $out .= "None&nbsp;:-(";
			}
			}
			
		// writing out in a file:
		if (is_writable($outfile)) {
			if (!$handle = fopen($outfile,"a+")) {
				echo "Cannot open file " . $outfile;
				exit;
				}
			if (fwrite($handle, $out) === FALSE) {
				echo "Could not write to " . $outfile;
				exit;
				}
			fclose($handle);
			}
		include($outfile);
		}
?>
</td></tr></table><P>
<?
if (!($inword==$theword)) {
showform();
// echo "<P>the right word is ".$theword."!</p>";
}
?>
</td></tr></table>
</td></tr></table>
</body>
</html>
