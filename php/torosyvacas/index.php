<?php
// html header and body start:
?>

<html>
<head><title>Zhmutj</title>
<style>
body {font-family:Tahoma;color:#dd9999;background:#000000;background-image:url('ab.jpg');text-size:0.9em}
h3 {font-family:Tahoma;color:#ffffff;}
</style>
<script>
<!--
function sf()
{
document.f.q.focus();
}
// -->
</script>
</head>

<body onLoad=sf()>
<table align="center" width="800" border="0" cellspacing="0" cellpadding="1">
<tr><td bgcolor="#cc8888" align="center" valign="bottom">
<table align="center" width="700" border="0" cellspacing="0" cellpadding="15">
<tr><td bgcolor="#000000" align="center">
<h3> WELCOME TO ZHMUTJ:<br>(the grandmother of all games!)</h3>

<table border="0" width="500" align="center">
<tr><td style="text-align:justify">
<b>Basic idea:</b>
<p>The goal is to guess a random word picked up according to the number of letters you enter. 
You guess by entering different words and getting feedback in a form of <font color="white">bulls and cows</font>, 
where<br><img src="toro.jpg" border="0"> stands for a correct letter at <b><i>the correct position</i></b>,
<br><img src="vaca.jpg" border="0"> stands for a correct letter at <b><i>the wrong position</i></b>.<p>
<font color="white">N.B.</font> The picked up word is a singular noun with no repeating letters.

<p>&nbsp;
<p>
<FORM ACTION ="zhmutj.php" method="POST" name="f">
<P>Enter the number of letters (4-6):&nbsp;&nbsp;
<INPUT NAME = "nr_l" SIZE = "5" maxsize="5" value="" id="q">
<INPUT TYPE = "hidden" NAME = "lang" value="en">
&nbsp;and&nbsp;
<INPUT TYPE = "SUBMIT" NAME= "begin" VALUE = "GO!">
</FORM>

</td></tr></table>
</td></tr></table>
</body>
</html>
