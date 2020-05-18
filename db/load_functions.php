<?php
include ".config.php";

function dbloader ($userid, $section, $payload)
{
	// Create connection
	global $servername,$username,$password,$dbname;

	$conn = new mysqli($servername, $username, $password, $dbname);

	//echo " servername: " . $servername . ", username: " . $username . ", pw: " . $password . ", dbname: " . $dbname;
	//echo ", userid: " . $userid . ", section: " . $section . ", payload: " . $payload . ", dt: " . $datetime;

	// Check connection
	if ($conn->connect_error) {
		throw new Exception('{"error":"Failed to connect to database: ' . $conn->connect_error . '"}');
		return $conn->connect_error;
	}

	// bind parameters and execute
	$stmt = $conn->prepare("SELECT values FROM socinfo WHERE userid LIKE ?");

	$stmt->bind_param('s', $userid);

	$result = $stmt->execute()

	if (!result) {
		throw new Exception('{"error": "Execute failed: (' . $stmt->errno . ') ' . $stmt->error . '"}');
	}

	if ($result->num_rows > 0)
	{
		$row = $result->fetch_assoc();
		$output = $row['values'];
	} else {
		$output = false;
	}

	$stmt->close();
	$conn->close();

	return $output;
}


if ($_SERVER['REQUEST_METHOD'] == 'POST') 
{
	$userid=$_POST["user_id"];
	$payload=$_POST["payload"];

	dbloader($userid,$section,$payload);

}
elseif ($_SERVER['REQUEST_METHOD'] == 'GET') 
{
	/*
	$email=$_GET["email"];
	$userid=$_GET["user_id"];
	$section="email";
	//$payload=json_encode($_GET);
	$datetime=new DateTime();
	$datetime=$datetime->getTimestamp();

	dbloader($userid,$section,$payload,$datetime);
	*/
	echo "222";
}
else
{
	echo "333";
}


?>
